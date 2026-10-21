import pytest
from src.shorten import new_short_wallet, restore_phrase, SHORT_WORDS, WORDLIST
from src.derive import key_from_phrase

SECRET = "correct horse battery staple, 2026"


def test_short_form_is_six_bip39_words():
    w = new_short_wallet(SECRET)
    assert len(w["short_words"]) == SHORT_WORDS
    assert all(x in WORDLIST for x in w["short_words"])


def test_round_trip_restores_same_phrase_and_account():
    w = new_short_wallet(SECRET)
    restored = restore_phrase(w["short_words"], SECRET)
    assert restored == w["seed_phrase"]
    key = key_from_phrase(restored)
    assert key["public_key_hex"] == w["account_id"]


def test_wrong_secret_gives_different_account():
    w = new_short_wallet(SECRET)
    wrong = restore_phrase(w["short_words"], SECRET + "x")
    assert key_from_phrase(wrong)["public_key_hex"] != w["account_id"]


def test_short_form_alone_does_not_match_account():
    # Six words without the secret must not reproduce the phrase.
    w = new_short_wallet(SECRET)
    with pytest.raises(ValueError):
        restore_phrase(w["short_words"][:5], SECRET)


def test_short_secret_rejected():
    with pytest.raises(ValueError):
        new_short_wallet("short")


def test_many_random_round_trips():
    for i in range(25):
        s = f"secret number {i} with enough length"
        w = new_short_wallet(s)
        assert restore_phrase(w["short_words"], s) == w["seed_phrase"]
