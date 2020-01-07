from http import HTTPStatus as HTTPLibHTTPStatus

from eynnyd.exceptions import InvalidHTTPStatusException
from eynnyd.internal.utils.http_status import HTTPStatus


class HTTPStatusFactory:

    _STATUS_BY_VALUE = {
        100: HTTPLibHTTPStatus.CONTINUE,
        101: HTTPLibHTTPStatus.SWITCHING_PROTOCOLS,
        102: HTTPLibHTTPStatus.PROCESSING,
        200: HTTPLibHTTPStatus.OK,
        201: HTTPLibHTTPStatus.CREATED,
        202: HTTPLibHTTPStatus.ACCEPTED,
        203: HTTPLibHTTPStatus.NON_AUTHORITATIVE_INFORMATION,
        204: HTTPLibHTTPStatus.NO_CONTENT,
        205: HTTPLibHTTPStatus.RESET_CONTENT,
        207: HTTPLibHTTPStatus.PARTIAL_CONTENT,
        208: HTTPLibHTTPStatus.ALREADY_REPORTED,
        226: HTTPLibHTTPStatus.IM_USED,
        300: HTTPLibHTTPStatus.MULTIPLE_CHOICES,
        301: HTTPLibHTTPStatus.MOVED_PERMANENTLY,
        302: HTTPLibHTTPStatus.FOUND,
        303: HTTPLibHTTPStatus.SEE_OTHER,
        304: HTTPLibHTTPStatus.NOT_MODIFIED,
        305: HTTPLibHTTPStatus.USE_PROXY,
        307: HTTPLibHTTPStatus.TEMPORARY_REDIRECT,
        308: HTTPLibHTTPStatus.PERMANENT_REDIRECT,
        400: HTTPLibHTTPStatus.BAD_REQUEST,
        401: HTTPLibHTTPStatus.UNAUTHORIZED,
        402: HTTPLibHTTPStatus.PAYMENT_REQUIRED,
        403: HTTPLibHTTPStatus.FORBIDDEN,
        404: HTTPLibHTTPStatus.NOT_FOUND,
        405: HTTPLibHTTPStatus.METHOD_NOT_ALLOWED,
        406: HTTPLibHTTPStatus.NOT_ACCEPTABLE,
        407: HTTPLibHTTPStatus.PROXY_AUTHENTICATION_REQUIRED,
        408: HTTPLibHTTPStatus.REQUEST_TIMEOUT,
        409: HTTPLibHTTPStatus.CONFLICT,
        410: HTTPLibHTTPStatus.GONE,
        411: HTTPLibHTTPStatus.LENGTH_REQUIRED,
        412: HTTPLibHTTPStatus.PRECONDITION_FAILED,
        413: HTTPLibHTTPStatus.REQUEST_ENTITY_TOO_LARGE,
        414: HTTPLibHTTPStatus.REQUEST_URI_TOO_LONG,
        415: HTTPLibHTTPStatus.UNSUPPORTED_MEDIA_TYPE,
        416: HTTPLibHTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE,
        417: HTTPLibHTTPStatus.EXPECTATION_FAILED,
        422: HTTPLibHTTPStatus.UNPROCESSABLE_ENTITY,
        423: HTTPLibHTTPStatus.LOCKED,
        424: HTTPLibHTTPStatus.FAILED_DEPENDENCY,
        426: HTTPLibHTTPStatus.UPGRADE_REQUIRED,
        428: HTTPLibHTTPStatus.PRECONDITION_REQUIRED,
        429: HTTPLibHTTPStatus.TOO_MANY_REQUESTS,
        431: HTTPLibHTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE,
        500: HTTPLibHTTPStatus.INTERNAL_SERVER_ERROR,
        501: HTTPLibHTTPStatus.NOT_IMPLEMENTED,
        502: HTTPLibHTTPStatus.BAD_GATEWAY,
        503: HTTPLibHTTPStatus.SERVICE_UNAVAILABLE,
        504: HTTPLibHTTPStatus.GATEWAY_TIMEOUT,
        505: HTTPLibHTTPStatus.HTTP_VERSION_NOT_SUPPORTED,
        506: HTTPLibHTTPStatus.VARIANT_ALSO_NEGOTIATES,
        507: HTTPLibHTTPStatus.INSUFFICIENT_STORAGE,
        508: HTTPLibHTTPStatus.LOOP_DETECTED,
        510: HTTPLibHTTPStatus.NOT_EXTENDED,
        511: HTTPLibHTTPStatus.NETWORK_AUTHENTICATION_REQUIRED
    }

    @staticmethod
    def create(status):
        if isinstance(status, HTTPStatus):
            return status

        if isinstance(status, HTTPLibHTTPStatus):
            return HTTPStatus(status.value, status.name)

        if status in HTTPStatusFactory._STATUS_BY_VALUE:
            lib_status = HTTPStatusFactory._STATUS_BY_VALUE.get(status)
            return HTTPStatus(lib_status.value, lib_status.name)

        if isinstance(status, int):
            return HTTPStatus(status, "Custom Status")

        raise InvalidHTTPStatusException("No status could be created from value: {s}".format(s=status))