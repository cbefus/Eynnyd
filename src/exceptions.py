

class EynnydWebappBuildException(Exception):
    pass


class ExceptionHandlingRegisterException(Exception):
    pass


class NoGenericExceptionHandlerRegistered(Exception):
    pass


class ResponseBuildException(Exception):
    pass


class HandlerNotFoundException(Exception):
    pass


class DuplicateHandlerRoutesException(Exception):
    pass


class RouteNotFoundException(Exception):
    pass


class RouteBuildException(Exception):
    pass


class InvalidHTTPStatusException(Exception):
    pass


class SettingNonTypedStatusWithContentTypeException(Exception):
    pass


class SettingContentTypeWithNonTypedStatusException(Exception):
    pass


class SettingBodyWithNonBodyStatusException(Exception):
    pass


class SettingNonBodyStatusWithBodyException(Exception):
    pass


class InvalidURIException(Exception):
    pass


class InvalidCookieBuildException(Exception):
    pass


class InvalidCookieHeaderException(Exception):
    pass


class InvalidHeaderException(Exception):
    pass


class InvalidBodyTypeException(Exception):
    pass


class UnknownResponseBodyTypeException(Exception):
    pass


class RequestInterceptorReturnedNonRequestException(Exception):
    pass


class HandlerReturnedNonResponseException(Exception):
    pass


class ResponseInterceptorReturnedNonResponseException(Exception):
    pass


class NonCallableInterceptor(Exception):
    pass


class NonCallableHandler(Exception):
    pass


class CallbackIncorrectNumberOfParametersException(Exception):
    pass


class NonCallableExceptionHandlerException(Exception):
    pass


class InvalidResponseCookieException(Exception):
    pass


class ExecutionPlanBuildException(Exception):
    pass
