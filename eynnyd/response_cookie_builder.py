import arrow
from optional import Optional

from eynnyd.exceptions import InvalidCookieBuildException
from eynnyd.internal.utils.cookies import rfc
from eynnyd.internal.utils.cookies.response_cookie import ResponseCookie


class ResponseCookieBuilder:
    """
    Response cookies are generally just key-value pairs but can be more complicated.  Using this builder
    allows for simple creation of generic or complex cookies with validation.
    """

    def __init__(self, name, value):
        """
        Constructs an initial ResponseCookieBuilder with common defaults.

        :param name: a valid cookie name (via rfc spec)
        :param value: a valid cookie value (via rfc spec)
        """
        self._name = name
        self._value = value
        self._expires = Optional.empty()
        self._max_age = Optional.empty()
        self._domain = Optional.empty()
        self._path = Optional.empty()
        self._secure = True
        self._http_only = True

    def set_expires(self, expires):
        """
        Sets the cookie to include an expiry date.

        :param expires: a date, parsable by python Arrow
        :return: This builder to allow for fluent design.
        """
        try:
            encoded = arrow.get(expires)
        except arrow.parser.ParserError as e:
            raise InvalidCookieBuildException("Invalid datetime {d}, unable to parse.".format(d=expires), e)
        self._expires = Optional.of(encoded)
        return self

    def set_expires_in_days(self, days_till_expiry):
        """
        Sets the cookie to include an expiry date in days from now.

        :param days_till_expiry: number of days from now to the expiry time.
        :return: This builder to allow for fluent design.
        """
        try:
            encoded = int(days_till_expiry)
        except ValueError as e:
            raise InvalidCookieBuildException("Invalid days {d}".format(d=days_till_expiry), e)
        self._expires = Optional.of(arrow.utcnow().shift(days=encoded))
        return self

    def set_max_age(self, max_age):
        """
        Sets the max age of the cookie.

        :param max_age: an rfc compliant max age
        :return: This builder to allow for fluent design.
        """
        if not bool(rfc.VALID_RFC_MAX_AGE.fullmatch(str(max_age))):
            raise InvalidCookieBuildException("Max Age {m} does not comply with RFC Cookies Specs.".format(m=max_age))
        self._max_age = Optional.of(str(max_age))
        return self

    def set_domain(self, domain):
        """
        Sets the limiting domain for the cookie.

        :param domain: an rfc compliant domain
        :return: This builder to allow for fluent design.
        """
        if not bool(rfc.VALID_RFC_DOMAIN.fullmatch(domain)):
            raise InvalidCookieBuildException("Domain {d} does not comply with RFC Cookie Specs.".format(d=domain))
        self._domain = Optional.of(domain)
        return self

    def set_path(self, path):
        """
        Sets the limiting path for the cookie.

        :param path: an rfc compliant path
        :return: This builder to allow for fluent design.
        """
        if not bool(rfc.VALID_RFC_PATH.fullmatch(path)):
            raise InvalidCookieBuildException("Path {p} does not comply with RFC Cookie Specs.".format(p=path))
        self._path = Optional.of(path)
        return self

    def set_secure(self, secure):
        """
        Sets whether the cookie is secure or not.

        :param secure: a boolean to indicate if we are setting secure or insecure
        :return: This builder to allow for fluent design.
        """
        self._secure = bool(secure)
        return self

    def set_http_only(self, http_only):
        """
        Sets whether the cookie is http only or not.

        :param http_only: a boolean to indicate if we are setting http only or not
        :return: This builder to allow for fluent design.
        """
        self._http_only = bool(http_only)
        return self

    def build(self):
        """
        Validates the name and value and builds the ResponseCookie object.
        :return: a valid ResponseCookie object.
        """
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