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
Cloud Files client library used internally
"""
import socket
from cStringIO import StringIO
from httplib import HTTPConnection, HTTPException, HTTPSConnection
from re import compile, DOTALL
from tokenize import generate_tokens, STRING, NAME, OP
from urllib import quote as _quote, unquote
from urlparse import urlparse, urlunparse

try:
    from eventlet import sleep
except:
    from time import sleep


def quote(value, safe='/'):
    """
    Patched version of urllib.quote that encodes utf8 strings before quoting
    """
    if isinstance(value, unicode):
        value = value.encode('utf8')
    return _quote(value, safe)


# look for a real json parser first
try:
    # simplejson is popular and pretty good
    from simplejson import loads as json_loads
except ImportError:
    try:
        # 2.6 will have a json module in the stdlib
        from json import loads as json_loads
    except ImportError:
        # fall back on local parser otherwise
        comments = compile(r'/\*.*\*/|//[^\r\n]*', DOTALL)

        def json_loads(string):
            '''
            Fairly competent json parser exploiting the python tokenizer and
            eval(). -- From python-cloudfiles

            _loads(serialized_json) -> object
            '''
            try:
                res = []
                consts = {'true': True, 'false': False, 'null': None}
                string = '(' + comments.sub('', string) + ')'
                for type, val, _, _, _ in \
                        generate_tokens(StringIO(string).readline):
                    if (type == OP and val not in '[]{}:,()-') or \
                            (type == NAME and val not in consts):
                        raise AttributeError()
                    elif type == STRING:
                        res.append('u')
                        res.append(val.replace('\\/', '/'))
                    else:
                        res.append(val)
                return eval(''.join(res), {}, consts)
            except:
                raise AttributeError()


class ClientException(Exception):

    def __init__(self, msg, http_scheme='', http_host='', http_port='',
                 http_path='', http_query='', http_status=0, http_reason='',
                 http_device=''):
        Exception.__init__(self, msg)
        self.msg = msg
        self.http_scheme = http_scheme
        self.http_host = http_host
        self.http_port = http_port
        self.http_path = http_path
        self.http_query = http_query
        self.http_status = http_status
        self.http_reason = http_reason
        self.http_device = http_device

    def __str__(self):
        a = self.msg
        b = ''
        if self.http_scheme:
            b += '%s://' % self.http_scheme
        if self.http_host:
            b += self.http_host
        if self.http_port:
            b += ':%s' % self.http_port
        if self.http_path:
            b += self.http_path
        if self.http_query:
            b += '?%s' % self.http_query
        if self.http_status:
            if b:
                b = '%s %s' % (b, self.http_status)
            else:
                b = str(self.http_status)
        if self.http_reason:
            if b:
                b = '%s %s' % (b, self.http_reason)
            else:
                b = '- %s' % self.http_reason
        if self.http_device:
            if b:
                b = '%s: device %s' % (b, self.http_device)
            else:
                b = 'device %s' % self.http_device
        return b and '%s: %s' % (a, b) or a


def http_connection(url):
    """
    Make an HTTPConnection or HTTPSConnection

    :param url: url to connect to
    :returns: tuple of (parsed url, connection object)
    :raises ClientException: Unable to handle protocol scheme
    """
    parsed = urlparse(url)
    if parsed.scheme == 'http':
        conn = HTTPConnection(parsed.netloc)
    elif parsed.scheme == 'https':
        conn = HTTPSConnection(parsed.netloc)
    else:
        raise ClientException('Cannot handle protocol scheme %s for url %s' %
                              (parsed.scheme, repr(url)))
    return parsed, conn


def get_auth(url, user, key, snet=False):
    """
    Get authentication credentials

    :param url: authentication URL
    :param user: user to auth as
    :param key: key or passowrd for auth
    :param snet: use SERVICENET internal network default is False 
    :returns: tuple of (storage URL, storage token, auth token)
    :raises ClientException: HTTP GET request to auth URL failed
    """
    parsed, conn = http_connection(url)
    conn.request('GET', parsed.path, '',
                 {'X-Auth-User': user, 'X-Auth-Key': key})
    resp = conn.getresponse()
    if resp.status < 200 or resp.status >= 300:
        raise ClientException('Auth GET failed', http_scheme=parsed.scheme,
                http_host=conn.host, http_port=conn.port,
                http_path=parsed.path, http_status=resp.status,
                http_reason=resp.reason)
    url = resp.getheader('x-storage-url')
    if snet:
        parsed = list(urlparse(url))
        # Second item in the list is the netloc 
        parsed[1] = 'snet-' + parsed[1]
        url = urlunparse(parsed)
    return url, resp.getheader('x-storage-token',
                                                resp.getheader('x-auth-token'))


def get_account(url, token, marker=None, limit=None, prefix=None,
                http_conn=None, full_listing=False):
    """
    Get a listing of containers for the account.

    :param url: storage URL
    :param token: auth token
    :param marker: marker query
    :param limit: limit query
    :param prefix: prefix query
    :param http_conn: HTTP connection object (If None, it will create the
                      conn object)
    :param full_listing: if True, return a full listing, else returns a max
                         of 10000 listings
    :returns: a list of accounts
    :raises ClientException: HTTP GET request failed
    """
    if not http_conn:
        http_conn = http_connection(url)
    if full_listing:
        rv = []
        listing = get_account(url, token, marker, limit, prefix, http_conn)
        while listing:
            rv.extend(listing)
            marker = listing[-1]['name']
            listing = get_account(url, token, marker, limit, prefix, http_conn)
        return rv
    parsed, conn = http_conn
    qs = 'format=json'
    if marker:
        qs += '&marker=%s' % quote(marker)
    if limit:
        qs += '&limit=%d' % limit
    if prefix:
        qs += '&prefix=%s' % quote(prefix)
    conn.request('GET', '%s?%s' % (parsed.path, qs), '',
                 {'X-Auth-Token': token})
    resp = conn.getresponse()
    if resp.status < 200 or resp.status >= 300:
        resp.read()
        raise ClientException('Account GET failed', http_scheme=parsed.scheme,
                http_host=conn.host, http_port=conn.port,
                http_path=parsed.path, http_query=qs, http_status=resp.status,
                http_reason=resp.reason)
    if resp.status == 204:
        resp.read()
        return []
    return json_loads(resp.read())


def head_account(url, token, http_conn=None):
    """
    Get account stats.

    :param url: storage URL
    :param token: auth token
    :param http_conn: HTTP connection object (If None, it will create the
                      conn object)
    :returns: a tuple of (container count, object count, bytes used)
    :raises ClientException: HTTP HEAD request failed
    """
    if http_conn:
        parsed, conn = http_conn
    else:
        parsed, conn = http_connection(url)
    conn.request('HEAD', parsed.path, '', {'X-Auth-Token': token})
    resp = conn.getresponse()
    if resp.status < 200 or resp.status >= 300:
        raise ClientException('Account HEAD failed', http_scheme=parsed.scheme,
                http_host=conn.host, http_port=conn.port,
                http_path=parsed.path, http_status=resp.status,
                http_reason=resp.reason)
    return int(resp.getheader('x-account-container-count', 0)), \
           int(resp.getheader('x-account-object-count', 0)), \
           int(resp.getheader('x-account-bytes-used', 0))


def get_container(url, token, container, marker=None, limit=None,
                  prefix=None, delimiter=None, http_conn=None,
                  full_listing=False):
    """
    Get a listing of objects for the container.

    :param url: storage URL
    :param token: auth token
    :param container: container name to get a listing for
    :param marker: marker query
    :param limit: limit query
    :param prefix: prefix query
    :param delimeter: string to delimit the queries on
    :param http_conn: HTTP connection object (If None, it will create the
                      conn object)
    :param full_listing: if True, return a full listing, else returns a max
                         of 10000 listings
    :returns: a list of objects
    :raises ClientException: HTTP GET request failed
    """
    if not http_conn:
        http_conn = http_connection(url)
    if full_listing:
        rv = []
        listing = get_container(url, token, container, marker, limit, prefix,
                                delimiter, http_conn)
        while listing:
            rv.extend(listing)
            if not delimiter:
                marker = listing[-1]['name']
            else:
                marker = listing[-1].get('name', listing[-1].get('subdir'))
            listing = get_container(url, token, container, marker, limit,
                                    prefix, delimiter, http_conn)
        return rv
    parsed, conn = http_conn
    path = '%s/%s' % (parsed.path, quote(container))
    qs = 'format=json'
    if marker:
        qs += '&marker=%s' % quote(marker)
    if limit:
        qs += '&limit=%d' % limit
    if prefix:
        qs += '&prefix=%s' % quote(prefix)
    if delimiter:
        qs += '&delimiter=%s' % quote(delimiter)
    conn.request('GET', '%s?%s' % (path, qs), '', {'X-Auth-Token': token})
    resp = conn.getresponse()
    if resp.status < 200 or resp.status >= 300:
        resp.read()
        raise ClientException('Container GET failed',
                http_scheme=parsed.scheme, http_host=conn.host,
                http_port=conn.port, http_path=path, http_query=qs,
                http_status=resp.status, http_reason=resp.reason)
    if resp.status == 204:
        resp.read()
        return []
    return json_loads(resp.read())


def head_container(url, token, container, http_conn=None):
    """
    Get container stats.

    :param url: storage URL
    :param token: auth token
    :param container: container name to get stats for
    :param http_conn: HTTP connection object (If None, it will create the
                      conn object)
    :returns: a tuple of (object count, bytes used)
    :raises ClientException: HTTP HEAD request failed
    """
    if http_conn:
        parsed, conn = http_conn
    else:
        parsed, conn = http_connection(url)
    path = '%s/%s' % (parsed.path, quote(container))
    conn.request('HEAD', path, '', {'X-Auth-Token': token})
    resp = conn.getresponse()
    resp.read()
    if resp.status < 200 or resp.status >= 300:
        raise ClientException('Container HEAD failed',
                http_scheme=parsed.scheme, http_host=conn.host,
                http_port=conn.port, http_path=path, http_status=resp.status,
                http_reason=resp.reason)
    return int(resp.getheader('x-container-object-count', 0)), \
           int(resp.getheader('x-container-bytes-used', 0))


def put_container(url, token, container, http_conn=None):
    """
    Create a container

    :param url: storage URL
    :param token: auth token
    :param container: container name to create
    :param http_conn: HTTP connection object (If None, it will create the
                      conn object)
    :raises ClientException: HTTP PUT request failed
    """
    if http_conn:
        parsed, conn = http_conn
    else:
        parsed, conn = http_connection(url)
    path = '%s/%s' % (parsed.path, quote(container))
    conn.request('PUT', path, '', {'X-Auth-Token': token})
    resp = conn.getresponse()
    resp.read()
    if resp.status < 200 or resp.status >= 300:
        raise ClientException('Container PUT failed',
                http_scheme=parsed.scheme, http_host=conn.host,
                http_port=conn.port, http_path=path, http_status=resp.status,
                http_reason=resp.reason)


def delete_container(url, token, container, http_conn=None):
    """
    Delete a container

    :param url: storage URL
    :param token: auth token
    :param container: container name to delete
    :param http_conn: HTTP connection object (If None, it will create the
                      conn object)
    :raises ClientException: HTTP DELETE request failed
    """
    if http_conn:
        parsed, conn = http_conn
    else:
        parsed, conn = http_connection(url)
    path = '%s/%s' % (parsed.path, quote(container))
    conn.request('DELETE', path, '', {'X-Auth-Token': token})
    resp = conn.getresponse()
    resp.read()
    if resp.status < 200 or resp.status >= 300:
        raise ClientException('Container DELETE failed',
                http_scheme=parsed.scheme, http_host=conn.host,
                http_port=conn.port, http_path=path, http_status=resp.status,
                http_reason=resp.reason)


def get_object(url, token, container, name, http_conn=None,
               resp_chunk_size=None):
    """
    Get an object

    :param url: storage URL
    :param token: auth token
    :param container: container name that the object is in
    :param name: object name to get
    :param http_conn: HTTP connection object (If None, it will create the
                      conn object)
    :param resp_chunk_size: if defined, chunk size of data to read
    :returns: a list of objects
    :raises ClientException: HTTP GET request failed
    """
    if http_conn:
        parsed, conn = http_conn
    else:
        parsed, conn = http_connection(url)
    path = '%s/%s/%s' % (parsed.path, quote(container), quote(name))
    conn.request('GET', path, '', {'X-Auth-Token': token})
    resp = conn.getresponse()
    if resp.status < 200 or resp.status >= 300:
        resp.read()
        raise ClientException('Object GET failed', http_scheme=parsed.scheme,
                http_host=conn.host, http_port=conn.port, http_path=path,
                http_status=resp.status, http_reason=resp.reason)
    metadata = {}
    for key, value in resp.getheaders():
        if key.lower().startswith('x-object-meta-'):
            metadata[unquote(key[len('x-object-meta-'):])] = unquote(value)
    if resp_chunk_size:

        def _object_body():
            buf = resp.read(resp_chunk_size)
            while buf:
                yield buf
                buf = resp.read(resp_chunk_size)
        object_body = _object_body()
    else:
        object_body = resp.read()
    return resp.getheader('content-type'), \
           int(resp.getheader('content-length', 0)), \
           resp.getheader('last-modified'), \
           resp.getheader('etag').strip('"'), \
           metadata, \
           object_body


def head_object(url, token, container, name, http_conn=None):
    """
    Get object info

    :param url: storage URL
    :param token: auth token
    :param container: container name that the object is in
    :param name: object name to get info for
    :param http_conn: HTTP connection object (If None, it will create the
                      conn object)
    :returns: a tuple of (content type, content length, last modfied, etag,
              dictionary of metadata)
    :raises ClientException: HTTP HEAD request failed
    """
    if http_conn:
        parsed, conn = http_conn
    else:
        parsed, conn = http_connection(url)
    path = '%s/%s/%s' % (parsed.path, quote(container), quote(name))
    conn.request('HEAD', path, '', {'X-Auth-Token': token})
    resp = conn.getresponse()
    resp.read()
    if resp.status < 200 or resp.status >= 300:
        raise ClientException('Object HEAD failed', http_scheme=parsed.scheme,
                http_host=conn.host, http_port=conn.port, http_path=path,
                http_status=resp.status, http_reason=resp.reason)
    metadata = {}
    for key, value in resp.getheaders():
        if key.lower().startswith('x-object-meta-'):
            metadata[unquote(key[len('x-object-meta-'):])] = unquote(value)
    return resp.getheader('content-type'), \
           int(resp.getheader('content-length', 0)), \
           resp.getheader('last-modified'), \
           resp.getheader('etag').strip('"'), \
           metadata


def put_object(url, token, container, name, contents, metadata={},
               content_length=None, etag=None, chunk_size=65536,
               content_type=None, http_conn=None):
    """
    Put an object

    :param url: storage URL
    :param token: auth token
    :param container: container name that the object is in
    :param name: object name to put
    :param contents: file like object to read object data from
    :param metadata: dictionary of object metadata
    :param content_length: value to send as content-length header
    :param etag: etag of contents
    :param chunk_size: chunk size of data to write
    :param content_type: value to send as content-type header
    :param http_conn: HTTP connection object (If None, it will create the
                      conn object)
    :returns: etag from server response
    :raises ClientException: HTTP PUT request failed
    """
    if http_conn:
        parsed, conn = http_conn
    else:
        parsed, conn = http_connection(url)
    path = '%s/%s/%s' % (parsed.path, quote(container), quote(name))
    headers = {'X-Auth-Token': token}
    for key, value in metadata.iteritems():
        headers['X-Object-Meta-%s' % quote(key)] = quote(value)
    if etag:
        headers['ETag'] = etag.strip('"')
    if content_length is not None:
        headers['Content-Length'] = str(content_length)
    if content_type is not None:
        headers['Content-Type'] = content_type
    if not contents:
        headers['Content-Length'] = '0'
    if hasattr(contents, 'read'):
        conn.putrequest('PUT', path)
        for header, value in headers.iteritems():
            conn.putheader(header, value)
        if not content_length:
            conn.putheader('Transfer-Encoding', 'chunked')
        conn.endheaders()
        chunk = contents.read(chunk_size)
        while chunk:
            if not content_length:
                conn.send('%x\r\n%s\r\n' % (len(chunk), chunk))
            else:
                conn.send(chunk)
            chunk = contents.read(chunk_size)
        if not content_length:
            conn.send('0\r\n\r\n')
    else:
        conn.request('PUT', path, contents, headers)
    resp = conn.getresponse()
    resp.read()
    if resp.status < 200 or resp.status >= 300:
        raise ClientException('Object PUT failed', http_scheme=parsed.scheme,
                http_host=conn.host, http_port=conn.port, http_path=path,
                http_status=resp.status, http_reason=resp.reason)
    return resp.getheader('etag').strip('"')


def post_object(url, token, container, name, metadata, http_conn=None):
    """
    Change object metadata

    :param url: storage URL
    :param token: auth token
    :param container: container name that the object is in
    :param name: object name to change
    :param metadata: dictionary of object metadata
    :param http_conn: HTTP connection object (If None, it will create the
                      conn object)
    :raises ClientException: HTTP POST request failed
    """
    if http_conn:
        parsed, conn = http_conn
    else:
        parsed, conn = http_connection(url)
    path = '%s/%s/%s' % (parsed.path, quote(container), quote(name))
    headers = {'X-Auth-Token': token}
    for key, value in metadata.iteritems():
        headers['X-Object-Meta-%s' % quote(key)] = quote(value)
    conn.request('POST', path, '', headers)
    resp = conn.getresponse()
    resp.read()
    if resp.status < 200 or resp.status >= 300:
        raise ClientException('Object POST failed', http_scheme=parsed.scheme,
                http_host=conn.host, http_port=conn.port, http_path=path,
                http_status=resp.status, http_reason=resp.reason)


def delete_object(url, token, container, name, http_conn=None):
    """
    Delete object

    :param url: storage URL
    :param token: auth token
    :param container: container name that the object is in
    :param name: object name to delete
    :param http_conn: HTTP connection object (If None, it will create the
                      conn object)
    :raises ClientException: HTTP DELETE request failed
    """
    if http_conn:
        parsed, conn = http_conn
    else:
        parsed, conn = http_connection(url)
    path = '%s/%s/%s' % (parsed.path, quote(container), quote(name))
    conn.request('DELETE', path, '', {'X-Auth-Token': token})
    resp = conn.getresponse()
    resp.read()
    if resp.status < 200 or resp.status >= 300:
        raise ClientException('Object DELETE failed',
                http_scheme=parsed.scheme, http_host=conn.host,
                http_port=conn.port, http_path=path, http_status=resp.status,
                http_reason=resp.reason)


class Connection(object):
    """Convenience class to make requests that will also retry the request"""

    def __init__(self, authurl, user, key, retries=5, preauthurl=None,
                 preauthtoken=None, snet=False):
        """
        :param authurl: authenitcation URL
        :param user: user name to authenticate as
        :param key: key/password to authenticate with
        :param retries: Number of times to retry the request before failing
        :param preauthurl: storage URL (if you have already authenticated)
        :param preauthtoken: authentication token (if you have already
                             authenticated)
        :param snet: use SERVICENET internal network default is False 
        """
        self.authurl = authurl
        self.user = user
        self.key = key
        self.retries = retries
        self.http_conn = None
        self.url = preauthurl
        self.token = preauthtoken
        self.attempts = 0
        self.snet = snet

    def _retry(self, func, *args, **kwargs):
        kwargs['http_conn'] = self.http_conn
        self.attempts = 0
        backoff = 1
        while self.attempts <= self.retries:
            self.attempts += 1
            try:
                if not self.url or not self.token:
                    self.url, self.token = \
                        get_auth(self.authurl, self.user, self.key, snet=self.snet)
                    self.http_conn = None
                if not self.http_conn:
                    self.http_conn = http_connection(self.url)
                    kwargs['http_conn'] = self.http_conn
                rv = func(self.url, self.token, *args, **kwargs)
                return rv
            except (socket.error, HTTPException):
                if self.attempts > self.retries:
                    raise
                self.http_conn = None
            except ClientException, err:
                if self.attempts > self.retries:
                    raise
                if err.http_status == 401:
                    self.url = self.token = None
                    if self.attempts > 1:
                        raise
                elif 500 <= err.http_status <= 599:
                    pass
                else:
                    raise
            sleep(backoff)
            backoff *= 2

    def head_account(self):
        """Wrapper for head_account"""
        return self._retry(head_account)

    def get_account(self, marker=None, limit=None, prefix=None,
                    full_listing=False):
        """Wrapper for get_account"""
        # TODO: With full_listing=True this will restart the entire listing
        # with each retry. Need to make a better version that just retries
        # where it left off.
        return self._retry(get_account, marker=marker, limit=limit,
                           prefix=prefix, full_listing=full_listing)

    def head_container(self, container):
        """Wrapper for head_container"""
        return self._retry(head_container, container)

    def get_container(self, container, marker=None, limit=None, prefix=None,
                      delimiter=None, full_listing=False):
        """Wrapper for get_container"""
        # TODO: With full_listing=True this will restart the entire listing
        # with each retry. Need to make a better version that just retries
        # where it left off.
        return self._retry(get_container, container, marker=marker,
                           limit=limit, prefix=prefix, delimiter=delimiter,
                           full_listing=full_listing)

    def put_container(self, container):
        """Wrapper for put_container"""
        return self._retry(put_container, container)

    def delete_container(self, container):
        """Wrapper for delete_container"""
        return self._retry(delete_container, container)

    def head_object(self, container, obj):
        """Wrapper for head_object"""
        return self._retry(head_object, container, obj)

    def get_object(self, container, obj, resp_chunk_size=None):
        """Wrapper for get_object"""
        return self._retry(get_object, container, obj,
                           resp_chunk_size=resp_chunk_size)

    def put_object(self, container, obj, contents, metadata={},
                   content_length=None, etag=None, chunk_size=65536,
                   content_type=None):
        """Wrapper for put_object"""
        return self._retry(put_object, container, obj, contents,
            metadata=metadata, content_length=content_length, etag=etag,
            chunk_size=chunk_size, content_type=content_type)

    def post_object(self, container, obj, metadata):
        """Wrapper for post_object"""
        return self._retry(post_object, container, obj, metadata)

    def delete_object(self, container, obj):
        """Wrapper for delete_object"""
        return self._retry(delete_object, container, obj)
