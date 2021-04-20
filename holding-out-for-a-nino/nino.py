#!/usr/bin/env python

import exrex

def doMeANino(realnino=False):
    """"""
    if realnino == True:
        r = '^[A-CEGHJ-PR-TW-Z]{1}[A-CEGHJ-NPR-TW-Z]{1}[0-9]{6}[A-D]{1}$'
    else:
        r = '[Q]{1}[A-CEGHJ-NPR-TW-Z]{1}[0-9]{6}[A-D]{1}$'
    n = exrex.getone(r)
    return n


if __name__ == "__main__":
    main()