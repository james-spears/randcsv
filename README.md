# randcsv

Generate random CSVs.

## Purpose

This project is intended to provide:

1) A utility for generating random comma separated values via command line interface.
2) A publicly available Python package for generating random comma separated values.

Where the purpose of 2) is easier integration of randcsv and automated testing suits.

## CLI

### Installation

The recommended way to install the randcsv CLI is using `pipx` which requires Python version `>=3.6`. A step-by-step installation is shown here (performed on Ubuntu 20.04).

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
    #
    ```

### Command line arguments

The randcsv command line tool makes available the following configuration parameters:

***N.B. All commands are available via long-hand and short-hand flags. So-called long-hand flags begin with two (2) hyphens `--` and short-hand flags begin with one (1) hyphen `-`.***

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
