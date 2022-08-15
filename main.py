#!/bin/python3.10

import os
import re

regex = r"((\\x)([a-fA-F0-9]{2}))"

for dir, subdir, files in os.walk('dummys/'):
    print(files)

with open('dummys/moreDummy/en.lua', 'r') as f:
    lines = "".join(f.readlines())
    matches = re.finditer(regex, lines, re.MULTILINE | re.IGNORECASE)

for matchNum, match in enumerate(matches, start=1):
    print(match)
