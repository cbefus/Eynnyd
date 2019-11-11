from abc import ABC, abstractmethod


class AbstractResponse(ABC):
    """
    The expected interface for a response.

    If you want to build your own response objects it must meet the contract of this class
    """

    @property
    @abstractmethod
    def status(self):
        """
        The status of the response

        :return: An instance of an Eynnyd HTTPStatus object with code and phrase properties
        """
        pass

    @property
    @abstractmethod
    def body(self):
        """
        The body of the response

        :return: An instance of an Eynnyd ResponseBody with type and content properties
        """
        pass

    @property
    @abstractmethod
    def headers(self):
        """
        The headers of the response

        :return: A dictionary of header name to header value
        """
        pass

    @property
    @abstractmethod
    def cookies(self):
        """
        The cookies of the response

        :return: a list of Eynnyd ResponseCookie objects
        """
        pass


