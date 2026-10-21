r"""End-to-end testnet check: the key restored from 6 words must be able to sign a transfer.

Testnet only. Two steps, run from the repo root:

  1. prepare   create a new short wallet, restore it from the 6 words, confirm the
               same account ID, and print the account ID to fund from the testnet faucet.
               The secret is read from RPS_SECRET, or generated (6 random words) and printed.
  2. transfer  restore the key from the 6 words + RPS_SECRET (checked against
               --account-id), sign a transfer of --amount NEAR to --to, broadcast
               it and confirm it on chain.

    python -m src.testnet_check prepare
    RPS_SECRET="..." python -m src.testnet_check transfer \
        --words "w1 w2 w3 w4 w5 w6" --account-id <64 hex> --to <account>
"""
import argparse
import base64
import hashlib
import json
import os
import secrets
import struct
import urllib.request

import base58
from nacl.signing import SigningKey

from src.derive import key_from_phrase
from src.shorten import WORDLIST, new_short_wallet, restore_phrase

RPC = "https://rpc.testnet.near.org"
YOCTO = 10**24
ED25519 = b"\x00"          # borsh key/signature type tag
TRANSFER = b"\x03"         # borsh action tag


def rpc(method: str, params):
    body = json.dumps({"jsonrpc": "2.0", "id": "rps", "method": method, "params": params}).encode()
    req = urllib.request.Request(RPC, body, {"content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        out = json.load(resp)
    if "error" in out:
        raise RuntimeError(out["error"])
    return out["result"]


def _view_account(account_id: str):
    try:
        return rpc("query", {"request_type": "view_account", "finality": "final", "account_id": account_id})
    except RuntimeError as exc:
        if "does not exist" in json.dumps(exc.args[0]):
            return None
        raise


def _str(s: str) -> bytes:
    raw = s.encode()
    return struct.pack("<I", len(raw)) + raw


def build_signed_transfer(secret_key: str, signer_id: str, receiver: str, yocto: int,
                          nonce: int, block_hash: bytes) -> str:
    """Borsh-encode and sign a single-Transfer transaction. Pure function, no network."""
    sk = SigningKey(base58.b58decode(secret_key.split(":", 1)[1])[:32])
    pub = bytes(sk.verify_key)
    tx = (_str(signer_id) + ED25519 + pub + struct.pack("<Q", nonce)
          + _str(receiver) + block_hash
          + struct.pack("<I", 1) + TRANSFER + yocto.to_bytes(16, "little"))
    sig = sk.sign(hashlib.sha256(tx).digest()).signature
    return base64.b64encode(tx + ED25519 + sig).decode()


def _signed_transfer(account_id: str, secret_key: str, receiver: str, yocto: int) -> str:
    sk = SigningKey(base58.b58decode(secret_key.split(":", 1)[1])[:32])
    pk = "ed25519:" + base58.b58encode(bytes(sk.verify_key)).decode()
    key = rpc("query", {"request_type": "view_access_key", "finality": "final",
                        "account_id": account_id, "public_key": pk})
    block_hash = base58.b58decode(rpc("block", {"finality": "final"})["header"]["hash"])
    return build_signed_transfer(secret_key, account_id, receiver, yocto, key["nonce"] + 1, block_hash)


def prepare() -> None:
    secret = os.environ.get("RPS_SECRET")
    generated = secret is None
    if generated:
        secret = " ".join(secrets.choice(WORDLIST) for _ in range(6))
    wallet = new_short_wallet(secret)
    restored = key_from_phrase(restore_phrase(wallet["short_words"], secret, wallet["account_id"]))
    assert restored["public_key_hex"] == wallet["account_id"], "restored account differs"
    print("short words :", " ".join(wallet["short_words"]))
    if generated:
        print("secret      :", secret, " (generated; keep it with the words)")
    print("account id  :", wallet["account_id"])
    print("restore matches the original account: yes")
    print("Fund this account on testnet, then run the transfer step.")


def transfer(words: str, account_id: str, to: str, amount: float) -> None:
    secret = os.environ["RPS_SECRET"]
    account_id = account_id.lower()
    key = key_from_phrase(restore_phrase(words.split(), secret, account_id))
    acct = _view_account(account_id)
    if acct is None:
        raise SystemExit(f"{account_id} is not funded yet")
    print("balance before (yocto):", acct["amount"])
    signed = _signed_transfer(account_id, key["secret_key"], to, int(amount * YOCTO))
    result = rpc("broadcast_tx_commit", [signed])
    status = result["status"]
    print("tx hash :", result["transaction"]["hash"])
    print("status  :", "SuccessValue" if "SuccessValue" in status else status)
    if "SuccessValue" not in status:
        raise SystemExit(1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("prepare")
    t = sub.add_parser("transfer")
    t.add_argument("--words", required=True)
    t.add_argument("--account-id", required=True, help="public account ID printed by prepare")
    t.add_argument("--to", required=True)
    t.add_argument("--amount", type=float, default=0.01)
    args = ap.parse_args()
    prepare() if args.cmd == "prepare" else transfer(args.words, args.account_id, args.to, args.amount)
