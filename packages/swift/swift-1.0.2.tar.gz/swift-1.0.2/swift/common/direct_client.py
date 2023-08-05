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

"""
Internal client library for making calls directly to the servers rather than
through the proxy.
"""

import socket
from httplib import HTTPException
from time import time
from urllib import quote as _quote, unquote

from eventlet import sleep, Timeout

from swift.common.bufferedhttp import http_connect
from swift.common.client import ClientException, json_loads
from swift.common.utils import normalize_timestamp


def quote(value, safe='/'):
    if isinstance(value, unicode):
        value = value.encode('utf8')
    return _quote(value, safe)


def direct_head_container(node, part, account, container, conn_timeout=5,
                          response_timeout=15):
    """
    Request container information directly from the container server.

    :param node: node dictionary from the ring
    :param part: partition the container is on
    :param account: account name
    :param container: container name
    :param conn_timeout: timeout in seconds for establishing the connection
    :param response_timeout: timeout in seconds for getting the response
    :returns: tuple of (object count, bytes used)
    """
    path = '/%s/%s' % (account, container)
    with Timeout(conn_timeout):
        conn = http_connect(node['ip'], node['port'], node['device'], part,
                            'HEAD', path)
    with Timeout(response_timeout):
        resp = conn.getresponse()
        resp.read()
    if resp.status < 200 or resp.status >= 300:
        raise ClientException(
                'Container server %s:%s direct HEAD %s gave status %s' %
                (node['ip'], node['port'],
                 repr('/%s/%s%s' % (node['device'], part, path)),
                 resp.status),
                http_host=node['ip'], http_port=node['port'],
                http_device=node['device'], http_status=resp.status,
                http_reason=resp.reason)
    return int(resp.getheader('x-container-object-count')), \
           int(resp.getheader('x-container-bytes-used'))


def direct_get_container(node, part, account, container, marker=None,
                         limit=None, prefix=None, delimiter=None,
                         conn_timeout=5, response_timeout=15):
    """
    Get container listings directly from the container server.

    :param node: node dictionary from the ring
    :param part: partition the container is on
    :param account: account name
    :param container: container name
    :param marker: marker query
    :param limit: query limit
    :param prefix: prefix query
    :param delimeter: delimeter for the query
    :param conn_timeout: timeout in seconds for establishing the connection
    :param response_timeout: timeout in seconds for getting the response
    :returns: list of objects
    """
    path = '/%s/%s' % (account, container)
    qs = 'format=json'
    if marker:
        qs += '&marker=%s' % quote(marker)
    if limit:
        qs += '&limit=%d' % limit
    if prefix:
        qs += '&prefix=%s' % quote(prefix)
    if delimiter:
        qs += '&delimiter=%s' % quote(delimiter)
    with Timeout(conn_timeout):
        conn = http_connect(node['ip'], node['port'], node['device'], part,
                            'GET', path, query_string='format=json')
    with Timeout(response_timeout):
        resp = conn.getresponse()
    if resp.status < 200 or resp.status >= 300:
        resp.read()
        raise ClientException(
            'Container server %s:%s direct GET %s gave stats %s' % (node['ip'],
                node['port'], repr('/%s/%s%s' % (node['device'], part, path)),
                resp.status),
            http_host=node['ip'], http_port=node['port'],
            http_device=node['device'], http_status=resp.status,
            http_reason=resp.reason)
    if resp.status == 204:
        resp.read()
        return []
    return json_loads(resp.read())


def direct_delete_container(node, part, account, container, conn_timeout=5,
                            response_timeout=15, headers={}):
    path = '/%s/%s' % (account, container)
    headers['X-Timestamp'] = normalize_timestamp(time())
    with Timeout(conn_timeout):
        conn = http_connect(node['ip'], node['port'], node['device'], part,
                'DELETE', path, headers)
    with Timeout(response_timeout):
        resp = conn.getresponse()
    if resp.status < 200 or resp.status >= 300:
        raise ClientException(
                'Container server %s:%s direct DELETE %s gave status %s' %
                (node['ip'], node['port'],
                repr('/%s/%s%s' % (node['device'], part, path)),
                resp.status),
                http_host=node['ip'], http_port=node['port'],
                http_device=node['device'], http_status=resp.status,
                http_reason=resp.reason)
    return resp


def direct_head_object(node, part, account, container, obj, conn_timeout=5,
                       response_timeout=15):
    """
    Request object information directly from the object server.

    :param node: node dictionary from the ring
    :param part: partition the container is on
    :param account: account name
    :param container: container name
    :param obj: object name
    :param conn_timeout: timeout in seconds for establishing the connection
    :param response_timeout: timeout in seconds for getting the response
    :returns: tuple of (content-type, object size, last modified timestamp,
              etag, metadata dictionary)
    """
    path = '/%s/%s/%s' % (account, container, obj)
    with Timeout(conn_timeout):
        conn = http_connect(node['ip'], node['port'], node['device'], part,
                            'HEAD', path)
    with Timeout(response_timeout):
        resp = conn.getresponse()
        resp.read()
    if resp.status < 200 or resp.status >= 300:
        raise ClientException(
                'Object server %s:%s direct HEAD %s gave status %s' %
                (node['ip'], node['port'],
                 repr('/%s/%s%s' % (node['device'], part, path)),
                 resp.status),
                http_host=node['ip'], http_port=node['port'],
                http_device=node['device'], http_status=resp.status,
                http_reason=resp.reason)
    metadata = {}
    for key, value in resp.getheaders():
        if key.lower().startswith('x-object-meta-'):
            metadata[unquote(key[len('x-object-meta-'):])] = unquote(value)
    return resp.getheader('content-type'), \
           int(resp.getheader('content-length')), \
           resp.getheader('last-modified'), \
           resp.getheader('etag').strip('"'), \
           metadata


def direct_get_object(node, part, account, container, obj, conn_timeout=5,
        response_timeout=15):
    """
    Get object directly from the object server.

    :param node: node dictionary from the ring
    :param part: partition the container is on
    :param account: account name
    :param container: container name
    :param obj: object name
    :param conn_timeout: timeout in seconds for establishing the connection
    :param response_timeout: timeout in seconds for getting the response
    :returns: object
    """
    path = '/%s/%s/%s' % (account, container, obj)
    with Timeout(conn_timeout):
        conn = http_connect(node['ip'], node['port'], node['device'], part,
                'GET', path)
    with Timeout(response_timeout):
        resp = conn.getresponse()
    if resp.status < 200 or resp.status >= 300:
        raise ClientException(
                'Object server %s:%s direct GET %s gave status %s' %
                (node['ip'], node['port'],
                repr('/%s/%s%s' % (node['device'], part, path)),
                resp.status),
                http_host=node['ip'], http_port=node['port'],
                http_device=node['device'], http_status=resp.status,
                http_reason=resp.reason)
    metadata = {}
    for key, value in resp.getheaders():
        if key.lower().startswith('x-object-meta-'):
            metadata[unquote(key[len('x-object-meta-'):])] = unquote(value)
    return (resp.getheader('content-type'),
           int(resp.getheader('content-length')),
           resp.getheader('last-modified'),
           resp.getheader('etag').strip('"'),
           metadata,
           resp.read())


def direct_delete_object(node, part, account, container, obj,
        conn_timeout=5, response_timeout=15, headers={}):
    """
    Delete object directly from the object server.

    :param node: node dictionary from the ring
    :param part: partition the container is on
    :param account: account name
    :param container: container name
    :param obj: object name
    :param conn_timeout: timeout in seconds for establishing the connection
    :param response_timeout: timeout in seconds for getting the response
    :returns: response from server
    """
    path = '/%s/%s/%s' % (account, container, obj)
    headers['X-Timestamp'] = normalize_timestamp(time())
    with Timeout(conn_timeout):
        conn = http_connect(node['ip'], node['port'], node['device'], part,
                'DELETE', path, headers)
    with Timeout(response_timeout):
        resp = conn.getresponse()
    if resp.status < 200 or resp.status >= 300:
        raise ClientException(
                'Object server %s:%s direct DELETE %s gave status %s' %
                (node['ip'], node['port'],
                repr('/%s/%s%s' % (node['device'], part, path)),
                resp.status),
                http_host=node['ip'], http_port=node['port'],
                http_device=node['device'], http_status=resp.status,
                http_reason=resp.reason)
    return resp


def retry(func, *args, **kwargs):
    """
    Helper function to retry a given function a number of times.

    :param func: callable to be called
    :param retries: number of retries
    :param error_log: logger for errors
    :param args: arguments to send to func
    :param kwargs: keyward arguments to send to func (if retries or
                   error_log are sent, they will be deleted from kwargs
                   before sending on to func)
    :returns: restult of func
    """
    retries = 5
    if 'retries' in kwargs:
        retries = kwargs['retries']
        del kwargs['retries']
    error_log = None
    if 'error_log' in kwargs:
        error_log = kwargs['error_log']
        del kwargs['error_log']
    attempts = 0
    backoff = 1
    while attempts <= retries:
        attempts += 1
        try:
            return attempts, func(*args, **kwargs)
        except (socket.error, HTTPException, Timeout), err:
            if error_log:
                error_log(err)
            if attempts > retries:
                raise
        except ClientException, err:
            if error_log:
                error_log(err)
            if attempts > retries or err.http_status < 500 or \
                    err.http_status == 507 or err.http_status > 599:
                raise
        sleep(backoff)
        backoff *= 2
    # Shouldn't actually get down here, but just in case.
    if args and 'ip' in args[0]:
        raise ClientException('Raise too many retries',
            http_host=args[0]['ip'], http_port=args[0]['port'],
            http_device=args[0]['device'])
    else:
        raise ClientException('Raise too many retries')
