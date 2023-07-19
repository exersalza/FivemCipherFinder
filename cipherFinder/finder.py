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
from datetime import datetime as dt

import os
import re
import sys
import platform
import argparse
import requests

from gibberish_detector import detector

REGEX = r'(((\\x|\\u)([a-fA-F0-9]{2})){2})'
COLORS = ['\033[0m', '\033[91m', '\033[92m']
RAW_BIG_MODEL = 'https://raw.githubusercontent.com/exersalza/FivemCipherFinder/main/big.model'

log = []

def get_big_model_file() -> int:
    # Check if the big.model file exists
    if not os.path.exists('./big.model'):
        with open('big.model', 'wb') as _file:
            for chunk in requests.get(RAW_BIG_MODEL, 
                                      stream=True, timeout=5) \
                    .iter_content(chunk_size=8192):
                if not chunk: continue

                _file.write(chunk)

    return 0


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

    ret: list[tuple] = []

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

    det = detector.create_from_model('./big.model')  # should work for now
    l_counter = 1
    matches = []

    for i in lines:
        if 'local' in i and det.is_gibberish(rf'{i}'):
            matches.append((l_counter, i))

        l_counter += 1
    return matches


def check_file(d: str, file: str, count: int, args: argparse.Namespace) -> tuple[int, int]: 
    """ Iterate over a file and check the lines

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

    with open(f'{d}/{file}', 'r', encoding='utf-8') as f:
        try:
            lines = f.readlines()
        except UnicodeDecodeError:
            print(f'Can\'t decode `{d}/{file}`.')
            return 1, count
        
        match = validate_lines(lines)
        
        if args.v2:
            match += do_gibberish_check(lines)

        if match:
            for ln, line in match:
                path = d.replace('\\', '/') + f'/{file}'
                to_log = f'File: {path}\nLineNumber: {ln}\n'

                if args.verbose:  # Log in console.
                    print(to_log)


                log.append(to_log + f'Line: {line!r}\n----------------\n')
                count += 1
    return 0, count


def write_log_file(**kw) -> int: 
    if kw.pop('args').no_log:
        return 0

    with open(f'CipherLog-{dt.now():%H-%M-%S}.txt', 'w+', encoding='utf-8') as f:
        f.writelines(log)
        
        print(f'{kw.pop("red")}Oh no, the program found a spy in your files x.x '
          f'Check the CipherLog.txt for location and trigger. {kw.pop("count")} where found!'
          f'{kw.pop("white")}\n#staysafe')
    return 0


def main() -> int:
    """ Validates lua files.

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

    parser = argparse.ArgumentParser(description='Validates lua files.')

    parser.add_argument('-p', '--path', nargs='?', default='.',
                        help='Give the path to search, when no path is given, the current working directory will be used "."')
    parser.add_argument('-x', '--exclude', nargs='*', default='',
                        help='Exclude directories where you don\'t want to search.')
    parser.add_argument('-n', '--no-log', action='store_true',
                        help='Don\'t create a log file, can be used hand in hand with --verbose')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Print a Cipher directly to the Command line on found.')
    parser.add_argument('--v2', action='store_true',
                        help='Uses an extra algorithm to find gibberish or randomly generated variable/function/table names. It can introduce more false-positives because of obfuscated scripts but can help find ciphers.')

    args = parser.parse_args()

    pattern = ''.join([(i.replace(',', ')|(') if '--' not in i else '') for i in args.exclude])
    local_path = args.path
    count = 0 

    get_big_model_file()  # sure there are other ways, but python is doing python stuff.
    
    for d, _, files in os.walk(local_path):
        if pattern and re.findall(f'{"(" + pattern + ")"}', 
                                  fr'{d}'.format(d=d), re.MULTILINE and re.IGNORECASE):
            continue

        for file in files:
            if '.lua' not in file:
                continue

            _, count = check_file(d, file, count, args)
    # Write log
    
    red = green = white = ''

    if 'linux' in platform.platform().lower():
        white, red, green = COLORS
    
    try:
        os.remove('big.model')
    except FileNotFoundError:
        pass

    if log:
        return write_log_file(white=white, red=red, 
                              count=count, args=args)

    print(f'{green}Nice! There were no Cipher\'s found!{white}')

    return 0


if __name__ == '__main__':
    sys.exit(main())
