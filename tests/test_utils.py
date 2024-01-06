import codecs
import os
from cipherFinder.utils import find_encoding, detect_encoding, fix_path


def test_find_encoding():
    assert find_encoding("utf-8") == codecs.lookup("utf-8")
    assert find_encoding("non-existent-encoding") == 0


def test_detect_encoding(tmp_path):
    # Create a temporary file with known encoding
    p = tmp_path / "temp.txt"
    p.write_text("This is a test file with ascii encoding.", encoding="ascii")

    enc, confidence = detect_encoding(str(p))
    assert enc == "ascii"
    assert 0 <= confidence <= 1


def test_fix_path():
    if os.name == "nt":  # Windows
        assert (
            fix_path("C://Users//Test//Desktop") == "C:\\Users\\Test\\Desktop"
        )
        assert (
            fix_path("C:\\Users\\Test\\Desktop") == "C:\\Users\\Test\\Desktop"
        )
    else:  # Unix-based
        assert fix_path("/home/test/Desktop") == "/home/test/Desktop"
        assert fix_path("//home//test//Desktop") == "/home/test/Desktop"
