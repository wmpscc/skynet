#!/usr/bin/python
import cgi
import json
import sys

import platform

sys.path.append('..')
from evaluate.product.estimate import classify

def main():
    print ("Content-type: text/html\n")
    form = cgi.FieldStorage()

    price = classify([3.2, 1425168000, 0], form.getvalue('model_id'))




    data = {"price": price}

    jsonss = json.dumps(data)
    print (jsonss)
main()