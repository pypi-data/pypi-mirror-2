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
def process_args():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-a", "--add", action="store_true", dest="add",
                      help="Add a name to my database.")
    parser.add_option("-n", "--name", action="store", dest="name",
                      help="Name to add to my database.")
    return parser.parse_args()

process_args()
d=libdrizzle.Drizzle()
c=d.create_client_connection()
c.set_tcp("localhost",9306)
c.set_auth("root",None)
c.set_db("test")
c.connect()
r=c.query("SELECT id, k, c  FROM sbtest")


for column in iter(r.column_read, None):
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
         column.type(), column.flags())

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


while True:
  row=r.row_read()
  if row == 0:
    break
  print "Row: %d" % (row)
  for x in range(r.column_count()):
    f=r.field_buffer()
    print "\t(%d) %s" % (len(f),f)
    r.field_free(f)
  print

print r.row_count()
