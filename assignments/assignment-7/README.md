# Assignment 7: Associative Arrays and Applications

Michael Ku

Data Structures and Algorithms, Fall 2026

## Part 1: Associative Array

`HashTable` in `hash_table.py` stores key/value pairs. It works like a Python
dictionary but is built from scratch.

- `set(key, value)` - adds a pair, or replaces the value if the key is already there
- `get(key)` - the value for a key, or `None`
- `contains(key)` - whether the key is in the table
- `remove(key)` - removes a key
- `size()` - how many pairs are stored
- `key_value_pairs()` - every pair in the table

How it works:

- **Buckets:** the table is a list of buckets, and each bucket is a list of pairs.
- **Hashing:** a key goes in bucket `hash(key) % m`, where m is the number of buckets.
- **Collisions:** keys that land in the same bucket are just added to that bucket's
  list (separate chaining).
- **Resizing:** the bucket count is always a prime, starting at 53. When there are
  more than 0.75 pairs per bucket, every pair is moved into a bigger table with the
  next prime number of buckets, so the buckets stay short.

Tests are in `tests/test_hash_table.py`.

## Part 2: Lempel-Ziv Compression

The encoder is in `lempel_ziv_encode.py` and the decoder is in
`lempel_ziv_decode.py`. Tests are in `tests/test_lempel_ziv.py`.

### Encoder

The input can be any text: letters, digits, spaces, punctuation, newlines, or
non-English characters. The encoder first turns the text into a list of UTF-8
bytes. Each byte can be any value from 0 to 255, and the encoder works on these
byte values.

The codebook is a `HashTable` from phrases (byte strings) to numbers. It starts
with only the empty phrase.

1. Read the bytes one at a time, building up a phrase.
2. Keep going while the phrase is already in the codebook.
3. When it isn't, write (number of the phrase without its last byte, last byte),
   and add the new phrase to the codebook.

For example, `hello world` splits into `h|e|l|lo| |w|o|r|ld`. Each piece is an
earlier piece (sometimes the empty one) plus one new character. The example from
class, `AABABBBABAABABBBABBABB`, uses only A and B to keep it short. It splits
into `A|AB|ABB|B|ABA|ABAB|BB|ABBA|BB`.

### Encoding to bits

The compressed output is written as a string of `0` and `1` characters, which
stand in for real bits so they are easy to count and print.

Each pair is the phrase number, then the new byte in 8 bits (8 bits covers all
256 possible bytes). The phrase number only uses as many bits as it needs: when
pair i is written there are only i + 1 phrases, so it fits in `i.bit_length()`
bits. If the text ends partway through a phrase that is already in the codebook,
only that phrase's number is written at the end.

### Decoder

The decoder reads the pairs back and builds the same codebook as a list. Each
pair's phrase is `codebook[number] + byte`, and joining the phrases gives back the
original text.

## Results

To test the compression, each file was run through the encoder, and the
number of output bits was divided by 8 to get the compressed size in bytes. That
size was then compared to the original file size.

| Input | Original (bytes) | Compressed (bytes) | % of original |
| --- | ---: | ---: | ---: |
| `repeated.txt` - one sentence 2000 times | 84,000 | 5,958 | 7.1% |
| `pride_and_prejudice.txt` - the full novel | 772,386 | 364,706 | 47.2% |
| `random_letters.txt` - 100,000 random letters | 100,000 | 79,448 | 79.4% |

The more a text repeats itself, the better it compresses. The repeated sentence
shrinks to 7% because the phrases in the codebook keep getting longer, so each
pair stands for more and more of the text. The novel shrinks to about half its
size because English reuses a lot of the same words and letter patterns. The
random letters have no real patterns, but they still shrink to 79% because they
only use 27 different characters (a to z and space), so short letter
combinations still repeat by chance.
