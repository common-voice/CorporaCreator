import re

# All special characters
FILTER_SYMBOLES_REG = re.compile(
    r'[\{\}\[\]«»_\|\(\)\\…"(^—)=&\ô*'
    r'/µ#’@℗`~¹½¼¾¿º±↨↑↓▼→▲←↔∟§°‼¸‰'
    r'‘¶“”•—´☺☻♥♦♠♣•◘○◙♂►♀☼♫♪¢¦Ξ≈˜†'
    r'√ƒοΔδΛΓκιςζυσρΣγτθΘφΦηχξβωγΩΨ◊░▒▓'
    r'│├╚┼┬┴└┐┤╝╗╬╣║ßÞ═™›³ª¯¬®]+')

# Detect abreviation ex: TVA, T V A
EXCLUDE_ABBREVIATION_REG = re.compile(r'([A-Z]){2,3}|(( [A-Z] )( ?[A-Z]){1, })')



def fr(client_id, sentence):
    """Cleans up the passed sentence, removing or reformatting invalid data.

    Args:
      client_id (str): Client ID of sentence's speaker
      sentence (str): Sentence to be cleaned up.

    Returns:
      (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
    """
    # TODO: Clean up fr data

    sentence = FILTER_SYMBOLES_REG.sub('', sentence)
    return sentence
