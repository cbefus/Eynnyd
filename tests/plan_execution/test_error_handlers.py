import unittest

from eynnyd.internal.plan_execution.error_handlers import ErrorHandlers
from eynnyd.exceptions import NoGenericErrorHandlerException


class TestErrorHandlers(unittest.TestCase):

    def test_no_matching_pre_error_handler_raises(self):

        class CustomTestException(Exception):
            pass

        class CustomRegisterException(Exception):
            pass

        class SpyFakeExceptionHandler:
            def __init__(self):
                self._call_count = 0

            @property
            def call_count(self):
                return self._call_count

            def test_fake_handler(self, exc, request):
                self._call_count += 1

        fake_handler = SpyFakeExceptionHandler()
        error_handlers = ErrorHandlers([], [(CustomRegisterException, fake_handler.test_fake_handler)])
        with self.assertRaises(NoGenericErrorHandlerException):
            error_handlers.handle_pre_response_error(CustomTestException(), None)
        self.assertEqual(0, fake_handler.call_count)

    def test_no_matching_post_error_handler_raises(self):

        class CustomTestException(Exception):
            pass

        class CustomRegisterException(Exception):
            pass

        class SpyFakeExceptionHandler:
            def __init__(self):
                self._call_count = 0

            @property
            def call_count(self):
                return self._call_count

            def test_fake_handler(self, exc, request, response):
                self._call_count += 1

        fake_handler = SpyFakeExceptionHandler()
        error_handlers = ErrorHandlers([], [(CustomRegisterException, fake_handler.test_fake_handler)])
        with self.assertRaises(NoGenericErrorHandlerException):
            error_handlers.handle_post_response_error(CustomTestException(), None, None)
        self.assertEqual(0, fake_handler.call_count)

    def test_matching_pre_error_handler_is_called(self):

        class CustomRegisterException(Exception):
            pass

        class SpyFakeExceptionHandler:
            def __init__(self):
                self._pre_call_count = 0
                self._post_call_count = 0

            @property
            def pre_call_count(self):
                return self._pre_call_count

            @property
            def post_call_count(self):
                return self._post_call_count

            def test_pre_fake_handler(self, exc, request):
                self._pre_call_count += 1

            def test_post_fake_handler(self, exc, request, response):
                self._post_call_count += 1

        fake_handler = SpyFakeExceptionHandler()
        error_handlers = \
            ErrorHandlers(
                [(CustomRegisterException, fake_handler.test_pre_fake_handler)],
                [(CustomRegisterException, fake_handler.test_post_fake_handler)])
        error_handlers.handle_pre_response_error(CustomRegisterException(), None)
        self.assertEqual(1, fake_handler.pre_call_count)
        self.assertEqual(0, fake_handler.post_call_count)

    def test_matching_post_error_handler_is_called(self):

        class CustomRegisterException(Exception):
            pass

        class SpyFakeExceptionHandler:
            def __init__(self):
                self._pre_call_count = 0
                self._post_call_count = 0

            @property
            def pre_call_count(self):
                return self._pre_call_count

            @property
            def post_call_count(self):
                return self._post_call_count

            def test_pre_fake_handler(self, exc, request):
                self._pre_call_count += 1

            def test_post_fake_handler(self, exc, request, response):
                self._post_call_count += 1

        fake_handler = SpyFakeExceptionHandler()
        error_handlers = \
            ErrorHandlers(
                [(CustomRegisterException, fake_handler.test_pre_fake_handler)],
                [(CustomRegisterException, fake_handler.test_post_fake_handler)])
        error_handlers.handle_post_response_error(CustomRegisterException(), None, None)
        self.assertEqual(0, fake_handler.pre_call_count)
        self.assertEqual(1, fake_handler.post_call_count)
