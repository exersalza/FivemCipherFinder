# FivemCipherFinder (v1.5.0)
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


## Install instructions for Python
Py-Version: 3.7 and above

run `pip install FivemCipherFinder` or download the latest release and unpack it.

The `finder.py` is your entry point, you can run it with `find-cipher <Your Path> [Exclude Path]`. 
You can also use the file as `Your Path` to scan only one file. `Exclude Path` is not required.

With the exclude path parameter, you can add one or more paths that shall be excluded (anti cheat or encrypted scripts, cars or MLOs).

The script with the Ciphers getting logged in a File (`CipherLog.txt`) that gets created.

## Known false positives
- `easy-admin`

## Contact
Discord: exersalza / exersalza[>'-']>#1337
