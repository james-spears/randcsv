import string
from math import nan
from random import randint, random, choice

from . import data_type as dt

def generate_integer(num_of_digits):
    """Generates a random integer of arbitrary size.

    :param num_of_digits: number of digits
    :type num_of_digits: int
    :return: random integer
    :rtype: number
    """
    if num_of_digits <= 0:
        raise ValueError("number of digits must be positive")

    range_start = 10**(num_of_digits-1)
    range_end = (10**num_of_digits)-1
    return randint(range_start, range_end)


def generate_float(num_of_decimal_places):
    """Generates a random float of arbitrary size.

    :param num_of_decimal_places: number of decimal places
    :type num_of_decimal_places: int
    :return: random float
    :rtype: float
    """
    if num_of_decimal_places <= 0:
        raise ValueError("number of decimal places must be positive")

    float_string_format = f"{{:.{num_of_decimal_places - 2}f}}"
    return float_string_format.format(random())


def generate_string(num_of_chars):
    """Generates a random string of arbitrary size.

    :param num_of_chars: number of characters
    :type num_of_chars: int
    :return: random string
    :rtype: str
    """
    if num_of_chars <= 0:
        raise ValueError("number of characters must be positive")

    letters = string.ascii_letters
    return ''.join(choice(letters) for _ in range(num_of_chars))


def generator_factory(data_type):
    """Factory function, returns the result of correct value generator.

    :param data_type: data type of value
    :type data_type: str
    :raises ValueError: Data type must be one of: str, int, float.
    :return: generator function
    :rtype: function
    """
    if data_type == dt.DataType.string.value:
        return generate_string
    elif data_type == dt.DataType.floating_point.value:
        return generate_float
    elif data_type == dt.DataType.integer.value:
        return generate_integer
    else:
        raise ValueError(
            "data type must be one of: str, int, float"
        )


def generate_value(all_value_types_sorted, data_types, value_length):
    """Generic value generator.

    :param all_value_types_sorted: list of tuples containing value types sorted by frequency
    :type all_value_types_sorted: List[Tuple]
    :param data_types: list of the desired sata types
    :type data_types: List[String]
    :param value_length: value length (implementation depends on data type)
    :type value_length: int
    :raises ValueError: Value must be either NaN, "empty", or a valid data type (regular value).
    :return: random value
    :rtype: Union[String, Number, Float]
    """
    generate_number = random()
    left_boundary = 0
    for item in all_value_types_sorted:
        right_boundary = item[1]
        if left_boundary <= generate_number < right_boundary:
            if item[0] == 0:
                # this is a regular number, so randomly select one
                num_of_data_types = len(data_types)
                selected_data_type = randint(0, num_of_data_types - 1)
                generator = generator_factory(data_types[selected_data_type])
                return generator(value_length)
            elif item[0] == 1:
                # this is a NaN value
                return nan
            elif item[0] == 2:
                # this is a NaN value
                return None
            else:
                # this must be an empty value
                raise ValueError(
                    'value must be either NaN, "empty", or a valid data type (regular value)'
                )
        else:
            left_boundary = right_boundary