from eynnyd.exceptions import InvalidCookieHeaderException
from eynnyd.internal.utils.cookies.request_cookie import RequestCookie
from eynnyd.internal.utils.cookies import rfc


class CookieHeaderConverter:

    @staticmethod
    def from_header(header):
        cookies = {}
        for token in header.split(";"):
            name, value = token.split("=")

            name = name.strip()
            if not name or not rfc.VALID_RFC_COOKIE_NAME.fullmatch(name):
                raise InvalidCookieHeaderException("Cookie named: '{n}' doesn't comply with RFC specs.".format(n=name))

            value = value.strip()
            if not value or not rfc.VALID_RFC_COOKIE_VALUE.fullmatch(value):
                raise InvalidCookieHeaderException("Cookie value: '{v}' doesn't comply with RFC specs.".format(v=value))

            if name not in cookies:
                cookies[name] = []
            cookies[name].append(RequestCookie(name, value))
        return cookies

    @staticmethod
    def from_cookie(cookie):
        header = "{n}={v}".format(n=str(cookie.name), v=str(cookie.value))
        header += cookie.expires.map(CookieHeaderConverter._format_expires).get_or_default("")
        header += cookie.max_age.map(CookieHeaderConverter._format_max_age).get_or_default("")
        header += cookie.domain.map(CookieHeaderConverter._format_domain).get_or_default("")
        header += cookie.path.map(CookieHeaderConverter._format_path).get_or_default("")
        header += CookieHeaderConverter._format_secure(cookie.secure)
        header += CookieHeaderConverter._format_http_only(cookie.http_only)
        return ("Set-Cookie", header)

    @staticmethod
    def _format_expires(expires):
        return "; Expires="+expires.format("ddd, DD MMM YYYY HH:MM:SS")+" GMT"

    @staticmethod
    def _format_max_age(max_age):
        return "; Max-Age="+str(max_age)

    @staticmethod
    def _format_domain(domain):
        return "; Domain="+str(domain)

    @staticmethod
    def _format_path(path):
        return "; Path="+str(path)

    @staticmethod
    def _format_secure(secure):
        return "; Secure" if secure else ""

    @staticmethod
    def _format_http_only(http_only):
        return "; HttpOnly" if http_only else ""


