# [CURRENTLY UNDER DEVELOPMENT] FivemCypherRemover
This is an Fivem Cypher remover for those that dont want Cyphers in there scripts :D

The idea behind this scripts are to remove a Cypher or more. Currently there is it only in Python availlable but I will soon add the C++ variant.

Desc:
The script will walk through your Servers directorys and scan for as example `\x41\x42\x43`. When it found something, you can add the option `-k or --kill` when you want to delete the cyphers automatically but be aware that obfuscated scripts may not work after that.

## Languages 
Planed are Python (Currently in development) and C++ (Not started)


## Install instructions for Python
Py-Version: 3.10 and above

Clone the Archive and unpack it.

The `main.py` is your entry point, you can run it with `python3.10 main.py <Your Path> [-k]`
When you don't add the `-k` option, the script with the Cyphers getting logged in a File that gets created in the `FoundCyphers` directory.
