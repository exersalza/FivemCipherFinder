import os

from cipherFinder.finder import (
    get_big_model_file,
    do_gibberish_check,
    prepare_log_line,
    log,
)


def test_get_big_model_file():
    get_big_model_file()

    assert os.path.exists("./big.model")
    os.remove("./big.model")


def test_validate_lines():
    ...
    # can't test due to random value inside string that can't be determined


def test_do_gibberish_check():
    test = [
        "fjdlksajkfdnvjndjsaiheiruahn",
        "local jflkdsajlkfndsajiewajnucdisan = {'jdkfsa'}",
        "local someRandomString = {'validate', 'the', 'HYPNOTOAD'}",
    ]

    get_big_model_file()

    assert do_gibberish_check(test) == [
        (
            2,
            "local jflkdsajlkfndsajiewajnucdisan = {'jdkfsa'}",
            "Can't de obfuscate due to use of --v2",
        )
    ]
    os.remove("./big.model")


def test_prepare_log_line():
    count = 68
    logged = {}
    count = prepare_log_line(count=count, logged=logged)

    assert count == 69
    assert log == [
        (
            "File: ./poggers.lua\nLineNumber: \nAttacker URL:"
            " \nDecodedLines: \n----------\n\n----------\nTrigger "
            "Line:\n''\n---------------\n"
        )
    ]
    assert logged == {"./poggers.lua": ""}


if __name__ == "__main__":
    test_prepare_log_line()
