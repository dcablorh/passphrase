"""NEAR key derivation from a BIP-39 recovery phrase.

Uses SLIP-10 ed25519 at the NEAR HD path m/44'/397'/0' via the
near-seed-phrase-py library (a port of near/near-seed-phrase).
"""
from near_seed_phrase.main import generate_seed_phrase, parse_seed_phrase

NEAR_HD_PATH = "m/44'/397'/0'"


def new_phrase_and_key():
    """Create a fresh 12-word phrase and its NEAR key material."""
    return generate_seed_phrase()


def key_from_phrase(seed_phrase: str):
    """Derive NEAR key material from an existing 12-word phrase.

    Returns a dict with seed_phrase, secret_key, public_key and public_key_hex.
    public_key_hex is the implicit NEAR account ID (64 lowercase hex chars).
    """
    return parse_seed_phrase(seed_phrase, NEAR_HD_PATH)
