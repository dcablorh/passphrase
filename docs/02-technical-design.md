# Technical Design: Recovery Phrase Shortener

## 1. Goal

Given a valid 12-word BIP-39 phrase `P` and a user secret `S`, produce a shorter word list `Q` such that:

- `Recover(Q, S) = P` exactly, and the same NEAR key is derived.
- `Q` alone reveals no usable information about `P` (within the stated secret-strength assumptions).

> Update 2026-10-21: the 6-word scheme is chosen and implemented. See docs/05-decision-6-word-scheme.md. The 132-bit figure below is wrong: BIP-39 entropy is 128 bits; the checksum is derived.

## 2. Why the short form needs the secret

A 12-word BIP-39 phrase encodes 128 bits of entropy plus a 4-bit checksum, 132 bits in total, at 11 bits per word.

A word list of `k` words carries `11k` bits. For `Q` to be shorter than `P`, `11k < 132`, so `Q` cannot encode the whole of `P`. The missing bits have to come from `S`.

Split of the information:

```
  P (132 bits)  =  Q (11k bits)  +  S (contributes the rest)
```

This is an information-theoretic fact, not an implementation choice. Any design that claims a short phrase plus no secret restores a 12-word phrase is wrong.

## 3. Proposed scheme (draft)

Use a split with a key-derivation step:

1. Parse `P` to 132 bits. Take the 128-bit entropy `E`.
2. Choose a short length `k` (for example 8 words, 88 bits). Let the short set carry the first 88 bits of `E` XORed with a key stream `K1 = KDF(S, salt, 88 bits)`.
3. The remaining 40 bits of `E` are derived from `S` with a second, independent key stream `K2 = KDF(S, salt, 40 bits)`. These are not stored. They must be re-derived from `S`.

Problem to resolve before building: step 3 as written means `S` alone determines the last 40 bits, so anyone who knows `S` can recover them without `Q`, but `Q` is still needed for the first 88. That is correct only if the 40 bits are derived deterministically from `S` and `E` is then recomputed. This is circular: `E` must be known to derive `K2`.

**Corrected design (to be tested):**

- Store `Q = E[0:88] XOR KDF(S, salt, 88)` (8 words) plus a short checksum over `E` so the app can detect a wrong secret.
- The restore path needs all 128 bits of `E`. It therefore needs `S` to supply the missing 40 bits in a way that is not circular. The clean option is to store 16 words instead of 8, which gives no shortening, or to make `S` a long passphrase that is hashed to 40 bits and used as a second XOR mask over a bit-level check.

**Recommendation for the hackathon:** Do not claim 8-word storage. Build a 12-word-to-N-word scheme where N is chosen so that the missing bits are derivable from `S`, and verify the information budget in code before the demo. Report the real word count in the pitch.

This is the main open design question. It needs a short written proof and a test before the project can say it "works".

## 4. Derivation for the NEAR key

- Seed: BIP-39 seed from the 12 words (empty passphrase, as in `near-seed-phrase`)
- Key: SLIP-10 ed25519 at `m/44'/397'/0'` (hardened path only)
- Account: implicit account ID is the lowercase hex of the 32-byte public key (64 characters)
- Verify: the restored phrase must give the same public key, public key string, and account ID as the original

## 5. Components

| Component | Responsibility | Notes |
|---|---|---|
| `shorten.py` or `shorten.js` | Phrase to short set + secret | Offline, pure function |
| `restore.py` or `restore.js` | Short set + secret to phrase | Offline, pure function |
| `derive.py` | Phrase to NEAR key and account | Uses `near-seed-phrase-py` or `@fastnear/seed-phrase` |
| `testnet_check.py` | Fund and sign a transfer | Testnet only; uses faucet |
| `index.html` | Two-step UI | Optional, for the demo video |

## 6. Test plan

1. Round trip: for 1,000 random phrases and secrets, `restore(shorten(P, S), S) == P`.
2. Wrong secret: restore with a wrong `S` fails the checksum on every try.
3. Derivation parity: derived public key equals the value from `near-seed-phrase-py` and `@fastnear/seed-phrase`.
4. Testnet: the restored account is funded, and a signed transfer succeeds.
5. Offline: no network requests during shorten or restore (checked in the browser devtools or with a proxy).
6. Secret strength: weak secrets are rejected below a stated entropy threshold.

## 7. Security notes

- Never send `P` or `S` over a network.
- Clear secrets from memory where the language allows.
- Keys stay in the browser or on the device. Never write them to the repository.
- Publish the threat model: what an attacker with `Q` learns, and what an attacker with `Q` and a guessed secret learns.

## 8. Tooling

- NEAR docs: https://docs.near.org/
- Derivation references: https://docs.rs/near-kit/latest/near_kit/types/enum.SecretKey.html , https://js.fastnear.com/accounts , https://pypi.org/project/near-seed-phrase-py
- Hackathon spec: https://nearhackathon.com/HACKATHON.md
