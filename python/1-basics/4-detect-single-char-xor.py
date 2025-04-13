import pathlib
from utils import detect_single_char_xor
import binascii

INPUT: bytes = b"1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"


def main() -> None:
    path_to_file = pathlib.Path("./assets/4.txt")

    idx, score, xor_result = sorted(
        [
            detect_single_char_xor(binascii.unhexlify(input.encode()))
            for input in path_to_file.read_text().splitlines()
        ],
        key=lambda t: t[1],
    )[0]
    print(f"Best score: {score:6f}, word: {xor_result}, character used: {chr(idx)}")


if __name__ == "__main__":
    main()
