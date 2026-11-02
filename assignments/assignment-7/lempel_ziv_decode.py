"""Lempel-Ziv decoder

Reads the bits from the encoder as (index of a seen phrase, new byte) pairs and
rebuilds each phrase as that seen phrase plus the new byte.
"""

from lempel_ziv_encode import BITS_PER_BYTE, index_width


def decode(bits: str) -> str:
    """Turns the 0s and 1s from encode back into the original text"""
    codebook = [b""]
    output = b""
    position = 0  # how far through the bits we have read

    while position < len(bits):
        # Read the index of the seen phrase
        width = index_width(len(codebook))
        index = int(bits[position:position + width], 2) if width else 0
        position += width

        # No bits left after the index: the text ended on a seen phrase
        if position == len(bits):
            output += codebook[index]
            break

        # Read the new byte that comes after the seen phrase
        new_byte = int(bits[position:position + BITS_PER_BYTE], 2)
        position += BITS_PER_BYTE

        # The new phrase is the seen phrase plus the new byte
        phrase = codebook[index] + bytes([new_byte])
        codebook.append(phrase)
        output += phrase

    return output.decode("utf-8")


if __name__ == "__main__":
    # The bits encode prints for "hello world"
    bits = (
        "0110100000110010100011011001101101111000001000000000111011100001"
        "10111100001110010001101100100"
    )
    print("bits:   ", bits)
    print("decoded:", decode(bits))
