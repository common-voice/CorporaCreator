def br(client_id, sentence):
    """Cleans up the passed sentence, removing or reformatting invalid data.

    Args:
      client_id (str): Client ID of sentence's speaker
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
    """
    sentence = sentence.replace("'", "ʼ")

        # this if loop will skip the following else loop in the case that
    # the sentence is purely Welsh characters as per https://github.com/
    # unicode-cldr/cldr-misc-full/blob/master/main/br/characters.json
    if set(list(sentence)).issubset(set([' ', 'a', 'b', 'c', 'ʼ', 'd', 'e', 'ê',
                                         'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                                         'n', 'ñ', 'o', 'p', 'r', 's', 't', 'u',
                                         'ù', 'v', 'w', 'x', 'y', 'z'])):
        pass
    else:
        # TODO: Clean up non-standard br data here
        pass
    
    return sentence
