from __future__ import print_function

import csv
import argparse
from random import randint, random, choice
from operator import itemgetter

from randcsv import random_csv
from randcsv import value_generators as vg


def mkcsv(argv):
    if argv.nan_freq < .0 or argv.nan_freq > 1.:
        raise ValueError("--nan-freq <nan-freq> must be [0, 1]")
    if argv.empty_freq < .0 or argv.empty_freq > 1.:
        raise ValueError("--empty-freq <empty-freq> must be [0, 1]")
    if argv.nan_freq + argv.empty_freq > 1.:
        raise ValueError("--empty-freq <empty-freq> + --nan-freq <nan-freq> must be [0, 1]")
    if argv.value_length <= 0:
        raise ValueError("--value-length must be positive")

    regular_values = 1 - argv.nan_freq - argv.empty_freq
    all_value_types = [(0, regular_values), (1, argv.nan_freq), (2, argv.empty_freq)]
    all_value_types_sorted = sorted(all_value_types, key=itemgetter(1))

    with open(argv.output, 'w+', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in range(argv.rows):
            if row == 0 and argv.title_row:
                csvwriter.writerow([str(col) for col in range(argv.cols)])
            else:
                if argv.index_col:
                    csvwriter.writerow([str(row)] + [vg.generate_value(all_value_types_sorted, argv.data_types, argv.value_length)
                                                     for _ in range(1, argv.cols)])
                else:
                    csvwriter.writerow(
                        [vg.generate_value(all_value_types_sorted, argv.data_types, argv.value_length) for _ in range(argv.cols)])

    print(f'mkcsv generated file: {argv.output}')


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
        '--nan-freq',
        '-a',
        action='store',
        type=float,
        required=False,
        default=.0,
        help='Frequency of NaN values contained in desired CSV file.'
    )
    mkcsv_parser.add_argument(
        '--empty-freq',
        '-e',
        action='store',
        type=float,
        required=False,
        default=.0,
        help='Frequency of empty values contained in desired CSV file.'
    )
    mkcsv_parser.add_argument(
        '--index-col',
        '-i',
        action='store_true',
        dest='index_col',
        help='Flag signaling whether the left most column should be a row index (ascending integer).'
    )
    mkcsv_parser.set_defaults(index=False)
    mkcsv_parser.add_argument(
        '--title-row',
        '-t',
        action='store_true',
        dest='title_row',
        help='Flag signaling whether the top most row should be a column index (ascending integer).'
    )
    mkcsv_parser.set_defaults(title=False)
    mkcsv_parser.add_argument(
        '--value-length',
        '-l',
        action='store',
        type=int,
        required=False,
        default=6,
        help='Character length of the individual random values.'
    )
    args = mkcsv_parser.parse_args()
    initialization_values = random_csv.RandomCSV(
        rows=args.rows,
        cols=args.cols,
        value_length=args.value_length,
        output=args.output,
        data_types=args.data_types,
        nan_freq=args.nan_freq,
        empty_freq=args.empty_freq,
        index_col=args.index_col,
        title_row=args.title_row,
        )
    mkcsv(initialization_values)
