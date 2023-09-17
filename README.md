# FivemCipherFinder (v2.4.3)

<div align="center">
    <h2> Visitors </h2>
    <img src="https://profile-counter.glitch.me/FivemCipherFinder/count.svg" />
</div>

[![Pylint and Flake8](https://github.com/exersalza/FivemCipherFinder/actions/workflows/pylint.yml/badge.svg)](https://github.com/exersalza/FivemCipherFinder/actions/workflows/pylint.yml)
[![PyTest](https://github.com/exersalza/FivemCipherFinder/actions/workflows/pytest.yml/badge.svg)](https://github.com/exersalza/FivemCipherFinder/actions/workflows/pytest.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

- [Installation](#installation)
- [Usage](#Usage)
- [Troubleshooting](#Troubleshooting)
- [Contributing](#Contributing)
- [Todo](#todo)
- [Contact](#Contact)


FivemCipherFinder is a tool designed to assist in the removal of Ciphers from your scripts. It is a console-based tool that can be used by anyone, regardless of their coding experience. The main purpose of FivemCipherFinder is to find and identify Ciphers in your script files.

## Installation

To install FivemCipherFinder, follow these steps:

1. Make sure you have Python 3.8 or above installed on your system. If not, you can download the latest version of Python from the official website [here](https://python.org/downloads/).

2. Open your command prompt or terminal and run the following command to install FivemCipherFinder using pip:

   ```
   pip install FivemCipherFinder
   ```

   Alternatively, you can download the latest release of FivemCipherFinder from the GitHub repository [here](https://github.com/exersalza/FivemCipherFinder/releases) and unpack it manually.

   **Note:** If you are using a Windows-based system, make sure you have added Python to your environment variables. You can test this by typing `python --version` into your command prompt or terminal. If Python is not recognized, you may need to add it to your system's PATH variable. You can find instructions on how to do this [here](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/).

3. Once installed, you can use the `find-cipher` command in your server's resources directory to start using FivemCipherFinder.

## Usage

To use FivemCipherFinder, you can run the `find-cipher` command with various options. Here are the available options:

- `-p|--path`: Redirect the search from the current path `.` to another one.
- `-x|--exclude`: Exclude paths that you don't want to scan.
- `-n|--no-log`: Prevents the creation of a log file.
- `-v|--verbose`: Show the found ciphers in the console as soon as they are found.
- `--v2`: Enable the gibberish search mode, which can detect ciphers like `local fjdlsajfdsancu = ...`.

You can run the `find-cipher` command in your server's resources folder, or you can specify a different folder by providing the path as an argument. For example:

```
find-cipher -p ~/FiveM/server-data/resources
```

If you are having trouble with returning ciphers in your script, you can try using the `--v2` flag to enable the gibberish search mode. For example:

```
find-cipher . --v2 cars,mlos
```

In the above example, the directories `cars` and `mlos` are excluded from the search to prevent false positives. Make sure to add a backslash `\` before curly and square brackets to avoid errors in the terminal.

FivemCipherFinder logs the found ciphers in a file named `CipherLog-HH-MM-SS.txt`, making it easy to review the results.

## Troubleshooting

If you encounter any issues with FivemCipherFinder, here are some troubleshooting steps you can follow:

1. Read the error or warning message carefully to understand the problem.

2. If you are installing FivemCipherFinder using pip and encounter the error code `externally-managed-environment`, try adding the `--break-system-packages` flag to the pip command. This is a change in pip's internals in newer versions.

3. On Windows, make sure that your Python scripts folder is added to your system's PATH variable. If the folder is missing, it will be shown as a warning during the pip installation. You can find instructions on how to add something to the PATH variable [here](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/).

## Known False Positives

- `EasyAdmin`
- Encrypted/obfuscated scripts

## Contributing

If you would like to contribute to FivemCipherFinder, you can open a pull request with your changes. The project has checks in place to ensure that the pull request passes without any issues. You can use the manual installation guide provided in the [Installation](#Installation) section to set up the project locally.

## Todo

- [ ] Detect cipher spreader
- [x] Add deobfuscator for detected ciphers
- [x] Find randomly generated character variable names

## Contact

If you have any questions or need assistance with FivemCipherFinder, you can reach out on Discord:

- Discord: exersalza / exersalza[>'-']>#1337 | [DE/EN]

Feel free to contact me for any inquiries or support related to FivemCipherFinder.
