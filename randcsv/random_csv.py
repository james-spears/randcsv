import csv
from operator import itemgetter
from multiprocessing import Pool, cpu_count
from typing import Union, List, Tuple

from . import value_generators as vg
from . import data_type as dt


class RandCSV:
    """
    All of the arguments (meta data) required to initialize randcsv.
    """
    def __init__(
        self,
        rows,
        cols,
        byte_size=8,
        data_types=None,
        nan_freq=.0,
        empty_freq=.0,
        index_col=False,
        title_row=False,
        max_procs=None
    ):
        if data_types is None:
            data_types = [dt.DataType.integer.value]
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
        if byte_size <= 0:
            raise ValueError("--value-length must be positive")

        self.nan_freq = nan_freq
        self.empty_freq = empty_freq
        self.byte_size = byte_size

        regular_values = 1 - self.nan_freq - self.empty_freq
        all_value_types = [(0, regular_values), (1, self.nan_freq), (2, self.empty_freq)]
        all_value_types_sorted = sorted(all_value_types, key=itemgetter(1))

        num_of_cpus = cpu_count()
        # The default value of max_procs will be the system cpu count.
        if max_procs is None:
            self.max_procs = num_of_cpus
        else:
            # In the case the user enters a negative number,
            # raise a value error.
            if max_procs <= 0:
                raise ValueError("--max-procs must be positive")
            # if max_procs > num_of_cpus:
            #     self.max_procs = num_of_cpus
            # else:
            self.max_procs = max_procs

        # If the machine has only 1 cpu, or the user has set
        # max_procs to 1 then we do not want to pool processes,
        # just run in the current thread.
        if self.max_procs < 2:
            self.data = []
            for row in range(self.rows):
                row_values = self.generate_row(row, all_value_types_sorted)
                self.data.append(row_values)
        # Otherwise, by this point, the machine
        else:
            with Pool(processes=self.max_procs) as pool:
                arguments = [(row, all_value_types_sorted) for row in range(self.rows)]
                p = pool.starmap(
                    self.generate_row,
                    arguments,
                )
                pool.close()

            self.data = p

    def to_file(self, file_name) -> None:
        """Save the data to local file system.

        :param file_name: name of output file
        :return: None
        """
        with open(file_name, 'w+', newline='') as csvfile:
            csvwriter = csv.writer(
                csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in range(len(self.data)):
                csvwriter.writerow(self.data[row])
        return None

    def generate_row(self, row_num: int, all_value_types_sorted: Tuple[Tuple]) -> List[Union[float, int, str, None]]:
        if row_num == 0 and self.title_row:
            return [str(col) for col in range(self.cols)]
        else:
            if self.index_col:
                row: List[Union[float, int, str, None]] = [str(row_num)]
                row += [
                    vg.generate_value(
                        all_value_types_sorted,
                        self.data_types,
                        self.byte_size
                    ) for _ in range(1, self.cols)
                ]
            else:
                row = [
                    vg.generate_value(
                        all_value_types_sorted,
                        self.data_types,
                        self.byte_size
                    ) for _ in range(self.cols)
                ]
        return row
