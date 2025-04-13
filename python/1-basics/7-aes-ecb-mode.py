import pathlib
import base64
from typing import LiteralString
from Crypto.Cipher import AES

AES128_ECB_KEY: bytes = b"YELLOW SUBMARINE"


def main() -> None:
    path_to_file = pathlib.Path("./assets/7.txt")
    b64_file_content_bytes = path_to_file.read_bytes()
    decoded_file_content_bytes = base64.b64decode(b64_file_content_bytes)

    cipher_aes = AES.new(AES128_ECB_KEY, AES.MODE_ECB)
    decrypted_data = cipher_aes.decrypt(decoded_file_content_bytes)
    print(decrypted_data)


if __name__ == "__main__":
    main()
