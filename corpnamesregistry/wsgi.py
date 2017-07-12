#!/usr/bin/python
import os

from server import app as application

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('0.0.0.0', 9000, application)
    print("Serving corporate names on http://0.0.0.0:9000/ \n")
    httpd.serve_forever()
    print("Terminated!!")
