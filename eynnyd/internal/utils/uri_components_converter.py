from eynnyd.exceptions import InvalidURIException


class URIComponentsConverter:

    @staticmethod
    def from_uri(uri_path):
        if "//" in uri_path:
            raise InvalidURIException("URI '{u}' has empty components".format(u=uri_path))

        if not uri_path.startswith("/"):
            raise InvalidURIException("URI '{u}' does not start with a /".format(u=uri_path))

        if len(uri_path) == 1:
            return []

        adjusted_uri = uri_path[1:]
        if uri_path.endswith("/"):
            adjusted_uri = adjusted_uri[:-1]
        return adjusted_uri.split("/")

