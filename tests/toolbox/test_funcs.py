import pytest

from brandenburg.toolbox.funcs import Funcs


def test_encode_string():
    assert "YnJhbmRlbmJ1cmc=" == Funcs.encode("brandenburg")


def test_encode_dict():
    assert "eyJhcHAiOiJicmFuZGVuYnVyZyJ9" == Funcs.encode({"app": "brandenburg"})


def test_decode_string():
    assert "brandenburg" == Funcs.decode("YnJhbmRlbmJ1cmc=")


def test_decode_dict():
    assert {"app": "brandenburg"} == Funcs.decode("eyJhcHAiOiJicmFuZGVuYnVyZyJ9")


def test_not_b64_string():
    assert "abc123" == Funcs.decode("abc123")


def test_clean_wrong_phonenumber():
    assert "+5521934452312" == Funcs.normalize_phonenumber("(21)934452312")


def test_clean_short_phonenumber():
    assert "" == Funcs.normalize_phonenumber("21 9344523")


def test_clean_spaced_phonenumber():
    assert "+5521934452312" == Funcs.normalize_phonenumber("55 21 9 3445 2312")
