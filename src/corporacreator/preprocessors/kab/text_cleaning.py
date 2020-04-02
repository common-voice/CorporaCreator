# created by Mestafa Kamal

import string
import collections

allowed = list(string.ascii_lowercase)
allowed.append("-")
allowed.append(" ")
allowed.extend(list("ẓṛṭɛṣḍǧḥɣč"))


replacer = {
    "àáâãåāăąǟǡǻȁȃȧâä": "a",
    "ǣǽ": "æ",
    "çćĉċ": "c",
    "ďđ": "d",
    "èéêëēĕėęěȅȇȩîêë": "e",
    "ĝġģǥǵ": "g",
    "ğ": "ǧ",
    "Ğ": "Ǧ",
    "ĥħȟ": "h",
    "ìíîïĩīĭįıȉȋîï": "i",
    "ĵǰ": "j",
    "ķĸǩǩκ": "k",
    "ĺļľŀł": "l",
    "м": "m",
    "ñńņňŉŋǹ": "n",
    "òóôõøōŏőǫǭǿȍȏðοöô": "o",
    "ŕŗřȑȓ": "r",
    "śŝşšș": "s",
    "γ": "ɣ",
    "Γ": "Ɣ",
    "ε": "ɛ",
    "σ": "ɛ",
    "ťŧț": "t",
    "ùúûũūŭůűųȕȗüû": "u",
    "ŵ": "w",
    "ýÿŷ": "y",
    "źżžȥ": "z",
    "ß": "ss",
}

punctuation = [
    "'",
    '"',
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
]

replacements = {}

for all, replacement in replacer.items():
    for to_replace in all:
        replacements[to_replace] = replacement

# print(allowed)


def remplaceSymbols(word):
    result = word
    for to_replace, replacement in replacements.items():
        result = result.replace(to_replace, replacement)
    return result


def removePunctuation(word):
    for i in word:
        if i in punctuation or i not in allowed:
            word = word.replace(i, "")
    return word


def cleanWord(word):
    word = word.lower()
    word = remplaceSymbols(word)
    word = replaceTs(word)
    word = removePunctuation(word)
    return word


def removeBadSpace(sentence):
    sentence = sentence.replace(" -", "-")
    sentence = sentence.replace("- ", "-")
    return sentence


def replaceTs(word):
    if word.endswith("ţţ"):
        word = word[0:-2] + "t"
    elif word.endswith("ţ"):
        word = word[0:-1] + "t"
    word = word.replace("ţţ", "tt")
    word = word.replace("ţ", "tt")
    return word


def cleanSentence(sentence):

    sentence = removeBadSpace(sentence)
    words = sentence.strip().split(" ")
    cleanedWords = []

    for word in words:
        word = cleanWord(word)
	word = word.strip()
        cleanedWords.append(word)

    result = " ".join(cleanedWords)
    return result

