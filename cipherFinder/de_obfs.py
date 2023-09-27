#!/bin/python3.11

import re
import random

from collections.abc import Generator

# Just random names bc we dont know what
# happens in that script
VAR_NAMES = [
    "gg",
    "rizz",
    "taco",
    "bell",
    "uber",
    "deez",
    "nuts",
    "jugz",
    "hell",
    "gyros",
    "fries",
    "towlie",
    "things",
]

TABLE_REGEX = r"(\{([^{}]+)\})"
REGEX = [
    r"((local(\s+)?(\w+)))",
    r"(function\s*\(((\w+(,(\s?))?)*)\))",
]


def grap(ls: list) -> str:
    """Get Random And Pop (grap)

    Parameters
    ----------
    ls : list
        Give the list from where you want a random value of.

    Returns
    -------
    str
        the popped string
    """
    # WHY PYTHON WHY
    if not ls:
        return random.choice(VAR_NAMES)

    f = random.choice(ls)
    ls.remove(f)
    return f


def do_regex(line: str, regex: str) -> list:
    """Do the regex template stuff

    Parameters
    ----------
    line : str
        Give the line to check to regex on
    regex : str
        The regex to search for in line

    Returns
    -------
    list
        The list with the found groups

    """
    return re.findall(regex, rf"{line}", re.MULTILINE and re.IGNORECASE)


def do_list_addition(char_set: list) -> Generator:
    """Does not directly adds stuff to the list BUT it yields content
    to create one

    Parameters
    ----------
    char_set : list
        Give a list to yield values from

    """
    for i in char_set:
        _t = i[1].strip("local").strip()

        yield [w.strip() for w in _t.split(",")]


def get_table_contents(line: str) -> list:
    """Get the values inside the lua table

    Parameters
    ----------
    line : str
        Give the line to find the table and get it's content

    Returns
    -------
    list :
        Return the list with found values

    """
    _t = []

    if not (_f := do_regex(line, TABLE_REGEX)):
        return _t

    for i in _f[0][1].split(","):
        _t.append(i.strip())

    return _t


def de_obfs_code(line: str, ret: list) -> str:
    """Trys to De-Obfuscate the trigger line

    Returns
    -------
    str
        the decoded string
    """
    var = []
    names = []
    grap_names = VAR_NAMES[:]

    for i in REGEX:
        if x := do_regex(line, i):
            for j in do_list_addition(x):
                var.extend(j)

    for i in var:
        name = grap(grap_names)
        names.append(name)
        line = line.replace(i.strip(), name)

    for v, t in de_obfs_char(ret):
        line = line.replace(t.strip('"'), v)

    # Prevent false positives, at least we hope it does
    if not (table := get_table_contents(line)):
        return line

    t_re = rf"({names[0]}\[\d+\])"
    omfg = set(do_regex(line, t_re))  # as the name tells, it was annoying

    for i, c in enumerate(sorted(omfg)):
        line = line.replace(c, table[i])

    return line


def de_obfs_char(found: list) -> list:
    """De-Obfuscate the \x23... lines

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
            if not i:
                continue

            t += chr(int(i, 16))
        temp.append((t, j[0]))

    return temp


def de_obfs(ret: list, line: str) -> str:
    """Just another way to entry the de-obfuscation

    Parameters
    ----------
    ret : list
        Give the ret list

    line : str
        Give the line to do stuff on

    Returns
    -------
    str
        Returns the de obfuscated code
    """
    return de_obfs_code(line, ret)
