import re
QUESTION_MARK_IN_WORD = re.compile(r'\?[aābcčdeēfgģhiījkķlļmnņoprsštuūvzž]')


def _remove_sentences_with_broken_encoding(sentence):
    """Will remove invalid sentences that have broken encoding, e.g. "?" in the middle of the word.

    Args:
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str, None): Returns the sentence 'as-is', if no broken encoding was found.
                   Returns None if broken encoding is found.
    """
    if bool(re.search(QUESTION_MARK_IN_WORD, sentence)):
        return None

    return sentence


def lv(client_id, sentence):
    """Will process Latvian sentences.

    Args:
      client_id (str): Client ID of sentence's speaker
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
    """
    sentence = _remove_sentences_with_broken_encoding(sentence)

    return sentence
