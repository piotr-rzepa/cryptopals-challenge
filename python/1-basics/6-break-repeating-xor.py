import pathlib
import base64
from utils import (
    split_into_chunks,
    calculate_hamming_distance,
    detect_single_char_xor,
    find_shortest_distance,
)


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
