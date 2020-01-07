import logging
from http import HTTPStatus
from eynnyd.response_builder import ResponseBuilder

LOG = logging.getLogger("default_error_handlers")


def default_route_not_found_error_handler(exc, request):
    return ResponseBuilder()\
        .set_status(HTTPStatus.NOT_FOUND)\
        .set_utf8_body(
            "No Route Found for Http Method '{m}' on path '{p}'."
                .format(m=request.http_method, p=request.request_uri))\
        .build()


def default_invalid_cookie_header_error_handler(exc, request):
    LOG.warning(
        "Request attempted with invalid cookie header: {rc}".format(rc=str(request.headers.get("COOKIE"))))
    return ResponseBuilder()\
        .set_status(HTTPStatus.BAD_REQUEST)\
        .set_utf8_body(
            "Invalid cookies sent (Did you forget to URLEncode them?). "
            "Check your formatting against RFC6265 standards.")\
        .build()


def default_internal_server_error_error_handler_only_request(exc, request):
    LOG.exception("Unexpected exception occurred with request {r}.".format(r=request), exc_info=exc)
    return ResponseBuilder()\
        .set_status(HTTPStatus.INTERNAL_SERVER_ERROR)\
        .set_utf8_body("Internal Server Error")\
        .build()


def default_internal_server_error_error_handler(exc, request, response):
    LOG.exception(
        "Unexpected exception occurred with request {q} and response {s}.".format(q=request, s=response), exc_info=exc)
    return ResponseBuilder()\
        .set_status(HTTPStatus.INTERNAL_SERVER_ERROR)\
        .set_utf8_body("Internal Server Error")\
        .build()