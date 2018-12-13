from urllib.parse import unquote

def common(sentence):
    """Cleans up the passed sentence in a language independent manner, removing or reformatting invalid data.

    Args:
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str): Cleaned up sentence.
    """
    # Decode any URL encoded elements of sentence
    sentence = unquote(sentence)
    # TODO: Clean up data in a language independent manner
    return sentence
