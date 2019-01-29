def sl(client_id, sentence):
    """Cleans up the passed sentence, removing or reformatting invalid data.

    Args:
      client_id (str): Client ID of sentence's speaker
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
    """
    # this if loop will skip the following else loop in the case that
    # the sentence is purely Slovenian characters as per https://github.com/
    # unicode-cldr/cldr-misc-full/blob/master/main/sl/characters.json
    if set(list(sentence)).issubset(set([' ', 'a', 'b', 'c', 'č', 'd', 'e', 'f',
                                         'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                                         'o', 'p', 'r', 's', 'š', 't', 'u', 'v',
                                         'z', 'ž'])):
        pass
    else:
        # TODO: Clean up slovenian data
        pass
    
    return sentence
