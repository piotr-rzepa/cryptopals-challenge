from typing import List, Tuple
from utils import score_function
import binascii

INPUT: bytes = b"1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"


def main() -> None:
    input_hex_decoded = binascii.unhexlify(INPUT)

    result: List[Tuple[int, float, bytes]] = []
    for i in range(256):
        xor_output_bytes = bytes([x ^ i for x in input_hex_decoded])

        score = score_function(xor_output_bytes)
        result.append((i, score, xor_output_bytes))

    idx, score, xor_result = sorted(result, key=lambda t: t[1])[0]

    print(
        f"The string, which after xor operation has the best score ({score:.4f}) english letters: {xor_result}"
    )
    print(f"Character used for XOR operation: {chr(idx)}")


if __name__ == "__main__":
    main()
