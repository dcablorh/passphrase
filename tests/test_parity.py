from src.derive import key_from_phrase

# Vector checked against @fastnear/seed-phrase (parseSeedPhrase) on 2026-10-21.
PHRASE = "dirt holiday borrow online web miracle problem obey capable general thumb inhale"
PUBLIC_KEY = "ed25519:AgKXuuBbNgVGsHihJPjXwW6Yp9nhYXzHmUpUvFCWS2bS"
ACCOUNT_ID = "8fcbca07e9feb71a81cf8414a37787bd824895c3d8141b16dfb6cbb3b6ddfc89"


def test_matches_fastnear_seed_phrase():
    k = key_from_phrase(PHRASE)
    assert k["public_key"] == PUBLIC_KEY
    assert k["public_key_hex"] == ACCOUNT_ID
