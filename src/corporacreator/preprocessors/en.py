def en(client_id, sentence):
    """Cleans up the passed sentence, removing or reformatting invalid data.

    Args:
      client_id (str): Client ID of sentence's speaker
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
    """
    ## collapse all apostrophe-like marks
    ## e.g. common_voice_en_18441344.mp3	‘I’m not a serpent!’ --> 'I'm not a serpent!'
    sentence = sentence.replace("’","'") # right-ticks --> apostrophes
    sentence = sentence.replace("‘","'") # left-ticks --> apostrophes
    return sentence
