from enum import Enum


class ResponseBodyType(Enum):
    EMPTY = 1
    UTF8 = 2
    BYTE = 3
    STREAM = 4
    ITERABLE = 5