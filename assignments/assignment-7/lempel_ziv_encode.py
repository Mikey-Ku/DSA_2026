"""Lempel-Ziv encoder

Splits text into phrases never seen before. Each phrase is a seen phrase plus one
new byte, so it is sent as (index of the seen phrase, the new byte in 8 bits).

Example: AABABBBABAABABBBABBABB -> A|AB|ABB|B|ABA|ABAB|BB|ABBA|BB
"""

from hash_table import HashTable

BITS_PER_BYTE = 8

def index_width(codebook_size: int) -> int:
    """How many bits an index needs when the codebook has codebook_size phrases.

    Indexes go from 0 to codebook_size - 1, so we need enough bits for biggest value
    """
    return (codebook_size - 1).bit_length()


def to_bits(number: int, width: int) -> str:
    """Writes number in binary using exactly width bits, e.g. 5 in 4 bits -> 0101"""
    return format(number, f"0{width}b") if width else ""


def encode(text: str) -> str:
    """Encodes any text as a string of 0s and 1s"""
    # The codebook maps each phrase we have seen to its index.
    # It starts with just the empty phrase at index 0.
    codebook: HashTable[bytes, int] = HashTable()
    codebook[b""] = 0

    bits = ""
    current_phrase = b""  # the phrase we are building, always one we have seen

    for byte in text.encode("utf-8"):
        next_phrase = current_phrase + bytes([byte])

        #  Read until hit non seen phrase
        if next_phrase in codebook:
            current_phrase = next_phrase
            continue

        # add new phrase to sequence
        width = index_width(len(codebook))
        bits += to_bits(codebook[current_phrase], width)
        bits += to_bits(byte, BITS_PER_BYTE)

        # store new phrase
        codebook[next_phrase] = len(codebook)
        current_phrase = b""

    # The text ended in the middle of a seen phrase: send just its index
    if current_phrase:
        width = index_width(len(codebook))
        bits += to_bits(codebook[current_phrase], width)

    return bits


if __name__ == "__main__":
    text = "hello world"
    encoded_bits = encode(text)
    print("text:", text)
    print("bits:", encoded_bits)
    print(f"{len(text) * BITS_PER_BYTE} bits -> {len(encoded_bits)} bits")
