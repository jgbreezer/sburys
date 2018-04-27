# Day value csv file processor

### Run program
This program is written for and requires either python v2.7 or python v3.0 or later.
It may also run in earlier versions of python 2 but is untested. If Python 2 or older
python 3 versions are used, the details for each day may not be output in the same order
for each line (due to dicts not being ordered in those versions).

Here is a sample command to process provided csv files
(assuming python is setup to run one of the versions required):

  `python list_dayinfo_csv.py 1.csv 2.csv 3.csv`

The csv files to process are specified on the command line. If none are provided
it will exit without processing anything; if -h option is given instead of files,
it will show about and usage information. The output consists of the filename
processed and then lines containing a python-style formatted list of dicts for
each day of the week's values. A blank line is output after each file's values.

The example command assumes the csv files are in the current directory,
specify correct paths otherwise.

#### CSV input data requirements and behaviour

There must be columns in each CSV for all five days of the week or the program
will output an error and exit. There must also be a 'description' column.
Extra columns will be ignored.

Days must be a weekday, as one of 'mon', 'tue', 'wed', 'thu', 'fri'. They can
be specified individually or in a (inclusive) range separated with a hyphen
eg. 'mon-thu'. Any other hypenated column headings cause that column to be ignored.
If ranges overlap or columns are duplicated, the last (right-most) column value
wins. If the start/end names are not a valid day name, it will be ignored.

Headings and values may be quoted as per MS Excel format.

### Test

To run the tests, it uses the py.test framework which is an external requirement
installable via pip. This has not been added to a requirements.txt as it is not
expected to be used in production. Run them with the following command (if in
the directory containing the test_list_dayinfo_csv.py test script and using a
default pytest setup):

  `pytest`

If it finishes with a zero exit status then all the tests ran successfully.
