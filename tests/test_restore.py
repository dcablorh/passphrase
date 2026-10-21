import json
import socket
import threading
import urllib.error
import urllib.request
from http.server import HTTPServer

import pytest

from src import shorten
from src.derive import key_from_phrase
from src.shorten import WrongSecret, new_short_wallet, restore_phrase

SECRET = "correct horse battery staple, 2026"


@pytest.fixture
def fast_kdf(monkeypatch):
    monkeypatch.setitem(shorten.SCRYPT, "n", 2**4)


def test_wrong_secret_is_detected_with_account_id(fast_kdf):
    w = new_short_wallet(SECRET)
    with pytest.raises(WrongSecret):
        restore_phrase(w["short_words"], SECRET + "x", w["account_id"])


def test_mistyped_word_is_detected(fast_kdf):
    w = new_short_wallet(SECRET)
    words = list(w["short_words"])
    words[0] = "abandon" if words[0] != "abandon" else "ability"
    with pytest.raises(WrongSecret):
        restore_phrase(words, SECRET, w["account_id"])


def test_correct_secret_passes_account_check(fast_kdf):
    w = new_short_wallet(SECRET)
    assert restore_phrase(w["short_words"], SECRET, w["account_id"].upper()) == w["seed_phrase"]


def test_real_cost_wrong_secret_detected():
    w = new_short_wallet(SECRET)
    with pytest.raises(WrongSecret):
        restore_phrase(w["short_words"], SECRET + "x", w["account_id"])


def test_1000_round_trips_and_wrong_secret_every_time(fast_kdf):
    for i in range(1000):
        s = f"round trip secret {i} with enough length"
        w = new_short_wallet(s)
        assert restore_phrase(w["short_words"], s, w["account_id"]) == w["seed_phrase"]
        with pytest.raises(WrongSecret):
            restore_phrase(w["short_words"], s + "!", w["account_id"])


@pytest.mark.parametrize("bad", ["short", "a" * 40, "abababababababababababab"])
def test_weak_secrets_rejected(bad):
    with pytest.raises(ValueError):
        new_short_wallet(bad)


def test_no_network_during_shorten_and_restore(monkeypatch, fast_kdf):
    def boom(*a, **k):
        raise AssertionError("network access attempted")

    monkeypatch.setattr(socket.socket, "connect", boom)
    monkeypatch.setattr(socket, "getaddrinfo", boom)
    w = new_short_wallet(SECRET)
    assert restore_phrase(w["short_words"], SECRET, w["account_id"]) == w["seed_phrase"]


def test_unknown_word_rejected():
    with pytest.raises(ValueError):
        restore_phrase(["zzzz"] * 6, SECRET)


def test_local_app_round_trip(fast_kdf):
    from src.app import Handler

    srv = HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_port}"

    def post(path, body):
        req = urllib.request.Request(base + path, json.dumps(body).encode(), method="POST")
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, json.load(r)
        except urllib.error.HTTPError as e:
            return e.code, json.load(e)

    try:
        code, w = post("/api/new", {"secret": SECRET})
        assert code == 200 and len(w["short_words"]) == 6
        code, r = post("/api/restore", {"words": w["short_words"], "secret": SECRET, "account_id": w["account_id"]})
        assert code == 200 and key_from_phrase(r["phrase"])["public_key_hex"] == w["account_id"]
        code, _ = post("/api/restore", {"words": w["short_words"], "secret": SECRET + "x", "account_id": w["account_id"]})
        assert code == 403
        code, _ = post("/api/new", {"secret": "short"})
        assert code == 400
    finally:
        srv.shutdown()
