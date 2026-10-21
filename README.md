# Recovery Phrase Shortener

Offline tool for NEAR wallets. Turns a 12-word recovery phrase plus a user
secret into a shorter word set, and restores the original phrase from that set
plus the same secret. Nothing leaves the device.

Status: prototype. The shortening scheme is not yet finalised; see
`docs/02-technical-design.md` (open problem: the secret must carry the bits a
shorter word list cannot hold).

## Setup

    python3 -m venv .venv
    . .venv/bin/activate
    pip install near-seed-phrase-py pytest
    python -m pytest -q

## Layout

- `src/derive.py`: NEAR key derivation (SLIP-10 ed25519, path m/44'/397'/0')
- `tests/`: derivation tests
- `docs/`: overview, technical design, feasibility check, plain-language explainer
- `skills/recovery-phrase-shortener/SKILL.md`: rules and workflow for agents

## Not for real funds

Testnet only. No security audit has been done.
