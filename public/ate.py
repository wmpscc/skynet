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

    price = classify([float(form.getvalue('kilometre')), int(form.getvalue('card_date')), int(form.getvalue('quality'))], form.getvalue('model_id'))

    data = {"price": price}

    jsonss = json.dumps(data)
    print (jsonss)
main()