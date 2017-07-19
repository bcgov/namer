#!/usr/bin/python
import sys

from search import Search
from server import app as application
from wsgiref.simple_server import make_server


def main():
    if sys.version_info[0] < 3:
        print("Server requires Python 3")
        return

    print("Loading server...")
    Search()  # Loads data into search engine cache

    httpd = make_server('0.0.0.0', 5000, application)
    print("Serving corporate names on http://0.0.0.0:5000/\n")
    httpd.serve_forever()
    print("Terminated!!")

if __name__ == '__main__':
    main()
