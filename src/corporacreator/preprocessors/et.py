def et(client_id, sentence):
    """Cleans up the passed sentence, removing or reformatting invalid data.
    Args:
      client_id (str): Client ID of sentence's speaker
      sentence (str): Sentence to be cleaned up.
    Returns:
      (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
    """
    # this if loop will skip the following else loop in the case that
    # the sentence is purely Estonian characters as per https://github.com/
    # unicode-cldr/cldr-misc-full/blob/master/main/et/characters.json
    if set(list(sentence)).issubset(set([' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g',
                                         'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                                         'p', 'q', 'r', 's', 'š', 'z', 'ž', 't',
                                         'u', 'v', 'w', 'õ', 'ä', 'ö', 'ü', 'x',
                                         'y'])):
        pass
    else:
        pass
        # TODO: Clean up estonian data

    
    return sentence
