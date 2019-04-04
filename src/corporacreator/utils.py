import re
from typing import Pattern


FIND_MULTIPLE_SPACES_REG = re.compile(r'\s{2,}')
FIND_PUNCTUATIONS_REG = re.compile(r"[/°\-,;!?.()\[\]*…—«»]")


def maybe_normalize(value: str, mapping):
    for norm in mapping:
        if isinstance(norm[0], str):
            value = value.replace(norm[0], norm[1])
        elif isinstance(norm[0], Pattern):
            value = norm[0].sub(norm[1], value)
        else:
            raise ValueError(f'expect first parameter to be a string or a regex, not {norm[0]}')

    return value
