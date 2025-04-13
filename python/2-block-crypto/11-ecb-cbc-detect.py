from typing import Tuple
from utils import add_pkcs7_padding, test_output, split_into_chunks, has_duplicates
import random
from utils import cbc_encrypt
from functools import partial
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import math

KEY_SIZE: int = 16


def gen_random_aes_key(key_size: int = KEY_SIZE) -> bytes:
    return get_random_bytes(key_size)


def detect_ecb(ciphertext: bytes) -> bool:
    chunked = list(split_into_chunks(ciphertext, KEY_SIZE))
    if has_duplicates(chunked):
        return True
    return False


def detect_mode(ciphertext: bytes) -> str:
    if detect_ecb(ciphertext) is True:
        return "ECB"
    return "CBC"


def encryption_oracle(input: bytes) -> Tuple[str, bytes]:
    encryption_key = gen_random_aes_key()
    extra_padding_prefix = get_random_bytes(random.randint(5, 10))
    extra_padding_suffix = get_random_bytes(random.randint(5, 10))

    plaintext = extra_padding_prefix + input + extra_padding_suffix

    # Plaintext has to be padded to be multiple of 16 bytes (ECB)
    padded_plaintext = add_pkcs7_padding(
        plaintext, len(encryption_key) * math.ceil(len(plaintext) / len(encryption_key))
    )

    random_init_vector = get_random_bytes(len(encryption_key))

    modes: dict = {
        0: ("ECB", AES.new(key=encryption_key, mode=AES.MODE_ECB).encrypt),
        1: (
            "CBC",
            AES.new(
                key=encryption_key, mode=AES.MODE_CBC, IV=random_init_vector
            ).encrypt,
        ),
    }
    cipher, cipher_func = modes.get(random.randint(0, 1), 0)
    return (cipher, cipher_func(padded_plaintext))


def main() -> None:
    for _ in range(100):
        encrypt_mode, ciphertext = encryption_oracle(
            bytes(KEY_SIZE) * random.randint(3, 8)
        )
        predicted_mode = detect_mode(ciphertext)
        test_output(predicted_mode.encode(), encrypt_mode.encode())


if __name__ == "__main__":
    main()
