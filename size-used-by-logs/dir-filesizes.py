#!/usr/bin/env python3

import os
import csv
import glob
import time
import datetime


def main():

    ts = time.time()
    dt = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    extension = "*.log"
    g = glob.glob(extension)

    print(f'filename,timestamp,date,size_in_bytes')
    for f in g:
        s = os.path.getsize(f)
        print(f'{f},{ts},{dt},{s}')


if __name__ == "__main__":
    main()