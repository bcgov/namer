def get_soup_object(url, parser="html.parser"):
    """
    Parses an HTML URL and returns a parseable BeautifulSoup object
    :param url: HTML URL to parse
    :param parser: Parser type to use
    :return: BeautifulSoup Object
    """
    from requests import get
    from bs4 import BeautifulSoup

    return BeautifulSoup(get(url).text, parser)


def re_alphanum(string):
    """
    Removes non-alphanumeric characters
    :param string: Input string
    :return: Sanitized string
    """
    import re

    if string is not None:
        return re.sub(r'[^a-zA-Z\d\s]', '', string)
    else:
        return string
