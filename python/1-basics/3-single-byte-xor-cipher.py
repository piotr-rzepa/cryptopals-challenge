from typing import LiteralString, Dict, List, Tuple

INPUT: LiteralString = (
    "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
)
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


def main() -> None:
    input_hex_decoded = bytes.fromhex(INPUT)

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
