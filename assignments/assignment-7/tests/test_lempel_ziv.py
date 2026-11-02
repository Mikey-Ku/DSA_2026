"""Tests for the Lempel-Ziv encoder and decoder

Each pair is (index of a seen phrase, new character in 8 bits). Phrase number i
writes its index in (i - 1).bit_length() bits, so phrase 1 has 0 index bits,
phrase 2 has 1, phrases 3-4 have 2, phrases 5-8 have 3, and so on. If the text
ends on a seen phrase, only its index is written.
"""

import unittest

from lempel_ziv_decode import decode
from lempel_ziv_encode import encode

def char(ch: str) -> str:
    """The 8 bits for a character, e.g. A -> 01000001"""
    return format(ord(ch), "08b")


A, B = char("A"), char("B")


class ShortStringTest(unittest.TestCase):
    """Short strings: encode gives the exact bits, and decode gives the text back"""

    def check(self, text: str, bits: str) -> None:
        """Checks both directions"""
        self.assertEqual(encode(text), bits)
        self.assertEqual(decode(bits), text)

    def test_empty(self) -> None:
        """Empty text <-> no bits"""
        self.check("", "")

    def test_one_letter(self) -> None:
        """A: (0, A), and phrase 1's index takes 0 bits"""
        self.check("A", A)

    def test_two_different_letters(self) -> None:
        """AB: A|B -> (0, A) (0, B)"""
        self.check("AB", A + "0" + B)

    def test_ends_on_seen_phrase(self) -> None:
        """AA: A|A, the second A is already phrase 1, so only index 1 is sent"""
        self.check("AA", A + "1")

    def test_repeat_builds_longer_phrase(self) -> None:
        """AAA: A|AA -> (0, A) (1, A)"""
        self.check("AAA", A + "1" + A)

    def test_abab(self) -> None:
        """ABAB: A|B|AB -> (0, A) (0, B) (1, B), the third index takes 2 bits"""
        self.check("ABAB", A + "0" + B + "01" + B)

    def test_word_with_symbol(self) -> None:
        """hi!: h|i|! -> (0, h) (0, i) (0, !)"""
        self.check("hi!", char("h") + "0" + char("i") + "00" + char("!"))

    def test_space(self) -> None:
        """a a: a| |a, the last a is already phrase 1 -> (0, a) (0, space) then index 1"""
        self.check("a a", char("a") + "0" + char(" ") + "01")

    def test_shor_example(self) -> None:
        """Shor's example from class: A|AB|ABB|B|ABA|ABAB|BB|ABBA|BB"""
        bits = (
            A               # 1: 0A
            + "1" + B       # 2: 1B
            + "10" + B      # 3: 2B
            + "00" + B      # 4: 0B
            + "010" + A     # 5: 2A
            + "101" + B     # 6: 5B
            + "100" + B     # 7: 4B
            + "011" + A     # 8: 3A
            + "0111"        # BB is phrase 7, already seen
        )
        self.check("AABABBBABAABABBBABBABB", bits)


class LongerStringTest(unittest.TestCase):
    """Longer strings: decode(encode(text)) gives the text back exactly"""

    def round_trip(self, text: str) -> str:
        """Encodes, checks the decode matches, and returns the bits"""
        bits = encode(text)
        self.assertEqual(decode(bits), text)
        return bits

    def test_every_letter_digit_and_symbol(self) -> None:
        """Every printable keyboard character, twice"""
        printable = "".join(chr(i) for i in range(32, 127))
        self.round_trip(printable * 2)

    def test_newlines_and_tabs(self) -> None:
        """Multiple lines with tabs"""
        self.round_trip("line one\n\tline two\nline three\n")

    def test_paragraph(self) -> None:
        """Several sentences of text"""
        paragraph = (
            "It is a truth universally acknowledged, that a single man in possession "
            "of a good fortune, must be in want of a wife. However little known the "
            "feelings or views of such a man may be on his first entering a neighbourhood, "
            "this truth is so well fixed in the minds of the surrounding families."
        )
        bits = self.round_trip(paragraph)
        self.assertLess(len(bits), len(paragraph) * 8)

    def test_long_repeat_shrinks(self) -> None:
        """10,000 copies of one letter need far fewer than 8 bits each"""
        bits = self.round_trip("a" * 10_000)
        self.assertLess(len(bits), 10_000)

    def test_repeated_sentence_shrinks_a_lot(self) -> None:
        """A sentence repeated 200 times compresses to under a quarter of its size"""
        text = "the rain in spain falls mainly on the plain. " * 200
        bits = self.round_trip(text)
        self.assertLess(len(bits), len(text) * 8 // 4)


if __name__ == "__main__":
    unittest.main()
