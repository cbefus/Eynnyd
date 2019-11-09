from abc import ABC, abstractmethod


class AbstractRequest(ABC):

    @property
    @abstractmethod
    def http_method(self):
        pass

    @property
    @abstractmethod
    def request_uri(self):
        pass

    @property
    @abstractmethod
    def forwarded_request_uri(self):
        pass

    @property
    @abstractmethod
    def headers(self):
        pass

    @property
    @abstractmethod
    def client_ip_address(self):
        pass

    @property
    @abstractmethod
    def cookies(self):
        pass

    @property
    @abstractmethod
    def query_parameters(self):
        pass

    @property
    @abstractmethod
    def path_parameters(self):
        pass

    @property
    @abstractmethod
    def byte_body(self):
        pass

    @property
    @abstractmethod
    def utf8_body(self):
        pass


