def kab(client_id, sentence):
    """Cleans up the passed sentence, removing or reformatting invalid data.

    Args:
      client_id (str): Client ID of sentence's speaker
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
    """

    # this if loop will skip the following else loop in the case that
    # the sentence is purely Kabyle characters as per https://github.com/
    # unicode-cldr/cldr-misc-full/blob/master/main/kab/characters.json
    if set(list(sentence)).issubset(set([' ', 'a', 'b', 'c', 'č', 'd', 'ḍ', 'e',
                                         'ɛ', 'f', 'g', 'ǧ', 'ɣ', 'h', 'ḥ', 'i',
                                         'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r',
                                         'ṛ', 's', 'ṣ', 't', 'ṭ', 'u', 'w', 'x',
                                         'y', 'z', 'ẓ'])):
        pass
    else:
        # TODO: Clean up kabyle data
        pass
    
    return sentence
