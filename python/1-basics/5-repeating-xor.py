import binascii
from typing import LiteralString

from utils import test_output

INPUT: LiteralString = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""
XOR_KEY: LiteralString = "ICE"
EXPECTED_OUTPUT: LiteralString = (
    "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
)


def main() -> None:
    input_bytes = INPUT.encode()

    repeated_xor_key = (
        XOR_KEY * (len(INPUT) // len(XOR_KEY)) + XOR_KEY[: len(INPUT) % len(XOR_KEY)]
    ).encode()

    encrypted_list = [x ^ y for x, y in zip(input_bytes, repeated_xor_key)]
    output = binascii.hexlify(bytes(encrypted_list))

    test_output(output, EXPECTED_OUTPUT.encode())


if __name__ == "__main__":
    main()
