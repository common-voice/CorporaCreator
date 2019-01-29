def cy(client_id, sentence):
    """Cleans up the passed sentence, removing or reformatting invalid data.

    Args:
      client_id (str): Client ID of sentence's speaker
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
    """
    # TODO: Clean up cy data

    # make sure all spaces are normal, single spaces
    sentence = sentence.replace("’","'")
    sentence = sentence.replace("wwna","wna")
    sentence = sentence.replace("\\\\tungellog","ungellog")

    # TODO: geiriau Saesneg / English inspired/pronunced words:
    # wallace, celsius, ddiesel, wicipedia, william, chiswell, f., h.

    # this if loop will skip the following else loop in the case that
    # the sentence is purely Welsh characters as per https://github.com/
    # unicode-cldr/cldr-misc-full/blob/master/main/cy/characters.json
    if set(list(sentence)).issubset(set([' ', 'a','á', 'à', 'â', 'ä', 'b', 'c',
                                         'd', 'e', 'é', 'è', 'ê', 'ë', 'f', 'g',
                                         'h', 'i', 'í', 'ì', 'î', 'ï', 'j', 'l',
                                         'm', 'n', 'o', 'ó', 'ò', 'ô', 'ö', 'p',
                                         'r', 's', 't', 'u', 'ú', 'ù', 'û', 'ü',
                                         'w', 'ẃ', 'ẁ', 'ŵ', 'ẅ', 'y', 'ý', 'ỳ',
                                         'ŷ', 'ÿ'])):
        pass
    else:
        # Not all chars are in the Welsh alphabet!
        # more processing needed here!
        pass

    return sentence
