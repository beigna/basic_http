
import httplib
from urlparse import urlparse
from urllib import urlencode

class BasicHttpError(Exception): pass
class UnsupportedScheme(BasicHttpError): pass
class UnexpectedResponse(BasicHttpError): pass

class BasicHttp(object):
    __slots__ = (
        '_url',
        '_status',
        '_header',
        '_body',
        '_conn',
        '_res',
    )

    def __init__(self, url, *args, **kwargs):
        self._url = urlparse(url)
        if self._url.scheme != 'http':
            raise UnsupportedScheme('%s is not supported.' % (self._url.scheme))

        self._status = None
        self._header = None
        self._body = None


    def authenticate(self, username, password):
        pass

    def _path(self):
        path = self._url.geturl()
        path = path.replace(self._url.scheme, '')
        path = path.replace(self._url.netloc, '')
        return path[3:]

    def _headers_to_dict(self):
        headers_dict = {}
        for k, v in self._res.getheaders():
            headers_dict[k.title()] = v

        return headers_dict

    def _request(self, method, data=None, headers={}, wanted_status=None):
        if 'User-Agent' not in headers.keys():
            headers['User-Agent'] = 'BasicHttp Lib 0.3 - ' \
                'http://github.com/nachopro/basic_http'

        if isinstance(data, dict):
            data = urlencode(data)

        self._conn = httplib.HTTPConnection(self._url.netloc)
        self._conn.request(method, self._path(), data, headers)
        self._res = self._conn.getresponse()

        if isinstance(wanted_status, list):
            if self._res.status not in wanted_status:
                raise UnexpectedResponse('Wanted status: %d ' \
                    'Responsed status: %d' % (wanted_status, self._res.status))

        self._status = self._res.status
        self._header = self._headers_to_dict()
        self._body = self._res.read()

        return {
            'satus': self._status,
            'header': self._header,
            'body': self._body
        }

    def GET(self, data=None, headers={}, wanted_status=None):
        return self._request('GET', data, headers, wanted_status)

    def POST(self, data=None, headers={}, wanted_status=None):
        return self._request('POST', data, headers, wanted_status)

    def HEAD(self, data=None, headers={}, wanted_status=None):
        return self._request('HEAD', data, headers, wanted_status)

    def PUT(self, data=None, headers={}, wanted_status=None):
        return self._request('PUT', data, headers, wanted_status)

