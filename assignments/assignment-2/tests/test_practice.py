"""Test cases for Exercise 4, is_valid_parentheses."""

import unittest

from linked_structures.practice import is_valid_parentheses


class ValidParenthesesTest(unittest.TestCase):
    """Runs is_valid_parentheses against a list of strings with known answers."""

    def test_cases(self) -> None:
        """Every string in the table gives the expected answer."""
        cases = [
            # Valid
            ("", True),
            ("()", True),
            ("[]", True),
            ("{}", True),
            ("()[]{}", True),
            ("([])", True),
            ("{[()]}", True),
            ("(((())))", True),
            ("([]{()})", True),
            ("f(a[0], {b: c})", True),
            ("no brackets here", True),
            # Closed by the wrong kind
            ("(]", False),
            ("{)", False),
            ("[}", False),
            ("([)]", False),
            ("{[}]", False),
            # Closing bracket with nothing open
            (")", False),
            ("]", False),
            ("}", False),
            ("())", False),
            ("){", False),
            # Opened but never closed
            ("(", False),
            ("[", False),
            ("{", False),
            ("([]", False),
            ("((()", False),
        ]
        for text, expected in cases:
            # subTest reports each failing string separately instead of stopping at the first.
            with self.subTest(text=text):
                self.assertEqual(is_valid_parentheses(text), expected)


if __name__ == "__main__":
    unittest.main()
