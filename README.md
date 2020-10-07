# RandCSV

Generate random CSVs.

[![License](https://poser.pugx.org/ali-irawan/xtra/license.svg)](https://poser.pugx.org/ali-irawan/xtra/license.svg)
![Lines of code](https://img.shields.io/tokei/lines/github/scriptloom/randcsv)
![GitHub repo size](https://img.shields.io/github/repo-size/scriptloom/randcsv)
![CircleCI](https://img.shields.io/circleci/build/github/scriptloom/randcsv/main)

## Purpose

This project is intended to provide:

1) A publicly available Python package for generating random comma separated values.
2) A utility for generating random comma separated values via command line interface.

Where the purpose of 1. is further integration of `randcsv` with automated testing suits.

## PyPI Package

### Installation

The package is publicly hosted on PyPI under the name `randcsv`; you can install it using `pip`.

1) Install `randcsv`.

```text
   $ pip install randcsv
   ...
```

### API

The `randcsv` API is exposed via a single class definition, `RandCSV`. Example usage is shown below.

```python
from randcsv import RandCSV

# Make a 4 x 3 CSV with title and index.
#
# Use all available data types: integer,
# token, and float.
#
# 10% NaN values, 15% empty values (implies 75% 
# randomly distributed "regular" values).

data = RandCSV(
    10,
    4,
    byte_size=8,
    data_types=['integer', 'token', 'float'],
    nan_freq=.1,
    empty_freq=.15,
    index_col=True,
    title_row=True,
)

# Save the CSV to a file `output.csv`
data.to_file('example.csv')
```

You should then find a file `example.csv` contained in the current working directory.

An example output is shown below:

|0  |1                 |2                  |3        |
|---|------------------|-------------------|---------|
|1  |0.5733712036037724|                   |-eLl9GnlEXo|
|2  |                  |                   |nan      |
|3  |RT3zxzTg4KI       |nan                |e2gOPMuGUGk|
|4  |12957925104777645606|0.13727825684393494|57589281133002397|
|5  |0.46730821418402785|0.7212639567220399 |10156229384055835642|
|6  |2884154713072591035|0.36739108321888597|0.9194898822958113|
|7  |17487691859213678632|MORTDt3Y6Vc        |680401081312304743|
|8  |0.6864180672941529|16386949079868257309|nX-IUxLb-A8|
|9  |                  |0.3868689478103007 |uZsUJyCLRU8|

### Data type examples

* (2, 1) and (2, 2) are examples of empty data types
* (3, 2) and (2, 3) are examples of NaN data types
* (5, 1) and (8, 1) are examples of floating point data types [0, 1)
* (7, 2) and (8, 3) are examples of token data types
* (7, 1) and (6, 1) are examples of integer data types
 

## CLI

### Installation

The recommended way to install the randcsv CLI is using `pipx` which requires Python version `>=3.6`.
A step-by-step installation is shown here (performed on Ubuntu 20.04).

1) Install `pipx` using `pip`.

```text
$ python3 -m pip install --user pipx
Collecting pipx
.... (output has been truncated)
Installing collected packages: pyparsing, packaging, argcomplete, click, distro, userpath, pipx
  WARNING: The script distro is installed in '/home/<username>/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
  WARNING: The script userpath is installed in '/home/<username>/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
  WARNING: The script pipx is installed in '/home/<username>/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
Successfully installed argcomplete-1.12.1 click-7.1.2 distro-1.5.0 packaging-20.4 pipx-0.15.5.1 pyparsing-2.4.7 userpath-1.4.1
```

2) As the warning contained in the output of the previous command, we now will ensure all required `pipx` scripts are available on PATH.

```text
$ python3 -m pipx ensurepath
Success! Added /home/<username>/.local/bin to the PATH environment
    variable.
/home/<username>/.local/bin has been been added to PATH, but you need to
    open a new terminal or re-login for this PATH change to take
    effect.

Consider adding shell completions for pipx. Run 'pipx completions' for
instructions.

You will need to open a new terminal or re-login for the PATH changes
to take effect.

Otherwise pipx is ready to go! ✨ 🌟 ✨
```

3) Install the randcsv CLI.

```text
$ pipx install randcsv
...
```

### Command line arguments

The randcsv command line tool makes available the following configuration parameters:

***N.B. All commands are available via long-hand and short-hand flags. So-called long-hand flags begin with two (2) hyphens `--` and short-hand flags begin with one (1) hyphen `-`.***

* `--rows`, `-m` Integer (Required)
  * Number of rows the desired CSV file contains.

* `--cols`, `n` Integer (Required)
  * Number of columns the desired CSV file contains.

* `--output`, `-o` String (Optional. Default: `--output test.csv`)
  * Output file name.

* `--data-types`, `-d` List (Optional. Default: `0.0`)
  * Data types present in the desired CSV file. Supported data types are: str, int, float. This argument accepts multiple values. Example: `--data-types str int float`. If more than one data type is provided, the logic randomly selects one of the provided data types on a per-value basis.

* `--nan-values`, `-a` Float (Optional. Default: `--nan-values 0.0`)
  * Frequency of NaN values contained in desired CSV file. Example: `--nan-values 0.25`, implies 25% of all the values in the CSV file will be `nan`.

* `--empty-values`, `-e` Float (Optional. Default: `--empty-values 0.0`)
  * Frequency of empty values contained in desired CSV file. Example: `--empty-values 0.25`, implies 25% of all the values in the CSV file will be `` (no value).

* `--index`, `-i` Boolean (Optional. Default: False)
  * Flag signaling whether the left most column should be a row index (ascending integer).

* `--title`, `-t` Boolean (Optional. Default: False)
  * Flag signaling whether the top most row should be a column index (ascending integer).

* `--byte-size`, `-b` Integer (Optional. Default: 8)
  * Number of bytes used to generate the random values. Increasing the byte size will
  increase the size of the set of possible random values.
