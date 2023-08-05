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
import errno
import mimetypes
import os
import socket
import time
from ConfigParser import ConfigParser, NoOptionError
from urllib import unquote, quote
import uuid
import sys
import functools

from eventlet.timeout import Timeout
from webob.exc import HTTPAccepted, HTTPBadRequest, HTTPConflict, \
    HTTPCreated, HTTPLengthRequired, HTTPMethodNotAllowed, HTTPNoContent, \
    HTTPNotFound, HTTPNotModified, HTTPPreconditionFailed, \
    HTTPRequestTimeout, HTTPServiceUnavailable, HTTPUnauthorized, \
    HTTPUnprocessableEntity, HTTPRequestEntityTooLarge, HTTPServerError, \
    status_map
from webob import Request, Response

from swift.common.ring import Ring
from swift.common.utils import get_logger, normalize_timestamp, split_path
from swift.common.bufferedhttp import http_connect
from swift.common.healthcheck import HealthCheckController
from swift.common.constraints import check_object_creation, check_metadata, \
    MAX_FILE_SIZE, check_xml_encodable
from swift.common.exceptions import ChunkReadTimeout, \
    ChunkWriteTimeout, ConnectionTimeout

MAX_CONTAINER_NAME_LENGTH = 256


def update_headers(response, headers):
    """
    Helper function to update headers in the response.

    :param response: webob.Response object
    :param headers: dictionary headers
    """
    if hasattr(headers, 'items'):
        headers = headers.items()
    for name, value in headers:
        if name == 'etag':
            response.headers[name] = value.replace('"', '')
        elif name not in ('date', 'content-length', 'content-type',
                          'connection', 'x-timestamp', 'x-put-timestamp'):
            response.headers[name] = value


def public(func):
    """
    Decorator to declare which methods are public accessible as HTTP requests

    :param func: function to make public
    """
    func.publicly_accessible = True

    @functools.wraps(func)
    def wrapped(*a, **kw):
        return func(*a, **kw)
    return wrapped


class Controller(object):
    """Base WSGI controller class for the proxy"""

    def __init__(self, app):
        self.account_name = None
        self.app = app
        self.trans_id = '-'

    def error_increment(self, node):
        """
        Handles incrementing error counts when talking to nodes.

        :param node: dictionary of node to increment the error count for
        """
        node['errors'] = node.get('errors', 0) + 1
        node['last_error'] = time.time()

    def error_occurred(self, node, msg):
        """
        Handle logging, and handling of errors.

        :param node: dictionary of node to handle errors for
        :param msg: error message
        """
        self.error_increment(node)
        self.app.logger.error(
            '%s %s:%s' % (msg, node['ip'], node['port']))

    def exception_occurred(self, node, typ, additional_info):
        """
        Handle logging of generic exceptions.

        :param node: dictionary of node to log the error for
        :param typ: server type
        :param additional_info: additional information to log
        """
        self.app.logger.exception(
            'ERROR with %s server %s:%s/%s transaction %s re: %s' % (typ,
            node['ip'], node['port'], node['device'], self.trans_id,
            additional_info))

    def error_limited(self, node):
        """
        Check if the node is currently error limited.

        :param node: dictionary of node to check
        :returns: True if error limited, False otherwise
        """
        now = time.time()
        if not 'errors' in node:
            return False
        if 'last_error' in node and node['last_error'] < \
                now - self.app.error_suppression_interval:
            del node['last_error']
            if 'errors' in node:
                del node['errors']
            return False
        limited = node['errors'] > self.app.error_suppression_limit
        if limited:
            self.app.logger.debug(
                'Node error limited %s:%s (%s)' % (
                    node['ip'], node['port'], node['device']))
        return limited

    def error_limit(self, node):
        """
        Mark a node as error limited.

        :param node: dictionary of node to error limit
        """
        node['errors'] = self.app.error_suppression_limit + 1
        node['last_error'] = time.time()

    def account_info(self, account):
        """
        Get account information, and also verify that the account exists.

        :param account: name of the account to get the info for
        :returns: tuple of (account partition, account nodes) or (None, None)
                  if it does not exist
        """
        partition, nodes = self.app.account_ring.get_nodes(account)
        path = '/%s' % account
        cache_key = 'account%s' % path
        # 0 = no responses, 200 = found, 404 = not found, -1 = mixed responses
        if self.app.memcache.get(cache_key):
            return partition, nodes
        result_code = 0
        attempts_left = self.app.account_ring.replica_count
        headers = {'x-cf-trans-id': self.trans_id}
        for node in self.iter_nodes(partition, nodes, self.app.account_ring):
            if self.error_limited(node):
                continue
            try:
                with ConnectionTimeout(self.app.conn_timeout):
                    conn = http_connect(node['ip'], node['port'],
                            node['device'], partition, 'HEAD', path, headers)
                with Timeout(self.app.node_timeout):
                    resp = conn.getresponse()
                    body = resp.read()
                    if 200 <= resp.status <= 299:
                        result_code = 200
                        break
                    elif resp.status == 404:
                        result_code = 404 if not result_code else -1
                    elif resp.status == 507:
                        self.error_limit(node)
                        continue
                    else:
                        result_code = -1
                        attempts_left -= 1
                        if attempts_left <= 0:
                            break
            except:
                self.exception_occurred(node, 'Account',
                    'Trying to get account info for %s' % path)
        if result_code == 200:
            cache_timeout = self.app.recheck_account_existence
        else:
            cache_timeout = self.app.recheck_account_existence * 0.1
        self.app.memcache.set(cache_key, result_code, timeout=cache_timeout)
        if result_code == 200:
            return partition, nodes
        return (None, None)

    def container_info(self, account, container):
        """
        Get container information and thusly verify container existance.
        This will also make a call to account_info to verify that the
        account exists.

        :param account: account name for the container
        :param container: container name to look up
        :returns: tuple of (container partition, container nodes) or
                           (None, None) if the container does not exist
        """
        partition, nodes = self.app.container_ring.get_nodes(
                account, container)
        path = '/%s/%s' % (account, container)
        cache_key = 'container%s' % path
        # 0 = no responses, 200 = found, 404 = not found, -1 = mixed responses
        if self.app.memcache.get(cache_key) == 200:
            return partition, nodes
        if not self.account_info(account)[1]:
            return (None, None)
        result_code = 0
        attempts_left = self.app.container_ring.replica_count
        headers = {'x-cf-trans-id': self.trans_id}
        for node in self.iter_nodes(partition, nodes, self.app.container_ring):
            if self.error_limited(node):
                continue
            try:
                with ConnectionTimeout(self.app.conn_timeout):
                    conn = http_connect(node['ip'], node['port'],
                            node['device'], partition, 'HEAD', path, headers)
                with Timeout(self.app.node_timeout):
                    resp = conn.getresponse()
                    body = resp.read()
                    if 200 <= resp.status <= 299:
                        result_code = 200
                        break
                    elif resp.status == 404:
                        result_code = 404 if not result_code else -1
                    elif resp.status == 507:
                        self.error_limit(node)
                        continue
                    else:
                        result_code = -1
                        attempts_left -= 1
                        if attempts_left <= 0:
                            break
            except:
                self.exception_occurred(node, 'Container',
                    'Trying to get container info for %s' % path)
        if result_code == 200:
            cache_timeout = self.app.recheck_container_existence
        else:
            cache_timeout = self.app.recheck_container_existence * 0.1
        self.app.memcache.set(cache_key, result_code, timeout=cache_timeout)
        if result_code == 200:
            return partition, nodes
        return (None, None)

    def iter_nodes(self, partition, nodes, ring):
        """
        Node iterator that will first iterate over the normal nodes for a
        partition and then the handoff partitions for the node.

        :param partition: partition to iterate nodes for
        :param nodes: list of node dicts from the ring
        :param ring: ring to get handoff nodes from
        """
        for node in nodes:
            yield node
        for node in ring.get_more_nodes(partition):
            yield node

    def get_update_nodes(self, partition, nodes, ring):
        """ Returns ring.replica_count nodes; the nodes will not be error
            limited, if possible. """
        """
        Attempt to get a non error limited list of nodes.

        :param partition: partition for the nodes
        :param nodes: list of node dicts for the partition
        :param ring: ring to get handoff nodes from
        :returns: list of node dicts that are not error limited (if possible)
        """

        # make a copy so we don't modify caller's list
        nodes = list(nodes)
        update_nodes = []
        for node in self.iter_nodes(partition, nodes, ring):
            if self.error_limited(node):
                continue
            update_nodes.append(node)
            if len(update_nodes) >= ring.replica_count:
                break
        while len(update_nodes) < ring.replica_count:
            node = nodes.pop()
            if node not in update_nodes:
                update_nodes.append(node)
        return update_nodes

    def best_response(self, req, statuses, reasons, bodies, server_type,
                      etag=None):
        """
        Given a list of responses from several servers, choose the best to
        return to the API.

        :param req: webob.Request object
        :param statuses: list of statuses returned
        :param reasons: list of reasons for each status
        :param bodies: bodies of each response
        :param server_type: type of server the responses came from
        :param etag: etag
        :returns: webob.Response object with the correct status, body, etc. set
        """
        resp = Response(request=req)
        if len(statuses):
            for hundred in (200, 300, 400):
                hstatuses = \
                    [s for s in statuses if hundred <= s < hundred + 100]
                if len(hstatuses) > len(statuses) / 2:
                    status = max(hstatuses)
                    status_index = statuses.index(status)
                    resp.status = '%s %s' % (status, reasons[status_index])
                    resp.body = bodies[status_index]
                    resp.content_type = 'text/plain'
                    if etag:
                        resp.headers['etag'] = etag.strip('"')
                    return resp
        self.app.logger.error('%s returning 503 for %s, transaction %s' %
                              (server_type, statuses, self.trans_id))
        resp.status = '503 Internal Server Error'
        return resp

    @public
    def GET(self, req):
        """Handler for HTTP GET requests."""
        return self.GETorHEAD(req)

    @public
    def HEAD(self, req):
        """Handler for HTTP HEAD requests."""
        return self.GETorHEAD(req)

    def GETorHEAD_base(self, req, server_type, partition, nodes, path,
                       attempts):
        """
        Base handler for HTTP GET or HEAD requests.

        :param req: webob.Request object
        :param server_type: server type
        :param partition: partition
        :param nodes: nodes
        :param path: path for the request
        :param attempts: number of attempts to try
        :returns: webob.Response object
        """
        statuses = []
        reasons = []
        bodies = []
        for node in nodes:
            if len(statuses) >= attempts:
                break
            if self.error_limited(node):
                continue
            try:
                with ConnectionTimeout(self.app.conn_timeout):
                    conn = http_connect(node['ip'], node['port'],
                        node['device'], partition, req.method, path,
                        headers=req.headers,
                        query_string=req.query_string)
                with Timeout(self.app.node_timeout):
                    source = conn.getresponse()
            except:
                self.exception_occurred(node, server_type,
                    'Trying to %s %s' % (req.method, req.path))
                continue
            if source.status == 507:
                self.error_limit(node)
                continue
            if 200 <= source.status <= 399:
                # 404 if we know we don't have a synced copy
                if not float(source.getheader('X-PUT-Timestamp', '1')):
                    statuses.append(404)
                    reasons.append('')
                    bodies.append('')
                    source.read()
                    continue
            if req.method == 'GET' and source.status in (200, 206):

                def file_iter():
                    try:
                        while True:
                            with ChunkReadTimeout(self.app.node_timeout):
                                chunk = source.read(self.app.object_chunk_size)
                            if not chunk:
                                break
                            yield chunk
                            req.sent_size += len(chunk)
                    except GeneratorExit:
                        req.client_disconnect = True
                        self.app.logger.info(
                            'Client disconnected on read transaction %s' %
                            self.trans_id)
                    except:
                        self.exception_occurred(node, 'Object',
                            'Trying to read during GET of %s' % req.path)
                        raise

                res = Response(app_iter=file_iter(), request=req,
                               conditional_response=True)
                update_headers(res, source.getheaders())
                res.status = source.status
                res.content_length = source.getheader('Content-Length')
                if source.getheader('Content-Type'):
                    res.charset = None
                    res.content_type = source.getheader('Content-Type')
                return res
            elif 200 <= source.status <= 399:
                res = status_map[source.status](request=req)
                update_headers(res, source.getheaders())
                if req.method == 'HEAD':
                    res.content_length = source.getheader('Content-Length')
                    if source.getheader('Content-Type'):
                        res.charset = None
                        res.content_type = source.getheader('Content-Type')
                return res
            statuses.append(source.status)
            reasons.append(source.reason)
            bodies.append(source.read())
            if source.status >= 500:
                self.error_occurred(node, 'ERROR %d %s From %s Server' %
                    (source.status, bodies[-1][:1024], server_type))
        return self.best_response(req, statuses, reasons, bodies,
                                  '%s %s' % (server_type, req.method))


class ObjectController(Controller):
    """WSGI controller for object requests."""

    def __init__(self, app, account_name, container_name, object_name,
                 **kwargs):
        Controller.__init__(self, app)
        self.account_name = unquote(account_name)
        self.container_name = unquote(container_name)
        self.object_name = unquote(object_name)

    def node_post_or_delete(self, req, partition, node, path):
        """
        Handle common POST/DELETE functionality

        :param req: webob.Request object
        :param partition: partition for the object
        :param node: node dictionary for the object
        :param path: path to send for the request
        """
        if self.error_limited(node):
            return 500, '', ''
        try:
            with ConnectionTimeout(self.app.conn_timeout):
                conn = http_connect(node['ip'], node['port'], node['device'],
                        partition, req.method, path, req.headers)
            with Timeout(self.app.node_timeout):
                response = conn.getresponse()
                body = response.read()
                if response.status == 507:
                    self.error_limit(node)
                elif response.status >= 500:
                    self.error_occurred(node,
                        'ERROR %d %s From Object Server' %
                        (response.status, body[:1024]))
                return response.status, response.reason, body
        except:
            self.exception_occurred(node, 'Object',
                'Trying to %s %s' % (req.method, req.path))
        return 500, '', ''

    def GETorHEAD(self, req):
        """Handle HTTP GET or HEAD requests."""
        partition, nodes = self.app.object_ring.get_nodes(
            self.account_name, self.container_name, self.object_name)
        return self.GETorHEAD_base(req, 'Object', partition,
                self.iter_nodes(partition, nodes, self.app.object_ring),
                req.path_info, self.app.object_ring.replica_count)

    @public
    def POST(self, req):
        """HTTP POST request handler."""
        error_response = check_metadata(req)
        if error_response:
            return error_response
        container_partition, containers = \
            self.container_info(self.account_name, self.container_name)
        if not containers:
            return HTTPNotFound(request=req)
        containers = self.get_update_nodes(container_partition, containers,
                                           self.app.container_ring)
        partition, nodes = self.app.object_ring.get_nodes(
            self.account_name, self.container_name, self.object_name)
        req.headers['X-Timestamp'] = normalize_timestamp(time.time())
        statuses = []
        reasons = []
        bodies = []
        for node in self.iter_nodes(partition, nodes, self.app.object_ring):
            container = containers.pop()
            req.headers['X-Container-Host'] = '%(ip)s:%(port)s' % container
            req.headers['X-Container-Partition'] = container_partition
            req.headers['X-Container-Device'] = container['device']
            status, reason, body = \
                self.node_post_or_delete(req, partition, node, req.path_info)
            if 200 <= status < 300 or 400 <= status < 500:
                statuses.append(status)
                reasons.append(reason)
                bodies.append(body)
            else:
                containers.insert(0, container)
            if not containers:
                break
        while len(statuses) < len(nodes):
            statuses.append(503)
            reasons.append('')
            bodies.append('')
        return self.best_response(req, statuses, reasons,
                bodies, 'Object POST')

    @public
    def PUT(self, req):
        """HTTP PUT request handler."""
        container_partition, containers = \
            self.container_info(self.account_name, self.container_name)
        if not containers:
            return HTTPNotFound(request=req)
        containers = self.get_update_nodes(container_partition, containers,
                                           self.app.container_ring)
        partition, nodes = self.app.object_ring.get_nodes(
            self.account_name, self.container_name, self.object_name)
        req.headers['X-Timestamp'] = normalize_timestamp(time.time())
        # this is a temporary hook for migrations to set PUT timestamps
        if '!Migration-Timestamp!' in req.headers:
            req.headers['X-Timestamp'] = \
                    normalize_timestamp(req.headers['!Migration-Timestamp!'])
        # Sometimes the 'content-type' header exists, but is set to None.
        if not req.headers.get('content-type'):
            guessed_type, _ = mimetypes.guess_type(req.path_info)
            if not guessed_type:
                req.headers['Content-Type'] = 'application/octet-stream'
            else:
                req.headers['Content-Type'] = guessed_type
        error_response = check_object_creation(req, self.object_name)
        if error_response:
            return error_response
        conns = []
        data_source = \
            iter(lambda: req.body_file.read(self.app.client_chunk_size), '')
        source_header = req.headers.get('X-Copy-From')
        if source_header:
            source_header = unquote(source_header)
            acct = req.path_info.split('/', 2)[1]
            if not source_header.startswith('/'):
                source_header = '/' + source_header
            source_header = '/' + acct + source_header
            try:
                src_container_name, src_obj_name = \
                    source_header.split('/',3)[2:]
            except ValueError:
                return HTTPPreconditionFailed(request=req,
                    body='X-Copy-From header must be of the form'
                    'container/object')
            source_req = Request.blank(source_header)
            orig_obj_name = self.object_name
            orig_container_name = self.container_name
            self.object_name = src_obj_name
            self.container_name = src_container_name
            source_resp = self.GET(source_req)
            if source_resp.status_int >= 300:
                return source_resp
            self.object_name = orig_obj_name
            self.container_name = orig_container_name
            data_source = source_resp.app_iter
            new_req = Request.blank(req.path_info,
                        environ=req.environ, headers=req.headers)
            new_req.content_length = source_resp.content_length
            new_req.etag = source_resp.etag
            new_req.headers['X-Copy-From'] = source_header.split('/', 2)[2]
            for k, v in source_resp.headers.items():
                if k.lower().startswith('x-object-meta-'):
                    new_req.headers[k] = v
            for k, v in req.headers.items():
                if k.lower().startswith('x-object-meta-'):
                    new_req.headers[k] = v
            req = new_req
        for node in self.iter_nodes(partition, nodes, self.app.object_ring):
            container = containers.pop()
            req.headers['X-Container-Host'] = '%(ip)s:%(port)s' % container
            req.headers['X-Container-Partition'] = container_partition
            req.headers['X-Container-Device'] = container['device']
            req.headers['Expect'] = '100-continue'
            resp = conn = None
            if not self.error_limited(node):
                try:
                    with ConnectionTimeout(self.app.conn_timeout):
                        conn = http_connect(node['ip'], node['port'],
                                node['device'], partition, 'PUT',
                                req.path_info, req.headers)
                        conn.node = node
                    with Timeout(self.app.node_timeout):
                        resp = conn.getexpect()
                except:
                    self.exception_occurred(node, 'Object',
                        'Expect: 100-continue on %s' % req.path)
            if conn and resp:
                if resp.status == 100:
                    conns.append(conn)
                    if not containers:
                        break
                    continue
                elif resp.status == 507:
                    self.error_limit(node)
            containers.insert(0, container)
        if len(conns) <= len(nodes) / 2:
            self.app.logger.error(
                'Object PUT returning 503, %s/%s required connections, '
                'transaction %s' %
                (len(conns), len(nodes) / 2 + 1, self.trans_id))
            return HTTPServiceUnavailable(request=req)
        try:
            req.creation_size = 0
            while True:
                with ChunkReadTimeout(self.app.client_timeout):
                    try:
                        chunk = data_source.next()
                    except StopIteration:
                        if req.headers.get('transfer-encoding'):
                            chunk = ''
                        else:
                            break
                len_chunk = len(chunk)
                req.creation_size += len_chunk
                if req.creation_size > MAX_FILE_SIZE:
                    req.creation_size = 0
                    return HTTPRequestEntityTooLarge(request=req)
                for conn in conns:
                    try:
                        with ChunkWriteTimeout(self.app.node_timeout):
                            if req.headers.get('transfer-encoding'):
                                conn.send('%x\r\n%s\r\n' % (len_chunk, chunk))
                            else:
                                conn.send(chunk)
                    except:
                        self.exception_occurred(conn.node, 'Object',
                            'Trying to write to %s' % req.path)
                        conns.remove(conn)
                if req.headers.get('transfer-encoding') and chunk == '':
                    break
        except ChunkReadTimeout, err:
            self.app.logger.info(
                'ERROR Client read timeout (%ss)' % err.seconds)
            return HTTPRequestTimeout(request=req)
        except:
            self.app.logger.exception(
                'ERROR Exception causing client disconnect')
            return Response(status='499 Client Disconnect')
        if req.content_length and req.creation_size < req.content_length:
            self.app.logger.info(
                'Client disconnected without sending enough data %s' %
                self.trans_id)
            return Response(status='499 Client Disconnect')
        statuses = []
        reasons = []
        bodies = []
        etags = set()
        for conn in conns:
            try:
                with Timeout(self.app.node_timeout):
                    response = conn.getresponse()
                    statuses.append(response.status)
                    reasons.append(response.reason)
                    bodies.append(response.read())
                    if response.status >= 500:
                        self.error_occurred(conn.node,
                            'ERROR %d %s From Object Server re: %s' %
                            (response.status, bodies[-1][:1024], req.path))
                    elif 200 <= response.status < 300:
                        etags.add(response.getheader('etag').strip('"'))
            except:
                self.exception_occurred(conn.node, 'Object',
                    'Trying to get final status of PUT to %s' % req.path)
        if len(etags) > 1:
            return HTTPUnprocessableEntity(request=req)
        etag = len(etags) and etags.pop() or None
        while len(statuses) < len(nodes):
            statuses.append(503)
            reasons.append('')
            bodies.append('')
        resp = self.best_response(req, statuses, reasons, bodies, 'Object PUT',
                                  etag=etag)
        if 'x-copy-from' in req.headers:
            resp.headers['X-Copied-From'] = req.headers['x-copy-from']
            for k, v in req.headers.items():
                if k.lower().startswith('x-object-meta-'):
                    resp.headers[k] = v
        resp.last_modified = float(req.headers['X-Timestamp'])
        return resp

    @public
    def DELETE(self, req):
        """HTTP DELETE request handler."""
        container_partition, containers = \
            self.container_info(self.account_name, self.container_name)
        if not containers:
            return HTTPNotFound(request=req)
        containers = self.get_update_nodes(container_partition, containers,
                                           self.app.container_ring)
        partition, nodes = self.app.object_ring.get_nodes(
            self.account_name, self.container_name, self.object_name)
        req.headers['X-Timestamp'] = normalize_timestamp(time.time())
        statuses = []
        reasons = []
        bodies = []
        for node in self.iter_nodes(partition, nodes, self.app.object_ring):
            container = containers.pop()
            req.headers['X-Container-Host'] = '%(ip)s:%(port)s' % container
            req.headers['X-Container-Partition'] = container_partition
            req.headers['X-Container-Device'] = container['device']
            status, reason, body = \
                self.node_post_or_delete(req, partition, node, req.path_info)
            if 200 <= status < 300 or 400 <= status < 500:
                statuses.append(status)
                reasons.append(reason)
                bodies.append(body)
            else:
                containers.insert(0, container)
            if not containers:
                break
        while len(statuses) < len(nodes):
            statuses.append(503)
            reasons.append('')
            bodies.append('')
        return self.best_response(req, statuses, reasons, bodies,
                                  'Object DELETE')

    @public
    def COPY(self, req):
        """HTTP COPY request handler."""
        dest = req.headers.get('Destination')
        if not dest:
            return HTTPPreconditionFailed(request=req,
                                          body='Destination header required')
        dest = unquote(dest)
        if not dest.startswith('/'):
            dest = '/' + dest
        try:
            _, dest_container, dest_object = dest.split('/', 3)
        except ValueError:
            return HTTPPreconditionFailed(request=req,
                    body='Destination header must be of the form container/object')
        new_source = '/' + self.container_name + '/' + self.object_name
        self.container_name = dest_container
        self.object_name = dest_object
        new_headers = {}
        for k, v in req.headers.items():
            new_headers[k] = v
        new_headers['X-Copy-From'] = new_source
        new_headers['Content-Length'] = 0
        del new_headers['Destination']
        new_path = '/' + self.account_name + dest
        new_req = Request.blank(new_path,
                        environ={'REQUEST_METHOD': 'PUT'}, headers=new_headers)
        return self.PUT(new_req)


class ContainerController(Controller):
    """WSGI controller for container requests"""

    def __init__(self, app, account_name, container_name, **kwargs):
        Controller.__init__(self, app)
        self.account_name = unquote(account_name)
        self.container_name = unquote(container_name)

    def GETorHEAD(self, req):
        """Handler for HTTP GET/HEAD requests."""
        if not self.account_info(self.account_name)[1]:
            return HTTPNotFound(request=req)
        part, nodes = self.app.container_ring.get_nodes(
                        self.account_name, self.container_name)
        resp = self.GETorHEAD_base(req, 'Container', part, nodes,
                req.path_info, self.app.container_ring.replica_count)
        return resp

    @public
    def PUT(self, req):
        """HTTP PUT request handler."""
        if len(self.container_name) > MAX_CONTAINER_NAME_LENGTH:
            resp = HTTPBadRequest(request=req)
            resp.body = 'Container name length of %d longer than %d' % \
                        (len(self.container_name), MAX_CONTAINER_NAME_LENGTH)
            return resp
        account_partition, accounts = self.account_info(self.account_name)
        if not accounts:
            return HTTPNotFound(request=req)
        accounts = self.get_update_nodes(account_partition, accounts,
                                         self.app.account_ring)
        container_partition, containers = self.app.container_ring.get_nodes(
            self.account_name, self.container_name)
        headers = {'X-Timestamp': normalize_timestamp(time.time()),
                   'x-cf-trans-id': self.trans_id}
        statuses = []
        reasons = []
        bodies = []
        for node in self.iter_nodes(container_partition, containers,
                                    self.app.container_ring):
            if self.error_limited(node):
                continue
            try:
                account = accounts.pop()
                headers['X-Account-Host'] = '%(ip)s:%(port)s' % account
                headers['X-Account-Partition'] = account_partition
                headers['X-Account-Device'] = account['device']
                with ConnectionTimeout(self.app.conn_timeout):
                    conn = http_connect(node['ip'], node['port'],
                            node['device'], container_partition, 'PUT',
                            req.path_info, headers)
                with Timeout(self.app.node_timeout):
                    source = conn.getresponse()
                    body = source.read()
                    if 200 <= source.status < 300 \
                            or 400 <= source.status < 500:
                        statuses.append(source.status)
                        reasons.append(source.reason)
                        bodies.append(body)
                    else:
                        if source.status == 507:
                            self.error_limit(node)
                        accounts.insert(0, account)
            except:
                accounts.insert(0, account)
                self.exception_occurred(node, 'Container',
                    'Trying to PUT to %s' % req.path)
            if not accounts:
                break
        while len(statuses) < len(containers):
            statuses.append(503)
            reasons.append('')
            bodies.append('')
        self.app.memcache.delete('container%s' % req.path_info.rstrip('/'))
        return self.best_response(req, statuses, reasons, bodies,
                                  'Container PUT')

    @public
    def DELETE(self, req):
        """HTTP DELETE request handler."""
        account_partition, accounts = self.account_info(self.account_name)
        if not accounts:
            return HTTPNotFound(request=req)
        accounts = self.get_update_nodes(account_partition, accounts,
                                         self.app.account_ring)
        container_partition, containers = self.app.container_ring.get_nodes(
            self.account_name, self.container_name)
        headers = {'X-Timestamp': normalize_timestamp(time.time()),
             'x-cf-trans-id': self.trans_id}
        statuses = []
        reasons = []
        bodies = []
        for node in self.iter_nodes(container_partition, containers,
                                    self.app.container_ring):
            if self.error_limited(node):
                continue
            try:
                account = accounts.pop()
                headers['X-Account-Host'] = '%(ip)s:%(port)s' % account
                headers['X-Account-Partition'] = account_partition
                headers['X-Account-Device'] = account['device']
                with ConnectionTimeout(self.app.conn_timeout):
                    conn = http_connect(node['ip'], node['port'],
                            node['device'], container_partition, 'DELETE',
                            req.path_info, headers)
                with Timeout(self.app.node_timeout):
                    source = conn.getresponse()
                    body = source.read()
                    if 200 <= source.status < 300 \
                            or 400 <= source.status < 500:
                        statuses.append(source.status)
                        reasons.append(source.reason)
                        bodies.append(body)
                    else:
                        if source.status == 507:
                            self.error_limit(node)
                        accounts.insert(0, account)
            except:
                accounts.insert(0, account)
                self.exception_occurred(node, 'Container',
                    'Trying to DELETE %s' % req.path)
            if not accounts:
                break
        while len(statuses) < len(containers):
            statuses.append(503)
            reasons.append('')
            bodies.append('')
        self.app.memcache.delete('container%s' % req.path_info.rstrip('/'))
        resp = self.best_response(req, statuses, reasons, bodies,
                                  'Container DELETE')
        if 200 <= resp.status_int <= 299:
            for status in statuses:
                if status < 200 or status > 299:
                    # If even one node doesn't do the delete, we can't be sure
                    # what the outcome will be once everything is in sync; so
                    # we 503.
                    self.app.logger.error('Returning 503 because not all '
                        'container nodes confirmed DELETE, transaction %s' %
                        self.trans_id)
                    return HTTPServiceUnavailable(request=req)
        if resp.status_int == 202:  # Indicates no server had the container
            return HTTPNotFound(request=req)
        return resp


class AccountController(Controller):
    """WSGI controller for account requests"""

    def __init__(self, app, account_name, **kwargs):
        Controller.__init__(self, app)
        self.account_name = unquote(account_name)

    def GETorHEAD(self, req):
        """Handler for HTTP GET/HEAD requests."""
        partition, nodes = self.app.account_ring.get_nodes(self.account_name)
        return self.GETorHEAD_base(req, 'Account', partition, nodes,
                req.path_info.rstrip('/'), self.app.account_ring.replica_count)


class BaseApplication(object):
    """Base WSGI application for the proxy server"""

    log_name = 'base_application'

    def __init__(self, conf, memcache, logger=None, account_ring=None,
                 container_ring=None, object_ring=None):
        if logger:
            self.logger = logger
        else:
            self.logger = get_logger(conf, self.log_name)
        if conf is None:
            conf = {}
        swift_dir = conf.get('swift_dir', '/etc/swift')
        self.node_timeout = int(conf.get('node_timeout', 10))
        self.conn_timeout = float(conf.get('conn_timeout', 0.5))
        self.client_timeout = int(conf.get('client_timeout', 60))
        self.object_chunk_size = int(conf.get('object_chunk_size', 65536))
        self.container_chunk_size = \
            int(conf.get('container_chunk_size', 65536))
        self.account_chunk_size = int(conf.get('account_chunk_size', 65536))
        self.client_chunk_size = int(conf.get('client_chunk_size', 65536))
        self.log_headers = conf.get('log_headers') == 'True'
        self.error_suppression_interval = \
            int(conf.get('error_suppression_interval', 60))
        self.error_suppression_limit = \
            int(conf.get('error_suppression_limit', 10))
        self.recheck_container_existence = \
            int(conf.get('recheck_container_existence', 60))
        self.recheck_account_existence = \
            int(conf.get('recheck_account_existence', 60))
        self.resellers_conf = ConfigParser()
        self.resellers_conf.read(os.path.join(swift_dir, 'resellers.conf'))
        self.object_ring = object_ring or \
            Ring(os.path.join(swift_dir, 'object.ring.gz'))
        self.container_ring = container_ring or \
            Ring(os.path.join(swift_dir, 'container.ring.gz'))
        self.account_ring = account_ring or \
            Ring(os.path.join(swift_dir, 'account.ring.gz'))
        self.memcache = memcache
        self.rate_limit = float(conf.get('rate_limit', 20000.0))
        self.account_rate_limit = float(conf.get('account_rate_limit', 200.0))
        self.rate_limit_whitelist = [x.strip() for x in
            conf.get('rate_limit_account_whitelist', '').split(',')
            if x.strip()]
        self.rate_limit_blacklist = [x.strip() for x in
            conf.get('rate_limit_account_blacklist', '').split(',')
            if x.strip()]
        self.container_put_lock_timeout = \
            int(conf.get('container_put_lock_timeout', 5))

    def get_controller(self, path):
        """
        Get the controller to handle a request.

        :param path: path from request
        :returns: tuple of (controller class, path dictionary)
        """
        version, account, container, obj = split_path(path, 1, 4, True)
        d = dict(version=version,
                account_name=account,
                container_name=container,
                object_name=obj)
        if obj and container and account:
            return ObjectController, d
        elif container and account:
            return ContainerController, d
        elif account and not container and not obj:
            return AccountController, d
        elif version and version == 'healthcheck':
            return HealthCheckController, d
        return None, d

    def __call__(self, env, start_response):
        """
        WSGI entry point.
        Wraps env in webob.Request object and passes it down.

        :param env: WSGI environment dictionary
        :param start_response: WSGI callable
        """
        try:
            req = self.update_request(Request(env))
            if 'eventlet.posthooks' in env:
                env['eventlet.posthooks'].append(
                    (self.posthooklogger, (req,), {}))
                return self.handle_request(req)(env, start_response)
            else:
                # Lack of posthook support means that we have to log on the
                # start of the response, rather than after all the data has
                # been sent. This prevents logging client disconnects
                # differently than full transmissions.
                response = self.handle_request(req)(env, start_response)
                self.posthooklogger(env, req)
                return response
        except:
            print "EXCEPTION IN __call__: %s" % env
            start_response('500 Server Error',
                    [('Content-Type', 'text/plain')])
            return ['Internal server error.\n']

    def posthooklogger(self, env, req):
        pass

    def update_request(self, req):
        req.creation_size = '-'
        req.sent_size = 0
        req.client_disconnect = False
        req.headers['x-cf-trans-id'] = 'tx' + str(uuid.uuid4())
        if 'x-storage-token' in req.headers and \
                'x-auth-token' not in req.headers:
            req.headers['x-auth-token'] = req.headers['x-storage-token']
        return req

    def handle_request(self, req):
        """
        Entry point for proxy server.
        Should return a WSGI-style callable (such as webob.Response).

        :param req: webob.Request object
        """
        try:
            try:
                controller, path_parts = self.get_controller(req.path)
            except ValueError:
                return HTTPNotFound(request=req)
            if controller == HealthCheckController:
                controller = controller(self, **path_parts)
                controller.trans_id = req.headers.get('x-cf-trans-id', '-')
                if req.method == 'GET':
                    return controller.GET(req)
                return HTTPMethodNotAllowed(request=req)

            if not check_xml_encodable(req.path_info):
                return HTTPPreconditionFailed(request=req, body='Invalid UTF8')
            if not controller:
                return HTTPPreconditionFailed(request=req, body='Bad URL')
            rate_limit_allowed_err_resp = \
                self.check_rate_limit(req, path_parts)
            if rate_limit_allowed_err_resp is not None:
                return rate_limit_allowed_err_resp

            controller = controller(self, **path_parts)
            controller.trans_id = req.headers.get('x-cf-trans-id', '-')
            try:
                handler = getattr(controller, req.method)
                if getattr(handler, 'publicly_accessible'):
                    if path_parts['version']:
                        req.path_info_pop()
                    return handler(req)
            except AttributeError:
                return HTTPMethodNotAllowed(request=req)
        except Exception:
            self.logger.exception('ERROR Unhandled exception in request')
            return HTTPServerError(request=req)

    def check_rate_limit(self, req, path_parts):
        """Check for rate limiting."""
        return None


class Application(BaseApplication):
    """WSGI application for the proxy server."""

    log_name = 'proxy'

    def handle_request(self, req):
        """
        Wraps the BaseApplication.handle_request and logs the request.
        """
        req.start_time = time.time()
        req.response = super(Application, self).handle_request(req)
        return req.response

    def posthooklogger(self, env, req):
        response = req.response
        trans_time = '%.4f' % (time.time() - req.start_time)
        if not response.content_length and response.app_iter and \
                    hasattr(response.app_iter, '__len__'):
            response.content_length = sum(map(len, response.app_iter))
        the_request = quote(unquote(req.path))
        if req.query_string:
            the_request = the_request + '?' + req.query_string
        # remote user for zeus
        client = req.headers.get('x-cluster-client-ip')
        if not client and 'x-forwarded-for' in req.headers:
            # remote user for other lbs
            client = req.headers['x-forwarded-for'].split(',')[0].strip()
        raw_in = req.content_length or 0
        if req.creation_size != '-':
            raw_in = req.creation_size
        raw_out = 0
        if req.method != 'HEAD':
            if response.content_length:
                raw_out = response.content_length
            if req.sent_size or req.client_disconnect:
                raw_out = req.sent_size
        logged_headers = None
        if self.log_headers:
            logged_headers = '\n'.join('%s: %s' % (k, v)
                for k, v in req.headers.items())
        status_int = req.client_disconnect and 499 or response.status_int
        self.logger.info(' '.join(quote(str(x)) for x in (
                client or '-',
                req.remote_addr or '-',
                time.strftime('%d/%b/%Y/%H/%M/%S', time.gmtime()),
                req.method,
                the_request,
                req.environ['SERVER_PROTOCOL'],
                status_int,
                req.referer or '-',
                req.user_agent or '-',
                req.headers.get('x-auth-token', '-'),
                raw_in or '-',
                raw_out or '-',
                req.headers.get('etag', '-'),
                req.headers.get('x-cf-trans-id', '-'),
                logged_headers or '-',
                trans_time,
            )))

    def check_rate_limit(self, req, path_parts):
        """
        Check for rate limiting.

        :param req: webob.Request object
        :param path_parts: parsed path dictionary
        """
        if path_parts['account_name'] in self.rate_limit_blacklist:
            self.logger.error('Returning 497 because of blacklisting')
            return Response(status='497 Blacklisted',
                body='Your account has been blacklisted', request=req)
        if path_parts['account_name'] not in self.rate_limit_whitelist:
            current_second = time.strftime('%x%H%M%S')
            general_rate_limit_key = '%s%s' % (path_parts['account_name'],
                                    current_second)
            ops_count = self.memcache.incr(general_rate_limit_key, timeout=2)
            if ops_count > self.rate_limit:
                self.logger.error(
                    'Returning 498 because of ops rate limiting')
                return Response(status='498 Rate Limited',
                        body='Slow down', request=req)
            elif (path_parts['container_name']
                    and not path_parts['object_name']) \
                or \
                    (path_parts['account_name']
                    and not path_parts['container_name']):
                # further limit operations on a single account or container
                rate_limit_key = '%s%s%s' % (path_parts['account_name'],
                                        path_parts['container_name'] or '-',
                                        current_second)
                ops_count = self.memcache.incr(rate_limit_key, timeout=2)
                if ops_count > self.account_rate_limit:
                    self.logger.error(
                        'Returning 498 because of account and container'
                        ' rate limiting')
                    return Response(status='498 Rate Limited',
                        body='Slow down', request=req)
        return None
