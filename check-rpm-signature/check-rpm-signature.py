#!/usr/bin/python -tt
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#Copyright 2003 Duke University
#    Seth Vidal skvidal at phy.duke.edu


######
# Simple docs: run it with a list of rpms as the args
# it will tell you if any of them is damaged and if so how
# it will tell you if any of them has a bad key or invalid sig or whatever
# it exits with the largest error code possible for the set of pkgs

# error codes are:
# 0 - all fine
# 100 = damaged pkg
# 101 = unsigned pkg
# 102 = signed but bad pkg - if we ever get this one I'll be amazed
# 103 = signed - but key not in rpmdb
# 104 = signed but untrusted key

import rpm
import re
import os
import os.path
import sys


def graylogBadRPM(message):
    print('Ooh dear this rpm is a teleported monkey : {0} we should tell graylog'.format(message))
    return

def lookupKeyID(ts, keyid):
    """looks up a key id - returns the header"""
    mi = ts.dbMatch('name','gpg-pubkey')
    mi.pattern('version', rpm.RPMMIRE_STRCMP, keyid)
    for hdr in mi:
        sum = hdr['summary']
        mo = re.search('\<.*\>', sum)
        email = mo.group()
        return email

def checkSig(ts, package):
    """ take a package, check it's sigs, return 0 if they are all fine, return 
    103 if the gpg key can't be found, 104 if the key is not trusted,100 if the 
    header is in someway damaged"""
    try:
        fdno = os.open(package, os.O_RDONLY)
    except OSError, e:
        return 100
    stderr = os.dup(2)
    null = os.open("/dev/null", os.O_WRONLY | os.O_APPEND)
    os.dup2(null, 2)
    try:
        ts.hdrFromFdno(fdno)
    except rpm.error, e:
        if str(e) == "public key not availaiable":
            error = 103
        if str(e) == "public key not available":
            error = 103
        if str(e) == "public key not trusted":
            error = 104
        if str(e) == "error reading package header":
            error = 100
        os.dup2(stderr, 2)
        os.close(null)
        os.close(stderr)
        os.close(fdno)
        return error
    os.dup2(stderr, 2)
    os.close(null)
    os.close(stderr)
    os.close(fdno)
    return 0

def returnHdr(ts, package):
    """hand back the hdr - duh - if the pkg is foobar handback None"""
    try:
        fdno = os.open(package, os.O_RDONLY)
    except OSError, e:
        hdr = None
        return hdr
    ts.setVSFlags(~(rpm.RPMVSF_NOMD5|rpm.RPMVSF_NEEDPAYLOAD))
    try:
        hdr = ts.hdrFromFdno(fdno)
    except rpm.error, e:
        hdr = None
    if type(hdr) != rpm.hdr:
        hdr = None
    ts.setVSFlags(0)
    os.close(fdno)
    return hdr


def getSigInfo(hdr):
    """hand back signature information and an error code"""
    string = '%|DSAHEADER?{%{DSAHEADER:pgpsig}}:{%|RSAHEADER?{%{RSAHEADER:pgpsig}}:{%|SIGGPG?{%{SIGGPG:pgpsig}}:{%|SIGPGP?{%{SIGPGP:pgpsig}}:{(none)}|}|}|}|'
    siginfo = hdr.sprintf(string)
    if siginfo != '(none)':
        error = 0 
        sigtype, sigdate, sigid = siginfo.split(',')
    else:
        error = 101
        sigtype = 'MD5'
        sigdate = 'None'
        sigid = 'None'
        
    infotuple = (sigtype, sigdate, sigid)
    return error, infotuple
    
    
    
def main(args):
    rpmroot = '/'

    finalexit = 0
    ts = rpm.TransactionSet(rpmroot)
    for package in args:
        error = 0
        sigerror = 0
        ts.setVSFlags(0)
        error = checkSig(ts, package)
        hdr = returnHdr(ts, package)
        if hdr == None:
            error = 100
            print '%s: FAILED - None <None>' % package
        else:
            sigerror, (sigtype, sigdate, sigid) = getSigInfo(hdr)
            if sigid == 'None':
                email = '<None>'
                keyid = 'None'
            else:
                keyid = sigid[-8:]
                email = lookupKeyID(ts, keyid)
            if error != 0:
                if error == 103:
                    msg = '%s: MISSING KEY - %s' % (package, keyid)
                    print msg
                    graylogBadRPM(msg)
                else:                
                    msg = '%s: FAILED - %s %s' % (package, keyid, email)
                    print msg
                    graylogBadRPM(msg)
            else:
                msg = '%s: %s - %s - %s' % (package, sigtype, keyid, email)
                print msg
                graylogBadRPM(msg)

        if error < sigerror:
            error = sigerror
        if error > finalexit:
            finalexit = error
            
        del hdr
    sys.exit(finalexit)


if __name__ == '__main__':
    main(sys.argv[1:])
