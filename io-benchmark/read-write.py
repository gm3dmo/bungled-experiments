#!/usr/bin/env python

import sys
import csv
import json
import pprint
import requests
import time
import random
import string
import socket


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        hostname = socket.gethostname()
        print '%r,%r,%r,%r,%2.2f' % \
              (hostname, ts, te, method.__name__,  te-ts)
        return result
    return timed


@timeit
def write_to_file(r):
 with open("x.txt", 'w') as f:
    data = f.write(r)


@timeit
def read_from_file():
 with open("x.txt", 'r') as f:
    data = f.read()


@timeit
def random_generator(size=65536, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for x in range(size))


def main():
    """Very simple I/O routine to test a server

read-write.py 5

    """
     

    if sys.argv[1] is None:
        sleep_interval = int(5)
    else:
        sleep_interval = int(sys.argv[1])


    while True:
        r = random_generator()
        write_to_file(r)
        read_from_file()
        time.sleep(sleep_interval)


if __name__ == "__main__":
    main()
