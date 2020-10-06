import csv
import argparse
import string
from enum import Enum
from random import randint, random, choice
from operator import itemgetter
from math import nan


class DataType(Enum):
    string = 'str'
    integer = 'int'
    float = 'float'

    def __str__(self):
        return self.value


def random_integer():
    return str(randint(100000, 999999))


def random_float():
    return "{:.5f}".format(random())


def random_string():
    letters = string.ascii_letters
    return ''.join(choice(letters) for _ in range(6))


def value_factory(data_type):
    if data_type == DataType.string.value:
        return random_string()
    elif data_type == DataType.float.value:
        return random_float()
    elif data_type == DataType.integer.value:
        return random_integer()
    else:
        raise ValueError(
            "Data type must be one of: str, int, float"
        )


def random_value(all_values_sorted, data_types):
    # # make sure frequencies are valid
    # if nan_values < .0 or nan_values > 1.:
    #     raise ValueError("--nan-values <nan-values> must be [0, 1]")
    # if empty_values < .0 or empty_values > 1.:
    #     raise ValueError("--empty-values <empty-values> must be [0, 1]")
    # if nan_values + empty_values > 1.:
    #     raise ValueError("--empty-values <empty-values> + --nan-values <nan-values> must be [0, 1]")
    #
    # regular_values = 1 - nan_values - empty_values
    # all_values = [(0, regular_values), (1, nan_values), (2, empty_values)]
    # all_values_sorted = sorted(all_values, key=itemgetter(1))

    random_number = random()
    left_boundary = 0
    for item in all_values_sorted:
        right_boundary = item[1]
        if left_boundary <= random_number < right_boundary:
            if item[0] == 0:
                # this is a regular number, so randomly select one
                num_of_data_types = len(data_types)
                selected_data_type = randint(0, num_of_data_types - 1)
                return value_factory(data_types[selected_data_type])
            elif item[0] == 1:
                # this is a NaN value
                return nan
            elif item[0] == 2:
                # this is a NaN value
                return None
            else:
                # this must be an empty value
                raise ValueError
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
    all_values = [(0, regular_values), (1, argv.nan_values), (2, argv.empty_values)]
    all_values_sorted = sorted(all_values, key=itemgetter(1))

    with open(f'{argv.output}.csv', 'w+', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in range(argv.rows):
            if row == 0 and argv.title:
                csvwriter.writerow([str(col) for col in range(argv.cols)])
            else:
                if argv.index:
                    csvwriter.writerow([str(row)] + [random_value(all_values_sorted, argv.data_types)
                                                     for _ in range(1, argv.cols)])
                else:
                    csvwriter.writerow(
                        [random_value(all_values_sorted, argv.data_types) for _ in range(argv.cols)])

    print(f'mkcsv generated file: {argv.output}.csv')  # Press Ctrl+F8 to toggle the breakpoint.


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
    mkcsv(args)
