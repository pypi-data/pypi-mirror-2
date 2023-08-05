# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Roberto Longobardi, Marco Cipriani
#

import re
from trac.core import *

def get_page_title(text):

    return text.split('\n')[0].strip('\r\n').strip('= \'')

    
def formatExceptionInfo(maxTBlevel=5):
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    
    try:
        excArgs = exc.__dict__["args"]
    except KeyError:
        excArgs = "<no args>"
    
    excTb = traceback.format_tb(trbk, maxTBlevel)
    return (excName, excArgs, excTb)


checked_utimestamp = False
has_utimestamp = False
    
def to_any_timestamp(date_obj):
    global checked_utimestamp
    global has_utimestamp

    if not checked_utimestamp:
        check_utimestamp()

    if has_utimestamp:
        from trac.util.datefmt import to_utimestamp
        return to_utimestamp(date_obj)
    else:
        # Trac 0.11
        from trac.util.datefmt import to_timestamp
        return to_timestamp(date_obj)


def from_any_timestamp(ts):
    global checked_utimestamp
    global has_utimestamp

    if not checked_utimestamp:
        check_utimestamp()

    if has_utimestamp:
        from trac.util.datefmt import from_utimestamp

        return from_utimestamp(ts)
    else:
        # Trac 0.11
        import datetime
        from trac.util.datefmt import utc

        return datetime.fromtimestamp(ts, utc)

        
def check_utimestamp():
    global checked_utimestamp
    global has_utimestamp

    try:
        from trac.util.datefmt import to_utimestamp, from_utimestamp
        has_utimestamp = True
    except:
        # Trac 0.11
        has_utimestamp = False

    checked_utimestamp = True
