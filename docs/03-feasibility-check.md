# Feasibility Check: Recovery Phrase Shortener

## Verdict

**Buildable as a hackathon prototype, but not yet confirmed as working.** The NEAR side is well documented. The shortening scheme is the open risk and must be fixed and tested first.

## Pages checked

| Page | What it confirmed | Status |
|---|---|---|
| https://nearhackathon.com/#tracks | 13 tracks; Privacy & Private AI and AI Security & Defense fit; submission needs a public repo and a demo post on X | Read |
| https://nearhackathon.com/HACKATHON.md | Dates, submission rules, track IDs (`privacy`, `security`), NEAR address rules, "never submit or post without human confirmation" | Read |
| https://docs.rs/near-kit/latest/near_kit/types/enum.SecretKey.html | `from_seed_phrase` uses SLIP-10 at `m/44'/397'/0'` | Read |
| https://docs.rs/near-kit/0.9.0/near_kit/client/struct.InMemorySigner.html | Signer from seed phrase; implicit account ID is hex of the public key | Read |
| https://docs.rs/crate/near-kit/latest/source/src/client/keyring_signer.rs | Seed-phrase import with explicit HD path | Read |
| https://docs.rs/duke-crypto-core/latest/src/duke_crypto_core/lib.rs.html | BIP-39 and SLIP-10 reference code | Read |
| https://js.fastnear.com/accounts | Matches `near-seed-phrase` and `near-cli` derivation; faucet is testnet only | Read |
| https://pypi.org/project/near-seed-phrase-py | Python port with generate and parse functions | Read |
| https://docs.near.org/integrator/implicit-accounts | Account ID is the lowercase hex of the 32-byte public key (64 characters); the page's examples use an old network and are outdated | Read, partly outdated |

## What is confirmed

- The NEAR derivation path and algorithm are documented and consistent across three independent implementations.
- The implicit account ID rule is documented.
- The hackathon allows an offline tool in the Privacy or Security track.
- The hackathon requires a public repository and a public demo post, and both must be done by a human.

## What is not confirmed

- **The shortening scheme.** A 12-word phrase cannot be stored in fewer words without losing bits. The secret must carry the difference, and the current draft in `02-technical-design.md` is circular for the 40-bit case. This must be solved and tested.
- **Secret strength.** A short password makes the short set attackable offline. No threshold has been chosen.
- **Testnet demo.** No transfer has been signed with a restored key yet.
- **Browser build.** No front end has been built or tested.

## Required before calling it "works"

1. Write the bit budget for the chosen word count, and check it with code.
2. Implement shorten and restore in code and pass the 1,000-case round-trip test.
3. Show derivation parity with `near-seed-phrase-py` or `@fastnear/seed-phrase`.
4. Run the testnet transfer with a restored key.
5. Confirm offline behaviour in the browser.

## Hackathon rule checks

- Repository must be public before 14 Nov 2026, 23:59 UTC.
- Demo post on X by the human, saying it was built at NEAR HACKATHON.
- Submit only after the human confirms the exact payload.
- Do not create or invent a NEAR address for the prize; the team provides it.
