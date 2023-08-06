from Cookie import CookieError, SimpleCookie

from aspen.http.headers import Headers
from diesel.protocols.http import ( http_response as DieselResponse
                                  , status_strings
                                   )


class Response(Exception):
    """Represent an HTTP Response message.
    """

    def __init__(self, code=200, body='', headers=None):
        """Takes an int, a string, and a dict (or list of tuples).

            - code      an HTTP response code, e.g., 404
            - body      the message body as a string
            - headers   a Headers instance
            - cookie    a Cookie.SimpleCookie instance

        Code is first because when you're raising your own Responses, they're
        usually error conditions. Body is second because one more often wants
        to specify a body without headers, than a header without a body.

        """
        if not isinstance(code, int):
            raise TypeError("'code' must be an integer")
        elif not isinstance(body, basestring):
            raise TypeError("'body' must be a string")
        elif headers is not None and not isinstance(headers, (dict, list)):
            raise TypeError("'headers' must be a dictionary or a list of " +
                            "2-tuples")

        Exception.__init__(self)
        self.code = code
        self.body = body
        self.headers = Headers('')
        if headers:
            if isinstance(headers, dict):
                headers = headers.items()
            for k, v in headers:
                self.headers.add(k, v)
        self.cookie = SimpleCookie()
        try:
            self.cookie.load(self.headers.one('Cookie', ''))
        except CookieError:
            pass


    def __repr__(self):
        return "<Response: %s>" % str(self)

    def __str__(self):
        return "%d %s" % (self.code, self._status())

    def _status(self):
        return status_strings.get(self.code, ('???','Unknown HTTP status'))

    def _to_diesel(self, _diesel_request):
        """This actually sends bits over the wire(!).
        """
        for morsel in self.cookie.values():
            self.headers.add('Set-Cookie', morsel.OutputString())
        self.headers._diesel_headers._headers = self.headers._dict
        return DieselResponse( _diesel_request
                             , self.code
                             , self.headers._diesel_headers
                             , self.body
                              )

    def _to_http(self, version):
        status_line = "HTTP/%s" % version
        headers = self.headers.to_http()
        body = self.body
        if self.headers.one('Content-Type', '').startswith('text/'):
            body = body.replace('\n', '\r\n')
            body = body.replace('\r\r', '\r')
        return '\r\n'.join([status_line, headers, '', body])

