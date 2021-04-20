#!/usr/bin/env python

import os
import sys
import csv
import logging
import datetime


def  string_to_date(s_date, pattern):
    """Return a datetime object from a string:
d = '01-JAN-2001'
e = '02-02-2002'

d_date = string_to_date(d, '%d-%b-%Y')
e_date = string_to_date(e, ')%d-%m-%Y')

2001-01-01 00:00:00
2002-02-02 00:00:00 """
    return datetime.datetime.strptime(s_date, pattern)


def openCSVFile(f):
    """Return a file as a csv dictionary."""
    csv_dict = csv.DictReader(open(f))
    logging.debug(f"""CSV Dialect: {csv_dict.dialect}""")
    logging.debug(f"""Field names: {csv_dict.fieldnames}""")
    return csv_dict


def summarizeCSV(csv_dict, num_rows_to_summarize=1, separator=" = ", mask_values=False):
    """Generate a view of each column in a csv file printed line by line:

fruit,count
apple,2

will be printed as:

fruit = apple
count = 2

*separator* changes what is printed to separate the row name from the variable.

*num_rows_to_summarize* is the number of rows from csv file to print out.
"""
    num_rows_to_summarize = 2 + num_rows_to_summarize
    if sys.stdout.isatty():
        hl_on = """\033[7m\033[31m"""
        hl_off = """\033[0m')"""
    else:
        hl_on = ""
        hl_off = ""
    for row in csv_dict:
        if csv_dict.line_num >= num_rows_to_summarize:
            break
        else:
            if mask_values is True:
                columns_to_mask = ["LastName"]
                row = maskValues(columns_to_mask, row)
            for item in row:
                l = f"{item}{separator}{hl_on}{row[item]}{hl_off}"
                print(l)
            logging.debug(f"""line number of csv: {csv_dict.line_num}""")
            print()


def lowercaseList(list):
    """Convert the items in a list to lowercase."""
    return [x.lower() for x in list]


def maskValues(columns_to_mask, row, mask_string="*****"):
    """Takes a list of column headings that need to be masked and replaces the valued in them with the value in *mask_string*"""
    logging.debug(f"Masking: {columns_to_mask}")
    columns_to_mask = lowercaseList(columns_to_mask)
    logging.debug(columns_to_mask)
    for column in row:
        if column.lower() in columns_to_mask:
            row[column] = replacement_value
            logging.debug(f"masking: {column}")
    return row


if __name__ == "__main__":
    main()
