from __future__ import annotations

import os

from cipherFinder.utils import detect_encoding, fix_path

_BACKUP_DIR = "./.fcf_remove.bak/"


def y_n_validator(x: str) -> bool:
    """Validates input if it is y or yes

    Parameters
    ----------
    x : str
        the input string to test

    """
    return x.lower() in {"y", "yes"}


# plan
# Getting a list of all potential cipher lines, so we can remove them.

# did we execute the plan? maybe.


def deleter_main(del_lines: list) -> int:
    """This function works as the entry point for the
    cipher deletion process.

    Parameters
    ----------
    del_lines : list
        the shadow list that's getting created in the main file.

    Returns
    -------
    int
        Return code
    """

    for cipher, ln, path in del_lines:
        if not y_n_validator(
            input(  # pylint: disable=bad-builtin
                f"Do you want to delete the following line? THIS CANNOT BE "
                f"UNDONE {path=} {ln=}: \n{cipher}\n[y/N]: "
            )
        ):
            continue

        enc, _ = detect_encoding(f"{path}")
        bak_path = _BACKUP_DIR + path[path.find("resources"):]
        bak_path = fix_path(bak_path)
        file = bak_path[bak_path.rfind("/" if "/" in bak_path else "\\") + 1:]

        try:
            with open(path, "r", encoding=enc) as f:
                lines = f.readlines()
                if not os.path.isfile(bak_path):
                    os.makedirs(bak_path.replace(file, ""), exist_ok=True)

                with open(bak_path, "w", encoding="utf-8") as j:
                    j.writelines(lines)

        except UnicodeDecodeError as e:
            if bool(os.getenv("DEBUG")):
                print(e)

            print(
                f"ERROR: Can't delete cipher from {path!r} due to illegal "
                f"characters, please delete it yourself.\nYou'll find it "
                f"on line: {ln}"
            )
            continue

        del lines[ln - 1]

        with open(path, "w", encoding=enc) as f:
            f.writelines(lines)

    return 0
