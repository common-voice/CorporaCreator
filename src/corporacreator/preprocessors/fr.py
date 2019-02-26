import re

from corporacreator.utils import maybe_normalize, FIND_MULTIPLE_SPACES_REG


SPELLED_ACRONYMS = {
    'ANPE',
    'APL',
    'CDI',
    'CICE',
    'DRH',
    'EDF',
    'HLM',
    'IGN',
    'INPI',
    'ISF',
    'IUT',
    'PHP',
    'PMA',
    'PME',
    'RSA',
    'RSI',
    'RTE',
    'SNCF',
    'TGV',
    'TVA',
    'UDI',
    'UMP',
    'USA',
}
REPLACE_SPELLED_ACRONYMS = [
    re.compile(r'(^|\s|\'|’)(' + '|'.join(SPELLED_ACRONYMS) + r')(\s|\.|,|\?|!|$)'),
    lambda match: f"{match.group(1)}{' '.join(match.group(2))}{match.group(3)}",
]


FR_NORMALIZATIONS = [
    ['Jean-Paul II', 'Jean-Paul deux'],
    [re.compile(r'(^|\s)/an(\s|\.|,|\?|!|$)'), r'\1par an\2'],
    [re.compile(r'(^|\s)km(\s|\.|,|\?|!|$)'), r'\1 kilomètres \2'],
    ['%', ' pourcent'],
    [re.compile(r'(^|\s)\+(\s|\.|,|\?|!|$)'), r'\1 plus \2'],
    [re.compile(r'(^|\s)m(?:2|²)(\s|\.|,|\?|!|$)'), r'\1mètre carré\2'],
    [re.compile(r'/\s?m(?:2|²)(\s|\.|,|\?|!|$)'), r' par mètre carré\1'],
    [re.compile(r'\s?€(.+)'), r' euros\1'],
    [re.compile(r'\s?€$'), r' euros'],
    [re.compile(r'(^| )(n)(?:°|º|°)(\s)?', flags=re.IGNORECASE), r'\1\2uméro '],
]


def fr(client_id, sentence):
    """Cleans up the passed sentence, removing or reformatting invalid data.

    Args:
      client_id (str): Client ID of sentence's speaker
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
    """
    text = maybe_normalize(sentence, mapping=FR_NORMALIZATIONS + [REPLACE_SPELLED_ACRONYMS])
    # TODO: restore this once we are clear on which punctuation marks should be kept or removed
    # text = FIND_PUNCTUATIONS_REG.sub(' ', text)
    text = FIND_MULTIPLE_SPACES_REG.sub(' ', text)
    return text.strip()
