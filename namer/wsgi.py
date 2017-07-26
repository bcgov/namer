#!/usr/bin/python
import logging
import sys

from search import Search
from server import app as application
from timeit import default_timer as timer
from validator import Validator
from wsgiref.simple_server import make_server

log = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    if sys.version_info[0] < 3:
        log.error("Server requires Python 3")
        return

    log.info("Loading server...")
    load_start = timer()
    Validator()  # Loads phrase list into memory
    Search()  # Loads data into search engine cache
    load_end = timer()
    log.info('Load time: %s', str(load_end - load_start))

    httpd = make_server('0.0.0.0', 5000, application)
    log.info("Serving corporate names on port 5000")
    httpd.serve_forever()
    log.info("Server terminated!")


if __name__ == '__main__':
    main()
