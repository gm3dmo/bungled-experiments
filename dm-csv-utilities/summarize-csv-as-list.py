#!/usr/bin/env python

import sys
import logging
from csvdm import openCSVFile, summarizeCSV


def main():
    logging.basicConfig(level=logging.DEBUG)
    f = sys.argv[1]
    csv_dict = openCSVFile(f)
    summarizeCSV(csv_dict, num_rows_to_summarize=1)


if __name__ == "__main__":
    main()
