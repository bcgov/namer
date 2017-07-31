#!/usr/bin/python
import logging
import os
import sys
import utils

from pytrie import StringTrie as Trie

log = logging.getLogger(__name__)


class Search:
    __search_trie = None

    def __new__(cls):
        """
        Indexes data into search_trie and caches names into memory
        :return: None
        """
        if Search.__search_trie is None:
            file_path = os.path.join(os.path.dirname(__file__), '..', 'files',
                                     'corp-name-data.csv')
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

        end_event_field = 'END_EVENT_ID'
        name_field = 'CORP_NME'

        Search.__search_trie = Trie()
        Search.__cached_name = dict()
        if not os.path.isfile(file_path):
            log.warning('File not found. Empty search trie instantiated')
            return

        with open(file_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';',
                                    quoting=csv.QUOTE_NONE)
            try:
                for row in reader:
                    # Ignore columns with specified END_EVENT_ID
                    if row[end_event_field] not in (None, ''):
                        continue

                    # Build Search Trie
                    # Remove non-alphanumeric characters and split words
                    clean_name = utils.re_alphanum(row[name_field])
                    if clean_name not in (None, ''):
                        for word in clean_name.strip().split():
                            # Create all possible suffixes of word
                            suffix_list = \
                                [(yield(word[i:])) for i in range(len(word))]
                            for suffix in suffix_list:
                                if suffix not in Search.__search_trie:
                                    Search.__search_trie[suffix] = set()
                                Search.__search_trie[suffix].add(
                                    row[name_field])

            except UnicodeDecodeError:
                log.error('Unexpected input at line %s', reader.line_num)
        log.info('Loaded and indexed name data')

    @staticmethod
    def _trie_search(prefix):
        """
        Searches and returns a set of values which contain the prefix
        :param prefix: Search term
        :return: Set containing results
        """
        results = set()
        try:
            log.debug('Prefix Matches: %s',
                      Search.__search_trie.keys(prefix))
            log.debug('Longest Prefix: %s',
                      Search.__search_trie.longest_prefix(prefix))

            for result in Search.__search_trie.values(prefix):
                results.update(result)  # Union
        except KeyError:
            pass

        return results

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

        clean_q = utils.re_alphanum(query)
        if clean_q not in (None, ''):
            # Filter results that do not contain all values in query
            name_list = [name for name in name_list if
                         all(term in utils.re_alphanum(name)
                             for term in clean_q.strip().split())]

            # Bring strings with matching prefix to the top
            starts_with_list = \
                [name for name in name_list if name.startswith(clean_q)]
            remaining_list = \
                [name for name in name_list if not name.startswith(clean_q)]
            name_list = starts_with_list + remaining_list

        return name_list

    @staticmethod
    def _get_synonyms(terms):
        """
        Returns a list of synonyms for all terms in term_list if they exist
        :param terms: List of words to check for synonyms
        :return: List of synonyms - empty list if none are found
        """
        return [Search._synonym(term) for term in terms] \
            if isinstance(terms, list) else Search._synonym(terms)

    @staticmethod
    def _synonym(term):
        """
        Returns a list of synonyms for term if they exist
        :param term: Single word to check for synonyms
        :return: List of synonyms - empty list if none are found
        """
        li = list()

        try:
            if len(term.split()) == 1:
                data = utils.get_soup_object(
                    "http://www.thesaurus.com/browse/{}".format(term))
                terms = data.select(
                    ".synonym-description ~ .relevancy-block")[0].findAll("li")
                for t in terms:
                    li.append(t.select("span.text")[0].getText().upper())
        finally:
            return li

    @staticmethod
    def search(query=None, limit=None, synonym=False):
        """
        Returns a dictionary containing the search results of term in hits
        Hits is a list of dictionaries containing an id, label and value
        :param query: String search term
        :param limit: Limites number of results returned
        :param synonym: Toggles synonym search support
        :return: Dictionary containing list of hits
        """
        hits = list()
        if query not in (None, ''):
            query = query.upper()
            clean_q = utils.re_alphanum(query)
            results = set()
            for term in clean_q.strip().split():
                if len(results) == 0:
                    results = Search._trie_search(term)
                else:
                    results.intersection_update(Search._trie_search(term))

            name_list = sorted(list(results), key=str.lower)
            names = Search._filter_names(name_list, query)

            if limit in (None, ''):
                limit = sys.maxsize
            for i, name in zip(range(int(limit)), names):
                hits.append({'id': str(i), 'label': name, 'value': name})

        return dict(hits=hits)

    @staticmethod
    def main(argv):
        """
        Searches and prints the results of the search term with timings
        :param argv: Command line arguments
        :return: None
        """
        from timeit import default_timer as timer

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        if len(argv) > 1:
            load_start = timer()
            Search()
            load_end = timer()
            search_start = timer()
            results = Search.search(argv[1])
            search_end = timer()

            log.debug('Results: %s', results)
            log.debug('Result Count: %s', str(len(results['hits'])))
            log.debug('Synonyms: %s', Search._get_synonyms(argv[1:]))
            log.debug('Data load time: %s', str(load_end - load_start))
            log.debug('Search time: %s', str(search_end - search_start))
        else:
            log.error('No search term specified')


if __name__ == "__main__":
    Search.main(sys.argv)
