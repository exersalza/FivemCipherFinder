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

# did we execute the plan? I think we did.


def deleter_main(del_lines: list) -> int:
    """ This function works as the entry point for the
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

    # Loop over found ciphers and ask the user if they
    # want to remove the line
    for cipher, ln, path in del_lines:
        if not y_n_validator(input(  # pylint: disable=bad-builtin
                f"Do you want to delete the following line?: "
                f"\n{cipher}\n[y/N]: ")):
            continue

        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        del lines[ln - 1]

        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    return 0
