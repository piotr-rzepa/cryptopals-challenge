from utils import add_pkcs7_padding, test_output

INPUT: bytes = b"YELLOW SUBMARINE"
BLOCK_LENGTH: int = 20
OUTPUT: bytes = b"YELLOW SUBMARINE\x04\x04\x04\x04"


def main() -> None:
    result = add_pkcs7_padding(INPUT, BLOCK_LENGTH)
    print(f"Plaintext block after padding: {result}")

    test_output(result, OUTPUT)


if __name__ == "__main__":
    main()
