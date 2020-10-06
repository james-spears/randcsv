# randcsv

Generate random CSVs.

# Purpose

This project is intended to provide:

1) A utility for generating random comma separated values via command line interface.
2) A publicly available Python package for generating random comma separated values.

Where the purpose of 2) is easier integration of randcsv and automated testing suits.

## CLI

The randcsv command line tool makes available the following configuration parameters:

N.B. All commands are available via long-hand and short-hand flags. So-called long-hand flags begin with two (2) hyphens `--` and short-hand flags begin with one (1) hyphen `-`.

* `--rows`, `-m` (Required)
  * Number of rows the desired CSV file contains.

* `--cols`, `n`(Required)
  * Number of columns the desired CSV file contains.

* `--output`, `-o` (Optional. Default: `--output test.csv`)
  * Output file name.

* `--data-types`, `-d` (Optional. Default: `0.0`)
  * Data types present in the desired CSV file. Supported data types are: str, int, float. This argument accepts multiple values. Example: `--data-types str int float`. If more than one data type is provided, the logic randomly selects one of the provided data types on a per-value basis.

* `--nan-values`, `-a` (Optional. Default: `--nan-values 0.0`)
  * Frequency of NaN values contained in desired CSV file. Example: `--nan-values 0.25`, implies 25% of all the values in the CSV file will be `nan`.

* `--empty-values`, `-e` (Optional. Default: `--empty-values 0.0`)
  * Frequency of empty values contained in desired CSV file. Example: `--empty-values 0.25`, implies 25% of all the values in the CSV file will be `` (no value).

* `--index`, `-i` Boolean (Optional. Default: False)
  * Flag signaling whether the left most column should be a row index (ascending integer).

* `--title`, `-t` Boolean (Optional. Default: False)
  * Flag signaling whether the top most row should be a column index (ascending integer).
