#!/bin/python3.11

#  Copyright (c) 2022-2023 - exersalza
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
from __future__ import annotations

import os
import re
import sys
import platform

from datetime import datetime as dt
from gibberish_detector import detector

REGEX = r'(((\\x|\\u)([a-fA-F0-9]{2})){2})'
COLORS = ['\033[0m', '\033[91m', '\033[92m']

det = detector.create_from_model('big.model')

log = []


def validate_lines(lines: list) -> list[tuple]:
    """ Validate the lines that are given through the 'lines' parameter.

    Parameters
    ----------
    lines : list
        The lines from the current read file.

    Returns
    -------
    list[tuple]
        A list with infected lines 
        (or false positives by AntiCheat or obfuscated code)
    """

    ret = []

    for ln, line in enumerate(lines, start=1):  # ln: lineNumber
        if re.findall(REGEX, rf'{line}', re.MULTILINE and re.IGNORECASE):
            ret.append((ln, line))

    return ret


def do_gibberish_check(lines: list) -> list[tuple[str, int]]:
    """ Do a check if the given lines are making any sens.
    Can still throw false-positives

    Parameters
    ----------
    lines : list
        The lines from the current read file.

    Returns
    -------
    list[tuple[str, int]]
        A Tuple List with infected lines or false positives
        as in `validate_lines`.

    """
    l_counter = 1
    matches = []

    for i in lines:
        if 'local' in i and det.is_gibberish(rf'{i}'):
            matches.append((l_counter, i))

        l_counter += 1
    return matches


def check_file(d: str, file: str, count: int) -> tuple[int, int]: 
    """ Iterate over a file and check the lines

    Parameters
    ----------
    d : str
        Give the path to the file e.g "/home/wildCiphers"
    file : str
        Give a file name to scan e.g "wildCipherInHere.lua"
    count: int
        Give the current cipher count.
    
    Returns
    -------
    tuple[ret_code, count]
        A Tuple with the return code and the current cipher count.
    """

    with open(f'{d}/{file}', 'r', encoding='utf-8') as f:
        try:
            lines = f.readlines()
        except UnicodeDecodeError:
            print(f'Can\'t decode `{d}/{file}`.')
            return 1, count
        
        match = validate_lines(lines)
        
        if '--v2' in sys.argv:
            match += do_gibberish_check(lines)

        if match:
            for ln, line in match:
                path = d.replace('\\', '/') + f'/{file}'
                to_log = f'File: {path}\nLineNumber: {ln}\n'

                if '--verbose' in sys.argv:  # Log in console.
                    print(to_log)


                log.append(to_log + f'Line: {line!r}\n----------------\n')
                count += 1
    return 0, count


def main() -> int:
    """ Validates lua files.

    Usage:
    ------
    Run the program: `find-cipher [path] [exclude path] [OPTIONS...]`.

    args:
        path : Optional : 
            Give the path to search, when no path is given, the 
            current working directory will be used `.`
        exclude path : Optional : 
            Exclude directory's where you don't want to search.
        --verbose : Optional : 
            Print a Cipher directly to the Command line on found.
        --v2 : Optional : 
            Uses an extra algorithm to find gibberish or randomly generated
            variable/function/table names. It can introduce more palse-positiv
            because of obfuscated scripts, but can help to find ciphers.

    Advertisement:
    --------------
    Get your beautiful Cipher today, just smack the play button and find some.
    I hope you don't have any but always be sure to have none.

    Returns
    -------
    int
        Return code
    """

    if '-h' in sys.argv or '--help' in sys.argv:
        print(main.__doc__)
        return 0

    pattern = ''.join([(i.replace(',', ')|(') if '--' not in i else '') for i in sys.argv[2:]])
    local_path = '.'
    count = 0 

    if len(sys.argv) > 1 and '--' not in sys.argv[1]:
        local_path = sys.argv[1]
    
    for d, _, files in os.walk(local_path):
        if pattern and re.findall(f'{"(" + pattern + ")"}', fr'{d}'.format(d=d), re.MULTILINE and re.IGNORECASE):
            continue

        for file in files:
            if '.lua' not in file:
                continue

            _, count = check_file(d, file, count)
    # Write log
    
    red = ''
    green = ''
    white = ''

    if 'linux' in platform.platform().lower():
        white, red, green = COLORS

    if log:
        with open(f'CipherLog-{dt.now():%H-%M-%S}.txt', 'w+', encoding='utf-8') as f:
            f.writelines(log)
        
        print(f'{red}Oh no, the program found a spy in your files x.x '
              f'Check the CipherLog.txt for location and trigger. {count} where found!'
              f'{white}\n#staysafe')
        return 0
    
    print(f'{green}Nice! There were no Cipher\'s found!{white}')

    return 0


if __name__ == '__main__':
    sys.exit(main())
