def it(client_id, sentence):
    """Cleans up the passed sentence, removing or reformatting invalid data.

    Args:
      client_id (str): Client ID of sentence's speaker
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
    """
    # this if loop will skip the following else loop in the case that
    # the sentence is purely Italian characters as per https://github.com/
    # unicode-cldr/cldr-misc-full/blob/master/main/it/characters.json
    if set(list(sentence)).issubset(set([' ', 'a', 'à', 'b', 'c', 'd', 'e', 'é',
                                         'è', 'f', 'g', 'h', 'i', 'ì', 'j', 'k',
                                         'l', 'm', 'n', 'o', 'ó', 'ò', 'p', 'q',
                                         'r', 's', 't', 'u', 'ù', 'v', 'w', 'x',
                                         'y', 'z'])):
        pass
    else:
        # TODO: Clean up italian data
        pass
    
    return sentence
