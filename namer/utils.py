def get_soup_object(url, parser="html.parser"):
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
