import re
from typing import Pattern

from num2words import num2words


NUMS_REGEX = re.compile(r"(\d+,?\u00A0?\d+)|(\d+\w+)|(\d)+")
FIND_MULTIPLE_SPACES_REG = re.compile(r'\s{2,}')
FIND_PUNCTUATIONS_REG = re.compile(r"[/°\-,;!?.()\[\]*…—]")


def get_numbers(text):
    return NUMS_REGEX.split(text)


def replace_numbers(inp: str, locale: str, ordinal_regex: Pattern = None):
    finalinp = ''
    for e in get_numbers(inp):
        if not e:
            continue
        newinp = e
        try:
            ee = ''.join(e.split())
            if int(e) >= 0:
                newinp = num2words(int(ee), lang=locale)
        except ValueError:
            try:
                ee = ''.join(e.replace(',', '.').split())
                if float(ee):
                    newinp = num2words(float(ee), lang=locale)
            except ValueError:
                if ordinal_regex:
                    matches = ordinal_regex.match(e)
                    if matches:
                        newinp = num2words(int(matches.group(1)), ordinal=True, lang=locale)

        finalinp += newinp

    return finalinp


def maybe_normalize(value: str, mapping):
    for norm in mapping:
        if type(norm[0]) == str:
            value = value.replace(norm[0], norm[1])
        elif isinstance(norm[0], Pattern):
            value = norm[0].sub(norm[1], value)
        else:
            print('UNEXPECTED', type(norm[0]), norm[0])

    return value
