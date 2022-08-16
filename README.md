# [CURRENTLY UNDER DEVELOPMENT] FivemCipherRemover (v1.0.0)
This is a Fivem Cipher remover for those that don't want Ciphers in their scripts :D

The idea behind these scripts are to remove a Cipher or more. Currently, there is it only in Python available, but I will soon add the C++ variant.

Desc:
The script will walk through your Servers directory's and scan for as example `\x41\x42\x43`. When it found something.

## Languages 
Planed are Python (Currently in development) and C++ (Not started)


## Install instructions for Python
Py-Version: 3.10 and above

Clone or Download the latest release and unpack it.

The `main.py` is your entry point, you can run it with `python3.10 main.py <Your Path> <Exclude Path>`. 
You can also just use the file as `Exclude Path` to scan only one file.

With the exclude path parameter, you can add one or more paths that shall be excluded (anticheat or anticheat, cars).

The script with the Ciphers getting logged in a File (`CipherLog.txt`) that gets created.
