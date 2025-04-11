from typing import List, Generator, Dict, Tuple
import math
from collections import Counter

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
def score_function(
    input: bytes, freq_dict: Dict[str, float] = ENGLISH_LETTERS_FREQS
) -> float:
    """Calculates letter frequency of a given word, passed as bytes.

    Args:
        input: Word to calculate character frequency for, in bytes.
        freq_dict: base frequencies for each english letter as a dict.

    Returns:
        Float value denoting a score value, based on letter frequency, of a given word.

    """
    word_freqs = {lt: 0.0 for lt in freq_dict.keys()}

    for w in input:
        if chr(w).lower() in freq_dict.keys():
            word_freqs[chr(w).lower()] += 1

    word_freqs = word_freqs | {
        lt: freq / len(input) for lt, freq in word_freqs.items() if freq != 0.0
    }
    return sum([abs(x - y) for x, y in zip(word_freqs.values(), freq_dict.values())])


def detect_single_char_xor(input: bytes) -> Tuple[int, float, bytes]:
    """Detects a single character used for encrypting the input using XOR.

    Args:
        input: Encrypted message using single character XOR, in bytes.

    Returns:
        Tuple containing the ASCII code of a potential character used for XOR,
        a calculated score and a result after decrypting the messages using inverted
        XOR with the same character.
    """
    result: List[Tuple[int, float, bytes]] = []
    for i in range(256):
        xor_output_bytes = bytes([x ^ i for x in input])

        score = score_function(xor_output_bytes)
        result.append((i, score, xor_output_bytes))

    idx, score, xor_result = sorted(result, key=lambda t: t[1])[0]

    return (idx, score, xor_result)


def binary_representation(utf_8_bytes: bytes) -> str:
    """Converts UTF-8 encoded bytes to binary string representation.

    Args:
        utf_8_bytes: UTF-8 encoded bytes input.

    Returns:
        Binary string representation of a UTF-8 encoded bytes input.
    """
    return "".join(f"{x:08b}" for x in utf_8_bytes)


# I'm using the following principle - for binary strings a and b the Hamming distance is equal to the number of ones (population count) in a XOR b.
def calculate_hamming_distance(str1: bytes, str2: bytes) -> int:
    """Calculates Hamming Distance between two bytes blocks.

    Args:
        str1: First block, as a bytes input.
        str2: Second block, as a bytes input.

    Returns:
        Integer value representing Hamming Distance between two bytes blocks.
    """
    first_as_bin, second_as_bin = (
        binary_representation(str1),
        binary_representation(str2),
    )
    xor_result = int(first_as_bin, 2) ^ int(second_as_bin, 2)
    ct = Counter(f"{xor_result:b}")
    return ct["1"]


def find_shortest_distance(content: bytes, key_size_range: range) -> Tuple[int, float]:
    """Finds the smallest Hamming Distance across the chunked content.

    Args:
        content: Input in bytes, which will be split into multiple chunks.
        key_size_range: range of values representig size of the chunk to use when calculating Hamming Distance.

    Returns:
        Tuple with integer value being a key size used for chunking and a float being the smallest calculated hamming distance.
    """
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


def has_duplicates(lst: List) -> bool:
    """Checks a list for duplicate elements.

    Args:
        lst: List of elements to check for duplicates.

    Returns:
        True if a list contains duplicates, False otherwise.
    """
    n = max(set(lst), key=lst.count)
    return lst.count(n) > 1


def split_into_chunks(content: bytes, chunk_size: int) -> Generator[bytes, None, None]:
    """Splits the bytes content into multiple chunks of a given size.

    Args:
        content: Content in bytes, which should be split into multiple chunks.
        chunk_size: Size of the chunk to be used for splitting the content.

    Yields:
        Iterator containing the next chunk of the splitted content.
    """
    for i in range(0, len(content), chunk_size):
        yield content[i : i + chunk_size]


def test_output(output: bytes, expected_output: bytes) -> None | AssertionError:
    """Verifies output against an expected output.

    Args:
        output: An output which should be verified, in bytes.
        expected_output: An expected output, against which the user output will be verified, in bytes.

    Returns:
        None if there is no difference between output and expected output, AssertionError othwerise.
    """
    assert output == expected_output
