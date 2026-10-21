import re
from src.derive import new_phrase_and_key, key_from_phrase, NEAR_HD_PATH


def test_new_phrase_has_12_words_and_implicit_account():
    r = new_phrase_and_key()
    assert len(r["seed_phrase"].split()) == 12
    assert re.fullmatch(r"[0-9a-f]{64}", r["public_key_hex"])
    assert r["public_key"].startswith("ed25519:")


def test_restore_gives_same_key_and_account():
    original = new_phrase_and_key()
    restored = key_from_phrase(original["seed_phrase"])
    assert restored["public_key"] == original["public_key"]
    assert restored["public_key_hex"] == original["public_key_hex"]
    assert restored["secret_key"] == original["secret_key"]


def test_path_is_near_default():
    assert NEAR_HD_PATH == "m/44'/397'/0'"
