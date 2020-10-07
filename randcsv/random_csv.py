import csv
from random import randint, random, choice
from operator import itemgetter

from . import value_generators as vg

class RandomCSV:
    """All of the arguments (meta data) required to initialize randcsv.
    """
    def __init__(
        self,
        rows,
        cols,
        value_length=6,
        data_types=['int'],
        nan_freq=.0,
        empty_freq=.0,
        index_col=False,
        title_row=False,
    ):
        self.rows = rows
        self.cols = cols
        self.data_types = data_types
        self.index_col = index_col
        self.title_row = title_row

        if nan_freq < .0 or nan_freq > 1.:
            raise ValueError("--nan-freq <nan-freq> must be [0, 1]")
        if empty_freq < .0 or empty_freq > 1.:
            raise ValueError("--empty-freq <empty-freq> must be [0, 1]")
        if nan_freq + empty_freq > 1.:
            raise ValueError("--empty-freq <empty-freq> + --nan-freq <nan-freq> must be [0, 1]")
        if value_length <= 0:
            raise ValueError("--value-length must be positive")

        self.nan_freq = nan_freq
        self.empty_freq = empty_freq
        self.value_length = value_length

        regular_values = 1 - self.nan_freq - self.empty_freq
        all_value_types = [(0, regular_values), (1, self.nan_freq), (2, self.empty_freq)]
        all_value_types_sorted = sorted(all_value_types, key=itemgetter(1))

        self.data = []
        for row in range(self.rows):
            if row == 0 and self.title_row:
                self.data.append([str(col) for col in range(self.cols)])
            else:
                if self.index_col:
                    self.data.append(
                        [str(row)] 
                        + [vg.generate_value(
                            all_value_types_sorted,
                            self.data_types,
                            self.value_length
                            ) for _ in range(1, self.cols)])
                else:
                    self.data.append(
                        [vg.generate_value(
                            all_value_types_sorted,
                            self.data_types,
                            self.value_length
                            ) for _ in range(self.cols)])


    def to_file(self, file_name):
        with open(file_name, 'w+', newline='') as csvfile:
            csvwriter = csv.writer(
                csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in range(len(self.data)):
                    csvwriter.writerow(row)
