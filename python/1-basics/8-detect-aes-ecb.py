import pathlib
import binascii
from typing import List, Tuple
from utils import split_into_chunks, has_duplicates

CHUNK_SIZE: int = 16


def main() -> None:
    path_to_file = pathlib.Path("./assets/8.txt")

    hex_encoded_file_content_lines = path_to_file.read_text().splitlines()
    decoded_file_content_lines_bytes = [
        binascii.unhexlify(x) for x in hex_encoded_file_content_lines
    ]

    candidates: List[Tuple[int, bytes]] = []

    for idx, x in enumerate(decoded_file_content_lines_bytes):
        chunked = list(split_into_chunks(x, CHUNK_SIZE))
        if has_duplicates(chunked):
            candidates.append((idx, x))

    for idx, candidate in candidates:
        print(f"Candidate: {candidate} at line: {idx}")


if __name__ == "__main__":
    main()
