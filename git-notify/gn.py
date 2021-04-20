#!/bin/env python

import sys
from git import Repo


def notifySubscribers(file_that_changed):
    pass


def main():

    files_to_watch = [
                       'README.txt',
                     ]

    repo = Repo ('/Users/dmo/src/exp')
    assert not repo.bare

    # I guess we need to do a pull
    git_from='HEAD~2'
    git_to='HEAD' 

    versions= '{f}..{t}'.format(f=git_from, t=git_to) 
    diff = repo.git.diff(versions, name_only=True)

    x = diff.split('\n')
    for file in files_to_watch:
        for l in x:
            print('File {} has been modified. '.format(l)) 
            if l.endswith(file):
                print('Alarm {} has been modified. '.format(l)) 
                
        

if __name__ == '__main__':
    sys.exit(main())

    
