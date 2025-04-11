import pathlib
import binascii
from typing import Generator, List


def has_duplicates(lst: List) -> bool:
    n = max(set(lst), key=lst.count)
    return lst.count(n) > 1


def split_into_chunks(content: bytes, chunk_size: int) -> Generator[bytes, None, None]:
    for i in range(0, len(content), chunk_size):
        yield content[i : i + chunk_size]


def main() -> None:
    path_to_file = pathlib.Path("./assets/8.txt")

    hex_encoded_file_content_lines = path_to_file.read_text().splitlines()
    decoded_file_content_lines_bytes = [
        binascii.unhexlify(x) for x in hex_encoded_file_content_lines
    ]

    candidates = []

    for idx, x in enumerate(decoded_file_content_lines_bytes):
        print(f"Splitting {idx} string into chunks...")
        chunked = list(split_into_chunks(x, 16))
        for i, c in enumerate(chunked):
            print(f"Index: {i}, chunk: {c}")
        if has_duplicates(chunked):
            candidates.append((idx, x))

    print(candidates)


if __name__ == "__main__":
    main()
