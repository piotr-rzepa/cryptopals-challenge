import base64
from typing import LiteralString

INPUT: LiteralString = (
    "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
)
EXPECTED_OUTPUT: LiteralString = (
    "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
)


def test_output(output: bytes) -> None | AssertionError:
    assert output == EXPECTED_OUTPUT.encode()


def main() -> None:
    input_decoded_bytes = bytes.fromhex(INPUT)
    output_bytes = base64.b64encode(input_decoded_bytes)

    print(f"Input (str): {input}")
    print(f"Expected output (bytes): {EXPECTED_OUTPUT.encode()}")
    print(f"Script output (bytes): {output_bytes}")

    test_output(output_bytes)


if __name__ == "__main__":
    main()
