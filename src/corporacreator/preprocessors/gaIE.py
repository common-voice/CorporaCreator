def gaIE(client_id, sentence):
    """Cleans up the passed sentence, removing or reformatting invalid data.

    Args:
      client_id (str): Client ID of sentence's speaker
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
    """
    # this if loop will skip the following else loop in the case that
    # the sentence is purely Irish Gaelic characters as per https://github.com/
    # unicode-cldr/cldr-misc-full/blob/master/main/ga/characters.json
    if set(list(sentence)).issubset(set([' ', 'a', 'á', 'b', 'c', 'd', 'e', 'é',
                                         'f', 'g', 'h', 'i', 'í', 'l', 'm', 'n',
                                         'o', 'ó', 'p', 'r', 's', 't', 'u',
                                         'ú'])):
        pass
    else:
        # TODO: Clean up ga-IE data
        pass
    
    
    return sentence
