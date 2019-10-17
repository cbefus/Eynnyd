from src.wsgi.wsgi_response import WSGIResponse
from src.utils.cookies.header_converter import CookieHeaderConverter


class WSGIResponseAdapter:

    @staticmethod
    def adapt(response):
        headers = [(str(k), str(v)) for k, v in response.headers.items()]

        for cookie in response.cookies:
            headers.append(CookieHeaderConverter.from_cookie(cookie))

        return WSGIResponse(
            response.status.wsgi_format,
            headers,
            [response.body.encode("utf-8")])
