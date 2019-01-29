def ky(client_id, sentence):
    """Cleans up the passed sentence, removing or reformatting invalid data.

    Args:
      client_id (str): Client ID of sentence's speaker
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
    """
    # this if loop will skip the following else loop in the case that
    # the sentence is purely Kyrgyz characters as per https://github.com/
    # unicode-cldr/cldr-misc-full/blob/master/main/ky/characters.json
    if set(list(sentence)).issubset(set([' ', 'а', 'б', 'г', 'д', 'е', 'ё', 'ж',
                                         'з', 'и', 'й', 'к', 'л', 'м', 'н', 'ң',
                                         'о', 'ө', 'п', 'р', 'с', 'т', 'у', 'ү',
                                         'х', 'ч', 'ш', 'ъ', 'ы', 'э', 'ю',
                                         'я'])):
        pass
    else:
        # TODO: Clean up kyrgyz data
        pass
    return sentence
