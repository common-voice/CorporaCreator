import re
import unicodedata

from urllib.parse import unquote
from html.parser import HTMLParser


RE_DIGITS = re.compile('\d')

def _has_digit(sentence):
    return RE_DIGITS.search(sentence)


class _HTMLStripper(HTMLParser):
    """Class that strips HTML from strings.

    Examples:
        >>> stripper = _HTMLStripper()
        >>> stripper.feed(html)
        >>> nohtml = stripper.get_data()
    """

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return "".join(self.fed)


def _strip_tags(html):
    """Removes HTML tags from passed text.

    Args:
      html (str): String containing HTML

    Returns:
      (str): String with HTML removed
    """
    s = _HTMLStripper()
    s.feed(html)
    return s.get_data()


def _strip_string(sentence):
    """Cleans a string based on a whitelist of printable unicode categories.

    You can find a full list of categories here:
    http://www.fileformat.info/info/unicode/category/index.htm
    """
    letters     = ('LC', 'Ll', 'Lm', 'Lo', 'Lt', 'Lu')
    numbers     = ('Nd', 'Nl', 'No')
    marks       = ('Mc', 'Me', 'Mn')
    punctuation = ('Pc', 'Pd', 'Pe', 'Pf', 'Pi', 'Po', 'Ps')
    symbol      = ('Sc', 'Sk', 'Sm', 'So')
    space       = ('Zs',)

    allowed_categories = letters + numbers + marks + punctuation + symbol + space

    return u''.join([c for c in sentence if unicodedata.category(c) in allowed_categories])


def common(sentence):
    """Cleans up the passed sentence in a language independent manner, removing or reformatting invalid data.

    Args:
      sentence (str): Sentence to be cleaned up.

    Returns:
      (is_valid,str): A boolean indicating validity and cleaned up sentence.
    """

    # Define a boolean indicating validity
    is_valid = True
    # Decode any URL encoded elements of sentence
    sentence = unquote(sentence)
    # Remove any HTML tags
    sentence = _strip_tags(sentence)
    # Remove non-printable characters
    sentence = _strip_string(sentence)
    # collapse all whitespace and replace with single space
    sentence = (' ').join(sentence.split())
    # TODO: Clean up data in a language independent manner
    # If the sentence contains digits reject it
    if _has_digit(sentence):
        is_valid = False
    # If the sentence is blank reject it
    if not sentence.strip():
        is_valid = False
    return (is_valid, sentence)
