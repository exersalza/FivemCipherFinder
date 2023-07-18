# FivemCipherFinder (v2.3.0)

<div align="center">
  <h2> Visitors </h2>
<img src="https://profile-counter.glitch.me/FivemCipherFinder/count.svg" />
</div>

[![Pylint](https://github.com/exersalza/FivemCipherFinder/actions/workflows/pylint.yml/badge.svg)](https://github.com/exersalza/FivemCipherFinder/actions/workflows/pylint.yml)

- [Installation](#installation)
- [Usage](#Usage)
- [Troubleshooting](#Troubleshooting)
- [Known false-positives](#known-false-positives)
- [Todo](#todo)
- [Contact](#Contact)

This is a Fivem Cipher finder for those that don't want Ciphers in their scripts :D

The idea behind these scripts is to find one or more Cipher in your script files. 
Currently, there is only the Python version available, but I will soon add the C++ variant.

Desc:
The script will walk through your Server's directories and scan, for example, `\x41\x42\x43`. When it found something it will write the line and trigger it into a Log file.

## Installation
Py-Version: 3.8 and above

run `pip install FivemCipherFinder` or download the latest release and unpack it.

Make sure to read the [Troubleshooting](#Troubleshooting) page first before you add me on Discord.

## Install instructions for Python
Py-Version: 3.8 and above

run `pip install FivemCipherFinder` or download the latest release and unpack it.

## Usage

Syntax: `find-cipher [-h] [-p [PATH]] [-x [EXCLUDE_PATH ...]] [-n] [-v] [--v2]`
Options are:
- `-p|--path` -> Redirect the search from the current path `.` to another one.
- `-x|--exclude` -> Exclude paths that you dont want to scan. 
- `-n|--no-log` -> Prevents that an logfile is being written. Works hand in hand with `-v`
- `-v|--verbose` -> To show the found ciphers inside the Console as soon as they were found.
- `--v2` -> For the gibberish search. Like `local fjdlsajfdsancu = ...`

It's a console tool so you can use `find-cipher` just like that in your `Resources` folder or you can specifiy you folder with `find-cipher ~/FiveM/server-data/resources` as example.

Should you struggle with returning ciphers in your script, try using the
`--v2` flag behind the command like `find-cipher . --v2 cars,mlos`.

As you can see in the last example, you can exclude Directories so can prevent false-positives like `\[cars\],\[mlos\],easy-admin` but make sure you add `\` before curly and square brackets, otherwise your terminal will throw an error.

The script logs found Cipher in a file names `CipherLog-HH-MM-SS.txt` so can easily find your log files.

### Troubleshooting

Should the installation with pip fail with the error code `externally-managed-environment`, add `--break-system-packages`. Pip changed something in their internals in the newer versions.

Also make sure (on Windows) that you have your python scripts folder inside your path variable. Should the folder be missing, it shows at the pip installation as a warning. [how to add something to the path variable](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/)


## Known-false-positives

- `EasyAdmin`
- `encrypted/obfuscated scripts`


## ToDo
- Detect cipher spreader
- Add de obfuscator for detectet cipher
- ~~Find random generated character variable names~~

## Contact
Discord: exersalza / exersalza[>'-']>#1337 | [DE/EN]
