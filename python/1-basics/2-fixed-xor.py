import binascii
from utils import test_output

INPUT: bytes = b"1c0111001f010100061a024b53535009181c"
XOR_VALUE: bytes = b"686974207468652062756c6c277320657965"
EXPECTED_OUTPUT: bytes = b"746865206b696420646f6e277420706c6179"


def main() -> None:
    decoded_input = binascii.unhexlify(INPUT)
    decoded_xor = binascii.unhexlify(XOR_VALUE)

    after_xor = [x ^ y for x, y in zip(decoded_input, decoded_xor)]
    output = "".join(list(map(chr, after_xor)))
    output_hex = binascii.hexlify(output.encode())

    print(f"Script output (str): {output}")
    print(f"Script output (hex): {output_hex}")

    test_output(output_hex, EXPECTED_OUTPUT)


if __name__ == "__main__":
    main()
