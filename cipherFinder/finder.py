#!/bin/python3.10

#  Copyright (c) 2022. - exersalza
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
from datetime import datetime as dt

REGEX = r'((\\x)([a-fA-F0-9]{2}))'


def validate_lines(lines) -> list[tuple]:
    """ Validate the lines that are given through the 'lines' parameter.

    Parameters
    ----------
    lines : list
        The lines from the current readed file.

    Returns
    -------
    list[tuple]
        A list with infected lines (or false positives by Anticheat or obfuscated code)
    """

    ret = []

    for ln, line in enumerate(lines, start=1):  # ln: lineNumber
        if re.findall(REGEX, rf'{line}', re.MULTILINE and re.IGNORECASE):
            ret.append((ln, line))

    return ret


def main() -> int:
    """ Validates lua files.

    Usage:
    ------
    Run the program: `python3.10 <path>`. path = give your fullpath to the files you want to scan, otherwise it will
    use the `.` as path (the current working directory).

    Advertisement:
    --------------
    Get your beautiful Cipher today, just smack the play button and find some.
    I hope you don't have any but always be sure to have none.

    Returns
    -------
    int
        Return code
    """

    if '-h' in sys.argv:
        print(main.__doc__)
        return 0

    log = []
    count = 0
    pattern = ''.join([i.replace(',', ')|(') for i in sys.argv[2:]])

    for d, _, files in os.walk(sys.argv[1] if len(sys.argv) > 1 else '.'):
        if pattern and re.findall(f'{"(" + pattern + ")"}', fr'{d}'.format(d=d), re.MULTILINE and re.IGNORECASE):
            continue

        for file in files:
            if '.lua' not in file:
                continue

            with open(f'{d}/{file}', 'r', encoding='utf-8') as f:
                try:
                    lines = f.readlines()
                except UnicodeDecodeError:
                    continue

                match = validate_lines(lines)

                if match:
                    for ln, line in match:
                        path = d.replace('\\', '/') + f'/{file}'
                        log.append(f'File: {path}\nLineNumber: {ln}\nLine: \'{line}\'\n----------------\n')
                        count += 1

    # Write log
    if log:
        with open(f'CipherLog-{dt.now():%H-%M-%S}.txt', 'w+', encoding='utf-8') as f:
            f.writelines(log)

        print('\033[91mOh no, the program find a spy in your files x.x '
              f'Check the CipherLog.txt file for location and trigger. {count} where found!'
              '\033[0m\n#staysafe')
        return 0

    print('\033[92mNice! There where no Cipher\'s found!\033[0m')

    return 0


if __name__ == '__main__':
    sys.exit(main())
