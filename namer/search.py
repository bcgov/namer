import bisect
import csv
import os
import re

from pytrie import SortedStringTrie as Trie


class Search(object):
    def __init__(self):
        """Initialization"""
        self.search_trie = None

        self._init_searchtrie()

    def _init_searchtrie(self):
        """Builds the searchtrie from input data into memory"""
        file_path = os.path.join(os.path.dirname(__file__), '..', 'files',
                                 'data-100k.csv')
        if os.path.isfile(file_path) and self.search_trie is None:
            self.search_trie = Trie()
            self.load_data(file_path)

    def load_data(self, file_path):
        """
        Temporary Proof of concept function
        Loads information from CSV file
        Parses and splits CORP_NME for search_trie
        """
        with open(file_path) as file:
            reader = csv.DictReader(file, delimiter=';')
            try:
                for row in reader:
                    clean_name = re.sub(r'[^a-zA-Z\d\s]', '', row['CORP_NME'])
                    for element in clean_name.split():
                        if element is not None:
                            if element not in self.search_trie:
                                self.search_trie[element] = set()
                            self.search_trie[element].add(row['CORP_NUM'])
            except UnicodeDecodeError:
                print('Unexpected input at line ' + reader.line_num)

    def search(self, prefix):
        """Searches and returns a list of values which match the key"""
        try:
            print(self.search_trie[prefix])
            print(prefix in self.search_trie)
            return self.search_trie.itervalues(prefix)

        except KeyError:
            return None

if __name__ == "__main__":
    from timeit import default_timer as timer

    engine = Search()
    start = timer()
    results = engine.search('ESTATE')
    end = timer()
    for result in results:
        print(result)
    print('Search time: ' + str(end - start))
