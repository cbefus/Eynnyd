
class HTTPStatus:

    def __init__(self, code, phrase, description=""):
        self._code = code
        self._phrase = phrase
        self._description = description

    @property
    def code(self):
        return self._code

    @property
    def phrase(self):
        return self._phrase

    @property
    def description(self):
        return self._description

    @property
    def wsgi_format(self):
        return str(self)

    def __str__(self):
        return "{c} {p}".format(c=self._code, p=self._phrase)

    def __hash__(self):
        return hash(self._code)
