import functools
import urllib.parse

from src.utils.cookies.header_converter import CookieHeaderConverter
from src.utils.request_uri import RequestURI


class Request:

    def __init__(self, wsgi_environment, path_parameters=None):
        self._wsgi_environment = wsgi_environment
        self._path_parameters = path_parameters if path_parameters else {}

    @staticmethod
    def copy_and_set_path_parameters(other_request, path_parameters):
        return Request(other_request.wsgi_environment, path_parameters)

    @property
    def wsgi_environment(self):
        return self._wsgi_environment

    @property
    def http_method(self):
        return self._wsgi_environment.get("REQUEST_METHOD")

    @property
    def request_uri(self):
        return RequestURI.from_wsgi_environment(self._wsgi_environment)

    # TODO: Make sure these lru_caches are per request and not per app
    # TODO:     create a request, put stuff in cache, sleep 500
    # TODO:     create a different request, pull and see if its from first cache
    @property
    @functools.lru_cache()
    def forwarded_request_uri(self):
        return RequestURI.forwarded_from_wsgi_environment(self._wsgi_environment)

    @property
    @functools.lru_cache()
    def headers(self):
        headers = {}
        for wsgi_environment_variable_name, wsgi_environment_variable_value in self.wsgi_environment.items():
            if wsgi_environment_variable_name.startswith("HTTP_"):
                headers[wsgi_environment_variable_name[5:].replace("_", "-")] = wsgi_environment_variable_value
            elif wsgi_environment_variable_name in ("CONTENT_LENGTH", "CONTENT_TYPE"):
                headers[wsgi_environment_variable_name.replace("_", "-")] = wsgi_environment_variable_value
        return headers

    @property
    def client_ip_address(self):
        return self._wsgi_environment.get("REMOTE_ADDR")

    @property
    def cookies(self):
        return CookieHeaderConverter.from_header(self._wsgi_environment.get("HTTP_COOKIE"))

    @property
    @functools.lru_cache()
    def query_parameters(self):
        parsed_params = urllib.parse.parse_qs(self._wsgi_environment.get("QUERY_STRING"))
        unquoted_parsed_params = {}
        for param_name, param_values in parsed_params:
            unquoted_name = urllib.parse.unquote(param_name)
            unquoted_parsed_params[unquoted_name] = []
            for param_value in param_values:
                unquoted_parsed_params[unquoted_name].append(urllib.parse.unquote(param_value))
        return unquoted_parsed_params

    @property
    def path_parameters(self):
        return self._path_parameters

    @property
    @functools.lru_cache()
    def byte_body(self):
        return self._wsgi_environment.get("wsgi.input").read(self._wsgi_environment.get("CONTENT_LENGTH", 0))

    @property
    @functools.lru_cache()
    def utf8_body(self):
        return str(self.byte_body.decode("utf-8"))

