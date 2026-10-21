---
name: recovery-phrase-shortener
description: Use when building, testing or explaining the offline Recovery Phrase Shortener for NEAR wallets. Covers shortening a 12-word BIP-39 recovery phrase with a user secret, restoring it, deriving the NEAR ed25519 key at m/44'/397'/0', and verifying the restore on testnet. Do not use for mainnet keys, real funds, or any network-based key handling.
---

# Recovery Phrase Shortener

## Purpose

Turn a 12-word NEAR recovery phrase plus a user secret into a shorter word set, and restore the original phrase from that set plus the same secret. Everything runs offline.

## Rules

1. The core shorten and restore functions make no network calls.
2. A shorter word set cannot hold all 128 bits of a 12-word phrase. Always state the bit budget. The secret supplies the difference.
3. Enforce a minimum secret strength. Reject short or simple secrets.
4. Never log, store or transmit the 12 words or the secret. Never commit them to the repository.
5. Testnet only. Never create, fund or move mainnet keys in the demo.
6. The NEAR key derivation must match `near-seed-phrase` and `@fastnear/seed-phrase` at `m/44'/397'/0'` (SLIP-10, ed25519).

## Workflow

1. Validate the 12-word phrase (BIP-39 wordlist and checksum).
2. Derive the NEAR public key and implicit account ID. Keep them for the parity check.
3. Shorten: produce the short word set from the phrase and the secret, using the scheme in `02-technical-design.md`.
4. Restore: rebuild the 12-word phrase from the short set and the secret. Compare with the original.
5. Parity: derive the key again from the restored phrase. Public key and account ID must match.
6. Testnet (optional for the demo): fund the account from the faucet and sign one small transfer.
7. Report: the round-trip test count, the parity result, and the testnet transaction if run.

## Test checklist

- [ ] 1,000 random round trips pass
- [ ] Wrong secret fails on every case
- [ ] Derived key matches two independent NEAR libraries
- [ ] Testnet transfer signed by the restored key succeeds
- [ ] No network requests during shorten or restore

## References

- NEAR implicit accounts: https://docs.near.org/integrator/implicit-accounts
- near-kit SecretKey: https://docs.rs/near-kit/latest/near_kit/types/enum.SecretKey.html
- FastNEAR keys and accounts: https://js.fastnear.com/accounts
- near-seed-phrase-py: https://pypi.org/project/near-seed-phrase-py
- Hackathon spec: https://nearhackathon.com/HACKATHON.md

## Out of scope

- Mainnet deployment
- Wallet integration with NEAR wallets
- Storing secrets in any online service
- Recovery without the secret
