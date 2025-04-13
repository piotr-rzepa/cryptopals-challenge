from typing import Generator
from Crypto.Cipher import AES


def add_pkcs7_padding(block: bytes, block_len: int) -> bytes:
    """Extends given bytes block to match block length by adding padding.

    Padding value is the difference between desired and actual block length.

    Args:
        block: Block of bytes to add padding to.
        block_len: Length the input block of bytes should be padded to.

    Returns:
        Bytes block of a given length with added padding.
    """
    assert block_len >= len(block)

    padding_len = block_len - len(block)
    if padding_len == 0:
        return block

    padded_block = bytearray(block)
    padded_block.extend([padding_len for _ in range(padding_len)])

    return bytes(padded_block)


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


def cbc_encrypt(
    content: bytes,
    encryption_key: bytes,
    init_vector: bytes,
) -> bytes:
    """Encrypts a message using CBC (Cipher block chaining) cipher.

    Args:
        content: A message to be enrypted using CBC cipher.
        encryption_key: A Key to use for encrypting the message.
        init_vector: An initialization vector for the first block. Has to match the key size.

    Returns:
        A content, in bytes, encrypted using CBC cipher.
    """
    chunked_content = split_into_chunks(content, len(encryption_key))
    padded_chunks = [
        add_pkcs7_padding(chunk, len(encryption_key)) for chunk in chunked_content
    ]
    previous_block = bytearray()
    cipher_aes = AES.new(encryption_key, AES.MODE_ECB)
    ciphertext = bytearray()
    for i, chunk in enumerate(padded_chunks):
        # Use IV initialization vector for first block
        if i == 0:
            xored = bytearray([x ^ y for x, y in zip(chunk, init_vector)])
        else:
            xored = bytearray([x ^ y for x, y in zip(chunk, previous_block)])

        previous_block = xored.copy()
        ciphertext_block = cipher_aes.encrypt(xored)
        ciphertext.extend(ciphertext_block)
    return bytes(ciphertext)


def cbc_decrypt(ciphertext: bytes, decryption_key: bytes, init_vector: bytes) -> bytes:
    """Decrypts the ciphertext encrypted using CBC cipher.

    Args:
        ciphertext: A secret message encrypted using CPC cipher.
        decryption_key: A key to use for decrypting the ciphertext.
        init_vector: An initialization vector for the first block. Has to match the key size.

    Returns:
        A decrypted plaintext, in bytes.
    """
    chunked_content = split_into_chunks(ciphertext, len(decryption_key))
    previous_block = bytearray()
    cipher_aes = AES.new(decryption_key, AES.MODE_ECB)
    plaintext = bytearray()
    for i, chunk in enumerate(chunked_content):
        plaintext_block = cipher_aes.decrypt(chunk)
        # Use IV initialization vector for first block
        if i == 0:
            xored = bytearray([x ^ y for x, y in zip(init_vector, plaintext_block)])
        else:
            xored = bytearray([x ^ y for x, y in zip(previous_block, plaintext_block)])

        previous_block = chunk
        plaintext.extend(xored)
    return bytes(plaintext)


def test_output(output: bytes, expected_output: bytes) -> None | AssertionError:
    """Verifies output against an expected output.

    Args:
        output: An output which should be verified, in bytes.
        expected_output: An expected output, against which the user output will be verified, in bytes.

    Returns:
        None if there is no difference between output and expected output, AssertionError othwerise.
    """
    assert output == expected_output
