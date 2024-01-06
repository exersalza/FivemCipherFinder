from __future__ import annotations

import codecs
import os
import re

import chardet


def find_encoding(name: str) -> codecs.CodecInfo | int:
    try:
        if x := codecs.lookup(name):
            return x
    except LookupError:
        return 0
    return 0


def detect_encoding(file_path) -> (str, float):
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read())

    if enc := result["encoding"]:
        if x := find_encoding(enc):
            enc = x.name

    if not enc:  # just to make sure we have an encoding
        enc = "utf-8"

    return enc, result["confidence"]


def fix_path(path: str) -> str:
    path = re.sub(r"\\+|//+", "/", path)

    if os.name == "nt":
        return path.replace("/", "\\").replace("~", os.getenv("userprofile"))

    return path
