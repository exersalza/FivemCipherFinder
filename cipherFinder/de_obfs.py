import re
import random
from collections.abc import Generator


VAR_NAMES = [  # Just random names bc we the hell dont know what happens in that script
    'gg',
    'gyros',
    'fries',
    'rizz',
    'taco',
    'bell',
    'uber',
    'deez',
    'nuts',
    'hell',
    'towlie'
]

REGEX = [    
    r'(function\s*\(((\w+(,(\s?))?)*)\))',
    r'((local(\s+)?(\w+)))'
]


def grap(ls: list) -> str:
    """ Get Random And Pop (grap)

    Parameters
    ----------
    ls : list
        Give the list from where you want a random value of.

    Returns
    -------
    str
        the popped string
    """

    f = random.choice(ls)
    ls.remove(f)
    return f


def do_regex(_line: str, regex: str) -> list:
    """ Do the regex template stuff
    
    Parameters
    ----------
    regex : str
        The regex to search for in _line

    Returns
    -------
    list
        The list with the found groups

    """
    return re.findall(regex, rf'{_line}', 
                      re.MULTILINE and re.IGNORECASE)


def do_list_addition(char_set: list) -> Generator:
    """ Does not directly adds stuff to the list BUT it yields content
    to create one

    Parameters
    ----------
    char_set : list
        Give a list to yield values from

    """
    for i in char_set:
       yield i[1].strip('local ').split(',')


def de_obfs_code(_line: str, _ret: list) -> str:
    """ Trys to de De-Obfuscate the trigger line
    
    Returns
    -------
    str
        the decoded string
    """
    code = ''
    var = []
    names = VAR_NAMES

    for i in REGEX:
        if x := do_regex(_line, i): 
            for j in do_list_addition(x):
                var.extend(j)
    
    for i in var:
        _line = _line.replace(i.strip(), grap(names))
    
    for v, t in de_obfs_char(_ret):
        _line = _line.replace(t.strip('"'), v)

    return code


def de_obfs_char(found: list) -> list: 
    """ De-Obfuscate the \x23... lines

    Parameters
    ----------
    found : list[tuple]
       Give the found lines.

    Returns
    -------
    list[tuple]
        Give the decoded lines back with the original version.

    """
    temp = []

    for j in found:
        t = ''
        # Get rid of the x and backslashes.
        for i in (j[0].strip('"').replace('\\', '')).split('x'):
            if i == '':
                continue

            t += chr(int(i, 16))
        temp.append((t, j[0]))
    return temp


def de_obfs(_ret: list, _line: str) -> str:
    return de_obfs_code(_line, _ret)

