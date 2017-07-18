import logging
import os
import sys

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
        Temporary Proof of concept function - Loads information from CSV file
        Parses and splits CORP_NME for search_trie
        :param file_path: File path of CSV
        :return: None
        """
        import csv
        import re

        # TODO: Move field constants elsewhere
        index_field = 'CORP_NUM'
        name_field = 'CORP_NME'
        end_event_field = 'END_EVENT_ID'

        Search.__search_trie = Trie()
        Search.__cached_name = dict()
        if not os.path.isfile(file_path):
            logger.warning('File not found. Empty search trie instantiated')
            return

        with open(file_path) as file:
            reader = csv.DictReader(file, delimiter=';', quoting=csv.QUOTE_NONE)
            try:
                for row in reader:
                    # Ignore columns with specified END_EVENT_ID
                    if row[end_event_field] in (None, ''):
                        continue

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
                        if element not in (None, ''):
                            if element not in Search.__search_trie:
                                Search.__search_trie[element] = set()

                            Search.__search_trie[element].add(row[index_field])
            except UnicodeDecodeError:
                logger.error('Unexpected input at line %s', reader.line_num)
        logger.info('Loaded and indexed data')

    @staticmethod
    def _trie_search(prefix):
        """
        Searches and returns a set of values which contain the prefix
        :param prefix: Search term
        :return: Set containing results
        """
        result = set()
        try:
            logger.debug('Prefix Matches: %s',
                         list(Search.__search_trie.iter_prefixes(prefix)))
            logger.debug('Longest Prefix: %s',
                         Search.__search_trie.longest_prefix(prefix))
            result = Search.__search_trie.longest_prefix_value(prefix)
        except KeyError:
            pass

        return result

    @staticmethod
    def _lookup_name(index):
        """
        Looks up indexed cached names if they exist
        :param index: Index value
        :return: String name value
        """
        if index in Search.__cached_name:
            return Search.__cached_name[index]
        else:
            return None

    @staticmethod
    def _gather_names(index_set, prefix=None):
        """
        Returns a sorted aggregate list of all names from index_set with entries
        beginning with prefix showing up first
        Filters results to longest prefix if specified
        :param index_set:
        :param prefix:
        :return:
        """
        name_list = list()
        for index in index_set:
            values = Search._lookup_name(index)
            if values is not None:
                name_list += values

        if prefix is not None:
            longest_prefix = Search.__search_trie.longest_prefix(prefix)
            name_list = [name for name in name_list if longest_prefix in name]

        name_list = sorted(name_list, key=str.lower)
        starts_with_list = \
            [name for name in name_list if name.startswith(longest_prefix)]
        remaining_list = \
            [name for name in name_list if not name.startswith(longest_prefix)]
        return starts_with_list + remaining_list

    @staticmethod
    def search(term=None, limit=None):
        """
        Returns a dictionary containing the search results of term in hits
        Hits is a list of dictionaries containing an id, label and value
        :param term: String search term
        :param limit: Limites number of results returned
        :return: Dictionary containing list of hits
        """
        hits = list()

        if term not in (None, ''):
            term = term.upper()
            results = Search._trie_search(term)
            names = Search._gather_names(results, term)

            if limit in (None, ''):
                limit = sys.maxsize
            for i, name in zip(range(int(limit)), names):
                hits.append({'id': str(i), 'label': name, 'value': name})

        return {'hits': hits}

    @staticmethod
    def main(argv):
        """
        Searches and prints the results of the search term with timings
        :param argv: Command line arguments
        :return: None
        """
        from timeit import default_timer as timer

        # TODO: Move logging infrastructure to proper place
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        if len(argv) > 1:
            load_start = timer()
            Search()
            load_end = timer()
            search_start = timer()
            results = Search.search(argv[1])
            search_end = timer()

            logger.info('Results: %s', results)
            logger.info('Data load time: %s', str(load_end - load_start))
            logger.info('Search time: %s', str(search_end - search_start))
        else:
            logger.error('No search term specified')

if __name__ == "__main__":
    Search.main(sys.argv)
