

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

    def __eq__(self, other):
        return \
            self.name == other.name and \
            self.value == other.value and \
            self.expires == other.expires and \
            self.max_age == other.max_age and \
            self.domain == other.domain and \
            self.path == other.path and \
            self.secure == other.secure and \
            self.http_only == other.http_only

