def de_obfs(ret: list[tuple]) -> list[tuple]:
    """ De-Obfuscate the \x23... lines

    Parameters
    ----------
    ret : list[tuple]
       Give the found lines.

    Returns
    -------
    list[tuple]
        Give the decoded lines back with the original version.

    """
    temp = []
    for j in ret:
        t = ""
        # Get rid of the x and backslashes.
        for i in (j[0].strip("\"").replace("\\", "")).split("x"):
            if i == "":
                continue

            t += chr(int(i, 16))
        temp.append((t, j[0]))
        
    return temp

