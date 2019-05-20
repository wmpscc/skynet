#!/usr/bin/python
import cgi
import json

def main():
    print "Content-type: text/html\n"
    #print "Content-Type: application/json; charset=UTF-8"
    form = cgi.FieldStorage()

    #print "<h1> Hello", form.getvalue('ServiceCode'), "</h1>"
    data = [{"a": 1}]

    jsonss = json.dumps(data)
    print jsonss
main()


#sqlalchemy