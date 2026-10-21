# Decision: 6-word short form (2026-10-21)

User choice: 6 words.

## Corrected bit budget

A BIP-39 12-word phrase is 128 bits of entropy. The 4-bit checksum is derived
from that entropy, so it adds no information. (The earlier docs said 132 bits;
that was wrong.)

- Short form: 6 words = 66 bits
- Secret must supply the remaining 62 bits

## Scheme v1 (implemented in src/shorten.py)

    E = A (66 bits, random) || B (62 bits, from secret)
    B = scrypt(secret, "rps-v1-B") truncated to 62 bits
    Q = A XOR scrypt(secret, "rps-v1-A") truncated to 66 bits  -> 6 words

Stored: 6 words. Restore: A = Q XOR KDF_A(secret), B = KDF_B(secret), phrase = mnemonic(A||B).

## Limits (must be stated in the pitch)

1. New wallets only. B comes from the secret, so an existing wallet whose
   phrase was generated elsewhere cannot be shortened with this scheme.
   The demo must create a new wallet with the app.
2. Strength is about 62 bits against offline guessing of the secret. The
   public account ID lets an attacker check guesses without a chain oracle, so
   scrypt cost is the main defence. Use scrypt n=2^15 (current) or higher.
3. Requires a secret of at least 20 characters (enforced). Recommend 6 random
   words from a standard list (about 66 bits).
4. Wrong secret is detected by comparing the restored account ID with the
   stored public account ID.

## Status

- Round-trip, wrong-secret, short-form and random-round-trip tests: pass (9 tests)
- Parity with @fastnear/seed-phrase: pass (same public key and account ID)
- Testnet transfer with restored key: NOT run. NEAR testnet RPC returns 403
  from the build sandbox. Run it from a machine with normal internet access.
