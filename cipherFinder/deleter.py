import os

from cipherFinder.utils import detect_encoding


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
        the shadow list thats getting created in the main file.

    Returns
    -------
    int
        Return code
    """

    for cipher, ln, path in del_lines:
        if not y_n_validator(
            input(  # pylint: disable=bad-builtin
                f"Do you want to delete the following line? THIS CANNOT BE "
                f"UNDONE: \n{cipher}\n[y/N]: "
            )
        ):
            continue

        enc, _ = detect_encoding(f"{path}")

        try:
            with open(path, "r", encoding=enc) as f:
                lines = f.readlines()
        except UnicodeDecodeError as e:
            print(os.getenv("DEBUG"), bool(os.getenv("DEBUG")))
            if bool(os.getenv("DEBUG")):
                print(e)

            print(
                f"ERROR: Can't delete cipher from {path!r} due to illegal "
                f"characters, please delete it yourself.\nYou'll find it "
                f"on line: {ln}"
            )
            return 1

        del lines[ln - 1]

        with open(path, "w", encoding=enc) as f:
            f.writelines(lines)

    return 0
