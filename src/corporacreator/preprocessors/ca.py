def ca(client_id, sentence):
    """Cleans up the passed sentence, removing or reformatting invalid data.

    Args:
      client_id (str): Client ID of sentence's speaker
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
    """
    # this if loop will skip the following else loop in the case that
    # the sentence is purely Welsh characters as per https://github.com/
    # unicode-cldr/cldr-misc-full/blob/master/main/ca/characters.json
    if set(list(sentence)).issubset(set([' ', '·', 'a', 'à', 'b', 'c', 'ç', 'd',
                                         'e', 'é', 'è', 'f', 'g', 'h', 'i', 'í',
                                         'ï', 'j', 'k', 'l', 'm', 'n', 'o', 'ó',
                                         'ò', 'p', 'q', 'r', 's', 't', 'u', 'ú',
                                         'ü', 'v', 'w', 'x', 'y', 'z'])):
        pass
    else:
        pass
    # TODO: Clean up ca data
    return sentence
