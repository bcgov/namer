#!/usr/bin/python
import logging
import sys

from gevent.pywsgi import WSGIServer
from search import Search
from server import app as application
from timeit import default_timer as timer
from validator import Validator

log = logging.getLogger(__name__)


def main(port=5000):
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

    log.info("Serving corporate names on port %s", str(port))
    WSGIServer(('', port), application).serve_forever()
    log.info("Server terminated!")


if __name__ == '__main__':
    main()
