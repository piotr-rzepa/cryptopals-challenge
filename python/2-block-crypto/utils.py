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


def test_output(output: bytes, expected_output: bytes) -> None | AssertionError:
    """Verifies output against an expected output.

    Args:
        output: An output which should be verified, in bytes.
        expected_output: An expected output, against which the user output will be verified, in bytes.

    Returns:
        None if there is no difference between output and expected output, AssertionError othwerise.
    """
    assert output == expected_output
