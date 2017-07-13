import logging
import os

from pytrie import SortedStringTrie as Trie

logger = logging.getLogger(__name__)


class Search(object):
    __search_trie = None
    __cached_name = None

    def __init__(self):
        """Builds the searchtrie from input data into memory"""
        if self.__search_trie is None:
            file_path = os.path.join(os.path.dirname(__file__), '..', 'files',
                                     'data-100k.csv')
            self.load_data(file_path)

    @staticmethod
    def load_data(file_path):
        """
            Temporary Proof of concept function
            Loads information from CSV file
            Parses and splits CORP_NME for search_trie
        """
        import csv
        import re

        # TODO: Move field constants elsewhere
        index_field = 'CORP_NUM'
        name_field = 'CORP_NME'

        Search.__search_trie = Trie()
        Search.__cached_name = dict()
        if not os.path.isfile(file_path):
            logger.warning('File not found. Empty search trie instantiated')
            return

        with open(file_path) as file:
            reader = csv.DictReader(file, delimiter=';')
            try:
                for row in reader:
                    # Build Cache Dictionary
                    if row[index_field] not in Search.__cached_name:
                        Search.__cached_name[row[index_field]] = \
                            [row[name_field]]
                    else:
                        Search.__cached_name[row[index_field]].append(
                            row[name_field])

                    # Build Search Trie
                    # Removes non-alphanumeric characters and splits words
                    clean_name = re.sub(r'[^a-zA-Z\d\s]', '', row[name_field])
                    for element in clean_name.split():
                        if element is not None:
                            if element not in Search.__search_trie:
                                Search.__search_trie[element] = set()

                            Search.__search_trie[element].add(row[index_field])
            except UnicodeDecodeError:
                logger.error('Unexpected input at line %s', reader.line_num)
        logger.info('Loaded and indexed data')

    @staticmethod
    def search(prefix):
        """Searches and returns a list of values which match the prefix"""
        result = set()
        try:
            logger.debug('Matches: %s',
                         list(Search.__search_trie.iter_prefixes(prefix)))
            for value in Search.__search_trie.itervalues(prefix):
                result.update(value)
        except KeyError:
            pass

        return result

    @staticmethod
    def lookup_name(index):
        """Looks up indexed cached names if they exist"""
        if index in Search.__cached_name:
            return Search.__cached_name[index]
        else:
            return None

    @staticmethod
    def gather_names(index_set):
        """Returns an aggregate list of all names from index_set"""
        name_list = list()
        for index in index_set:
            values = Search.lookup_name(index)
            if values is not None:
                name_list += values

        return name_list


if __name__ == "__main__":
    from timeit import default_timer as timer

    # TODO: Move logging infrastructure to proper place
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    load_start = timer()
    engine = Search()
    load_end = timer()

    search_start = timer()
    results = Search.search('LAWN')
    search_end = timer()

    logger.info('Results: %s', results)

    gather_start = timer()
    names = Search.gather_names(results)
    gather_end = timer()

    logger.info('Names: %s', names)

    logger.info('Total results: %s', sum(1 for _ in results))
    logger.info('Data load time: %s', str(load_end - load_start))
    logger.info('Search time: %s', str(search_end - search_start))
    logger.info('Gather time: %s', str(gather_end - gather_start))
