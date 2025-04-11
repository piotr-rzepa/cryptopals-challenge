from typing import LiteralString, List, Tuple
import pathlib
from utils import score_function

INPUT: LiteralString = (
    "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
)


def detect_single_char_xor(input: str) -> Tuple[int, float, bytes]:
    input_hex_decoded = bytes.fromhex(input)
    result: List[Tuple[int, float, bytes]] = []
    for i in range(256):
        xor_output_bytes = bytes([x ^ i for x in input_hex_decoded])

        score = score_function(xor_output_bytes)
        result.append((i, score, xor_output_bytes))

    idx, score, xor_result = sorted(result, key=lambda t: t[1])[0]

    return (idx, score, xor_result)


def main() -> None:
    path_to_file = pathlib.Path("./assets/4.txt")

    idx, score, xor_result = sorted(
        [
            detect_single_char_xor(input)
            for input in path_to_file.read_text().splitlines()
        ],
        key=lambda t: t[1],
    )[0]
    print(f"Best score: {score:6f}, word: {xor_result}, character used: {chr(idx)}")


if __name__ == "__main__":
    main()
