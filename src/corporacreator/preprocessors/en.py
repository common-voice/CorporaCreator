import re
import sys
from num2words import num2words

num_comma_re    = re.compile(r'([0-9][0-9\,]+[0-9])')
def remove_commata(m):
    return m.group(1).replace(',', '')

num_currency_re = re.compile(r'(£|\$|€)(([0-9]+)(\.[0-9]+)?)')
def convert_currency(m):
    c = m.group(1)
    amount = float(m.group(2))
    str = num2words(amount, \
                    to='currency', \
                    seperator='#', \
                    currency='USD' if c == '$' else ('GBP' if c == '£' else 'EUR'),
                    lang='en')
    return str.split('#')[0] if amount.is_integer() else str.replace('#', ',')

num_suffix_re   = re.compile(r'([0-9]+%)')
def expand_suffix(m):
    return m.group(1).replace('%', ' percent')

num_decimal_re  = re.compile(r'([0-9]+\.[0-9]+)')
def convert_decimal(m):
    return num2words(m.group(1))

num_ordinal_re  = re.compile(r'([0-9]+)(st|nd|rd|th)')
def convert_ordinal(m):
    return num2words(int(m.group(1)), to='ordinal', lang='en')

num_cardinal_re = re.compile(r'([0-9]+)')
def convert_cardinal(m):
    return num2words(int(m.group(1)), lang='en')

def normalize_numbers(text):
    # the order of the following statements is crucial
    text = re.sub(num_comma_re,    remove_commata,   text)
    text = re.sub(num_currency_re, convert_currency, text)
    text = re.sub(num_suffix_re,   expand_suffix,    text)
    text = re.sub(num_decimal_re,  convert_decimal,  text)
    text = re.sub(num_ordinal_re,  convert_ordinal,  text)
    text = re.sub(num_cardinal_re, convert_cardinal, text)
    return text

abbreviations = {
    '&':    'and', 
    'e.g.': 'for example',
    'w/o':  'without'
}

def replace_abbreviations(text):
    tokens = []
    for token in text.split(' '):
        tokens.append(abbreviations[token] if token in abbreviations else token)
    return ' '.join(tokens)

def en(user_id, sentence):
    """Cleans up the passed sentence, removing or reformatting invalid data.

    Args:
      user_id (str): User ID of sentence's speaker
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str): Cleaned up sentence.
    """
    sentence = normalize_numbers(sentence)
    sentence = replace_abbreviations(sentence)
    return sentence
