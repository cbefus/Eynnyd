from unittest import TestCase
from http import HTTPStatus as HTTPLibStatus

from eynnyd.exceptions import InvalidHTTPStatusException
from eynnyd.internal.utils.http_status import HTTPStatus
from eynnyd.internal.utils.http_status_factory import HTTPStatusFactory

class TestHTTPStatusFactory(TestCase):

    def test_build_from_eynnyd_http_status(self):
        status = HTTPStatus(200, "ok")
        self._assertSameStatus(status, HTTPStatusFactory.create(status))

    def test_build_from_http_lib_status(self):
        self._assertSameStatus(HTTPStatus(200, "OK"), HTTPStatusFactory.create(HTTPLibStatus.OK))

    def test_build_from_number(self):
        self._assertSameStatus(HTTPStatus(200, "OK"), HTTPStatusFactory.create(200))

    def test_build_from_custom(self):
        self._assertSameStatus(HTTPStatus(602, "Custom Status"), HTTPStatusFactory.create(602))

    def test_raises_on_invalid_type(self):
        with self.assertRaises(InvalidHTTPStatusException):
            HTTPStatusFactory.create("OK")

    def _assertSameStatus(self, expected, actual):
        self.assertEqual(expected.code, actual.code)
        self.assertEqual(expected.phrase, actual.phrase)
        self.assertEqual(expected.description, actual.description)



