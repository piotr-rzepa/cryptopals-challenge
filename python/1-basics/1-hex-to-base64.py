import base64
from utils import test_output
import binascii

INPUT: bytes = b"49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
EXPECTED_OUTPUT: bytes = (
    b"SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
)


def main() -> None:
    input_decoded_bytes = binascii.unhexlify(INPUT)
    output_bytes = base64.b64encode(input_decoded_bytes)

    print(f"Script output: {output_bytes}")

    test_output(output_bytes, EXPECTED_OUTPUT)


if __name__ == "__main__":
    main()
