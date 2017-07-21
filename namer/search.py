import logging
import os
import sys
import utils

from pytrie import SortedStringTrie as Trie

logger = logging.getLogger(__name__)


class Search:
    __search_trie = None
    __cached_name = None

    def __new__(cls):
        """
        Indexes data into search_trie and caches names into memory
        :return: None
        """
        if Search.__search_trie is None:
            file_path = os.path.join(os.path.dirname(__file__), '..', 'files',
                                     'data-100k.csv')
            Search._load_data(file_path)

    @staticmethod
    def _load_data(file_path):
        """
        Temporary Proof of concept function - Loads information from CSV file
        Parses and splits CORP_NME for search_trie
        :param file_path: File path of CSV
        :return: None
        """
        import csv

        index_field = 'CORP_NUM'
        end_event_field = 'END_EVENT_ID'
        name_field = 'CORP_NME'

        Search.__search_trie = Trie()
        Search.__cached_name = dict()
        if not os.path.isfile(file_path):
            logger.warning('File not found. Empty search trie instantiated')
            return

        with open(file_path) as file:
            reader = csv.DictReader(file, delimiter=';',
                                    quoting=csv.QUOTE_NONE)
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
                    # Remove non-alphanumeric characters and split words
                    clean_name = utils.clean_string(row[name_field])
                    for word in clean_name.split():
                        if word not in (None, ''):
                            # Create all possible suffixes of word
                            suffix_list = \
                                [(yield(word[i:])) for i in range(len(word))]
                            for suffix in suffix_list:
                                if suffix not in Search.__search_trie:
                                    Search.__search_trie[suffix] = set()
                                Search.__search_trie[suffix].add(
                                    row[index_field])

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
        results = set()
        try:
            logger.debug('Prefix Matches: %s',
                         Search.__search_trie.keys(prefix))
            logger.debug('Longest Prefix: %s',
                         Search.__search_trie.longest_prefix(prefix))

            for result in Search.__search_trie.values(prefix):
                results.update(result)  # Union
        except KeyError:
            pass

        return results

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
    def _gather_names(index_set):
        """
        Returns a sorted aggregate list of all names from index_set with
        entries beginning with prefix showing up first
        :param index_set: Set of Index values
        :return: List of sorted names
        """
        # Gather cached names into a single list
        name_list = list()
        for index in index_set:
            values = Search._lookup_name(index)
            if values is not None:
                name_list += values

        # Return alphabetically sorted names
        return sorted(name_list, key=str.lower)

    @staticmethod
    def _filter_names(name_list, query):
        """
        Filters name_list to only contain names with all words in query_list
        Attempts to reorder entries starting with query_list to the top
        :param name_list: List of names
        :param query: Raw query String
        :return:
        """
        # If nothing to filter and sort with
        if query in (None, ''):
            return name_list

        clean_q = utils.clean_string(query)
        if clean_q not in (None, ''):
            # Filter results that do not contain all values in query
            name_list = [name for name in name_list if all(
                term in utils.clean_string(name) for term in clean_q.split())]

            # Bring strings with matching prefix to the top
            starts_with_list = \
                [name for name in name_list if name.startswith(clean_q)]
            remaining_list = \
                [name for name in name_list if not name.startswith(clean_q)]
            name_list = starts_with_list + remaining_list

        return name_list

    @staticmethod
    def search(query=None, limit=None):
        """
        Returns a dictionary containing the search results of term in hits
        Hits is a list of dictionaries containing an id, label and value
        :param query: String search term
        :param limit: Limites number of results returned
        :return: Dictionary containing list of hits
        """
        hits = list()
        if query not in (None, ''):
            query = query.upper()
            clean_q = utils.clean_string(query)
            results = set()
            for term in clean_q.split():
                if len(results) == 0:
                    results = Search._trie_search(term)
                else:
                    results.intersection_update(Search._trie_search(term))

            name_list = Search._gather_names(results)
            names = Search._filter_names(name_list, query)

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
