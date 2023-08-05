# -*- coding: utf-8 -*-
# Tokyo Cabinet Python ctypes binding.

import hdb
import bdb
import fdb
import tdb
import adb
from tc import __version__


# enumeration for error codes
ESUCCESS = 0                    # success
ETHREAD  = 1                    # threading error
EINVALID = 2                    # invalid operation
ENOFILE  = 3                    # file not found
ENOPERM  = 4                    # no permission
EMETA    = 5                    # invalid meta data
ERHEAD   = 6                    # invalid record header
EOPEN    = 7                    # open error
ECLOSE   = 8                    # close error
ETRUNC   = 9                    # trunc error
ESYNC    = 10                   # sync error
ESTAT    = 11                   # stat error
ESEEK    = 12                   # seek error
EREAD    = 13                   # read error
EWRITE   = 14                   # write error
EMMAP    = 15                   # mmap error
ELOCK    = 16                   # lock error
EUNLINK  = 17                   # unlink error
ERENAME  = 18                   # rename error
EMKDIR   = 19                   # mkdir error
ERMDIR   = 20                   # rmdir error
EKEEP    = 21                   # existing record
ENOREC   = 22                   # no record found
EMISC    = 9999                 # miscellaneous error


def hdbopen(path, **kwargs):
    """Simple hdb class constructor."""
    db = hdb.HDB()
    db.open(path, **kwargs)
    return db

def bdbopen(path, **kwargs):
    """Simple bdb class constructor."""
    db = bdb.BDB()
    db.open(path, **kwargs)
    return db

def fdbopen(path, **kwargs):
    """Simple fdb class constructor."""
    db = fdb.FDB()
    db.open(path, **kwargs)
    return db

def tdbopen(path, **kwargs):
    """Simple tdb class constructor."""
    db = tdb.TDB()
    db.open(path, **kwargs)
    return db

def adbopen(path, **kwargs):
    """Simple adb class constructor."""
    db = adb.ADB()
    db.open(path, **kwargs)
    return db
