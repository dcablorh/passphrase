import base64
import hashlib
import struct

import base58
from nacl.signing import VerifyKey

from src.derive import key_from_phrase
from src.testnet_check import YOCTO, build_signed_transfer

PHRASE = "dirt holiday borrow online web miracle problem obey capable general thumb inhale"


def test_signed_transfer_layout_and_signature_verify():
    k = key_from_phrase(PHRASE)
    signer = k["public_key_hex"]
    block_hash = bytes(range(32))
    raw = base64.b64decode(build_signed_transfer(k["secret_key"], signer, "bob.testnet", 5 * YOCTO, 7, block_hash))
    tx, sig = raw[:-65], raw[-65:]
    assert sig[0] == 0
    pub = base58.b58decode(k["public_key"].split(":")[1])
    VerifyKey(pub).verify(hashlib.sha256(tx).digest(), sig[1:])
    n = struct.unpack_from("<I", tx)[0]
    assert tx[4:4 + n].decode() == signer
    o = 4 + n
    assert tx[o] == 0 and tx[o + 1:o + 33] == pub
    assert struct.unpack_from("<Q", tx, o + 33)[0] == 7
    o += 41
    m = struct.unpack_from("<I", tx, o)[0]
    assert tx[o + 4:o + 4 + m] == b"bob.testnet"
    o += 4 + m
    assert tx[o:o + 32] == block_hash
    assert struct.unpack_from("<I", tx, o + 32)[0] == 1 and tx[o + 36] == 3
    assert int.from_bytes(tx[o + 37:o + 53], "little") == 5 * YOCTO
    assert len(tx) == o + 53
