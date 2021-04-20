#!/bin/env python

import os
import re
import sys
import time
import tarfile


tarf1 = sys.argv[1]
tarf2 = sys.argv[2]

def splatDate(noshstring):
    """files have dates embedded in the name making them difficult to compare. Dates begone!"""
    z = re.sub('_[0-9].*.json.gz','',noshstring)
    return z


def stripDir(noshstring):
    """We are only interested in the last piece for comparison"""
    z = os.path.split(noshstring)
    return z[1]


def list_difference(list1, list2):
    """uses list1 as the reference, returns list of items not in list2"""
    diff_list = []
    for item in list1:
        if not item in list2:
            diff_list.append(item)
    return diff_list


def tarf(tarzan):
    """Read the table of contents of the tar file and return a list of interesting components."""
    count = 0
    x = []
    t = tarfile.open(tarzan, 'r')
    for member_info in t.getmembers():
        count = count + 1
        unnoshed_file = member_info.name
        noshed_file = splatDate(member_info.name)
        noshed_file = stripDir(noshed_file)
        x.append([noshed_file, time.ctime(member_info.mtime), member_info.size, count, unnoshed_file ])
    return x


def main():
    """
    tarzan.py - reads the contents of two tar archives and prepares a list of files in the first but not in the second.
    """
    x = tarf(tarf1)
    y = tarf(tarf2)

    names1 = []
    for z in x:
        names1.append(z[0])

    names2 = []
    for z in y:
        names2.append(z[0])

    ld = list_difference(names1, names2)
    list_of_files_not_in_batch = []

    for n in ld:
        for a in x:
            if a[0] == n:
                list_of_files_not_in_batch.append(a)

    print( """The following files/directories: are in: {0} but are not in in: {1}: """.format(tarf1, tarf2) )
    for file in list_of_files_not_in_batch:
        print('{nn:40} {tm:30} size: {sz:12} original file: {on}'.format(nn=file[0], tm=file[1], on=file[4], sz=file[2]))


if __name__ == "__main__":
    main()
