from typing import Dict, Tuple, List, Generator
import math
from collections import Counter
import pathlib
import base64

# https://web.archive.org/web/20170918020907/http://www.data-compression.com/english.html
ENGLISH_LETTERS_FREQS: Dict[str, float] = {
    "a": 0.0651738,
    "b": 0.0124248,
    "c": 0.0217339,
    "d": 0.0349835,
    "e": 0.1041442,
    "f": 0.0197881,
    "g": 0.0158610,
    "h": 0.0492888,
    "i": 0.0558094,
    "j": 0.0009033,
    "k": 0.0050529,
    "l": 0.0331490,
    "m": 0.0202124,
    "n": 0.0564513,
    "o": 0.0596302,
    "p": 0.0137645,
    "q": 0.0008606,
    "r": 0.0497563,
    "s": 0.0515760,
    "t": 0.0729357,
    "u": 0.0225134,
    "v": 0.0082903,
    "w": 0.0171272,
    "x": 0.0013692,
    "y": 0.0145984,
    "z": 0.0007836,
    " ": 0.1918182,
}


# Helper function for calculating letter frequency of a word
def score_function(input: bytes) -> float:
    word_freqs = {lt: 0.0 for lt in ENGLISH_LETTERS_FREQS.keys()}

    for w in input:
        if chr(w).lower() in ENGLISH_LETTERS_FREQS.keys():
            word_freqs[chr(w).lower()] += 1

    word_freqs = word_freqs | {
        lt: freq / len(input) for lt, freq in word_freqs.items() if freq != 0.0
    }
    return sum(
        [
            abs(x - y)
            for x, y in zip(word_freqs.values(), ENGLISH_LETTERS_FREQS.values())
        ]
    )


def detect_single_char_xor(input: bytes) -> Tuple[int, float, bytes]:
    result: List[Tuple[int, float, bytes]] = []
    for i in range(256):
        xor_output_bytes = bytes([x ^ i for x in input])

        score = score_function(xor_output_bytes)
        result.append((i, score, xor_output_bytes))

    idx, score, xor_result = sorted(result, key=lambda t: t[1])[0]

    return (idx, score, xor_result)


def binary_representation(utf_8_bytes: bytes) -> str:
    return "".join(f"{x:08b}" for x in utf_8_bytes)


# I'm using the following principle - for binary strings a and b the Hamming distance is equal to the number of ones (population count) in a XOR b.
def calculate_hamming_distance(str1: bytes, str2: bytes) -> int:
    first_as_bin, second_as_bin = (
        binary_representation(str1),
        binary_representation(str2),
    )
    xor_result = int(first_as_bin, 2) ^ int(second_as_bin, 2)
    ct = Counter(f"{xor_result:b}")
    return ct["1"]


def find_shortest_distance(content: bytes, key_size_range: range) -> Tuple[int, float]:
    best_candidate = (0, math.inf)
    for key_size in key_size_range:
        chunks = [content[i : i + key_size] for i in range(0, len(content), key_size)]
        output = []
        for i in range(0, len(chunks) - 1):
            first_block, second_block = chunks[i], chunks[i + 1]
            block_distance = calculate_hamming_distance(first_block, second_block)
            output.append(block_distance / key_size)

        candidate = sum(output) / len(output)
        if candidate < best_candidate[1]:
            best_candidate = (key_size, candidate)

    # The smallest hamming distance is our best candidate
    return best_candidate


def split_into_chunks(content: bytes, chunk_size: int) -> Generator[bytes, None, None]:
    for i in range(0, len(content), chunk_size):
        yield content[i : i + chunk_size]


def main() -> None:
    assert calculate_hamming_distance(b"this is a test", b"wokka wokka!!!") == 37
    assert calculate_hamming_distance(b"wokka wokka!!!", b"this is a test") == 37

    path_to_file = pathlib.Path("./assets/6.txt")
    file_content_bytes = path_to_file.read_bytes()

    decoded_file_content = base64.b64decode(file_content_bytes)

    key_size, hamming_distance = find_shortest_distance(
        decoded_file_content, range(2, 41)
    )
    print(f"key size: {key_size}, distance: {hamming_distance}")
    chunked_content = list(split_into_chunks(decoded_file_content, key_size))

    idx_to_remove = []
    for i, x in enumerate(chunked_content):
        if len(x) != key_size:
            idx_to_remove.append(i)

    for idx in idx_to_remove:
        chunked_content.pop(idx)

    transposed_list = [[x[i] for x in chunked_content] for i in range(key_size)]

    letters = []
    for x in transposed_list:
        idx, _, _ = detect_single_char_xor(bytes(x))
        letters.append(chr(idx).encode())

    print(b"".join(letters), key_size)


if __name__ == "__main__":
    main()
