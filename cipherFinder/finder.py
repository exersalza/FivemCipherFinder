#!/bin/python3.11

#  Copyright (c) 2022-2023 - exersalza
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal # noqa
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all # noqa
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, # noqa
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE # noqa
#  SOFTWARE.
from __future__ import annotations
from datetime import datetime as dt

import os
import sys
import platform
import argparse
import requests

from gibberish_detector import detector

from cipherFinder.de_obfs import de_obfs, do_regex

REGEX = r"(((\\x|\\u)([a-fA-F0-9]{2}))+)"
URL_REGEX = (
    r"(https?://(www\.)?[-\w@:%.\+~#=]{2,256}\."
    r"[a-z]{2,4}\b([-\w@:%\+.~#?&//=]*))"
)
COLORS = ["\033[0m", "\033[91m", "\033[92m"]
RAW_BIG_MODEL = (
    "https://raw.githubusercontent.com/exersalza/"
    "FivemCipherFinder/main/big.model"
)

log = []


def get_big_model_file() -> int:
    """Get the big.model file from GitHub.

    Returns
    -------
    int :
        status code

    """
    if os.path.exists("./big.model"):
        os.remove("./big.model")

    with open("big.model", "wb") as _file:
        for chunk in requests.get(
            RAW_BIG_MODEL, stream=True, timeout=5
        ).iter_content(chunk_size=8192):
            if not chunk:
                continue

            _file.write(chunk)
    return 0


def validate_lines(lines: list) -> list[tuple]:
    """Validate the lines that are given through the 'lines' parameter.

    Parameters
    ----------
    lines : list
        The lines from the current read file.

    Returns
    -------
    list[tuple]
        A list with infected line
        (or false positives by AntiCheat or obfuscated code)
    """

    ret: list[tuple] = []

    for ln, line in enumerate(lines, start=1):  # ln: lineNumber
        # get all the lines that match the regex
        if x := do_regex(line, REGEX):
            ret.append((ln, line, de_obfs(x, line)))
    return ret


def do_gibberish_check(lines: list) -> list[tuple[str, int, str]]:
    """Do a check if the given lines are making any sens.
    Can still throw false-positives

    Parameters
    ----------
    lines : list
        The lines from the current read file.

    Returns
    -------
    list[tuple[str, int, str]]
        A Tuple List with infected lines or false positives
        as in `validate_lines`.

    """

    det = detector.create_from_model("./big.model")  # should work for now
    l_counter = 1
    matches = []

    for i in lines:
        if "local" in i and det.is_gibberish(rf"{i}"):
            matches.append(
                (l_counter, i, "Can't de obfuscate due to use of --v2")
            )

        l_counter += 1
    return matches


def prepare_log_line(**kw) -> int:
    """Prepares the string for the logging

    Parameters
    ----------
    kw : str, Any
        Somevalues listed below

    Returns
    -------
    int
        Returns the current count
    """
    d = kw.pop("d", ".")
    ln = kw.pop("ln", "")
    file = kw.pop("file", "poggers.lua")
    line = kw.pop("line", "")
    count = kw.pop("count", 0)
    target = kw.pop("target", "")
    logged = kw.pop("logged", {})

    path = d.replace("\\", "/") + f"/{file}"
    url = ""

    if x := do_regex(target, URL_REGEX):
        url = x[0][0]

    # prevent printing stuff twice to the log file
    if logged.get(path, -1) == ln:
        return count

    to_log = (
        f"File: {path}\n"
        f"LineNumber: {ln}\n"
        f"Attacker URL: {url}\n"
        f"DecodedLines: \n{'-'*10}\n{target}\n{'-'*10}"
    )

    if kw.pop("verbose", False):  # Log in console.
        print(to_log)

    log.append(to_log + f"\nTrigger Line:\n{line!r}\n{'-'*15}\n")
    count += 1
    logged[path] = ln
    return count


def check_file(
    d: str, file: str, count: int, args: argparse.Namespace
) -> tuple[int, int]:
    """Iterate over a file and check the lines

    Parameters
    ----------
    d : str
        Give the path to the file e.g "/home/wildCiphers"
    file : str
        Give a file name to scan e.g "wildCipherInHere.lua"
    count: int
        Give the current cipher count.
    args: argparse.Namespace
        Give the arguments delieverd from the Cmd line.

    Returns
    -------
    tuple[ret_code, count]
        A Tuple with the return code and the current cipher count.
    """

    with open(f"{d}/{file}", "r", encoding="utf-8") as f:
        try:
            lines = f.readlines()
        except UnicodeDecodeError:
            print(f"Can't decode `{d}/{file}`. File is not utf-8")
            return 1, count

        match = validate_lines(lines)
        logged = {}

        if args.v2:
            match += do_gibberish_check(lines)

        if not match:
            return 0, count

        for ln, line, target in match:
            count = prepare_log_line(
                d=d,
                ln=ln,
                file=file,
                line=line,
                count=count,
                target=target,
                logged=logged,
                verbose=args.verbose,
            )
    return 0, count


def write_log_file(**kw) -> int:
    """Writes the logfile

    Parameters
    ----------
    kw : dict
        red : str : Colorcode for red
        white : str : Colorcode for white
        count : int : The found cipher count

    Returns
    -------
    int
        Statuscode
    """
    print(
        f'{kw.pop("red")}Oh no, the program found a spy in your files x.x '
        f"Check the CipherLog.txt for location and trigger. "
        f'{kw.pop("count")} where found!'
        f'{kw.pop("white")}\n#staysafe'
    )

    if kw.pop("args").no_log:
        return 0

    with open(
        f"CipherLog-{dt.now():%H-%M-%S}.txt", "w+", encoding="utf-8"
    ) as f:
        f.writelines(log)

    return 0


def main() -> int:
    """Validates lua files.

    Usage:
    ------
    Run the program: `find-cipher [path] [exclude path] [OPTIONS...]`.

    args:
        --path : Optional :
            Give the path to search, when no path is given, the
            current working directory will be used `.`
        --exclude-path : Optional :
            Exclude directory's where you don't want to search.
        --no-log: Optional :
            Don't create a log file, can be used hand in hand with --verbose
        --verbose : Optional :
            Print a Cipher directly to the Command line on found.
        --v2 : Optional :
            Uses an extra algorithm to find gibberish or randomly generated
            variable/function/table names. It can introduce more palse-positiv
            because of obfuscated scripts, but can help to find ciphers.

    Advertisement:
    --------------
    Get your beautiful Cipher today, just smack the play button and find some.
    Just for $9.99 you can get the Base edition, and just for anohter $49.99
    you can get yourself access to the Version 2.
    I hope you don't have any but always be sure to have none.

    Returns
    -------
    int
        Return code
    """

    parser = argparse.ArgumentParser(description="Validates lua files.")

    parser.add_argument(
        "-p",
        "--path",
        nargs="?",
        default=".",
        help="Give the path to search, when no path is given"
        ', the current working directory will be used "."',
    )

    parser.add_argument(
        "-x",
        "--exclude",
        nargs="*",
        default="",
        help="Exclude directories where you don't want to" " search.",
    )

    parser.add_argument(
        "-n",
        "--no-log",
        action="store_true",
        help="Don't create a log file, can be used hand in hand with -v",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print a Cipher directly to the Command line " " on found.",
    )

    parser.add_argument(
        "--v2",
        action="store_true",
        help="Uses an extra algorithm to find gibberish "
        "or randomly generated variable/function/table "
        "names. It can introduce more false-positives "
        "because of obfuscated scripts but "
        "can help find ciphers.",
    )

    parser.add_argument(
        "--no-del",
        action="store_true",
        help="Debug command to not delete the big.model "
        "file after the script finishes.",
    )

    parser.add_argument(
        "--get-train-file",
        action="store_true",
        help="Debug command to get the big.model file",
    )

    args = parser.parse_args()

    if args.get_train_file:
        get_big_model_file()
        return 0

    pattern = "".join(
        [
            (i.replace(",", ")|(") if "--" not in i else "")
            for i in args.exclude
        ]
    )
    local_path = args.path
    count = 0

    if args.v2:
        # sure there are other ways, but python is doing python stuff.
        get_big_model_file()

    for d, _, files in os.walk(local_path):
        if pattern and do_regex(rf"{d}", f'{"(" + pattern + ")"}'):
            continue

        for file in files:
            if ".lua" not in file:
                continue

            _, count = check_file(d, file, count, args)

    # Write log
    red = green = white = ""

    if "linux" in platform.platform().lower():
        white, red, green = COLORS

    try:
        if not args.no_del:
            os.remove("big.model")
    except FileNotFoundError:
        pass

    if log:
        return write_log_file(white=white, red=red, count=count, args=args)

    print(f"{green}Nice! There were no Cipher's found!{white}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
