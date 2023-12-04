import chardet


def detect_encoding(file_path):
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read())
    return result["encoding"]


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
                f"Do you want to delete the following line?: "
                f"\n{cipher}\n[y/N]: "
            )
        ):
            continue

        file_encoding = detect_encoding(f"{path}")

        with open(path, "r", encoding=file_encoding) as f:
            lines = f.readlines()

        del lines[ln - 1]

        with open(path, "w", encoding=file_encoding) as f:
            f.writelines(lines)

    return 0
