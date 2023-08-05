#  drizzle-interface: Interface Wrappers for Drizzle
#
#  Copyright (c) 2010 Max Goodman
#
#  All rights reserved.
# 
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
# 
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#  3. The name of the author may not be used to endorse or promote products
#     derived from this software without specific prior written permission.
# 
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import types
import time
import datetime
from decimal import Decimal
from drizzle import libdrizzle as libd

__all__ = ["from_db", "to_db", "STRING", "BINARY", "NUMBER", "DATETIME", 
           "ROWID", "DateFromTicks", "TimeFromTicks", "TimestampFromTicks",
           "Timestamp", "Date", "Time", "Binary"]

# Inspired by MySQLdb
class DBAPIColumnType(frozenset):
    def __eq__(self, val):
        if isinstance(val, DBAPIColumnType):
            return not self.difference(val)
        return val in self

class ConversionSet(object):
    def __init__(self, converters={}):
        self.converters = converters

    def register(self, valuetype, converter, force=False):
        """Register a converter for a given type. 
        
        If a converter already exists, ValueError will be raised unless 
        the optional force parameter is set to True.
        
        """
        if converter in self.converters and force == false:
            raise ValueError
        else:
            self.converters[valuetype] = converter
            
    def convert(self, value, valuetype=None):
        """Convert a value using the set of converters.
        
        If an appropriate converter cannot be found, KeyError will be 
        raised with the type of the value.
        
        """
        
        if valuetype is None:
            valuetype = type(value)
        
        if valuetype in self.converters:
            if value is None:
                return None
            else:
                return self.converters[valuetype](value)
        else:
            raise KeyError(valuetype)

# DB-API "Type Objects":
# When compared with the "type" field of a description, equality denotes identity.
# To categorize:
#   DRIZZLE_COLUMN_TYPE_DRIZZLE_MAX
#   DRIZZLE_COLUMN_TYPE_DRIZZLE_NULL

STRING = DBAPIColumnType([
    libd.DRIZZLE_COLUMN_TYPE_VARCHAR,
    libd.DRIZZLE_COLUMN_TYPE_ENUM    
])

BINARY = DBAPIColumnType([
    libd.DRIZZLE_COLUMN_TYPE_BLOB
])

NUMBER = DBAPIColumnType([
    libd.DRIZZLE_COLUMN_TYPE_DOUBLE,
    libd.DRIZZLE_COLUMN_TYPE_LONG,
    libd.DRIZZLE_COLUMN_TYPE_LONGLONG,
    libd.DRIZZLE_COLUMN_TYPE_NEWDECIMAL,
    libd.DRIZZLE_COLUMN_TYPE_TINY
])

DATETIME = DBAPIColumnType([
    libd.DRIZZLE_COLUMN_TYPE_DATE,
    libd.DRIZZLE_COLUMN_TYPE_DATETIME,
    libd.DRIZZLE_COLUMN_TYPE_TIMESTAMP
])

ROWID = DBAPIColumnType([
    # Nothing to see here. There is no special row id type in Drizzle.
])

# The following three methods are from OurSQL, by Aaron Gallagher
# https://launchpad.net/oursql
def _datetime_from_string(s):
    tt = time.strptime(s, '%Y-%m-%d %H:%M:%S')
    return datetime.datetime(*tt[:6])

def _date_from_string(s):
    tt = time.strptime(s, '%Y-%m-%d')
    return datetime.date(*tt[:3])

def _time_from_string(s):
    tt = time.strptime(s, '%H:%M:%S')
    return datetime.time(*tt[3:6])

def DateFromTicks(ticks):
    return Date(*time.localtime(ticks)[:3])

def TimeFromTicks(ticks):
    return Time(*time.localtime(ticks)[3:6])

def TimestampFromTicks(ticks):
    return Timestamp(*time.localtime(ticks)[:6])


Timestamp = datetime.datetime
Date = datetime.date
Time = datetime.time
Binary = buffer

from_db = ConversionSet({
    # String types
    # FIXME: unicode handling here?
    libd.DRIZZLE_COLUMN_TYPE_VARCHAR:       str,
    libd.DRIZZLE_COLUMN_TYPE_ENUM:          str,
    
    # Binary types
    libd.DRIZZLE_COLUMN_TYPE_BLOB:          buffer,
    
    # Numeric types
    libd.DRIZZLE_COLUMN_TYPE_LONG:          int,
    libd.DRIZZLE_COLUMN_TYPE_LONGLONG:      int,
    libd.DRIZZLE_COLUMN_TYPE_TINY:          int,
    libd.DRIZZLE_COLUMN_TYPE_DOUBLE:        float,
    libd.DRIZZLE_COLUMN_TYPE_NEWDECIMAL:    Decimal,
    
    # Date/time types
    libd.DRIZZLE_COLUMN_TYPE_DATE:          _date_from_string,
    libd.DRIZZLE_COLUMN_TYPE_DATETIME:      _datetime_from_string,
    libd.DRIZZLE_COLUMN_TYPE_TIMESTAMP:     _time_from_string,
})

to_db = ConversionSet({
    #types.IntType:                          str,
    #types.LongType:                         str,
    #types.FloatType:                        str,
    #types.NoneType:                         lambda v: "NULL",
    #types.StringType:                       repr,
    #FIXME: types.UnicodeType: ,
    #FIXME: types.BooleanType: ???
})
