from enum import Enum

class DataType(Enum):
    """An enumeration of the allowed data types."""

    string = 'str'
    integer = 'int'
    floating_point = 'float'

    def __str__(self):
        return self.value