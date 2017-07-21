def clean_string(string):
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
