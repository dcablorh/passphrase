# Recovery Phrase Shortener

Offline tool for NEAR wallets. Creates a new wallet whose 12-word recovery
phrase can be stored as 6 words plus a user secret, and restores the phrase
from those 6 words, the secret and the public account ID. Nothing leaves the
device.

Status: prototype, 6-word scheme v1 (see `docs/05-decision-6-word-scheme.md`).
New wallets only: an existing phrase cannot be shortened.

## Setup

    python3 -m venv .venv
    . .venv/bin/activate
    pip install near-seed-phrase-py pytest
    python -m pytest -q

## Use

    python -m src.cli new         # 6 words + account ID (asks for the secret)
    python -m src.cli restore     # 6 words + account ID + secret -> 12-word phrase
    python -m src.app             # local two-step UI at http://127.0.0.1:8765

Restore checks the result against the account ID and refuses a wrong secret or
a mistyped word. Save the 6 words and the account ID together; keep the secret
separate. The secret needs 20+ characters (8+ distinct), or 6 random words.

## Testnet check

    python -m src.testnet_check prepare      # prints words, secret, account ID
    # fund the account ID from a testnet faucet, then:
    RPS_SECRET="<secret>" python -m src.testnet_check transfer \
        --words "<6 words>" --account-id <64 hex> --to <testnet account>

## Layout

- `src/derive.py`: NEAR key derivation (SLIP-10 ed25519, path m/44'/397'/0')
- `src/shorten.py`: 6-word scheme, `new_short_wallet` and `restore_phrase`
- `src/cli.py`, `src/app.py`: command line and local demo UI
- `src/testnet_check.py`: signs and broadcasts a testnet transfer with the restored key
- `tests/`: derivation, round-trip (1,000 cases), wrong-secret, offline and transaction tests
- `docs/`: overview, technical design, feasibility check, plain-language explainer, decision
- `skills/recovery-phrase-shortener/SKILL.md`: rules and workflow for agents

## Not for real funds

Testnet only. No security audit has been done.
