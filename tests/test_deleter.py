from cipherFinder.deleter import y_n_validator


def test_y_n_validator():
    assert y_n_validator("y")
    assert y_n_validator("yes")

    assert not y_n_validator("jfkdslajflk")


def test_deleter_main():  # yeah, naaahhh
    ...
