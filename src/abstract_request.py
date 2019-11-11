from abc import ABC, abstractmethod


class AbstractRequest(ABC):
    """
    The expected interface for a request.

    If you want to build your own request object it needs to meet the requirements set out in this class.
    """

    @property
    @abstractmethod
    def http_method(self):
        """
        The HTTP method used for the request.  This gets matched against the handler routes and must be an exact match.

        :return: a string like: "GET", "PUT", "POST", "DELETE", etc.
        """
        pass

    @property
    @abstractmethod
    def request_uri(self):
        """
        The request uri encapsulates the scheme, host, port, path, and query.

        :return: An Eynnyd RequestURI object with properties for scheme, host, port, path, and query
        """
        pass

    @property
    @abstractmethod
    def forwarded_request_uri(self):
        """
        The request uri but using forwarded info.

        :return: An Eynnyd RequestURI object with properties for scheme, host, port, path, and query
        """
        pass

    @property
    @abstractmethod
    def headers(self):
        """
        The HTTP headers from the request

        :return: A dictionary of header names to header values
        """
        pass

    @property
    @abstractmethod
    def client_ip_address(self):
        """
        The ip address of the remote user

        :return: a string ip address
        """
        pass

    @property
    @abstractmethod
    def cookies(self):
        """
        The cookies from the request

        :return: A dictionary of cookie name to Eynnyd Cookie objects with name and value properties
        """
        pass

    @property
    @abstractmethod
    def query_parameters(self):
        """
        The query part of the request

        :return: a dictionary of parameter names to lists of parameter values
        """
        pass

    @property
    @abstractmethod
    def path_parameters(self):
        """
        The parameters set in the path of request matching against pattern matching path parameters.

        :return: A dictionary of path variable name to request path value.
        """
        pass

    @property
    @abstractmethod
    def byte_body(self):
        """
        The raw request body

        :return:  The body of the request left encoded as bytes.
        """
        pass

    @property
    @abstractmethod
    def utf8_body(self):
        """
        The encoded request body

        :return: The request body after being encoded to utf-8
        """
        pass


