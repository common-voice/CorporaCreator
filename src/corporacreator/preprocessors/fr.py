def fr(client_id, sentence):
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
    if set(list(sentence)).issubset(set([' ', '-', 'a', 'à', 'â', 'æ', 'b', 'c',
                                         'ç', 'd', 'e', 'é', 'è', 'ê', 'ë', 'f',
                                         'g', 'h', 'i', 'î', 'ï', 'j', 'k', 'l',
                                         'm', 'n', 'o', 'ô', 'œ', 'p', 'q', 'r',
                                         's', 't', 'u', 'ù', 'û', 'ü', 'v', 'w',
                                         'x', 'y', 'ÿ', 'z'])):
        pass
    else:
        # TODO: Clean up fr data
        pass
    
    
    return sentence
