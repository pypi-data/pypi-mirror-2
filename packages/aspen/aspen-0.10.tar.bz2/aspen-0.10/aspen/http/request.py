import urllib
import urlparse
from Cookie import CookieError, SimpleCookie

from aspen import Response
from aspen.http.headers import Headers
from aspen.http.wwwform import WwwForm


class Path(dict):
    def __init__(self, bytes):
        self.raw = bytes
        dict.__init__(self)
    def __str__(self):
        return self.raw


class Request(object):
    """Represent an HTTP Request message. Attributes:

    http://sync.in/aspen-request

    """
   
    def hydrate(self):
        """Populate a number of attributes on self based on primitives.
        """
        self.body = WwwForm(self.raw_body)
        self.headers = Headers(self.raw_headers)
        self.cookie = SimpleCookie()
        try:
            self.cookie.load(self.headers.one('Cookie', ''))
        except CookieError:
            pass

        urlparts = urlparse.urlparse(self.raw_url)
        self.path = Path(urlparts[2]) # populated by Website
        self.raw_querystring = urlparts[4]
        self.qs = WwwForm(self.raw_querystring)
        self.url = self.rebuild_url() # needs things above
        self.urlparts = urlparse.urlparse(self.url)

        self.transport = None # set by Website for *.sock files
        self.session_id = None # set by Website for *.sock files
        self.root = '' # set by Website
        self.fs = '' # set by Website
        self.namespace = {} # populated by user in inbound hooks

    @classmethod
    def from_wsgi(cls, environ):
        """Set primitives from a WSGI environ.
        """
        self = cls()
        self.method = environ['REQUEST_METHOD']
        self.version = environ['SERVER_PROTOCOL']

        raw_headers = []
        for k, v in environ.items():
            if k.startswith('HTTP_'):
                k = k[len('HTTP_'):]
                raw_headers.append(': '.join([k, v]))
        raw_headers = '\r\n'.join(raw_headers)
        self.raw_headers = raw_headers
        self.raw_body = environ['wsgi.input'].read()
        self.remote_addr = environ['REMOTE_ADDR']
        self.raw_url = environ['PATH_INFO']

        self.hydrate()
        return self

    def __str__(self):
        return "<%s %s>" % (self.method, self.path)
    __repr__ = __str__

    def allow(self, *methods):
        """Given a list of methods, raise 405 if we don't meet the requirement.
        """
        methods = [x.upper() for x in methods]
        if self.method not in methods:
            raise Response(405, headers={'Allow': ', '.join(methods)})

    @property
    def is_xhr(self):
        val = self.headers.one('X-Requested-With', '')
        return val.lower() == 'xmlhttprequest'

    def rebuild_url(self):
        """Return a full URL for this request, per PEP 333:

            http://www.python.org/dev/peps/pep-0333/#url-reconstruction

        This function is kind of naive.

        """
        # http://docs.python.org/library/wsgiref.html#wsgiref.util.guess_scheme
        scheme = self.headers.one('HTTPS') and 'https' or 'http'
        url = scheme
        url += '://'

        if 'X-Forwarded-Host' in self.headers:
            url += self.headers.one('X-Forwarded-Host')
        elif 'Host' in self.headers:
            url += self.headers.one('Host')
        else:
            # per spec, respond with 400 if no Host header given
            raise Response(400)

        url += urllib.quote(self.path.raw)
        # screw params, fragment?
        if self.raw_querystring:
            url += '?' + self.raw_querystring
        return url
