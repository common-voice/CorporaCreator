import re

from corporacreator.utils import maybe_normalize, replace_numbers, FIND_PUNCTUATIONS_REG, FIND_MULTIPLE_SPACES_REG

FIND_ORDINAL_REG = re.compile(r"(\d+)([ème|éme|ieme|ier|iere]+)")


FR_NORMALIZATIONS = [
    [re.compile(r'(^|\s)(\d+)\s(0{3})(\s|\.|,|\?|!|$)'), r'\1\2\3\4'],  # "123 000 …" => "123000 …"
    [re.compile(r'(^|\s)km(\s|\.|,|\?|!|$)'), r'\1 kilomètres \2'],
    [re.compile(r'(^|\s)0(\d)(\s|\.|,|\?|!|$)'), r'\1zéro \2 \3'],
    ['%', ' pourcent'],
    [re.compile(r'(^|\s)\+(\s|\.|,|\?|!|$)'), r'\1 plus \2'],
    [re.compile(r'(\d+)\s?m(?:2|²)(\s|\.|,|\?|!|$)'), r'\1 mètre carré\2'],
    [re.compile(r'(^|\s|/)m(?:2|²)(\s|\.|,|\?|!|$)'), r' mètre carré\2'],
    [re.compile(r'(^|\s)(\d+),(\d{2})\s?€(\s|\.|,|\?|!|$)'), r'\1\2 euros \3 \4'],
    [re.compile(r'\s?€(.+)'), r' euros\1'],
    [re.compile(r'\s?€$'), r' euros'],
    [re.compile(r'(^| )(n)(?:°|º|°)(\s)?', flags=re.IGNORECASE), r'\1\2uméro '],
    [re.compile(r'(^|\s)(\d+)h(\d*)(\s|\.|,|$)'), r'\1\2 heure \3\4'],
    [re.compile(r'(^|\s)(\d+)h(\s|\.|,|$)'), r'\1\2 heure \3'],
]


def fr(client_id, sentence):
    """Cleans up the passed sentence, removing or reformatting invalid data.

    Args:
      client_id (str): Client ID of sentence's speaker
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
    """
    text = maybe_normalize(sentence, mapping=FR_NORMALIZATIONS)
    text = replace_numbers(text, locale='fr', ordinal_regex=FIND_ORDINAL_REG)
    text = text.replace('’', "'").replace('\u00A0', ' ')
    text = FIND_PUNCTUATIONS_REG.sub(' ', text)
    text = FIND_MULTIPLE_SPACES_REG.sub(' ', text)
    return text.strip().lower()
