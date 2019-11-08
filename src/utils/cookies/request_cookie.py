

class RequestCookie:

    def __init__(self, name, value):
        self._name = name
        self._value = value

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    def __eq__(self, other_cookie):
        return self._name == other_cookie.name and self._value == other_cookie.value
