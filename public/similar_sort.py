#!/usr/bin/python
import cgi
import json
import sys

sys.path.append('..')

from service.train import similarSort

def main():
    print ("Content-type: text/html\n")
    form = cgi.FieldStorage()

    master = json.loads(form.getvalue('master'))
    origin = json.loads(form.getvalue('origin'))

    sortResult = similarSort(master, origin)
    jsonss = json.dumps(sortResult)
    print (jsonss)
main()