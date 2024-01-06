from cipherFinder.finder import (
    prepare_log_line,
    _log,
    get_filename,
)


def test_validate_lines():
    ...
    # can't test due to random value inside string that can't be determined


def test_get_filename():
    assert get_filename(["someRandom/file.txt"]) == "someRandom/file.txt"


def test_prepare_log_line():
    count = 68
    logged = {}
    count = prepare_log_line(count=count, logged=logged)

    assert count == 69
    assert _log == [
        (
            "File: ./poggers.lua\nLineNumber: \nAttacker URL:"
            " \nDecodedLines: \n----------\n\n----------\nTrigger "
            "Line:\n''\n---------------\n"
        )
    ]
    assert logged == {"./poggers.lua": ""}


if __name__ == "__main__":
    test_prepare_log_line()
