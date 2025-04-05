import binascii
from typing import LiteralString

INPUT: LiteralString = "1c0111001f010100061a024b53535009181c"
XOR_VALUE: LiteralString = "686974207468652062756c6c277320657965"
EXPECTED_OUTPUT: LiteralString = "746865206b696420646f6e277420706c6179"


def test_output(output: bytes) -> None | AssertionError:
    assert output == EXPECTED_OUTPUT.encode()


def main() -> None:
    decoded_input = bytes.fromhex(INPUT)
    decoded_xor = bytes.fromhex(XOR_VALUE)

    after_xor = [x ^ y for x, y in zip(decoded_input, decoded_xor)]
    output = "".join(list(map(chr, after_xor)))
    output_hex = binascii.hexlify(output.encode())

    print(f"Input (str): {input}")
    print(f"Expected output (bytes): {EXPECTED_OUTPUT.encode()}")
    print(f"Script output (str): {output}")
    print(f"Script output (hex): {output_hex}")

    test_output(output_hex)


if __name__ == "__main__":
    main()
