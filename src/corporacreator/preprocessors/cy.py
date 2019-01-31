# compile the set of the alphabet just once
alphabet = set([' ', 'a','á', 'à', 'â', 'ä', 'b', 'c',
                'd', 'e', 'é', 'è', 'ê', 'ë', 'f', 'g',
                'h', 'i', 'í', 'ì', 'î', 'ï', 'j', 'l',
                'm', 'n', 'o', 'ó', 'ò', 'ô', 'ö', 'p',
                'r', 's', 't', 'u', 'ú', 'ù', 'û', 'ü',
                'w', 'ẃ', 'ẁ', 'ŵ', 'ẅ', 'y', 'ý', 'ỳ',
                'ŷ', 'ÿ'])

def cy(client_id, sentence):
    """
    Cleans up the passed sentence, removing or reformatting invalid data.
    Args:
      client_id (str): Client ID of sentence's speaker
      sentence (str): Sentence to be cleaned up.
      alphabet (set): set of unique, lowercased characters in language.

    Returns:
      (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
    """
    # TODO: geiriau Saesneg / English inspired/pronunced words:
    # wallace, celsius, ddiesel, wicipedia, william, chiswell, f., h.

    # this if loop will skip the following else loop in the case that
    # the sentence is purely Welsh characters as per https://github.com/
    # unicode-cldr/cldr-misc-full/blob/master/main/cy/characters.json
    if set(sentence.lower()).issubset(alphabet):
        pass
    else:
        # Not all chars are in the Welsh alphabet!
        # more processing needed here!
        sentence = sentence.replace(",", "") # remove commas
        sentence = sentence.replace("’", "'") # fix apostrophes
        sentence = sentence.replace("wwna", "wna")
        sentence = sentence.replace(" siwr ", " siŵr ")
        sentence = sentence.replace("\\tungellog"," ungellog")
        
    return sentence
