# created by Mestafa Kamal

import string


"""
Keep Upper case
Keep Punctuation

Replace wrong characters
Remove bad spaces

Strip
Unvalidate sentences containing not allowed characters
"""


allowed = list(string.ascii_lowercase)
allowed.extend(list("ẓṛṭɛṣḍǧḥɣč"))


majuscule = []

for i in allowed:
    majuscule.append(i.upper())

allowed.extend(list(majuscule))

print(allowed)

replacer = {
    "Ğ": "Ǧ",
    "ğ": "ǧ",
    "Γ": "Ɣ",
    "γ": "ɣ",
    "Σ": "Ɛ",
    "εσ": "ɛ",
    "«»“”": "\"",
}

punctuation = [
    " ",
    "-",    
    ".",
    "?",
    ",",
    "!",
    ";",
    "_",
    ":",
    "/",
    "(",
    ")",
    "{",
    "}",
    "[",
    "]",
    "\"",
]

replacements = {}

for all, replacement in replacer.items():
    for to_replace in all:
        replacements[to_replace] = replacement


def remplaceSymbols(word):
    result = word
    for to_replace, replacement in replacements.items():
        result = result.replace(to_replace, replacement)
    return result


def removeBadSpace(sentence):
    sentence = sentence.replace(" -", "-")
    sentence = sentence.replace("- ", "-")
    return sentence


def replaceTs(word):
    if word.endswith("ţţ"):
        word = word[0:-2] + "t"
    elif word.endswith("-ţ"):
        word = word[0:-2] + "-tt"
    elif word.endswith("ţ"):
        word = word[0:-1] + "t"
    word = word.replace("ţţ", "tt")
    word = word.replace("ţ", "tt")
    return word

def checkSentence (sentence):
    for i in sentence:
        if i  not in allowed and i not in punctuation:
               return False
    return True


def cleanSentence(sentence):

    sentence = removeBadSpace(sentence)
    sentence = remplaceSymbols(sentence)

    words = sentence.strip().split(" ")
    cleanedWords = []

    for word in words:
        word = replaceTs(word)
        word = word.strip()
        cleanedWords.append(word)

    result = " ".join(cleanedWords)

    if (checkSentence(result)==False):
        return " "
        
    return result
