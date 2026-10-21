# Recovery Phrase Shortener

**Track fit:** Privacy & Private AI (primary), AI Security & Defense (secondary)
**Event:** NEAR HACKATHON, development 1–14 Nov 2026, results by 18 Nov 2026

## One-line pitch

An offline tool that turns a 12-word NEAR recovery phrase into a shorter word set, which can only be turned back into the original phrase together with the user's own secret.

## Problem

A NEAR wallet is controlled by a 12-word recovery phrase. Anyone who has the phrase owns the wallet. Users have to write it down and store it somewhere safe, and long lists of words are easy to copy wrong, lose, or photograph by accident.

## Solution

The user enters their 12 words and a secret (a long passphrase they choose). The app runs entirely on their device and produces a shorter word set. Without the secret, the short set does not reveal the wallet. With the secret, the app rebuilds the original 12 words and the same NEAR key.

## Demo that proves it

1. Generate a 12-word phrase and derive the NEAR account.
2. Shorten it with a secret. Show the short word set.
3. Restore from the short set plus the secret. Show the same account ID.
4. On NEAR testnet, fund the restored account from the faucet and send a small transfer signed with the restored key.

Step 4 is the proof judges can check: the restored key controls a real account.

## Stack

- Browser or Python front end, offline (no network calls in the core flow)
- BIP-39 word list and SLIP-10 ed25519 derivation at the NEAR path `m/44'/397'/0'`
- Key derivation checked against NEAR tooling (`near-seed-phrase`, `@fastnear/seed-phrase`, `near-kit`)
- Testnet demo only; no mainnet keys are created or moved

## Honest limits

- A shorter word set cannot hold all 128 bits of a 12-word phrase by itself. The user's secret must carry the difference. See `02-technical-design.md`.
- A weak secret (a short password) makes the short set brute-forceable offline. The app must enforce a minimum strength.
- Losing the secret means losing the wallet. The app cannot recover it.
- This is a hackathon prototype, not a production wallet. Do not use it for real funds until it has a security audit.

## Judging angle

- Originality: a recovery method that needs both the words and a secret, instead of words alone
- Impact: safer backups for NEAR users who now store plain word lists
- Technical quality: deterministic restore, tested against real NEAR derivation, offline by design
- Design: a simple two-step flow a non-technical user can follow
