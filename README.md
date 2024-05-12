# FivemCipherFinder (v2.6.3)

<div align="center">
    <h2> Visitors </h2>
    <img src="https://profile-counter.glitch.me/FivemCipherFinder/count.svg" />
</div>

[![Pylint and Flake8](https://github.com/exersalza/FivemCipherFinder/actions/workflows/pylint.yml/badge.svg)](https://github.com/exersalza/FivemCipherFinder/actions/workflows/pylint.yml)
[![PyTest](https://github.com/exersalza/FivemCipherFinder/actions/workflows/pytest.yml/badge.svg)](https://github.com/exersalza/FivemCipherFinder/actions/workflows/pytest.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![](https://tokei.rs/b1/github/exersalza/fivemcipherfinder)
![PyPI - Downloads](https://img.shields.io/pypi/dm/fivemcipherfinder?label=pypi%20downloads)


- [FivemCipherFinder (v2.6.3)](#fivemcipherfinder-v263)
  - [Installation](#installation)
    - [New version](#new-version)
    - [Old Version](#old-version)
  - [Usage](#usage)
  - [Troubleshooting](#troubleshooting)
  - [Known False Positives](#known-false-positives)
  - [Plugins](#plugins)
  - [Contributing](#contributing)
  - [Todo](#todo)
  - [Disclaimer](#disclaimer)
  - [Prevention](#prevention)
  - [Contact](#contact)
  - [Star History](#star-history)
  - [Credits](#credits)


FivemCipherFinder is a tool designed to assist in the removal of Ciphers from your scripts. It is a console-based tool that can be used by anyone, regardless of their coding experience. The main purpose of FivemCipherFinder is to find and identify Ciphers in your script files.

## Installation

To install FivemCipherFinder, follow these steps:
INSTALL PYTHON FROM THIS [TUTORIAL](https://phoenixnap.com/kb/how-to-install-python-3-windows)
PLEASE MAKE SURE TO CHECK THOSE CHECKBOXES
![img_2.png](img_2.png)

### New version
Get the `install.ps1` script and run it, it'll do anything for you, you just have to run the finder by itself afterward. For more information press [here](POWERSHELL_INSTALL.md)

### Old Version
1. Make sure you have Python 3.8 or above installed on your system. If not, you can download the latest version of Python from the official website [here](https://python.org/downloads/).

2. Open your command prompt or terminal and run the following command to install FivemCipherFinder using pip:
   ```
   pip install FivemCipherFinder
   ```

   Alternatively, you can download the latest release of FivemCipherFinder from the GitHub repository [here](https://github.com/exersalza/FivemCipherFinder/releases) and unpack it manually.
   1. Clone the Repo with one of those 2 commands: `git clone https://github.com/exersalza/FivemCipherFinder` or `git clone git@github.com:exersalza/FivemCipherFinder`
   2. Change into the directory you just cloned with: `cd FivemCipherFinder`
   3. To build and run use this Command: `python3 -m build . && pip install . --user`. Alternatively create a local venv to not interfere with other project dependencies: `python3 -m venv venv`. You can activate it with `.\venv\Scripts\activate.bat` on Windows or `source venv/bin/activate` on unix-like systems.

   **Note:** If you are using a Windows-based system, make sure you have added Python to your environment variables. You can test this by typing `python --version` into your command prompt or terminal. If Python is not recognized, you may need to add it to your system's PATH variable. You can find instructions on how to do this [here](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/).

3. Once installed, you can use the `find-cipher` command in your server's resources directory to start using FivemCipherFinder.

## Usage

To use FivemCipherFinder, you can run the `find-cipher` command with various options. Here are the available options:

- `-p|--path`: Redirect the search from the current path `.` to another one.
- `-x|--exclude`: Exclude paths that you don't want to scan.
- `-n|--no-log`: Prevents the creation of a log file.
- `-v|--verbose`: Show the found ciphers in the console as soon as they are found. Also adds more verbosity for the deletion of ciphers.
- `--plug-dir`: Specify a Plugin directory. See the `plugins` directory for further information. Keep in mind, that the Script needs to be able to access the choosen directory.
- `-w|--no-wizard`: Don't run the eraser wizard after the program ran.
- `--get-remote-plugins`: Download the latest plugins from the remote repository.
- `--no-deobfs`: Skip the De Obfuscation part, can help when you get the MemoryError error.

Example Command: `find-cipher -v --plug-dir ~/cipherfinderPlugins`

You can run the `find-cipher` command in your server's resources folder, or you can specify a different folder by providing the path as an argument. For example:

```
find-cipher -p ~/FiveM/server-data/resources
```
Here we scan a whole directory located at the Path given, if you're on windows make sure to use the windows equivalent like "C:\User\...". Also if you should forget to change it, but your server is inside your home directory, the finder will convert the path to a windows like one


FivemCipherFinder logs the found ciphers in a file named `CipherLog-HH-MM-SS.txt`, making it easy to review the results.

**Keep in mind**
- The CipherFinder can't find 100% of maybe placed ciphers.
- Should you use a Code Formatter, it's possible when you use the Eraser function, that your scripts can fail to start because of syntax errors. Read the [Disclaimer](#Disclaimer).
- Cipher spreader can hide everywhere, consider reinstalling yarn and webpack, also make sure you changed your default ports like ssh and rdp.

## Troubleshooting

If you encounter any issues with FivemCipherFinder, here are some troubleshooting steps you can follow, please try all of them first before you contact me or another developer:

1. Read the error or warning message carefully to understand the problem.

2. If you are installing FivemCipherFinder using pip and encounter the error code `externally-managed-environment`, try adding the `--break-system-packages` flag to the pip command. This is a change in pip's internals in newer versions.

3. If you encounter the error "pip is not recognised as internal command" or something similar, please follow these instructions on how to add something to the PATH variable [here](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/).
   * Add your python path to the env paths, the default python installation path is `%LOCALAPPDATA%\Programs\Python\Python312` and `%LOCALAPPDATA%\Programs\Python\Python312\Scripts`
   * Please also make sure to install Python from [Download](https://python.org/downloads/) and **not** from the Microsoft store.
   * When you install Python, please tick the "add to path" checkbox.

4. Should you get an error called `MemoryError` try running the same command with the `--de-obfs` argument.

## Known False Positives

- `EasyAdmin`
- Encrypted/obfuscated scripts

## Plugins

If you would like to have a Plugin that fetches data while the cipherfinder is running you can read into it further under [Plugins](plugins/README.md).
If you want a Pre-Written plugin that sends a message onto an Webhook

## Contributing

If you would like to contribute to FivemCipherFinder, you can open a pull request with your changes. The project has checks in place to ensure that the pull request passes without any issues. You can use the manual installation guide provided in the [Installation](#Installation) section to set up the project locally.

## Todo

- [ ] Detect cipher spreader
- [x] Add deobfuscator for detected ciphers
- [x] Find randomly generated character variable names
- [ ] Add an UI and Exe/Bin
- [x] Hook System

## Disclaimer
[DISCLAIMER](DISCLAIMER.md)


## Prevention

You can add the following URLs to your hosts file or Firewall. See [here](https://docs.rackspace.com/docs/modify-your-hosts-file) if you're not sure how to edit the hosts file.

Also read [here](https://github.com/ProjecteEndCipher/Cipher-Panel) and [here](https://github.com/ericstolly/cipher) for further information.

```
127.0.0.1       cipher-panel.me
127.0.0.1       ciphercheats.com
127.0.0.1       keyx.club
127.0.0.1       dark-utilities.xyz
127.0.0.1       ketamin.cc
127.0.0.1       pqzskjptss.shop
127.0.0.1       admin-panel.sbs
127.0.0.1       malware-panel.io
127.0.0.1       docsfivem.com
127.0.0.1       thedreamofficeem.com
127.0.0.1       thedreamoffivem.com
127.0.0.1       rpserveur.fr
127.0.0.1       abxcgraovp.pics
127.0.0.1       sayebrouhk.com
```

Change default ports like RDP (3389), Ftp (21), SSH (22) and MySql (3306)

## Contact

If you have any questions or need assistance that can't be resolved with the [Troubleshooting](#troubleshooting) page, you can reach out on Discord:

- Discord: exersalza / exersalza[>'-']>#1337 | [DE/EN]

## Star History
<a href="https://star-history.com/#exersalza/fivemcipherfinder&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=exersalza/fivemcipherfinder&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=exersalza/fivemcipherfinder&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=exersalza/fivemcipherfinder&type=Date" />
  </picture>
</a>


## Credits
- [exersalza](https://github.com/exersalza) -> me (Main Dev)
- [ZerxGit](https://github.com/ZerxGit) -> Inspiration for the whole Project
- [Firav](https://github.com/Firav) -> Big baller in testing my stuff :D

