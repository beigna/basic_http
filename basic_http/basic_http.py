
import httplib
from urlparse import urlparse
from urllib import urlencode
from base64 import encodestring

class BasicHttpError(Exception): pass
class UnsupportedScheme(BasicHttpError): pass
class UnexpectedResponse(BasicHttpError): pass

class BasicHttp(object):
    __slots__ = (
        '_url',
        '_follow_redirect',
        '_max_redirects',
        '_followable_codes',
        '_status',
        '_header',
        '_body',
        '_conn',
        '_res',
        '_auth',
    )

    def __init__(self, url, *args, **kwargs):
        self._url = urlparse(url)
        if self._url.scheme != 'http':
            raise UnsupportedScheme('%s is not supported.' % (self._url.scheme))

        self._follow_redirect = kwargs.get('follow_redirect', True)
        self._max_redirects = kwargs.get('max_redirects', 5)
        self._followable_codes = (301, 302, 303)

        self._status = None
        self._header = None
        self._body = None
        self._auth = None

    def authenticate(self, username, password):
        self._auth = 'Basic %s' % (
            encodestring('%s:%s' % (username, password))[:-1]
        )

    def _path(self):
        path = self._url.geturl()
        path = path.replace(self._url.scheme, '', 1)
        path = path.replace(self._url.netloc, '', 1)
        return path[3:]

    def _headers_to_dict(self):
        headers_dict = {}
        for k, v in self._res.getheaders():
            headers_dict[k.title()] = v

        return headers_dict

    def _process_response(self):
        self._status = self._res.status
        self._header = self._headers_to_dict()
        self._body = self._res.read()

    def _location_redirect(self, location):
        location_url = urlparse(location)
        if location_url.netloc == '':
            final_url = '%s://%s%s' % (
                self._url.scheme,
                self._url.netloc,
                location_url.geturl())

            self._url = urlparse(final_url)
            return

        self._url = location_url

    def _request(self, method, data=None, headers={}, wanted_status=None):
        if 'User-Agent' not in headers.keys():
            headers['User-Agent'] = 'BasicHttp Lib 0.4.2 - ' \
                'http://github.com/nachopro/basic_http'

        if self._auth:
            headers['Authorization'] = self._auth

        if isinstance(data, dict):
            data = urlencode(data)

        redirects_count = 0
        while True:
            self._conn = httplib.HTTPConnection(self._url.netloc)
            self._conn.request(method, self._path(), data, headers)
            self._res = self._conn.getresponse()

            self._process_response()

            if self._res.status in self._followable_codes and \
            self._follow_redirect is True:
                if redirects_count < self._max_redirects:
                    redirects_count += 1
                    self._location_redirect(self._header['Location'])
                    continue

            break

        if isinstance(wanted_status, list):
            if self._res.status not in wanted_status:
                raise UnexpectedResponse('Wanted status: %s ' \
                    'Responsed status: %d' % (wanted_status, self._res.status))

        return {
            'status': self._status,
            'header': self._header,
            'body': self._body
        }

    def GET(self, data=None, headers={}, wanted_status=None):
        return self._request('GET', data, headers, wanted_status)

    def POST(self, data=None, headers={}, wanted_status=None):
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        return self._request('POST', data, headers, wanted_status)

    def HEAD(self, data=None, headers={}, wanted_status=None):
        return self._request('HEAD', data, headers, wanted_status)

    def PUT(self, data=None, headers={}, wanted_status=None):
        return self._request('PUT', data, headers, wanted_status)

