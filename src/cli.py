"""Offline command line: create a 6-word wallet and restore the phrase from it.

    python -m src.cli new        prints the 6 words and the public account ID
    python -m src.cli restore    asks for the 6 words and account ID, prints the 12-word phrase

The secret is read with getpass (or RPS_SECRET for scripts). The 12-word phrase is
never printed by `new`; only `restore` shows it, because that is its purpose.
No network access.
"""
import argparse
import getpass
import os
import sys

from src.shorten import WrongSecret, new_short_wallet, restore_phrase


def _secret(confirm: bool) -> str:
    secret = os.environ.get("RPS_SECRET")
    if secret is not None:
        return secret
    secret = getpass.getpass("Secret: ")
    if confirm and getpass.getpass("Repeat secret: ") != secret:
        raise SystemExit("secrets do not match")
    return secret


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="rps")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("new")
    r = sub.add_parser("restore")
    r.add_argument("--words", help="the 6 words, space separated")
    r.add_argument("--account-id", help="public account ID saved with the words")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "new":
            w = new_short_wallet(_secret(confirm=True))
            print("Short words :", " ".join(w["short_words"]))
            print("Account ID  :", w["account_id"])
            print("Save the words and the account ID. Keep the secret separate. Testnet only.")
        else:
            words = (args.words or input("6 words: ")).split()
            account_id = args.account_id or input("Account ID: ").strip()
            print("Phrase:", restore_phrase(words, _secret(confirm=False), account_id))
    except WrongSecret as exc:
        print("error:", exc, file=sys.stderr)
        return 2
    except ValueError as exc:
        print("error:", exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
