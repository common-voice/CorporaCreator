def cy(client_id, sentence):
    """
    Cleans up the passed sentence, removing or reformatting invalid data.
    Args:
      client_id (str): Client ID of sentence's speaker
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
    """
    # TODO: geiriau Saesneg / English inspired/pronunced words:
    # wallace, celsius, ddiesel, wicipedia, william, chiswell, f., h.

    sentence = sentence.replace("’", "'") # fix apostrophes
    sentence = sentence.replace("wwna", "wna")
    sentence = sentence.replace(" siwr ", " siŵr ")
    sentence = sentence.replace("\\tungellog"," ungellog")
        
    return sentence
