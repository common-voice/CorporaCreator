def nl(user_id, sentence):
    """Cleans up the passed sentence, removing or reformatting invalid data.

    Args:
      user_id (str): User ID of sentence's speaker
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
    """
    # this if loop will skip the following else loop in the case that
    # the sentence is purely Dutch characters as per https://github.com/
    # unicode-cldr/cldr-misc-full/blob/master/main/nl/characters.json
    if set(list(sentence)).issubset(set([' ', 'a', 'á', 'ä', 'b', 'c', 'd', 'e',
                                         'é', 'ë', 'f', 'g', 'h', 'i', 'í', 'ï',
                                         'j', 'k', 'l', 'm', 'n', 'o', 'ó', 'ö',
                                         'p', 'q', 'r', 's', 't', 'u', 'ú', 'ü',
                                         'v', 'w', 'x', 'y', 'z'])):
        pass
    else:
        # TODO: Clean up dutch data
        pass
    
    return sentence
