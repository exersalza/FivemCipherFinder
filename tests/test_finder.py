import os

from cipherFinder.finder import (
    get_big_model_file,
    do_gibberish_check,
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
        "local someRandomString = {'validate', 'the', 'HYPTNOTOAD'}",
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


if __name__ == "__main__":
    test_do_gibberish_check()
