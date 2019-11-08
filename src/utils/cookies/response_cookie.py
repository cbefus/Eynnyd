import arrow
from arrow.parser import ParserError
from optional import Optional

from src.exceptions import InvalidCookieBuildException
from src.utils.cookies import rfc


class ResponseCookie:

    def __init__(self, name, value, expires, max_age, domain, path, secure, http_only):
        self._name = name
        self._value = value
        self._expires = expires
        self._max_age = max_age
        self._domain = domain
        self._path = path
        self._secure = secure
        self._http_only = http_only

    @staticmethod
    def build_basic(name, value):
        return ResponseCookieBuilder(name, value).build()

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @property
    def expires(self):
        return self._expires

    @property
    def max_age(self):
        return self._max_age

    @property
    def domain(self):
        return self._domain

    @property
    def path(self):
        return self._path

    @property
    def secure(self):
        return self._secure

    @property
    def http_only(self):
        return self._http_only


class ResponseCookieBuilder:

    def __init__(self, name, value):
        self._name = name
        self._value = value
        self._expires = Optional.empty()
        self._max_age = Optional.empty()
        self._domain = Optional.empty()
        self._path = Optional.empty()
        self._secure = True
        self._http_only = True

    def set_expires(self, expires):
        try:
            encoded = arrow.get(expires)
        except arrow.parser.ParserError as e:
            raise InvalidCookieBuildException("Invalid datetime {d}, unable to parse.".format(d=expires), e)
        self._expires = Optional.of(encoded)
        return self

    def set_expires_in_days(self, days_till_expiry):
        try:
            encoded = int(days_till_expiry)
        except ValueError as e:
            raise InvalidCookieBuildException("Invalid days {d}".format(d=days_till_expiry), e)
        self._expires = Optional.of(arrow.utcnow().shift(days=encoded))
        return self

    def set_max_age(self, max_age):
        if not bool(rfc.VALID_RFC_MAX_AGE.fullmatch(str(max_age))):
            raise InvalidCookieBuildException("Max Age {m} does not comply with RFC Cookies Specs.".format(m=max_age))
        self._max_age = Optional.of(str(max_age))
        return self

    def set_domain(self, domain):
        if not bool(rfc.VALID_RFC_DOMAIN.fullmatch(domain)):
            raise InvalidCookieBuildException("Domain {d} does not comply with RFC Cookie Specs.".format(d=domain))
        self._domain = Optional.of(domain)
        return self

    def set_path(self, path):
        if not bool(rfc.VALID_RFC_PATH.fullmatch(path)):
            raise InvalidCookieBuildException("Path {p} does not comply with RFC Cookie Specs.".format(p=path))
        self._path = Optional.of(path)
        return self

    def set_secure(self, secure):
        self._secure = bool(secure)
        return self

    def set_http_only(self, http_only):
        self._http_only = bool(http_only)
        return self

    def build(self):
        if not bool(rfc.VALID_RFC_COOKIE_NAME.fullmatch(self._name)):
            raise InvalidCookieBuildException("Cookie Name {n} does not comply with RFC Cookie Specs.".format(n=self._name))

        if not bool(rfc.VALID_RFC_COOKIE_VALUE.fullmatch((self._value))):
            raise InvalidCookieBuildException(
                "Cookie Value {v} does not comply with RFC Cookie Specs.".format(v=self._value))

        return ResponseCookie(
            self._name,
            self._value,
            self._expires,
            self._max_age,
            self._domain,
            self._path,
            self._secure,
            self._http_only)


