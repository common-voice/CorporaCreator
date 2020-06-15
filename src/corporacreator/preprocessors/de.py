import re
QUOTE_PATTERN = re.compile(r'^\"{3}(.*)\"{2}(.*)\"{1}$')
QUOTE_PATTERN_2 = re.compile(r'^\"{1}(.*)\"{2}(.*)\"{2}(.*)\"{1}$')
QUOTE_PATTERN_3 = re.compile(r'^\"{1}(.*)\"{1}$')


def _change_multi_quotes(sentence):
    """Changes all quotes from patterns like
    [\"""content""content"] to ["content"content] or
    ["content""content""content"] to [content"content"content] or
    ["content" to content]

    Args:
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str): Cleaned up sentence. Returns the sentence 'as-is', if matching
      did not work as expected
    """
    matches = QUOTE_PATTERN.match(sentence)  # pattern: \"\"\"content\"\"content\"
    matches2 = QUOTE_PATTERN_2.match(sentence)  # pattern: \"content\"\"content\"\"content\"
    matches3 = QUOTE_PATTERN_3.match(sentence)  # patter: \"content\"

    if matches is not None and matches.lastindex == 2:
        return "\"{}\"{}".format(matches.group(1), matches.group(2))
    elif matches2 is not None and matches2.lastindex == 3:
        return "{}\"{}\"{}".format(matches2.group(1), matches2.group(2), matches2.group(3))
    elif matches3 is not None and matches3.lastindex == 1:
        return "{}".format(matches3.group(1))

    return sentence


def de(client_id, sentence):
    """Cleans up the passed sentence, removing or reformatting invalid data.

    Args:
      client_id (str): Client ID of sentence's speaker
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
    """
    sentence = _change_multi_quotes(sentence)

    # TODO: Clean up de data
    return sentence
