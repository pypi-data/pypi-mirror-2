# Copyright (c) 2010 OpenStack, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import with_statement
import cPickle as pickle
import logging
import os
import sys
import unittest
from ConfigParser import ConfigParser
from contextlib import contextmanager
from cStringIO import StringIO
from gzip import GzipFile
from httplib import HTTPException
from shutil import rmtree
from time import time
from urllib import unquote, quote

import eventlet
from eventlet import sleep, spawn, TimeoutError, util, wsgi, listen
from eventlet.timeout import Timeout
import simplejson
from webob import Request

from test.unit import connect_tcp, readuntil2crlfs
from swift.proxy import server as proxy_server
from swift.account import server as account_server
from swift.container import server as container_server
from swift.obj import server as object_server
from swift.common import ring
from swift.common.constraints import MAX_META_NAME_LENGTH, \
    MAX_META_VALUE_LENGTH, MAX_META_COUNT, MAX_META_OVERALL_SIZE, MAX_FILE_SIZE
from swift.common.utils import mkdirs, normalize_timestamp, NullLogger


# mocks
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

def fake_http_connect(*code_iter, **kwargs):
    class FakeConn(object):
        def __init__(self, status, etag=None):
            self.status = status
            self.reason = 'Fake'
            self.host = '1.2.3.4'
            self.port = '1234'
            self.sent = 0
            self.received = 0
            self.etag = etag
        def getresponse(self):
            if 'raise_exc' in kwargs:
                raise Exception('test')
            return self
        def getexpect(self):
            return FakeConn(100)
        def getheaders(self):
            headers = {'content-length': 0,
                       'content-type': 'x-application/test',
                       'x-timestamp': '1',
                       'x-object-meta-test': 'testing',
                       'etag':
                            self.etag or '"68b329da9893e34099c7d8ad5cb9c940"',
                       'x-works': 'yes',
                       }
            try:
                if container_ts_iter.next() is False:
                    headers['x-container-timestamp'] = '1'
            except StopIteration:
                pass
            if 'slow' in kwargs:
                headers['content-length'] = '4'
            return headers
        def read(self, amt=None):
            if 'slow' in kwargs:
                if self.sent < 4:
                    self.sent += 1
                    sleep(0.1)
                    return ' '
            return ''
        def send(self, amt=None):
            if 'slow' in kwargs:
                if self.received < 4:
                    self.received += 1
                    sleep(0.1)
        def getheader(self, name, default=None):
            return self.getheaders().get(name.lower(), default)
    etag_iter = iter(kwargs.get('etags') or [None] * len(code_iter))
    x = kwargs.get('missing_container', [False] * len(code_iter))
    if not isinstance(x, (tuple, list)):
        x = [x] * len(code_iter)
    container_ts_iter = iter(x)
    code_iter = iter(code_iter)
    def connect(*args, **ckwargs):
        if 'give_content_type' in kwargs:
            if len(args) >= 7 and 'content_type' in args[6]:
                kwargs['give_content_type'](args[6]['content-type'])
            else:
                kwargs['give_content_type']('')
        status = code_iter.next()
        etag = etag_iter.next()
        if status == -1:
            raise HTTPException()
        return FakeConn(status, etag)
    return connect


class FakeRing(object):

    def __init__(self):
        # 9 total nodes (6 more past the initial 3) is the cap, no matter if
        # this is set higher.
        self.max_more_nodes = 0
        self.devs = {}
        self.replica_count = 3

    def get_nodes(self, account, container=None, obj=None):
        devs = []
        for x in xrange(3):
            devs.append(self.devs.get(x))
            if devs[x] is None:
                self.devs[x] = devs[x] = \
                    {'ip': '10.0.0.%s' % x, 'port': 1000 + x, 'device': 'sda'}
        return 1, devs

    def get_more_nodes(self, nodes):
        # 9 is the true cap
        for x in xrange(3, min(3 + self.max_more_nodes, 9)):
            yield {'ip': '10.0.0.%s' % x, 'port': 1000 + x, 'device': 'sda'}


class FakeMemcache(object):
    def __init__(self):
        self.store = {}

    def get(self, key):
        return self.store.get(key)

    def set(self, key, value, timeout=0):
        self.store[key] = value
        return True

    def incr(self, key, timeout=0):
        self.store[key] = self.store.setdefault(key, 0) + 1
        return self.store[key]

    @contextmanager
    def soft_lock(self, key, timeout=0, retries=5):
        yield True

    def delete(self, key):
        try:
            del self.store[key]
        except:
            pass
        return True


class FakeMemcacheReturnsNone(FakeMemcache):

    def get(self, key):
        # Returns None as the timestamp of the container; assumes we're only
        # using the FakeMemcache for container existence checks.
        return None

class NullLoggingHandler(logging.Handler):

    def emit(self, record):
        pass

@contextmanager
def save_globals():
    orig_http_connect = getattr(proxy_server, 'http_connect', None)
    try:
        yield True
    finally:
        proxy_server.http_connect = orig_http_connect

# tests


class TestProxyServer(unittest.TestCase):

    def test_unhandled_exception(self):
        class MyApp(proxy_server.Application):
            def get_controller(self, path):
                raise Exception('this shouldnt be caught')
        app = MyApp(None, FakeMemcache(), account_ring=FakeRing(),
                container_ring=FakeRing(), object_ring=FakeRing())
        req = Request.blank('/account', environ={'REQUEST_METHOD': 'HEAD'})
        req.account = 'account'
        resp = app.handle_request(req)
        self.assertEquals(resp.status_int, 500)


class TestObjectController(unittest.TestCase):

    def setUp(self):
        self.app = proxy_server.Application(None, FakeMemcache(),
            account_ring=FakeRing(), container_ring=FakeRing(),
            object_ring=FakeRing())

    def assert_status_map(self, method, statuses, expected, raise_exc=False):
        with save_globals():
            kwargs = {}
            if raise_exc:
                kwargs['raise_exc'] = raise_exc
            proxy_server.http_connect = fake_http_connect(*statuses, **kwargs)
            self.app.memcache.store = {}
            req = Request.blank('/a/c/o', headers={'Content-Length': '0',
                    'Content-Type': 'text/plain'})
            req.account = 'a'
            res = method(req)
            self.assertEquals(res.status_int, expected)
            proxy_server.http_connect = fake_http_connect(*statuses, **kwargs)
            self.app.memcache.store = {}
            req = Request.blank('/a/c/o', headers={'Content-Length': '0',
                    'Content-Type': 'text/plain'})
            req.account = 'a'
            res = method(req)
            self.assertEquals(res.status_int, expected)

    def test_PUT_auto_content_type(self):
        with save_globals():
            controller = proxy_server.ObjectController(self.app, 'account',
                'container', 'object')
            def test_content_type(filename, expected):
                proxy_server.http_connect = fake_http_connect(201, 201, 201,
                    give_content_type=lambda content_type:
                        self.assertEquals(content_type, expected.next()))
                req = Request.blank('/a/c/%s' % filename, {})
                req.account = 'a'
                res = controller.PUT(req)
            test_content_type('test.jpg',
                              iter(['', '', '', 'image/jpeg', 'image/jpeg', 'image/jpeg']))
            test_content_type('test.html',
                              iter(['', '', '', 'text/html', 'text/html', 'text/html']))
            test_content_type('test.css',
                              iter(['', '', '', 'text/css', 'text/css', 'text/css']))

    def test_PUT(self):
        with save_globals():
            controller = proxy_server.ObjectController(self.app, 'account',
                'container', 'object')
            def test_status_map(statuses, expected):
                proxy_server.http_connect = fake_http_connect(*statuses)
                req = Request.blank('/a/c/o.jpg', {})
                req.content_length = 0
                req.account = 'a'
                self.app.memcache.store = {}
                res = controller.PUT(req)
                expected = str(expected)
                self.assertEquals(res.status[:len(expected)], expected)
            test_status_map((200, 200, 201, 201, 201), 201)
            test_status_map((200, 200, 201, 201, 500), 201)
            test_status_map((200, 200, 204, 404, 404), 404)
            test_status_map((200, 200, 204, 500, 404), 503)

    def test_PUT_connect_exceptions(self):
        def mock_http_connect(*code_iter, **kwargs):
            class FakeConn(object):
                def __init__(self, status):
                    self.status = status
                    self.reason = 'Fake'
                def getresponse(self): return self
                def read(self, amt=None): return ''
                def getheader(self, name): return ''
                def getexpect(self): return FakeConn(100)
            code_iter = iter(code_iter)
            def connect(*args, **ckwargs):
                status = code_iter.next()
                if status == -1:
                    raise HTTPException()
                return FakeConn(status)
            return connect
        with save_globals():
            controller = proxy_server.ObjectController(self.app, 'account',
                'container', 'object')
            def test_status_map(statuses, expected):
                proxy_server.http_connect = mock_http_connect(*statuses)
                self.app.memcache.store = {}
                req = Request.blank('/a/c/o.jpg', {})
                req.content_length = 0
                req.account = 'a'
                res = controller.PUT(req)
                expected = str(expected)
                self.assertEquals(res.status[:len(expected)], expected)
            test_status_map((200, 200, 201, 201, -1), 201)
            test_status_map((200, 200, 201, -1, -1), 503)
            test_status_map((200, 200, 503, 503, -1), 503)

    def test_PUT_send_exceptions(self):
        def mock_http_connect(*code_iter, **kwargs):
            class FakeConn(object):
                def __init__(self, status):
                    self.status = status
                    self.reason = 'Fake'
                    self.host = '1.2.3.4'
                    self.port = 1024
                def getresponse(self): return self
                def read(self, amt=None): return ''
                def send(self, amt=None):
                    if self.status == -1:
                        raise HTTPException()
                def getheader(self, name): return ''
                def getexpect(self): return FakeConn(100)
            code_iter = iter(code_iter)
            def connect(*args, **ckwargs):
                return FakeConn(code_iter.next())
            return connect
        with save_globals():
            controller = proxy_server.ObjectController(self.app, 'account',
                'container', 'object')
            def test_status_map(statuses, expected):
                self.app.memcache.store = {}
                proxy_server.http_connect = mock_http_connect(*statuses)
                req = Request.blank('/a/c/o.jpg', {})
                req.account = 'a'
                req.body_file = StringIO('some data')
                res = controller.PUT(req)
                expected = str(expected)
                self.assertEquals(res.status[:len(expected)], expected)
            test_status_map((200, 200, 201, 201, -1), 201)
            test_status_map((200, 200, 201, -1, -1), 503)
            test_status_map((200, 200, 503, 503, -1), 503)

    def test_PUT_max_size(self):
        with save_globals():
            proxy_server.http_connect = fake_http_connect(201, 201, 201)
            controller = proxy_server.ObjectController(self.app, 'account',
                'container', 'object')
            req = Request.blank('/a/c/o', {}, headers={
                'Content-Length': str(MAX_FILE_SIZE + 1),
                'Content-Type': 'foo/bar'})
            req.account = 'a'
            res = controller.PUT(req)
            self.assertEquals(res.status_int, 413)

    def test_PUT_getresponse_exceptions(self):
        def mock_http_connect(*code_iter, **kwargs):
            class FakeConn(object):
                def __init__(self, status):
                    self.status = status
                    self.reason = 'Fake'
                    self.host = '1.2.3.4'
                    self.port = 1024
                def getresponse(self):
                    if self.status == -1:
                        raise HTTPException()
                    return self
                def read(self, amt=None): return ''
                def send(self, amt=None): pass
                def getheader(self, name): return ''
                def getexpect(self): return FakeConn(100)
            code_iter = iter(code_iter)
            def connect(*args, **ckwargs):
                return FakeConn(code_iter.next())
            return connect
        with save_globals():
            controller = proxy_server.ObjectController(self.app, 'account',
                'container', 'object')
            def test_status_map(statuses, expected):
                self.app.memcache.store = {}
                proxy_server.http_connect = mock_http_connect(*statuses)
                req = Request.blank('/a/c/o.jpg', {})
                req.content_length = 0
                req.account = 'a'
                res = controller.PUT(req)
                expected = str(expected)
                self.assertEquals(res.status[:len(str(expected))],
                                  str(expected))
            test_status_map((200, 200, 201, 201, -1), 201)
            test_status_map((200, 200, 201, -1, -1), 503)
            test_status_map((200, 200, 503, 503, -1), 503)

    def test_POST(self):
        with save_globals():
            controller = proxy_server.ObjectController(self.app, 'account',
                'container', 'object')
            def test_status_map(statuses, expected):
                proxy_server.http_connect = fake_http_connect(*statuses)
                self.app.memcache.store = {}
                req = Request.blank('/a/c/o', {}, headers={
                                                'Content-Type': 'foo/bar'})
                req.account = 'a'
                res = controller.POST(req)
                expected = str(expected)
                self.assertEquals(res.status[:len(expected)], expected)
            test_status_map((200, 200, 202, 202, 202), 202)
            test_status_map((200, 200, 202, 202, 500), 202)
            test_status_map((200, 200, 202, 500, 500), 503)
            test_status_map((200, 200, 202, 404, 500), 503)
            test_status_map((200, 200, 202, 404, 404), 404)
            test_status_map((200, 200, 404, 500, 500), 503)
            test_status_map((200, 200, 404, 404, 404), 404)

    def test_DELETE(self):
        with save_globals():
            controller = proxy_server.ObjectController(self.app, 'account',
                'container', 'object')
            def test_status_map(statuses, expected):
                proxy_server.http_connect = fake_http_connect(*statuses)
                self.app.memcache.store = {}
                req = Request.blank('/a/c/o', {})
                req.account = 'a'
                res = controller.DELETE(req)
                self.assertEquals(res.status[:len(str(expected))],
                                  str(expected))
            test_status_map((200, 200, 204, 204, 204), 204)
            test_status_map((200, 200, 204, 204, 500), 204)
            test_status_map((200, 200, 204, 404, 404), 404)
            test_status_map((200, 200, 204, 500, 404), 503)
            test_status_map((200, 200, 404, 404, 404), 404)
            test_status_map((200, 200, 404, 404, 500), 404)

    def test_HEAD(self):
        with save_globals():
            controller = proxy_server.ObjectController(self.app, 'account',
                'container', 'object')
            def test_status_map(statuses, expected):
                proxy_server.http_connect = fake_http_connect(*statuses)
                self.app.memcache.store = {}
                req = Request.blank('/a/c/o', {})
                req.account = 'a'
                res = controller.HEAD(req)
                self.assertEquals(res.status[:len(str(expected))],
                                  str(expected))
                if expected < 400:
                    self.assert_('x-works' in res.headers)
                    self.assertEquals(res.headers['x-works'], 'yes')
            test_status_map((200, 404, 404), 200)
            test_status_map((200, 500, 404), 200)
            test_status_map((304, 500, 404), 304)
            test_status_map((404, 404, 404), 404)
            test_status_map((404, 404, 500), 404)
            test_status_map((500, 500, 500), 503)

    def test_POST_meta_val_len(self):
        with save_globals():
            controller = proxy_server.ObjectController(self.app, 'account',
                'container', 'object')
            proxy_server.http_connect = \
                fake_http_connect(200, 200, 202, 202, 202)
                #                 acct cont obj  obj  obj
            req = Request.blank('/a/c/o', {}, headers={
                                            'Content-Type': 'foo/bar',
                                            'X-Object-Meta-Foo': 'x'*256})
            req.account = 'a'
            res = controller.POST(req)
            self.assertEquals(res.status_int, 202)
            proxy_server.http_connect = fake_http_connect(202, 202, 202)
            req = Request.blank('/a/c/o', {}, headers={
                                            'Content-Type': 'foo/bar',
                                            'X-Object-Meta-Foo': 'x'*257})
            req.account = 'a'
            res = controller.POST(req)
            self.assertEquals(res.status_int, 400)

    def test_POST_meta_key_len(self):
        with save_globals():
            controller = proxy_server.ObjectController(self.app, 'account',
                'container', 'object')
            proxy_server.http_connect = \
                fake_http_connect(200, 200, 202, 202, 202)
                #                 acct cont obj  obj  obj
            req = Request.blank('/a/c/o', {}, headers={
                                            'Content-Type': 'foo/bar',
                                            ('X-Object-Meta-'+'x'*128): 'x'})
            req.account = 'a'
            res = controller.POST(req)
            self.assertEquals(res.status_int, 202)
            proxy_server.http_connect = fake_http_connect(202, 202, 202)
            req = Request.blank('/a/c/o', {}, headers={
                                            'Content-Type': 'foo/bar',
                                            ('X-Object-Meta-'+'x'*129): 'x'})
            req.account = 'a'
            res = controller.POST(req)
            self.assertEquals(res.status_int, 400)

    def test_POST_meta_count(self):
        with save_globals():
            controller = proxy_server.ObjectController(self.app, 'account',
                'container', 'object')
            headers = dict((('X-Object-Meta-'+str(i), 'a') for i in xrange(91)))
            headers.update({'Content-Type': 'foo/bar'})
            proxy_server.http_connect = fake_http_connect(202, 202, 202)
            req = Request.blank('/a/c/o', {}, headers=headers)
            req.account = 'a'
            res = controller.POST(req)
            self.assertEquals(res.status_int, 400)

    def test_POST_meta_size(self):
        with save_globals():
            controller = proxy_server.ObjectController(self.app, 'account',
                'container', 'object')
            headers = dict((('X-Object-Meta-'+str(i), 'a'*256) for i in xrange(1000)))
            headers.update({'Content-Type': 'foo/bar'})
            proxy_server.http_connect = fake_http_connect(202, 202, 202)
            req = Request.blank('/a/c/o', {}, headers=headers)
            req.account = 'a'
            res = controller.POST(req)
            self.assertEquals(res.status_int, 400)

    def test_client_timeout(self):
        with save_globals():
            self.app.account_ring.get_nodes('account')
            for dev in self.app.account_ring.devs.values():
                dev['ip'] = '127.0.0.1'
                dev['port'] = 1
            self.app.container_ring.get_nodes('account')
            for dev in self.app.container_ring.devs.values():
                dev['ip'] = '127.0.0.1'
                dev['port'] = 1
            self.app.object_ring.get_nodes('account')
            for dev in self.app.object_ring.devs.values():
                dev['ip'] = '127.0.0.1'
                dev['port'] = 1
            class SlowBody():
                def __init__(self):
                    self.sent = 0
                def read(self, size=-1):
                    if self.sent < 4:
                        sleep(0.1)
                        self.sent += 1
                        return ' '
                    return ''
            req = Request.blank('/a/c/o',
                environ={'REQUEST_METHOD': 'PUT', 'wsgi.input': SlowBody()},
                headers={'Content-Length': '4', 'Content-Type': 'text/plain'})
            req.account = 'account'
            controller = proxy_server.ObjectController(self.app, 'account',
                                                       'container', 'object')
            proxy_server.http_connect = \
                fake_http_connect(200, 200, 201, 201, 201)
                #                 acct cont obj  obj  obj
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 201)
            self.app.client_timeout = 0.1
            req = Request.blank('/a/c/o',
                environ={'REQUEST_METHOD': 'PUT', 'wsgi.input': SlowBody()},
                headers={'Content-Length': '4', 'Content-Type': 'text/plain'})
            req.account = 'account'
            proxy_server.http_connect = \
                fake_http_connect(201, 201, 201)
                #                 obj  obj  obj
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 408)

    def test_client_disconnect(self):
        with save_globals():
            self.app.account_ring.get_nodes('account')
            for dev in self.app.account_ring.devs.values():
                dev['ip'] = '127.0.0.1'
                dev['port'] = 1
            self.app.container_ring.get_nodes('account')
            for dev in self.app.container_ring.devs.values():
                dev['ip'] = '127.0.0.1'
                dev['port'] = 1
            self.app.object_ring.get_nodes('account')
            for dev in self.app.object_ring.devs.values():
                dev['ip'] = '127.0.0.1'
                dev['port'] = 1
            class SlowBody():
                def __init__(self):
                    self.sent = 0
                def read(self, size=-1):
                    raise Exception('Disconnected')
            req = Request.blank('/a/c/o',
                environ={'REQUEST_METHOD': 'PUT', 'wsgi.input': SlowBody()},
                headers={'Content-Length': '4', 'Content-Type': 'text/plain'})
            req.account = 'account'
            controller = proxy_server.ObjectController(self.app, 'account',
                                                       'container', 'object')
            proxy_server.http_connect = \
                fake_http_connect(200, 200, 201, 201, 201)
                #                 acct cont obj  obj  obj
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 499)

    def test_node_read_timeout(self):
        with save_globals():
            self.app.account_ring.get_nodes('account')
            for dev in self.app.account_ring.devs.values():
                dev['ip'] = '127.0.0.1'
                dev['port'] = 1
            self.app.container_ring.get_nodes('account')
            for dev in self.app.container_ring.devs.values():
                dev['ip'] = '127.0.0.1'
                dev['port'] = 1
            self.app.object_ring.get_nodes('account')
            for dev in self.app.object_ring.devs.values():
                dev['ip'] = '127.0.0.1'
                dev['port'] = 1
            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'GET'})
            req.account = 'account'
            controller = proxy_server.ObjectController(self.app, 'account',
                                                       'container', 'object')
            proxy_server.http_connect = \
                fake_http_connect(200, 200, 200, slow=True)
            req.sent_size = 0
            resp = controller.GET(req)
            got_exc = False
            try:
                resp.body
            except proxy_server.ChunkReadTimeout:
                got_exc = True
            self.assert_(not got_exc)
            self.app.node_timeout=0.1
            proxy_server.http_connect = \
                fake_http_connect(200, 200, 200, slow=True)
            resp = controller.GET(req)
            got_exc = False
            try:
                resp.body
            except proxy_server.ChunkReadTimeout:
                got_exc = True
            self.assert_(got_exc)

    def test_node_write_timeout(self):
        with save_globals():
            self.app.account_ring.get_nodes('account')
            for dev in self.app.account_ring.devs.values():
                dev['ip'] = '127.0.0.1'
                dev['port'] = 1
            self.app.container_ring.get_nodes('account')
            for dev in self.app.container_ring.devs.values():
                dev['ip'] = '127.0.0.1'
                dev['port'] = 1
            self.app.object_ring.get_nodes('account')
            for dev in self.app.object_ring.devs.values():
                dev['ip'] = '127.0.0.1'
                dev['port'] = 1
            req = Request.blank('/a/c/o',
                environ={'REQUEST_METHOD': 'PUT'},
                headers={'Content-Length': '4', 'Content-Type': 'text/plain'},
                body='    ')
            req.account = 'account'
            controller = proxy_server.ObjectController(self.app, 'account',
                                                       'container', 'object')
            proxy_server.http_connect = \
                fake_http_connect(200, 200, 201, 201, 201, slow=True)
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 201)
            self.app.node_timeout=0.1
            proxy_server.http_connect = \
                fake_http_connect(201, 201, 201, slow=True)
            req = Request.blank('/a/c/o',
                environ={'REQUEST_METHOD': 'PUT'},
                headers={'Content-Length': '4', 'Content-Type': 'text/plain'},
                body='    ')
            req.account = 'account'
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 503)

    def test_iter_nodes(self):
        with save_globals():
            try:
                self.app.object_ring.max_more_nodes = 2
                controller = proxy_server.ObjectController(self.app, 'account',
                                'container', 'object')
                partition, nodes = self.app.object_ring.get_nodes('account',
                                    'container', 'object')
                collected_nodes = []
                for node in controller.iter_nodes(partition, nodes,
                                                  self.app.object_ring):
                    collected_nodes.append(node)
                self.assertEquals(len(collected_nodes), 5)

                self.app.object_ring.max_more_nodes = 20
                controller = proxy_server.ObjectController(self.app, 'account',
                                'container', 'object')
                partition, nodes = self.app.object_ring.get_nodes('account',
                                    'container', 'object')
                collected_nodes = []
                for node in controller.iter_nodes(partition, nodes,
                                                  self.app.object_ring):
                    collected_nodes.append(node)
                self.assertEquals(len(collected_nodes), 9)
            finally:
                self.app.object_ring.max_more_nodes = 0

    def test_best_response_sets_etag(self):
        controller = proxy_server.ObjectController(self.app, 'account',
                                                   'container', 'object')
        req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'GET'})
        resp = controller.best_response(req, [200] * 3, ['OK'] * 3, [''] * 3,
                                        'Object')
        self.assertEquals(resp.etag, None)
        resp = controller.best_response(req, [200] * 3, ['OK'] * 3, [''] * 3,
            'Object', etag='68b329da9893e34099c7d8ad5cb9c940')
        self.assertEquals(resp.etag, '68b329da9893e34099c7d8ad5cb9c940')

    def test_proxy_passes_content_type(self):
        with save_globals():
            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'GET'})
            req.account = 'account'
            controller = proxy_server.ObjectController(self.app, 'account',
                                                       'container', 'object')
            proxy_server.http_connect = fake_http_connect(200, 200, 200)
            resp = controller.GET(req)
            self.assertEquals(resp.status_int, 200)
            self.assertEquals(resp.content_type, 'x-application/test')
            proxy_server.http_connect = fake_http_connect(200, 200, 200)
            resp = controller.GET(req)
            self.assertEquals(resp.status_int, 200)
            self.assertEquals(resp.content_length, 0)
            proxy_server.http_connect = \
                fake_http_connect(200, 200, 200, slow=True)
            resp = controller.GET(req)
            self.assertEquals(resp.status_int, 200)
            self.assertEquals(resp.content_length, 4)

    def test_proxy_passes_content_length_on_head(self):
        with save_globals():
            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'HEAD'})
            req.account = 'account'
            controller = proxy_server.ObjectController(self.app, 'account',
                                                       'container', 'object')
            proxy_server.http_connect = fake_http_connect(200, 200, 200)
            resp = controller.HEAD(req)
            self.assertEquals(resp.status_int, 200)
            self.assertEquals(resp.content_length, 0)
            proxy_server.http_connect = \
                fake_http_connect(200, 200, 200, slow=True)
            resp = controller.HEAD(req)
            self.assertEquals(resp.status_int, 200)
            self.assertEquals(resp.content_length, 4)

    def test_error_limiting(self):
        with save_globals():
            controller = proxy_server.ObjectController(self.app, 'account',
                                                       'container', 'object')
            self.assert_status_map(controller.HEAD, (503, 200, 200), 200)
            self.assertEquals(controller.app.object_ring.devs[0]['errors'], 2)
            self.assert_('last_error' in controller.app.object_ring.devs[0])
            for _ in xrange(self.app.error_suppression_limit):
                self.assert_status_map(controller.HEAD, (503, 503, 503), 503)
            self.assertEquals(controller.app.object_ring.devs[0]['errors'],
                              self.app.error_suppression_limit + 1)
            self.assert_status_map(controller.HEAD, (200, 200, 200), 503)
            self.assert_('last_error' in controller.app.object_ring.devs[0])
            self.assert_status_map(controller.PUT, (200, 201, 201, 201), 503)
            self.assert_status_map(controller.POST, (200, 202, 202, 202), 503)
            self.assert_status_map(controller.DELETE, (200, 204, 204, 204), 503)
            self.app.error_suppression_interval = -300
            self.assert_status_map(controller.HEAD, (200, 200, 200), 200)
            self.assertRaises(BaseException,
                self.assert_status_map, controller.DELETE,
                (200, 204, 204, 204), 503, raise_exc=True)

    def test_acc_or_con_missing_returns_404(self):
        with save_globals():
            self.app.memcache = FakeMemcacheReturnsNone()
            for dev in self.app.account_ring.devs.values():
                del dev['errors']
                del dev['last_error']
            for dev in self.app.container_ring.devs.values():
                del dev['errors']
                del dev['last_error']
            controller = proxy_server.ObjectController(self.app, 'account',
                                                     'container', 'object')
            proxy_server.http_connect = \
                fake_http_connect(200, 200, 200, 200, 200, 200)
            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'DELETE'})
            req.account = 'a'
            resp = getattr(controller, 'DELETE')(req)
            self.assertEquals(resp.status_int, 200)

            proxy_server.http_connect = \
                fake_http_connect(404, 404, 404)
                #                 acct acct acct
            resp = getattr(controller, 'DELETE')(req)
            self.assertEquals(resp.status_int, 404)

            proxy_server.http_connect = \
                fake_http_connect(503, 404, 404)
                #                 acct acct acct
            resp = getattr(controller, 'DELETE')(req)
            self.assertEquals(resp.status_int, 404)

            proxy_server.http_connect = \
                fake_http_connect(503, 503, 404)
                #                 acct acct acct
            resp = getattr(controller, 'DELETE')(req)
            self.assertEquals(resp.status_int, 404)

            proxy_server.http_connect = \
                fake_http_connect(503, 503, 503)
                #                 acct acct acct
            resp = getattr(controller, 'DELETE')(req)
            self.assertEquals(resp.status_int, 404)

            proxy_server.http_connect = \
                fake_http_connect(200, 200, 204, 204, 204)
                #                 acct cont obj  obj  obj
            resp = getattr(controller, 'DELETE')(req)
            self.assertEquals(resp.status_int, 204)

            proxy_server.http_connect = \
                fake_http_connect(200, 404, 404, 404)
                #                 acct cont cont cont
            resp = getattr(controller, 'DELETE')(req)
            self.assertEquals(resp.status_int, 404)

            proxy_server.http_connect = \
                fake_http_connect(200, 503, 503, 503)
                #                 acct cont cont cont
            resp = getattr(controller, 'DELETE')(req)
            self.assertEquals(resp.status_int, 404)

            for dev in self.app.account_ring.devs.values():
                dev['errors'] = self.app.error_suppression_limit + 1
                dev['last_error'] = time()
            proxy_server.http_connect = \
                fake_http_connect(200)
                #                 acct [isn't actually called since everything
                #                       is error limited]
            resp = getattr(controller, 'DELETE')(req)
            self.assertEquals(resp.status_int, 404)

            for dev in self.app.account_ring.devs.values():
                dev['errors'] = 0
            for dev in self.app.container_ring.devs.values():
                dev['errors'] = self.app.error_suppression_limit + 1
                dev['last_error'] = time()
            proxy_server.http_connect = \
                fake_http_connect(200, 200)
                #                 acct cont [isn't actually called since
                #                            everything is error limited]
            resp = getattr(controller, 'DELETE')(req)
            self.assertEquals(resp.status_int, 404)

    def test_PUT_POST_requires_container_exist(self):
        with save_globals():
            self.app.memcache = FakeMemcacheReturnsNone()
            controller = proxy_server.ObjectController(self.app, 'account',
                                                       'container', 'object')
            proxy_server.http_connect = \
                fake_http_connect(404, 404, 404, 200, 200, 200)
            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'PUT'})
            req.account = 'a'
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 404)

            proxy_server.http_connect = \
                fake_http_connect(404, 404, 404, 200, 200, 200)
            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'POST'},
                                headers={'Content-Type': 'text/plain'})
            req.account = 'a'
            resp = controller.POST(req)
            self.assertEquals(resp.status_int, 404)

    def test_bad_metadata(self):
        with save_globals():
            controller = proxy_server.ObjectController(self.app, 'account',
                                                       'container', 'object')
            proxy_server.http_connect = \
                fake_http_connect(200, 200, 201, 201, 201)
                #                 acct cont obj  obj  obj
            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'PUT'},
                                headers={'Content-Length': '0'})
            req.account = 'a'
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 201)

            proxy_server.http_connect = fake_http_connect(201, 201, 201)
            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'PUT'},
                headers={'Content-Length': '0',
                         'X-Object-Meta-' + ('a' *
                            MAX_META_NAME_LENGTH) : 'v'})
            req.account = 'a'
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 201)
            proxy_server.http_connect = fake_http_connect(201, 201, 201)
            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'PUT'},
                headers={'Content-Length': '0',
                         'X-Object-Meta-' + ('a' *
                            (MAX_META_NAME_LENGTH + 1)) : 'v'})
            req.account = 'a'
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 400)

            proxy_server.http_connect = fake_http_connect(201, 201, 201)
            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'PUT'},
                headers={'Content-Length': '0',
                         'X-Object-Meta-Too-Long': 'a' *
                            MAX_META_VALUE_LENGTH})
            req.account = 'a'
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 201)
            proxy_server.http_connect = fake_http_connect(201, 201, 201)
            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'PUT'},
                headers={'Content-Length': '0',
                         'X-Object-Meta-Too-Long': 'a' *
                            (MAX_META_VALUE_LENGTH + 1)})
            req.account = 'a'
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 400)

            proxy_server.http_connect = fake_http_connect(201, 201, 201)
            headers = {'Content-Length': '0'}
            for x in xrange(MAX_META_COUNT):
                headers['X-Object-Meta-%d' % x] = 'v'
            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'PUT'},
                                headers=headers)
            req.account = 'a'
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 201)
            proxy_server.http_connect = fake_http_connect(201, 201, 201)
            headers = {'Content-Length': '0'}
            for x in xrange(MAX_META_COUNT + 1):
                headers['X-Object-Meta-%d' % x] = 'v'
            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'PUT'},
                                headers=headers)
            req.account = 'a'
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 400)

            proxy_server.http_connect = fake_http_connect(201, 201, 201)
            headers = {'Content-Length': '0'}
            header_value = 'a' * MAX_META_VALUE_LENGTH
            size = 0
            x = 0
            while size < MAX_META_OVERALL_SIZE - 4 - \
                    MAX_META_VALUE_LENGTH:
                size += 4 + MAX_META_VALUE_LENGTH
                headers['X-Object-Meta-%04d' % x] = header_value
                x += 1
            if MAX_META_OVERALL_SIZE - size > 1:
                headers['X-Object-Meta-a'] = \
                    'a' * (MAX_META_OVERALL_SIZE - size - 1)
            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'PUT'},
                                headers=headers)
            req.account = 'a'
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 201)
            proxy_server.http_connect = fake_http_connect(201, 201, 201)
            headers['X-Object-Meta-a'] = \
                'a' * (MAX_META_OVERALL_SIZE - size)
            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'PUT'},
                                headers=headers)
            req.account = 'a'
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 400)

    def test_copy_from(self):
        with save_globals():
            controller = proxy_server.ObjectController(self.app, 'account',
                                                       'container', 'object')
            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'PUT'},
                                headers={'Content-Length': '0'})
            req.account = 'a'
            proxy_server.http_connect = \
                fake_http_connect(200, 200, 201, 201, 201)
                #                 acct cont obj  obj  obj
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 201)

            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'PUT'},
                                headers={'Content-Length': '0',
                                          'X-Copy-From': 'c/o'})
            req.account = 'a'
            proxy_server.http_connect = \
                fake_http_connect(200, 200, 200, 200, 200, 201, 201, 201)
                #                 acct cont acct cont objc obj  obj  obj
            self.app.memcache.store = {}
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 201)
            self.assertEquals(resp.headers['x-copied-from'], 'c/o')

            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'PUT'},
                                headers={'Content-Length': '0',
                                          'X-Copy-From': '/c/o'})
            req.account = 'a'
            proxy_server.http_connect = \
                fake_http_connect(200, 200, 200, 200, 200, 201, 201, 201)
                #                 acct cont acct cont objc obj  obj  obj
            self.app.memcache.store = {}
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 201)
            self.assertEquals(resp.headers['x-copied-from'], 'c/o')

            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'PUT'},
                                headers={'Content-Length': '0',
                                          'X-Copy-From': '/c/o'})
            req.account = 'a'
            proxy_server.http_connect = \
                fake_http_connect(200, 200, 503, 503, 503)
                #                 acct cont objc objc objc
            self.app.memcache.store = {}
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 503)

            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'PUT'},
                                headers={'Content-Length': '0',
                                          'X-Copy-From': '/c/o'})
            req.account = 'a'
            proxy_server.http_connect = \
                fake_http_connect(200, 200, 404, 404, 404)
                #                 acct cont objc objc objc
            self.app.memcache.store = {}
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 404)

            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'PUT'},
                                headers={'Content-Length': '0',
                                          'X-Copy-From': '/c/o'})
            req.account = 'a'
            proxy_server.http_connect = \
                fake_http_connect(200, 200, 404, 404, 200, 201, 201, 201)
                #                 acct cont objc objc objc obj  obj  obj
            self.app.memcache.store = {}
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 201)

            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'PUT'},
                                headers={'Content-Length': '0',
                                          'X-Copy-From': '/c/o',
                                          'X-Object-Meta-Ours': 'okay'})
            req.account = 'a'
            proxy_server.http_connect = \
                fake_http_connect(200, 200, 200, 201, 201, 201)
                #                 acct cont objc obj  obj  obj
            self.app.memcache.store = {}
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 201)
            self.assertEquals(resp.headers.get('x-object-meta-test'), 'testing')
            self.assertEquals(resp.headers.get('x-object-meta-ours'), 'okay')

    def test_chunked_put_and_a_bit_more(self):
        # Since we're starting up a lot here, we're going to test more than
        # just chunked puts; we're also going to test parts of
        # proxy_server.Application we couldn't get to easily otherwise.
        path_to_test_xfs = os.environ.get('PATH_TO_TEST_XFS')
        if not path_to_test_xfs or not os.path.exists(path_to_test_xfs):
            print >>sys.stderr, 'WARNING: PATH_TO_TEST_XFS not set or not ' \
                'pointing to a valid directory.\n' \
                'Please set PATH_TO_TEST_XFS to a directory on an XFS file ' \
                'system for testing.'
            return
        testdir = \
            os.path.join(path_to_test_xfs, 'tmp_test_proxy_server_chunked')
        mkdirs(testdir)
        rmtree(testdir)
        mkdirs(os.path.join(testdir, 'sda1'))
        mkdirs(os.path.join(testdir, 'sda1', 'tmp'))
        mkdirs(os.path.join(testdir, 'sdb1'))
        mkdirs(os.path.join(testdir, 'sdb1', 'tmp'))
        try:
            conf = {'devices': testdir, 'swift_dir': testdir,
                    'mount_check': 'false'}
            prolis = listen(('localhost', 0))
            acc1lis = listen(('localhost', 0))
            acc2lis = listen(('localhost', 0))
            con1lis = listen(('localhost', 0))
            con2lis = listen(('localhost', 0))
            obj1lis = listen(('localhost', 0))
            obj2lis = listen(('localhost', 0))
            pickle.dump(ring.RingData([[0, 1, 0, 1], [1, 0, 1, 0]],
                [{'id': 0, 'zone': 0, 'device': 'sda1', 'ip': '127.0.0.1',
                  'port': acc1lis.getsockname()[1]},
                 {'id': 1, 'zone': 1, 'device': 'sdb1', 'ip': '127.0.0.1',
                  'port': acc2lis.getsockname()[1]}], 30),
                GzipFile(os.path.join(testdir, 'account.ring.gz'), 'wb'))
            pickle.dump(ring.RingData([[0, 1, 0, 1], [1, 0, 1, 0]],
                [{'id': 0, 'zone': 0, 'device': 'sda1', 'ip': '127.0.0.1',
                  'port': con1lis.getsockname()[1]},
                 {'id': 1, 'zone': 1, 'device': 'sdb1', 'ip': '127.0.0.1',
                  'port': con2lis.getsockname()[1]}], 30),
                GzipFile(os.path.join(testdir, 'container.ring.gz'), 'wb'))
            pickle.dump(ring.RingData([[0, 1, 0, 1], [1, 0, 1, 0]],
                [{'id': 0, 'zone': 0, 'device': 'sda1', 'ip': '127.0.0.1',
                  'port': obj1lis.getsockname()[1]},
                 {'id': 1, 'zone': 1, 'device': 'sdb1', 'ip': '127.0.0.1',
                  'port': obj2lis.getsockname()[1]}], 30),
                GzipFile(os.path.join(testdir, 'object.ring.gz'), 'wb'))
            prosrv = proxy_server.Application(conf, FakeMemcacheReturnsNone())
            acc1srv = account_server.AccountController(conf)
            acc2srv = account_server.AccountController(conf)
            con1srv = container_server.ContainerController(conf)
            con2srv = container_server.ContainerController(conf)
            obj1srv = object_server.ObjectController(conf)
            obj2srv = object_server.ObjectController(conf)
            nl = NullLogger()
            prospa = spawn(wsgi.server, prolis, prosrv, nl)
            acc1spa = spawn(wsgi.server, acc1lis, acc1srv, nl)
            acc2spa = spawn(wsgi.server, acc2lis, acc2srv, nl)
            con1spa = spawn(wsgi.server, con1lis, con1srv, nl)
            con2spa = spawn(wsgi.server, con2lis, con2srv, nl)
            obj1spa = spawn(wsgi.server, obj1lis, obj1srv, nl)
            obj2spa = spawn(wsgi.server, obj2lis, obj2srv, nl)
            try:
                # healthcheck test
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('GET /healthcheck HTTP/1.1\r\nHost: localhost\r\n'
                    'Connection: close\r\nContent-Length: 0\r\n\r\n')
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 200'
                self.assertEquals(headers[:len(exp)], exp)
                body = fd.read()
                self.assertEquals(body, 'OK')
                # Check bad version
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('GET /v0 HTTP/1.1\r\nHost: localhost\r\n'
                    'Connection: close\r\nContent-Length: 0\r\n\r\n')
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 412'
                self.assertEquals(headers[:len(exp)], exp)
                # Check bad path
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('GET invalid HTTP/1.1\r\nHost: localhost\r\n'
                    'Connection: close\r\nContent-Length: 0\r\n\r\n')
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 404'
                self.assertEquals(headers[:len(exp)], exp)
                # Check bad method
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('LICK /healthcheck HTTP/1.1\r\nHost: localhost\r\n'
                    'Connection: close\r\nContent-Length: 0\r\n\r\n')
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 405'
                self.assertEquals(headers[:len(exp)], exp)
                # Check blacklist
                prosrv.rate_limit_blacklist = ['a']
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('GET /v1/a HTTP/1.1\r\nHost: localhost\r\n'
                    'Connection: close\r\nContent-Length: 0\r\n\r\n')
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 497'
                self.assertEquals(headers[:len(exp)], exp)
                prosrv.rate_limit_blacklist = []
                # Check invalid utf-8
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('GET /v1/a%80 HTTP/1.1\r\nHost: localhost\r\n'
                    'Connection: close\r\nX-Auth-Token: t\r\n'
                    'Content-Length: 0\r\n\r\n')
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 412'
                self.assertEquals(headers[:len(exp)], exp)
                # Check bad path, no controller
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('GET /v1 HTTP/1.1\r\nHost: localhost\r\n'
                    'Connection: close\r\nX-Auth-Token: t\r\n'
                    'Content-Length: 0\r\n\r\n')
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 412'
                self.assertEquals(headers[:len(exp)], exp)
                # Check rate limiting
                orig_rate_limit = prosrv.rate_limit
                prosrv.rate_limit = 0
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('GET /v1/a HTTP/1.1\r\nHost: localhost\r\n'
                    'Connection: close\r\nX-Auth-Token: t\r\n'
                    'Content-Length: 0\r\n\r\n')
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 498'
                self.assertEquals(headers[:len(exp)], exp)
                prosrv.rate_limit = orig_rate_limit
                orig_rate_limit = prosrv.account_rate_limit
                prosrv.account_rate_limit = 0
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('PUT /v1/a/c HTTP/1.1\r\nHost: localhost\r\n'
                    'Connection: close\r\nX-Auth-Token: t\r\n'
                    'Content-Length: 0\r\n\r\n')
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 498'
                self.assertEquals(headers[:len(exp)], exp)
                prosrv.account_rate_limit = orig_rate_limit
                # Check bad method
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('LICK /v1/a HTTP/1.1\r\nHost: localhost\r\n'
                    'Connection: close\r\nX-Auth-Token: t\r\n'
                    'Content-Length: 0\r\n\r\n')
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 405'
                self.assertEquals(headers[:len(exp)], exp)
                # Check unhandled exception
                orig_rate_limit = prosrv.rate_limit
                del prosrv.rate_limit
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('HEAD /v1/a HTTP/1.1\r\nHost: localhost\r\n'
                    'Connection: close\r\nX-Auth-Token: t\r\n'
                    'Content-Length: 0\r\n\r\n')
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 500'
                self.assertEquals(headers[:len(exp)], exp)
                prosrv.rate_limit = orig_rate_limit
                # Okay, back to chunked put testing; Create account
                ts = normalize_timestamp(time())
                partition, nodes = prosrv.account_ring.get_nodes('a')
                for node in nodes:
                    conn = proxy_server.http_connect(node['ip'], node['port'],
                            node['device'], partition, 'PUT', '/a',
                            {'X-Timestamp': ts, 'X-CF-Trans-Id': 'test'})
                    resp = conn.getresponse()
                    self.assertEquals(resp.status, 201)
                # Head account, just a double check and really is here to test
                # the part Application.log_request that 'enforces' a
                # content_length on the response.
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('HEAD /v1/a HTTP/1.1\r\nHost: localhost\r\n'
                    'Connection: close\r\nX-Auth-Token: t\r\n'
                    'Content-Length: 0\r\n\r\n')
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 204'
                self.assertEquals(headers[:len(exp)], exp)
                self.assert_('\r\nContent-Length: 0\r\n' in headers)
                # Create container
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('PUT /v1/a/c HTTP/1.1\r\nHost: localhost\r\n'
                    'Connection: close\r\nX-Auth-Token: t\r\n'
                    'Content-Length: 0\r\n\r\n')
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 201'
                self.assertEquals(headers[:len(exp)], exp)
                # GET account with a query string to test that
                # Application.log_request logs the query string. Also, throws
                # in a test for logging x-forwarded-for (first entry only).
                class Logger(object):
                    def info(self, msg):
                        self.msg = msg
                orig_logger = prosrv.logger
                prosrv.logger = Logger()
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('GET /v1/a?format=json HTTP/1.1\r\nHost: localhost\r\n'
                    'Connection: close\r\nX-Auth-Token: t\r\n'
                    'Content-Length: 0\r\nX-Forwarded-For: host1, host2\r\n'
                    '\r\n')
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 200'
                self.assertEquals(headers[:len(exp)], exp)
                self.assert_('/v1/a%3Fformat%3Djson' in prosrv.logger.msg,
                             prosrv.logger.msg)
                exp = 'host1'
                self.assertEquals(prosrv.logger.msg[:len(exp)], exp)
                prosrv.logger = orig_logger
                # Turn on header logging.
                class Logger(object):
                    def info(self, msg):
                        self.msg = msg
                orig_logger = prosrv.logger
                prosrv.logger = Logger()
                prosrv.log_headers = True
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('GET /v1/a HTTP/1.1\r\nHost: localhost\r\n'
                    'Connection: close\r\nX-Auth-Token: t\r\n'
                    'Content-Length: 0\r\nGoofy-Header: True\r\n\r\n')
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 200'
                self.assertEquals(headers[:len(exp)], exp)
                self.assert_('Goofy-Header%3A%20True' in prosrv.logger.msg,
                             prosrv.logger.msg)
                prosrv.log_headers = False
                prosrv.logger = orig_logger
                # Test UTF-8 Unicode all the way through the system
                ustr = '\xe1\xbc\xb8\xce\xbf\xe1\xbd\xba \xe1\xbc\xb0\xce' \
                       '\xbf\xe1\xbd\xbb\xce\x87 \xcf\x84\xe1\xbd\xb0 \xcf' \
                       '\x80\xe1\xbd\xb1\xce\xbd\xcf\x84\xca\xbc \xe1\xbc' \
                       '\x82\xce\xbd \xe1\xbc\x90\xce\xbe\xe1\xbd\xb5\xce' \
                       '\xba\xce\xbf\xce\xb9 \xcf\x83\xce\xb1\xcf\x86\xe1' \
                       '\xbf\x86.Test'
                ustr_short = '\xe1\xbc\xb8\xce\xbf\xe1\xbd\xbatest'
                # Create ustr container
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('PUT /v1/a/%s HTTP/1.1\r\nHost: localhost\r\n'
                         'Connection: close\r\nX-Storage-Token: t\r\n'
                         'Content-Length: 0\r\n\r\n' % quote(ustr))
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 201'
                self.assertEquals(headers[:len(exp)], exp)
                # List account with ustr container (test plain)
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('GET /v1/a HTTP/1.1\r\nHost: localhost\r\n'
                         'Connection: close\r\nX-Storage-Token: t\r\n'
                         'Content-Length: 0\r\n\r\n')
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 200'
                self.assertEquals(headers[:len(exp)], exp)
                containers = fd.read().split('\n')
                self.assert_(ustr in containers)
                # List account with ustr container (test json)
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('GET /v1/a?format=json HTTP/1.1\r\n'
                         'Host: localhost\r\nConnection: close\r\n'
                         'X-Storage-Token: t\r\nContent-Length: 0\r\n\r\n')
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 200'
                self.assertEquals(headers[:len(exp)], exp)
                listing = simplejson.loads(fd.read())
                self.assertEquals(listing[1]['name'], ustr.decode('utf8'))
                # List account with ustr container (test xml)
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('GET /v1/a?format=xml HTTP/1.1\r\n'
                         'Host: localhost\r\nConnection: close\r\n'
                         'X-Storage-Token: t\r\nContent-Length: 0\r\n\r\n')
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 200'
                self.assertEquals(headers[:len(exp)], exp)
                self.assert_('<name>%s</name>' % ustr in fd.read())
                # Create ustr object with ustr metadata in ustr container
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('PUT /v1/a/%s/%s HTTP/1.1\r\nHost: localhost\r\n'
                         'Connection: close\r\nX-Storage-Token: t\r\n'
                         'X-Object-Meta-%s: %s\r\nContent-Length: 0\r\n\r\n' %
                         (quote(ustr), quote(ustr), quote(ustr_short),
                          quote(ustr)))
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 201'
                self.assertEquals(headers[:len(exp)], exp)
                # List ustr container with ustr object (test plain)
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('GET /v1/a/%s HTTP/1.1\r\nHost: localhost\r\n'
                         'Connection: close\r\nX-Storage-Token: t\r\n'
                         'Content-Length: 0\r\n\r\n' % quote(ustr))
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 200'
                self.assertEquals(headers[:len(exp)], exp)
                objects = fd.read().split('\n')
                self.assert_(ustr in objects)
                # List ustr container with ustr object (test json)
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('GET /v1/a/%s?format=json HTTP/1.1\r\n'
                         'Host: localhost\r\nConnection: close\r\n'
                         'X-Storage-Token: t\r\nContent-Length: 0\r\n\r\n' %
                         quote(ustr))
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 200'
                self.assertEquals(headers[:len(exp)], exp)
                listing = simplejson.loads(fd.read())
                self.assertEquals(listing[0]['name'], ustr.decode('utf8'))
                # List ustr container with ustr object (test xml)
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('GET /v1/a/%s?format=xml HTTP/1.1\r\n'
                         'Host: localhost\r\nConnection: close\r\n'
                         'X-Storage-Token: t\r\nContent-Length: 0\r\n\r\n' %
                         quote(ustr))
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 200'
                self.assertEquals(headers[:len(exp)], exp)
                self.assert_('<name>%s</name>' % ustr in fd.read())
                # Retrieve ustr object with ustr metadata
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('GET /v1/a/%s/%s HTTP/1.1\r\nHost: localhost\r\n'
                         'Connection: close\r\nX-Storage-Token: t\r\n'
                         'Content-Length: 0\r\n\r\n' %
                         (quote(ustr), quote(ustr)))
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 200'
                self.assertEquals(headers[:len(exp)], exp)
                self.assert_('\r\nX-Object-Meta-%s: %s\r\n' %
                    (quote(ustr_short).lower(), quote(ustr)) in headers)
                # Do chunked object put
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                # Also happens to assert that x-storage-token is taken as a
                # replacement for x-auth-token.
                fd.write('PUT /v1/a/c/o/chunky HTTP/1.1\r\nHost: localhost\r\n'
                    'Connection: close\r\nX-Storage-Token: t\r\n'
                    'Transfer-Encoding: chunked\r\n\r\n'
                    '2\r\noh\r\n4\r\n hai\r\nf\r\n123456789abcdef\r\n'
                    '0\r\n\r\n')
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 201'
                self.assertEquals(headers[:len(exp)], exp)
                # Ensure we get what we put
                sock = connect_tcp(('localhost', prolis.getsockname()[1]))
                fd = sock.makefile()
                fd.write('GET /v1/a/c/o/chunky HTTP/1.1\r\nHost: localhost\r\n'
                         'Connection: close\r\nX-Auth-Token: t\r\n\r\n')
                fd.flush()
                headers = readuntil2crlfs(fd)
                exp = 'HTTP/1.1 200'
                self.assertEquals(headers[:len(exp)], exp)
                body = fd.read()
                self.assertEquals(body, 'oh hai123456789abcdef')
            finally:
                prospa.kill()
                acc1spa.kill()
                acc2spa.kill()
                con1spa.kill()
                con2spa.kill()
                obj1spa.kill()
                obj2spa.kill()
        finally:
            rmtree(testdir)

    def test_mismatched_etags(self):
        with save_globals():
            controller = proxy_server.ObjectController(self.app, 'account',
                                                       'container', 'object')
            req = Request.blank('/a/c/o', environ={'REQUEST_METHOD': 'PUT'},
                                headers={'Content-Length': '0'})
            req.account = 'a'
            proxy_server.http_connect = fake_http_connect(200, 201, 201, 201,
                etags=[None,
                       '68b329da9893e34099c7d8ad5cb9c940',
                       '68b329da9893e34099c7d8ad5cb9c940',
                       '68b329da9893e34099c7d8ad5cb9c941'])
            resp = controller.PUT(req)
            self.assertEquals(resp.status_int, 422)


class TestContainerController(unittest.TestCase):
    "Test swift.proxy_server.ContainerController"

    def setUp(self):
        self.app = proxy_server.Application(None, FakeMemcache(),
            account_ring=FakeRing(), container_ring=FakeRing(),
            object_ring=FakeRing())

    def assert_status_map(self, method, statuses, expected, raise_exc=False, missing_container=False):
        with save_globals():
            kwargs = {}
            if raise_exc:
                kwargs['raise_exc'] = raise_exc
            kwargs['missing_container'] = missing_container
            proxy_server.http_connect = fake_http_connect(*statuses, **kwargs)
            self.app.memcache.store = {}
            req = Request.blank('/a/c', headers={'Content-Length': '0',
                    'Content-Type': 'text/plain'})
            req.account = 'a'
            res = method(req)
            self.assertEquals(res.status_int, expected)
            proxy_server.http_connect = fake_http_connect(*statuses, **kwargs)
            self.app.memcache.store = {}
            req = Request.blank('/a/c/', headers={'Content-Length': '0',
                    'Content-Type': 'text/plain'})
            req.account = 'a'
            res = method(req)
            self.assertEquals(res.status_int, expected)

    def test_HEAD(self):
        with save_globals():
            controller = proxy_server.ContainerController(self.app, 'account',
                'container')
            def test_status_map(statuses, expected, **kwargs):
                proxy_server.http_connect = fake_http_connect(*statuses, **kwargs)
                self.app.memcache.store = {}
                req = Request.blank('/a/c', {})
                req.account = 'a'
                res = controller.HEAD(req)
                self.assertEquals(res.status[:len(str(expected))],
                                  str(expected))
                if expected < 400:
                    self.assert_('x-works' in res.headers)
                    self.assertEquals(res.headers['x-works'], 'yes')
            test_status_map((200, 200, 404, 404), 200)
            test_status_map((200, 200, 500, 404), 200)
            test_status_map((200, 304, 500, 404), 304)
            test_status_map((200, 404, 404, 404), 404)
            test_status_map((200, 404, 404, 500), 404)
            test_status_map((200, 500, 500, 500), 503)

    def test_PUT(self):
        with save_globals():
            controller = proxy_server.ContainerController(self.app, 'account',
                                                          'container')
            def test_status_map(statuses, expected, **kwargs):
                proxy_server.http_connect = fake_http_connect(*statuses, **kwargs)
                self.app.memcache.store = {}
                req = Request.blank('/a/c', {})
                req.content_length = 0
                req.account = 'a'
                res = controller.PUT(req)
                expected = str(expected)
                self.assertEquals(res.status[:len(expected)], expected)
            test_status_map((200, 201, 201, 201), 201, missing_container=True)
            test_status_map((200, 201, 201, 500), 201, missing_container=True)
            test_status_map((200, 204, 404, 404), 404, missing_container=True)
            test_status_map((200, 204, 500, 404), 503, missing_container=True)

    def test_PUT_max_container_name_length(self):
        with save_globals():
            controller = proxy_server.ContainerController(self.app, 'account',
                                                              '1'*256)
            self.assert_status_map(controller.PUT, (200, 200, 200, 201, 201, 201), 201, missing_container=True)
            controller = proxy_server.ContainerController(self.app, 'account',
                                                              '2'*257)
            self.assert_status_map(controller.PUT, (201, 201, 201), 400, missing_container=True)

    def test_PUT_connect_exceptions(self):
        with save_globals():
            controller = proxy_server.ContainerController(self.app, 'account',
                                                          'container')
            self.assert_status_map(controller.PUT, (200, 201, 201, -1), 201, missing_container=True)
            self.assert_status_map(controller.PUT, (200, 201, -1, -1), 503, missing_container=True)
            self.assert_status_map(controller.PUT, (200, 503, 503, -1), 503, missing_container=True)

    def test_acc_missing_returns_404(self):
        for meth in ('DELETE', 'PUT'):
            with save_globals():
                self.app.memcache = FakeMemcacheReturnsNone()
                for dev in self.app.account_ring.devs.values():
                    del dev['errors']
                    del dev['last_error']
                controller = proxy_server.ContainerController(self.app,
                                'account', 'container')
                if meth == 'PUT':
                    proxy_server.http_connect = \
                        fake_http_connect(200, 200, 200, 200, 200, 200, missing_container=True)
                else:
                    proxy_server.http_connect = \
                        fake_http_connect(200, 200, 200, 200)
                self.app.memcache.store = {}
                req = Request.blank('/a/c', environ={'REQUEST_METHOD': meth})
                req.account = 'a'
                resp = getattr(controller, meth)(req)
                self.assertEquals(resp.status_int, 200)

                proxy_server.http_connect = \
                    fake_http_connect(404, 404, 404, 200, 200, 200)
                resp = getattr(controller, meth)(req)
                self.assertEquals(resp.status_int, 404)

                proxy_server.http_connect = \
                    fake_http_connect(503, 404, 404)
                resp = getattr(controller, meth)(req)
                self.assertEquals(resp.status_int, 404)

                proxy_server.http_connect = \
                    fake_http_connect(503, 404, raise_exc=True)
                resp = getattr(controller, meth)(req)
                self.assertEquals(resp.status_int, 404)

                for dev in self.app.account_ring.devs.values():
                    dev['errors'] = self.app.error_suppression_limit + 1
                    dev['last_error'] = time()
                proxy_server.http_connect = \
                    fake_http_connect(200, 200, 200, 200, 200, 200)
                resp = getattr(controller, meth)(req)
                self.assertEquals(resp.status_int, 404)

    def test_put_locking(self):
        class MockMemcache(FakeMemcache):
            def __init__(self, allow_lock=None):
                self.allow_lock = allow_lock
                super(MockMemcache, self).__init__()
            @contextmanager
            def soft_lock(self, key, timeout=0, retries=5):
                if self.allow_lock:
                    yield True
                else:
                    raise MemcacheLockError()
        with save_globals():
            controller = proxy_server.ContainerController(self.app, 'account',
                                                          'container')
            self.app.memcache = MockMemcache(allow_lock=True)
            proxy_server.http_connect = fake_http_connect(200, 200, 200, 201, 201, 201, missing_container=True)
            req = Request.blank('/a/c', environ={'REQUEST_METHOD': 'PUT'})
            req.account = 'a'
            res = controller.PUT(req)
            self.assertEquals(res.status_int, 201)

    def test_error_limiting(self):
        with save_globals():
            controller = proxy_server.ContainerController(self.app, 'account',
                                                          'container')
            self.assert_status_map(controller.HEAD, (200, 503, 200, 200), 200, missing_container=False)
            self.assertEquals(
                controller.app.container_ring.devs[0]['errors'], 2)
            self.assert_('last_error' in controller.app.container_ring.devs[0])
            for _ in xrange(self.app.error_suppression_limit):
                self.assert_status_map(controller.HEAD, (200, 503, 503, 503), 503)
            self.assertEquals(controller.app.container_ring.devs[0]['errors'],
                              self.app.error_suppression_limit + 1)
            self.assert_status_map(controller.HEAD, (200, 200, 200, 200), 503)
            self.assert_('last_error' in controller.app.container_ring.devs[0])
            self.assert_status_map(controller.PUT, (200, 201, 201, 201), 503, missing_container=True)
            self.assert_status_map(controller.DELETE, (200, 204, 204, 204), 503)
            self.app.error_suppression_interval = -300
            self.assert_status_map(controller.HEAD, (200, 200, 200, 200), 200)
            self.assert_status_map(controller.DELETE, (200, 204, 204, 204), 404,
                                   raise_exc=True)

    def test_DELETE(self):
        with save_globals():
            controller = proxy_server.ContainerController(self.app, 'account',
                                                          'container')
            self.assert_status_map(controller.DELETE, (200, 204, 204, 204), 204)
            self.assert_status_map(controller.DELETE, (200, 204, 204, 503), 503)
            self.assert_status_map(controller.DELETE, (200, 204, 503, 503), 503)
            self.assert_status_map(controller.DELETE, (200, 204, 404, 404), 404)
            self.assert_status_map(controller.DELETE, (200, 404, 404, 404), 404)
            self.assert_status_map(controller.DELETE, (200, 204, 503, 404), 503)

            self.app.memcache = FakeMemcacheReturnsNone()
            # 200: Account check, 404x3: Container check
            self.assert_status_map(controller.DELETE, (200, 404, 404, 404), 404)


class TestAccountController(unittest.TestCase):

    def setUp(self):
        self.app = proxy_server.Application(None, FakeMemcache(),
            account_ring=FakeRing(), container_ring=FakeRing(),
            object_ring=FakeRing)

    def assert_status_map(self, method, statuses, expected):
        with save_globals():
            proxy_server.http_connect = fake_http_connect(*statuses)
            req = Request.blank('/a', {})
            req.account = 'a'
            res = method(req)
            self.assertEquals(res.status_int, expected)
            proxy_server.http_connect = fake_http_connect(*statuses)
            req = Request.blank('/a/', {})
            req.account = 'a'
            res = method(req)
            self.assertEquals(res.status_int, expected)

    def test_GET(self):
        with save_globals():
            controller = proxy_server.AccountController(self.app, 'account')
            self.assert_status_map(controller.GET, (200, 200, 200), 200)
            self.assert_status_map(controller.GET, (200, 200, 503), 200)
            self.assert_status_map(controller.GET, (200, 503, 503), 200)
            self.assert_status_map(controller.GET, (204, 204, 204), 204)
            self.assert_status_map(controller.GET, (204, 204, 503), 204)
            self.assert_status_map(controller.GET, (204, 503, 503), 204)
            self.assert_status_map(controller.GET, (204, 204, 200), 204)
            self.assert_status_map(controller.GET, (204, 200, 200), 204)
            self.assert_status_map(controller.GET, (404, 404, 404), 404)
            self.assert_status_map(controller.GET, (404, 404, 200), 200)
            self.assert_status_map(controller.GET, (404, 200, 200), 200)
            self.assert_status_map(controller.GET, (404, 404, 503), 404)
            self.assert_status_map(controller.GET, (404, 503, 503), 503)
            self.assert_status_map(controller.GET, (404, 204, 503), 204)

            self.app.memcache = FakeMemcacheReturnsNone()
            self.assert_status_map(controller.GET, (404, 404, 404), 404)

    def test_HEAD(self):
        with save_globals():
            controller = proxy_server.AccountController(self.app, 'account')
            self.assert_status_map(controller.HEAD, (200, 200, 200), 200)
            self.assert_status_map(controller.HEAD, (200, 200, 503), 200)
            self.assert_status_map(controller.HEAD, (200, 503, 503), 200)
            self.assert_status_map(controller.HEAD, (204, 204, 204), 204)
            self.assert_status_map(controller.HEAD, (204, 204, 503), 204)
            self.assert_status_map(controller.HEAD, (204, 503, 503), 204)
            self.assert_status_map(controller.HEAD, (204, 204, 200), 204)
            self.assert_status_map(controller.HEAD, (204, 200, 200), 204)
            self.assert_status_map(controller.HEAD, (404, 404, 404), 404)
            self.assert_status_map(controller.HEAD, (404, 404, 200), 200)
            self.assert_status_map(controller.HEAD, (404, 200, 200), 200)
            self.assert_status_map(controller.HEAD, (404, 404, 503), 404)
            self.assert_status_map(controller.HEAD, (404, 503, 503), 503)
            self.assert_status_map(controller.HEAD, (404, 204, 503), 204)

    def test_connection_refused(self):
        self.app.account_ring.get_nodes('account')
        for dev in self.app.account_ring.devs.values():
            dev['ip'] = '127.0.0.1'
            dev['port'] = 1 ## can't connect on this port
        controller = proxy_server.AccountController(self.app, 'account')
        req = Request.blank('/account', environ={'REQUEST_METHOD': 'HEAD'})
        req.account = 'account'
        resp = controller.HEAD(req)
        self.assertEquals(resp.status_int, 503)

    def test_other_socket_error(self):
        self.app.account_ring.get_nodes('account')
        for dev in self.app.account_ring.devs.values():
            dev['ip'] = '127.0.0.1'
            dev['port'] = -1 ## invalid port number
        controller = proxy_server.AccountController(self.app, 'account')
        req = Request.blank('/account', environ={'REQUEST_METHOD': 'HEAD'})
        req.account = 'account'
        resp = controller.HEAD(req)
        self.assertEquals(resp.status_int, 503)


if __name__ == '__main__':
    unittest.main()
