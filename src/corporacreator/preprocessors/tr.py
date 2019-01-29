def tr(client_id, sentence):
    """Cleans up the passed sentence, removing or reformatting invalid data.

    Args:
      client_id (str): Client ID of sentence's speaker
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
    """
    
    # this if loop will skip the following else loop in the case that
    # the sentence is purely Turkish characters as per https://github.com/
    # unicode-cldr/cldr-misc-full/blob/master/main/tr/characters.json
    if set(list(sentence)).issubset(set([' ', 'a', 'b', 'c', 'ç', 'd', 'e', 'f',
                                         'g', 'ğ', 'h', 'ı', 'i', 'İ', 'j', 'k',
                                         'l', 'm', 'n', 'o', 'ö', 'p', 'r', 's',
                                         'ş', 't', 'u', 'ü', 'v', 'y', 'z'])):
        pass
    else:
        # TODO: Clean up turkish data
        pass
    
    return sentence
