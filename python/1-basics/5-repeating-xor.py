import binascii

from utils import test_output

INPUT: bytes = b"""Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""
XOR_KEY: bytes = b"ICE"
EXPECTED_OUTPUT: bytes = b"0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"


def main() -> None:
    repeated_xor_key = (
        XOR_KEY * (len(INPUT) // len(XOR_KEY)) + XOR_KEY[: len(INPUT) % len(XOR_KEY)]
    )

    encrypted_list = [x ^ y for x, y in zip(INPUT, repeated_xor_key)]
    output = binascii.hexlify(bytes(encrypted_list))

    print(output)

    test_output(output, EXPECTED_OUTPUT)


if __name__ == "__main__":
    main()
