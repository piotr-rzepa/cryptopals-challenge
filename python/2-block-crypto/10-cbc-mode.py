import pathlib
import random
import base64
from typing import LiteralString
from utils import (
    cbc_encrypt,
    cbc_decrypt,
    test_output,
)
from string import ascii_uppercase
from random import choice

CBC_DECRYPTION_KEY: bytes = b"YELLOW SUBMARINE"
IV_INIT_VECTOR: bytes = b"\x00" * len(CBC_DECRYPTION_KEY)


def main() -> None:
    path_to_file = pathlib.Path("./assets/10.txt")
    file_content_b64 = path_to_file.read_bytes()
    file_content_plain = base64.b64decode(file_content_b64)

    # Testing
    random_key_size = random.choice([16, 32])
    plaintexts = [
        "".join(choice(ascii_uppercase) for _ in range(random_key_size)).encode()
        for _ in range(20)
    ]
    encr_keys = [
        "".join(choice(ascii_uppercase) for _ in range(random_key_size)).encode()
        for _ in range(20)
    ]
    init_vectors = [
        "".join(choice(ascii_uppercase) for _ in range(random_key_size)).encode()
        for _ in range(20)
    ]
    for msg, encr_key, init_v in zip(plaintexts, encr_keys, init_vectors):
        ciphertext = cbc_encrypt(msg, encr_key, init_v)
        decrypted_msg = cbc_decrypt(ciphertext, encr_key, init_v)

        test_output(decrypted_msg, msg)

    decrypted_file = cbc_decrypt(file_content_plain, CBC_DECRYPTION_KEY, IV_INIT_VECTOR)
    print(decrypted_file)


if __name__ == "__main__":
    main()
