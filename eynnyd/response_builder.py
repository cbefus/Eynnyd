import inspect
from http import HTTPStatus

from eynnyd.exceptions import SettingNonTypedStatusWithContentTypeException, SettingNonBodyStatusWithBodyException, \
    SettingBodyWithNonBodyStatusException, InvalidBodyTypeException, InvalidHeaderException, \
    SettingContentTypeWithNonTypedStatusException, InvalidResponseCookieException
from eynnyd.internal.response import Response
from eynnyd.internal.response_body import ResponseBody
from eynnyd.internal.response_body_type import ResponseBodyType
from eynnyd.internal.utils.cookies.response_cookie import ResponseCookie
from eynnyd.response_cookie_builder import ResponseCookieBuilder
from eynnyd.internal.utils.http_status_factory import HTTPStatusFactory
from eynnyd.internal.utils.http_status_groups import NON_TYPED_STATUSES, NON_BODY_STATUSES


class ResponseBuilder:
    """
    A builder allowing for the easy and validated building of a Response.
    """

    def __init__(self):
        self._status = HTTPStatusFactory.create(HTTPStatus.OK)
        self._body = ResponseBody.empty_response()
        self._headers = {}
        self._cookies = []

    def set_status(self, status):
        """
        Sets the HTTP status of the response. Raises if the type conflicts with other attributes of the response.

        :param status: a value indicating response status (can be an int, http.HTTPStatus or Eynnyd HttpStatus)
        :return: This builder to allow for fluent design.
        """
        encoded_status = HTTPStatusFactory.create(status)
        if encoded_status.code in NON_TYPED_STATUSES and "content-type" in self._headers:
            raise SettingNonTypedStatusWithContentTypeException(
                "Cannot set status {s} when content-type header exists.".format(s=status))
        if encoded_status.code in NON_BODY_STATUSES and self._body.type != ResponseBodyType.EMPTY:
            raise SettingNonBodyStatusWithBodyException(
                "Cannot set status {s} on response with body".format(s=status))
        self._status = encoded_status
        return self

    def set_utf8_body(self, body):
        """
        Sets a utf8 body on the request (overwriting any other set body).  Raises if setting the body conflicts
        with the status.  Sets a content-length header if one has not already been set.

        :param body: The utf-8 encoded body
        :return: This builder to allow for fluent design.
        """
        if self._status.code in NON_BODY_STATUSES:
            raise SettingBodyWithNonBodyStatusException(
                "Cannot set a body on response with status {s}".format(s=self._status))
        encoded_body = body.encode("utf-8")
        if len(body) != len(encoded_body):
            raise InvalidBodyTypeException("Body must be UTF8 to set via set_utf8_body method.")
        if "content-length" not in self._headers:
            self._headers["content-length"] = str(len(encoded_body))
        self._body = ResponseBody(ResponseBodyType.UTF8, encoded_body)
        return self

    def set_byte_body(self, body):
        """
        Sets a byte body on the request (overwriting any other set body).  Raises if setting the body conflicts
        with the status.  Sets a content-length header if one has not already been set.

        :param body: The bytes encoded body
        :return: This builder to allow for fluent design.
        """
        if self._status.code in NON_BODY_STATUSES:
            raise SettingBodyWithNonBodyStatusException(
                "Cannot set a body on response with status {s}".format(s=self._status))
        if not isinstance(body, bytes):
            raise InvalidBodyTypeException("Body must be byte encoded to set via set_byte_body mothod.")
        if "content-length" not in self._headers:
            self._headers["content-length"] = str(len(body))
        self._body = ResponseBody(ResponseBodyType.BYTE, body)
        return self

    def set_stream_body(self, body):
        """
        Sets a streaming body on the request (overwriting any other set body).  Raises if setting the body conflicts
        with the status.

        :param body: A streamable object with a read method taking 1 parameter (and an optional close method)
        :return: This builder to allow for fluent design.
        """
        if self._status.code in NON_BODY_STATUSES:
            raise SettingBodyWithNonBodyStatusException(
                "Cannot set a body on response with status {s}".format(s=self._status))
        if not hasattr(body, "read"):
            raise InvalidBodyTypeException("Streamable body must have a read method.")

        if 1 != len(inspect.signature(body.read).parameters):
            raise InvalidBodyTypeException("Streamable body read method must take a block size parameter")

        self._body = ResponseBody(ResponseBodyType.STREAM, body)
        return self

    def set_iterable_body(self, body):
        """
        Sets an iterable body on the request (overwriting any other set body).  Raises if setting the body conflicts
        with the status.

        For simple strings you should use the utf-8 body as using this would be highly inefficient.

        :param body: The iterable body
        :return: This builder to allow for fluent design.
        """
        if self._status.code in NON_BODY_STATUSES:
            raise SettingBodyWithNonBodyStatusException(
                "Cannot set a body on response with status {s}".format(s=self._status))
        try:
            iter(body)
        except TypeError as e:
            raise InvalidBodyTypeException("Iterable bodies must be iterable", e)
        self._body = ResponseBody(ResponseBodyType.ITERABLE, body)
        return self

    def unset_body(self):
        """
        Unsets the body on the request.

        :return: This builder to allow for fluent design.
        """
        self._body = ResponseBody.empty_response()
        return self

    def set_headers(self, headers_by_name):
        """
        Sets the headers on the response (deleting/overwriting all current headers).

        Raises if this method is attempted to be used to set cookies.  Use the set_cookies/add_cookie
        methods for that.

        :param headers_by_name: a dictionary of header values keyed by name
        :return: This builder to allow for fluent design.
        """
        self._headers = {}
        for name, value in headers_by_name.items():
            self.add_header(name, value)
        return self

    def add_header(self, name, value):
        """
        Adds a single header to the response.

        Raises if this method is attempted to be used to set cookies.  Use the set_cookies/add_cookie
        methods for that.

        :param name: the name to use for the header
        :param value: the value to store in the header
        :return: This builder to allow for fluent design.
        """
        ascii_lowered_name = str(name).lower()
        if ascii_lowered_name == 'set-cookie':
            raise InvalidHeaderException("Cannot set header with {n} as name".format(n=name))
        if self._status.code in NON_TYPED_STATUSES and ascii_lowered_name == 'content-type':
            raise SettingContentTypeWithNonTypedStatusException(
                "Cannot set content-type header on response with status {s}".format(s=self._status))
        self._headers[ascii_lowered_name] = str(value)
        return self

    def remove_header(self, name):
        """
        Removes a header from the response by name.

        :param name: The name for the header to remove.
        :return: This builder to allow for fluent design.
        """
        ascii_lowered_name = str(name).lower()
        if ascii_lowered_name in self._headers:
            self._headers.pop(ascii_lowered_name)
        return self

    def set_cookies(self, cookies):
        """
        Sets all the cookies on the response (deleting/overwriting any previously set).

        :param cookies: An iterable of Eynnyd ResponseCookie objects.
        :return: This builder to allow for fluent design.
        """
        for cookie in cookies:
            if not isinstance(cookie, ResponseCookie):
                raise InvalidResponseCookieException("Cookie {c} is not a valid response cookie.".format(c=str(cookie)))
        self._cookies = cookies
        return self

    def add_cookie(self, cookie):
        """
        Adds a single cookie to the response.

        :param cookie: an Eynnyd ResponseCookie object.
        :return: This builder to allow for fluent design.
        """
        if not isinstance(cookie, ResponseCookie):
            raise InvalidResponseCookieException("Cookie {c} is not a valid response cookie.".format(c=str(cookie)))
        self._cookies.append(cookie)
        return self

    def add_basic_cookie(self, name, value):
        """
        Adds a simple cookie to the response (allowing the skipping of using Eynnyd specific objects).

        :param name: An rfc valid name for the cookie.
        :param value: An rfc valid value for the cookie.
        :return: This builder to allow for fluent design.
        """
        self._cookies.append(ResponseCookieBuilder(name, value).build())
        return self

    def remove_cookie(self, name):
        """
        Removes a cookie from the response by name.

        :param name: the name of the cookie to remove.
        :return: This builder to allow for fluent design.
        """
        self._cookies = list(filter(lambda cookie: cookie.name != name, self._cookies))
        return self

    def build(self):
        """
        :return: A response ready for returning from the webapp.
        """
        return Response(
            self._status,
            self._body,
            self._headers,
            self._cookies)