import csv
import argparse
import string
from enum import Enum
from random import randint, random, choice
from operator import itemgetter
from math import nan


class DataType(Enum):
    """An enumeration of the allowed data types."""

    string = 'str'
    integer = 'int'
    floating_point = 'float'

    def __str__(self):
        return self.value


def generate_integer(num_of_digits):
    """Generates a random integer of arbitrary size.

    :param num_of_digits: number of digits
    :type num_of_digits: int
    :return: random integer
    :rtype: number
    """
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
    float_string_format = f"{{:.{num_of_decimal_places}f}}"
    return float_string_format.format(random())


def generate_string(num_of_chars):
    """Generates a random string of arbitrary size.

    :param num_of_chars: number of characters
    :type num_of_chars: int
    :return: random string
    :rtype: str
    """
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
    if data_type == DataType.string.value:
        return generate_string
    elif data_type == DataType.floating_point.value:
        return generate_float
    elif data_type == DataType.integer.value:
        return generate_integer
    else:
        raise ValueError(
            "Data type must be one of: str, int, float."
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
                    'Value must be either NaN, "empty", or a valid data type (regular value).'
                )
        else:
            left_boundary = right_boundary


def mkcsv(argv):
    if argv.nan_values < .0 or argv.nan_values > 1.:
        raise ValueError("--nan-values <nan-values> must be [0, 1]")
    if argv.empty_values < .0 or argv.empty_values > 1.:
        raise ValueError("--empty-values <empty-values> must be [0, 1]")
    if argv.nan_values + argv.empty_values > 1.:
        raise ValueError("--empty-values <empty-values> + --nan-values <nan-values> must be [0, 1]")

    regular_values = 1 - argv.nan_values - argv.empty_values
    all_value_types = [(0, regular_values), (1, argv.nan_values), (2, argv.empty_values)]
    all_value_types_sorted = sorted(all_value_types, key=itemgetter(1))

    with open(f'{argv.output}.csv', 'w+', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in range(argv.rows):
            if row == 0 and argv.title:
                csvwriter.writerow([str(col) for col in range(argv.cols)])
            else:
                if argv.index:
                    csvwriter.writerow([str(row)] + [generate_value(all_value_types_sorted, argv.data_types, argv.value_length)
                                                     for _ in range(1, argv.cols)])
                else:
                    csvwriter.writerow(
                        [generate_value(all_value_types_sorted, argv.data_types, argv.value_length) for _ in range(argv.cols)])

    print(f'mkcsv generated file: {argv.output}.csv')


if __name__ == '__main__':
    # Create the parser.
    mkcsv_parser = argparse.ArgumentParser(
        description="Generate random CSVs."
    )

    # Add arguments
    mkcsv_parser.add_argument(
        '--rows',
        '-m',
        action='store',
        type=int,
        required=True,
        help='Number of rows the desired CSV file contains.'
    )
    mkcsv_parser.add_argument(
        '--cols',
        '-n',
        action='store',
        type=int,
        required=True,
        help='Number of columns the desired CSV file contains.'
    )
    mkcsv_parser.add_argument(
        '--output',
        '-o',
        action='store',
        type=str,
        required=False,
        default="test",
        help='Output file name. A ".csv" file extension will be appended to this value.'
    )
    mkcsv_parser.add_argument(
        '--data-types',
        '-d',
        action='store',
        nargs='+',
        required=False,
        default=['int'],
        help='Data types present in the desired CSV file. Supported data types are: str, int, float.'
    )
    mkcsv_parser.add_argument(
        '--nan-values',
        '-a',
        action='store',
        type=float,
        required=False,
        default=.0,
        help='Frequency of NaN values contained in desired CSV file.'
    )
    mkcsv_parser.add_argument(
        '--empty-values',
        '-e',
        action='store',
        type=float,
        required=False,
        default=.0,
        help='Frequency of empty values contained in desired CSV file.'
    )
    mkcsv_parser.add_argument(
        '--index',
        '-i',
        action='store_true',
        dest='index',
        help='Flag signaling whether the left most column should be a row index (ascending integer).'
    )
    mkcsv_parser.set_defaults(index=False)
    mkcsv_parser.add_argument(
        '--title',
        '-t',
        action='store_true',
        dest='title',
        help='Flag signaling whether the top most row should be a column index (ascending integer).'
    )
    mkcsv_parser.set_defaults(title=False)
    args = mkcsv_parser.parse_args()
    mkcsv_parser.add_argument(
        '--value-length',
        '-l',
        action='store',
        type=int,
        required=False,
        default=6,
        help='Character length of the individual random values.'
    )
    mkcsv(args)
