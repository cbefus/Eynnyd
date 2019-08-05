
from abc import ABC, abstractmethod


class AbstractResponse(ABC):

    @property
    @abstractmethod
    def status(self):
        pass

    @property
    @abstractmethod
    def body(self):
        pass

    #  TODO: Add byte body and streaming body options

    @property
    @abstractmethod
    def headers(self):
        pass

    @property
    @abstractmethod
    def cookies(self):
        pass

