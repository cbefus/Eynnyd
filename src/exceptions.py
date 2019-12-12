

class EynnydWebappBuildException(Exception):
    """
    Raised if there is a problem with the configured webapp when it attempts to build.
    """
    pass


class ErrorHandlingBuilderException(Exception):
    """
    Raised when there is a problem with adding an error handler.
    """
    pass


class NoGenericErrorHandlerException(Exception):
    """
    Raised when attempting to handle an exception and there are no configured handlers (even the base Exception).
    This should not happen.
    """
    pass


class HandlerNotFoundException(Exception):
    """
    This is raised when a handler is not found for a request.  Note that this is caught and rethrown as a more
    generic RouteNotFoundException which is what is used for retuning 404 responses.
    """
    pass


class DuplicateHandlerRoutesException(Exception):
    """
    Raised when trying to add a handler to the routes which is already registered for that method/path pair. Note
    this is caught and rethrown as a more generic RouteBuildException.
    """
    pass


class RouteNotFoundException(Exception):
    """
    Raised when no route could be found for a request. Indicates a 404.
    """
    pass


class RouteBuildException(Exception):
    """
    Raised when there is a problem with route building.
    """
    pass


class InvalidHTTPStatusException(Exception):
    """
    Raised when the status given to a response cannot be translated into a recognizable format.
    """
    pass


class SettingNonTypedStatusWithContentTypeException(Exception):
    """
    Raised when a response has a content type but trying to set a non content type status.
    """
    pass


class SettingContentTypeWithNonTypedStatusException(Exception):
    """
    Raised when a response has a non content type status but trying to set a content-type.
    """
    pass


class SettingBodyWithNonBodyStatusException(Exception):
    """
    Raised when a response has a non body type status but trying to set a body.
    """
    pass


class SettingNonBodyStatusWithBodyException(Exception):
    """
    Raised when a response has a body but trying to set a non body status.
    """
    pass


class InvalidURIException(Exception):
    """
    Raised when a uri (for example the path given to a route) is badly formatted.
    """
    pass


class InvalidCookieBuildException(Exception):
    """
    Raised when attempting to build a cookie with bad values.
    """
    pass


class InvalidCookieHeaderException(Exception):
    """
    Raised when a request cookie is not rfc compliant (Ideally, should not happen).
    """
    pass


class InvalidHeaderException(Exception):
    """
    Raised when a response header uses invalid characters.
    """
    pass


class InvalidBodyTypeException(Exception):
    """
    Raised when a body being set on a response is invalid (ex. setting a utf-8 body using the set_byte_body method).
    """
    pass


class UnknownResponseBodyTypeException(Exception):
    """
    Raised when a body is set on the response with an unknown type (should not happen).
    """
    pass


class RequestInterceptorReturnedNonRequestException(Exception):
    """
    Raised when a request interceptor does not return a valid request object.
    """
    pass


class HandlerReturnedNonResponseException(Exception):
    """
    Raised when a handler does not return a valid response object.
    """
    pass


class ResponseInterceptorReturnedNonResponseException(Exception):
    """
    Raised when a response interceptor does not return a valid response object.
    """
    pass


class NonCallableInterceptor(Exception):
    """
    Raised when a interceptor is registered without being a callable.
    """
    pass


class NonCallableHandler(Exception):
    """
    Raised when a handler is registered without being a callable.
    """
    pass


class CallbackIncorrectNumberOfParametersException(Exception):
    """
    Raised when a callback doesn't match the correct number of parameters.
    """
    pass


class NonCallableExceptionHandlerException(Exception):
    """
    Raised when an exception handler is registered but is not a callable.
    """
    pass


class InvalidResponseCookieException(Exception):
    """
    Raised when a response cookie is of a non rfc compliant format.
    """
    pass


class ExecutionPlanBuildException(Exception):
    """
    Raised when an execution plan is finished but cannot build. (should not happen)
    """
    pass
