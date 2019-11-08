from abc import ABC, abstractmethod


class AbstractResponseBody(ABC):

    @abstractmethod
    def get_body(self):
        pass