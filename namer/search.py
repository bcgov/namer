from pytrie import SortedStringTrie as Trie


def search():
    trie = Trie()
    trie.update({'an': 0})
    trie.update({'ant': 1})
    trie.update({'all': 2})
    trie.update({'allot': 3})
    trie.update({'alloy': 4})
    trie.update({'aloe': 5})
    trie.update({'are': 6})
    trie.update({'be': 7})

    print(trie.keys(prefix='al'))
    print(trie.items(prefix='an'))
    print(trie.longest_prefix('antonym'))
    print(trie.longest_prefix_item('allstar'))
    print(trie.longest_prefix_value('area', default='N/A'))
    print(trie.longest_prefix_value('alsa', default=-1))
    print(list(trie.iter_prefixes('allotment')))
    print(list(trie.iter_prefix_items('antonym')))


if __name__ == "__main__":
    search()
