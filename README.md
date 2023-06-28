# FivemCipherFinder (v1.7.0)
<div align="center">
  <h2> Visitors </h2>
<img src="https://profile-counter.glitch.me/FivemCipherFinder/count.svg" />
</div>

[![Pylint](https://github.com/exersalza/FivemCipherFinder/actions/workflows/pylint.yml/badge.svg)](https://github.com/exersalza/FivemCipherFinder/actions/workflows/pylint.yml)

This is a Fivem Cipher remover for those that don't want Ciphers in their scripts :D

The idea behind these scripts is to remove a Cipher or more. Currently, there is only the Python version available, but I will soon add the C++ variant.

Desc:
The script will walk through your Server's directories and scan, for example, `\x41\x42\x43`. When it found something it will write the line and trigger it into a Log file.

## Languages 
Planed are Python (Finished so far)

## Usage

Syntax: `find-cipher [search path] [exclude paths]... [OPTIONS]...`
Options are:
- `--verbose` -> To show the found ciphers inside the Console
- `--v2` -> For the gibberish search. Like `local fjdlsajfdsancu = ...`

It's a console tool so you can use `find-cipher` just like that in your `Resources` folder or you can specifiy you folder with `find-cipher ~/FiveM/server-data/resources` as example.

Should you struggle with returning ciphers in your script, try using the
`--v2` flag behind the command like `find-cipher . --v2 cars,mlos`.

As you can see in the last example, you can exclude Directories so can prevent false-positives like `\[cars\],\[mlos\],easy-admin` but make sure you add `\` before curly and square brackets, otherwise your terminal will throw an error.

The script logs found Cipher in a file names `CipherLog-HH-MM-SS.txt` so can easily find your log files.

## Install instructions for Python
Py-Version: 3.7 and above

run `pip install FivemCipherFinder` or download the latest release and unpack it.

### Troubleshooting

Should the installation with pip fail with the error code `externally-managed-environment`, add `--break-system-packages`. Pip changed something in their internals in the newer versions.

## Known false positives
- `easy-admin`
- `encrypted scripts`

## ToDo
- Detect cipher spreader
- ~~Find random generated character variable names~~

## Contact
Discord: exersalza / exersalza[>'-']>#1337 | [DE/EN]
