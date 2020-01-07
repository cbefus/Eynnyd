from eynnyd.internal.utils.header_helpers import HeaderSplitter


class RequestURI:

    def __init__(self, scheme, host, port, path, query):
        self._scheme = scheme
        self._host = host
        self._port = port
        self._path = path
        self._query = query

    @staticmethod
    def from_wsgi_environment(wsgi_environment):
        return RequestURI(
            wsgi_environment.get("wsgi.url_scheme"),
            wsgi_environment.get("SERVER_NAME"),  # https://perfect-co.de/2011/02/why-http_host-is-evil/
            wsgi_environment.get("SERVER_PORT"),
            wsgi_environment.get("PATH_INFO"),
            wsgi_environment.get("QUERY_STRING"))

    @staticmethod
    def forwarded_from_wsgi_environment(wsgi_environment):
        scheme = wsgi_environment.get("wsgi.url_scheme")
        host = wsgi_environment.get("SERVER_NAME")
        if "HTTP_FORWARDED" in wsgi_environment:
            forwarded_kv = HeaderSplitter.split_to_kv(wsgi_environment.get("HTTP_FORWARDED"))
            if "proto" in forwarded_kv:
                scheme = forwarded_kv["proto"]
            if "host" in forwarded_kv:
                host = forwarded_kv["host"]
        else:
            if "HTTP_X_FORWARDED_PROTO" in wsgi_environment:
                scheme = wsgi_environment.get("HTTP_X_FORWARDED_PROTO")
            if "HTTP_X_FORWARDED_HOST" in wsgi_environment:
                host = wsgi_environment.get("HTTP_X_FORWARDED_HOST")
        return RequestURI(
            scheme,
            host,
            wsgi_environment.get("SERVER_PORT"),
            wsgi_environment.get("PATH_INFO"),
            wsgi_environment.get("QUERY_STRING"))

    @property
    def scheme(self):
        return self._scheme

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def path(self):
        return self._path

    @property
    def query(self):
        return self._query

    def __str__(self):
        return self.scheme + "://" + self.host + ":" + str(self.port) + self.path + "?" + self.query

    def __repr__(self):
        return str(self)