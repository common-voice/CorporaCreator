def eo(user_id, sentence):
    """Cleans up the passed sentence, removing or reformatting invalid data.

    Args:
      user_id (str): User ID of sentence's speaker
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
    """
    
    # this if loop will skip the following else loop in the case that
    # the sentence is purely Esperanto characters as per https://github.com/
    # unicode-cldr/cldr-misc-full/blob/master/main/eo/characters.json
    if set(list(sentence)).issubset(set([' ', 'a', 'b', 'c', 'ĉ', 'd', 'e', 'f',
                                         'g', 'ĝ', 'h', 'ĥ', 'i', 'j', 'ĵ', 'k',
                                         'l', 'm', 'n', 'o', 'p', 'r', 's', 'ŝ',
                                         't', 'u', 'ŭ', 'v', 'z'])):
        pass
    else:
        # TODO: Clean up eo data
        pass
   
    return sentence
