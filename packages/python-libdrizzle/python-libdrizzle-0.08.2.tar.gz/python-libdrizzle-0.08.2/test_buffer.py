#  drizzle-interface: Interface Wrappers for Drizzle
#  Copyright (c) 2009 Sun Microsystems
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

from drizzle import libdrizzle

d=libdrizzle.Drizzle()
c=d.add_tcp("localhost",3306,"root",None,"information_schema", libdrizzle.DRIZZLE_CON_MYSQL)
r=c.query("select * from information_schema.tables")

print """
Result:     row_count=%d
            insert_id=%d
        warning_count=%d
          column_count=%d
	    error_code=%d
""" % ( r.row_count(),
        r.insert_id(),
        r.warning_count(),
        r.column_count(),
        r.error_code())

r.buffer_result()

for column in iter(r.next_column, None):
  print """
Field:   catalog=%s
              db=%s
           table=%s
       org_table=%s
            name=%s
        org_name=%s
         charset=%d
          length=%d
            type=%d
           flags=%d""" % (column.catalog(), column.db(),
         column.table(), column.orig_table(),
         column.name(), column.orig_name(),
         column.charset(), column.size(),
         column.column_type(), column.flags())

x=0
while True:
  x+=1
  row=r.next_row()
  if row is None:
    break
  print row
