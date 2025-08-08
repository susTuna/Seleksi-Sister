import re

LETTER_PATTERNS = {
    'a': '[aA4@]',
    'b': '[bB8]',
    'c': '[cC\\(]',
    'd': '[dD]',
    'e': '[eE3€]',
    'f': '[fF]',
    'g': '[gG9]',
    'h': '[hH]',
    'i': '[iI1!|]',
    'j': '[jJ]',
    'k': '[kK]',
    'l': '[lL1|]',
    'm': '[mM]',
    'n': '[nN]',
    'o': '[oO0]',
    'p': '[pP]',
    'q': '[qQ]',
    'r': '[rR]',
    's': '[sS5$]',
    't': '[tT7+]',
    'u': '[uU]',
    'v': '[vV]',
    'w': '[wW]',
    'x': '[xX\\*]',
    'y': '[yY]',
    'z': '[zZ2]',
    # Non-letter characters
    ' ': '\\s*',
    '.': '[\\.]',
    ',': '[\\,]',
    '?': '[\\?]',
    '!': '[\\!]'
}

def word_to_regex_pattern(word):
    pattern = ''
    for char in word.lower():
        if char in LETTER_PATTERNS:
            pattern += LETTER_PATTERNS[char]
        else:
            pattern += re.escape(char)
    return pattern

def email_validator(email: str) -> bool:
    import re
    email_regex = r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$'
    return re.match(email_regex, email) is not None