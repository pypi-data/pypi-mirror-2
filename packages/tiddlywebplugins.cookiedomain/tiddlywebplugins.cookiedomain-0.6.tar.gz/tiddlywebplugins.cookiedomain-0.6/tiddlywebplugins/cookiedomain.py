"""
Description of My Plugin.
"""

import Cookie

from tiddlyweb.web.wsgi import EncodeUTF8


COOKIE_NAME = 'tiddlyweb_user'


class CookieDomain(object):

    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):

        def replacement_start_response(status, headers, exc_info=None):
            for index, header in enumerate(headers):
                name, value = header
                if name.lower() == 'set-cookie':
                    cookie = Cookie.SimpleCookie()
                    cookie.load(value)
                    try:
                        if (cookie[COOKIE_NAME] and not
                                cookie[COOKIE_NAME]['domain']):
                            cookie[COOKIE_NAME]['domain'] = self._get_domain(
                                    environ)
                            value = cookie.output(header='') + '; httponly'
                            headers[index] = (name, value)
                    except KeyError:
                        pass
            return start_response(status, headers, exc_info)
        return self.application(environ, replacement_start_response)

    def _get_domain(self, environ):
        try:
            domain = environ['tiddlyweb.config']['cookie_domain']
        except KeyError:
            http_host = environ.get('HTTP_HOST')
            server_host = environ['tiddlyweb.config']['server_host']['host']
            if http_host:
                domain = http_host.split(':', 1)[0]
                if server_host in domain:
                    domain = server_host
            else:
                domain = server_host
        return domain


def init(config):
    if CookieDomain not in config['server_response_filters']:
        config['server_response_filters'].insert(
                config['server_response_filters'].index(
                    EncodeUTF8) + 1, CookieDomain)
