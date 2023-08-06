# #!/usr/bin/env python
# -*- coding: utf-8 -*-
# <HTTPretty - HTTP client mock for Python>
# Copyright (C) <2011>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
version = '0.1'

import re
import socket
import warnings

from datetime import datetime
from StringIO import StringIO
from urlparse import urlsplit

old_socket = socket.socket
old_create_connection = socket.create_connection
old_gethostbyname = socket.gethostbyname
old_gethostname = socket.gethostname
old_getaddrinfo = socket.getaddrinfo
old_socksocket = None

try:
    import socks
    old_socksocket = socks.socksocket
except ImportError:
    socks = None

class HTTPrettyError(Exception):
    pass

class FakeSockFile(StringIO):
    def read(self, amount=None):
        amount = amount or self.len
        new_amount = amount

        if amount > self.len:
            new_amount = self.len - self.tell()

        ret = StringIO.read(self, new_amount)
        remaining = amount - new_amount - 1
        if remaining > 0:
            ret = ret + (" " * remaining)

        return ret

class fakesock(object):
    class socket(object):
        _entry = None
        debuglevel = 0

        def __init__(self, family, type, protocol):
            self.family = family
            self.type = type
            self.protocol = protocol
            self.truesock = old_socket(family, type, protocol)
            self._closed = True
            self.fd = FakeSockFile()
            self.timeout = socket._GLOBAL_DEFAULT_TIMEOUT

        def connect(self, address):
            self._address = (self._host, self._port) = address
            self._closed = False

        def close(self):
            if not self._closed:
                self.truesock.close()
            self._closed = True

        def makefile(self, mode, bufsize):
            self._mode = mode
            self._bufsize = bufsize

            if self._entry:
                self._entry.fill_filekind(self.fd)

            return self.fd

        def _true_sendall(self, data):
            self.truesock.connect(self._address)
            self.truesock.sendall(data)
            _d = self.truesock.recv(255)
            self.fd.seek(0)
            self.fd.write(_d)
            while _d:
                _d = self.truesock.recv(255)
                self.fd.write(_d)

            self.fd.seek(0)
            self.truesock.close()

        def sendall(self, data):
            self.fd.seek(0)
            try:
                verb, headers_string = data.split('\n', 1)
            except ValueError:
                return self._true_sendall(data)

            method, path, version = re.split('\s+', verb.strip(), 3)

            info = URIInfo(hostname=self._host, port=self._port, path=path)

            entries = []
            for key, value in HTTPretty._entries.items():
                if key == info:
                    entries = value
                    info = key
                    break

            if not entries:
                self._true_sendall(data)
                return

            entry = info.get_next_entry()
            if entry.method == method:
                self._entry = entry

def create_fake_connection(address, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
    s = fakesock.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    if timeout is not socket._GLOBAL_DEFAULT_TIMEOUT:
        s.settimeout(timeout)

    s.connect(address)
    return s

def fake_gethostbyname(host):
    return host

def fake_gethostname():
    return 'localhost'

def fake_getaddrinfo(host, port, family=None, socktype=None, proto=None, flags=None):
    return [(2, 1, 6, '', (host, port))]

STATUSES = {
    100: "Continue",
    101: "Switching Protocols",
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    307: "Temporary Redirect",
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Time-out",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Request Entity Too Large",
    414: "Request-URI Too Large",
    415: "Unsupported Media Type",
    416: "Requested range not satisfiable",
    417: "Expectation Failed",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Time-out",
    505: "HTTP Version not supported",
}

class Entry(object):
    def __init__(self, method, uri, body, adding_headers=None, forcing_headers=None, status=200, **headers):
        self.method = method
        self.uri = uri
        self.body = body
        self.body_length = len(body or '')
        self.adding_headers = adding_headers or {}
        self.forcing_headers = forcing_headers or {}
        self.status = int(status)

        for k, v in headers.items():
            name = "-".join(k.split("_")).capitalize()
            self.adding_headers[name] = v

        self.validate()

    def validate(self):
        content_length_keys = 'Content-Length', 'content-cength'
        for key in content_length_keys:
            got = self.adding_headers.get(key, self.forcing_headers.get(key, None))
            if got is None:
                continue

            try:
                igot = int(got)
            except ValueError:
                warnings.warn('HTTPretty got to register the Content-Length header with "%r" which is not a number' % got)

            if igot > self.body_length:
                raise HTTPrettyError(
                    'HTTPretty got inconsistent parameters. The header Content-Length you registered expects size "%d" '
                    'but the body you registered for that has actually length "%d".\n'
                    'Fix that, or if you really want that, call register_uri with "fill_with" callback.' % (
                        igot, self.body_length
                    )
                )


    def __repr__(self):
        return r'<Entry %s %s getting %d>' % (self.method, self.uri, self.status)

    def fill_filekind(self, fk):
        now = datetime.utcnow()

        headers = {
            'Status': self.status,
            'Date': now.strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'Server': 'Python/HTTPretty',
            'Connection': 'close',
        }

        if self.forcing_headers:
            headers = self.forcing_headers

        if self.adding_headers:
            headers.update(self.adding_headers)

        status = headers.get('Status', self.status)

        string_list = [
            'HTTP/1.1 %d %s' % (status, STATUSES[status]),
        ]

        if 'Date' in headers:
            string_list.append('Date: %s' % headers.pop('Date'))

        if not self.forcing_headers:
            string_list.append('Content-Type: %s' % headers.pop('Content-Type', 'text/plain; charset=utf-8'))
            string_list.append('Content-Length: %s' % headers.pop('Content-Length', len(self.body)))
            string_list.append('Server: %s' % headers.pop('Server')),

        for k, v in headers.items():
            string_list.append(
                '%s: %s' % (k, unicode(v))
            )

        fk.write("\n".join(string_list))
        fk.write('\n\r\n')
        fk.write(self.body)
        fk.seek(0)

class URIInfo(object):
    def __init__(self, username='', password='', hostname='', port=80, path='/', query='', fragment='', entries=None):
        self.username = username or ''
        self.password = password or ''
        self.hostname = hostname or ''
        self.port = int(port) != 80 and str(port) or ''
        self.path = path or ''
        self.query = query or ''
        self.fragment = fragment or ''
        self.entries = entries
        self.current_entry = 0

    def get_next_entry(self):
        if self.current_entry >= len(self.entries):
            self.current_entry = -1


        if not self.entries:
            raise ValueError('I have no entries: %s' % self)

        entry = self.entries[self.current_entry]
        if self.current_entry != -1:
            self.current_entry += 1
        return entry

    def __unicode__(self):
        attrs = 'username', 'password', 'hostname', 'port', 'path', 'query', 'fragment'
        return ur'<httpretty.URIInfo(%s)>' % ", ".join(['%s="%s"' % (k, getattr(self, k, '')) for k in attrs])

    def __repr__(self):
        return unicode(self)

    def __hash__(self):
        return hash(unicode(self))

    def __eq__(self, other):
        return unicode(self) == unicode(other)

    @classmethod
    def from_uri(cls, uri, entry):
        result = urlsplit(uri)
        return cls(result.username,
                   result.password,
                   result.hostname,
                   result.port or 80,
                   result.path,
                   result.query,
                   result.fragment,
                   entry)


class HTTPretty(object):
    u"""The URI registration class"""
    _entries = {}

    GET = 'GET'
    PUT = 'PUT'
    POST = 'POST'
    DELETE = 'DELETE'
    HEAD = 'HEAD'

    @classmethod
    def register_uri(cls, method, uri, body='HTTPretty :)', adding_headers=None, forcing_headers=None, status=200, responses=None, **headers):
        if isinstance(responses, list) and len(responses) > 0:
            entries_for_this_uri = responses
        else:
            entries_for_this_uri = [
                cls.Response(
                    body=body,
                    adding_headers=adding_headers,
                    forcing_headers=forcing_headers,
                    status=status, **headers
                )
            ]

        map(lambda e: setattr(e, 'uri', uri) or setattr(e, 'method', method), entries_for_this_uri)

        info = URIInfo.from_uri(uri, entries_for_this_uri)
        if cls._entries.has_key(info):
            del cls._entries[info]

        cls._entries[info] = entries_for_this_uri

    def __repr__(self):
        return u'<HTTPretty with %d URI entries>' % len(self._entries)

    @classmethod
    def Response(cls, body, adding_headers=None, forcing_headers=None, status=200, **headers):
        return Entry(
            method=None,
            uri=None,
            body=body,
            adding_headers=adding_headers,
            forcing_headers=forcing_headers,
            status=status,
            **headers
        )

    @classmethod
    def disable(cls):
        socket.socket = old_socket
        socket.create_connection = old_create_connection
        socket.gethostname = old_gethostname
        socket.gethostbyname = old_gethostbyname
        socket.getaddrinfo = old_getaddrinfo
        socket.inet_aton = old_gethostbyname

        socket.__dict__['socket'] = old_socket
        socket.__dict__['create_connection'] = old_create_connection
        socket.__dict__['gethostname'] = old_gethostname
        socket.__dict__['gethostbyname'] = old_gethostbyname
        socket.__dict__['getaddrinfo'] = old_getaddrinfo
        socket.__dict__['inet_aton'] = old_gethostbyname

        if socks:
            socks.socksocket = old_socksocket
            socks.__dict__['socksocket'] = old_socksocket

    @classmethod
    def enable(cls):
        socket.socket = fakesock.socket
        socket.create_connection = create_fake_connection
        socket.gethostname = fake_gethostname
        socket.gethostbyname = fake_gethostbyname
        socket.getaddrinfo = fake_getaddrinfo
        socket.inet_aton = fake_gethostbyname

        socket.__dict__['socket'] = fakesock.socket
        socket.__dict__['create_connection'] = create_fake_connection
        socket.__dict__['gethostname'] = fake_gethostname
        socket.__dict__['gethostbyname'] = fake_gethostbyname
        socket.__dict__['inet_aton'] = fake_gethostbyname
        socket.__dict__['getaddrinfo'] = fake_getaddrinfo

        if socks:
            socks.socksocket = fakesock.socket
            socks.__dict__['socksocket'] = fakesock.socket

HTTPretty.enable()
