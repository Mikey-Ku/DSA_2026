"""Tests for HashTable"""

import unittest

from hash_table import PRIMES, HashTable


class HashTableTest(unittest.TestCase):
    """Checks each associative array operation, then rehashing"""

    def test_new_table_is_empty(self) -> None:
        """A new table has size 0 and no pairs"""
        table: HashTable[str, int] = HashTable()
        self.assertEqual(len(table), 0)
        self.assertEqual(table.key_value_pairs(), [])

    def test_set_and_get(self) -> None:
        """A value that is set can be read back"""
        table: HashTable[str, int] = HashTable()
        table["a"] = 1
        self.assertEqual(table["a"], 1)

    def test_get_missing_is_none(self) -> None:
        """Getting a key that isn't there returns None"""
        table: HashTable[str, int] = HashTable()
        self.assertIsNone(table["missing"])

    def test_set_replaces_old_value(self) -> None:
        """Setting a key twice keeps the new value and size stays 1"""
        table: HashTable[str, int] = HashTable()
        table["a"] = 1
        table["a"] = 2
        self.assertEqual(table["a"], 2)
        self.assertEqual(len(table), 1)

    def test_contains(self) -> None:
        """in is True only for keys that were set"""
        table: HashTable[str, int] = HashTable()
        table["a"] = 1
        self.assertIn("a", table)
        self.assertNotIn("b", table)

    def test_remove(self) -> None:
        """remove returns True and deletes the key, then False the second time"""
        table: HashTable[str, int] = HashTable()
        table["a"] = 1
        self.assertTrue(table.remove("a"))
        self.assertNotIn("a", table)
        self.assertFalse(table.remove("a"))
        self.assertEqual(len(table), 0)

    def test_collisions_in_same_bucket(self) -> None:
        """Keys that land in the same bucket are all kept (ints hash to themselves)"""
        table: HashTable[int, str] = HashTable()
        num_buckets = PRIMES[0]
        table[1] = "one"
        table[1 + num_buckets] = "two"
        self.assertEqual(table[1], "one")
        self.assertEqual(table[1 + num_buckets], "two")

    def test_rehash_keeps_everything(self) -> None:
        """After many inserts the table grows and every key is still there"""
        table: HashTable[int, int] = HashTable()
        for i in range(1000):
            table[i] = i * i
        self.assertGreater(len(table.buckets), PRIMES[0])
        self.assertEqual(len(table), 1000)
        for i in range(1000):
            self.assertEqual(table[i], i * i)

    def test_key_value_pairs(self) -> None:
        """key_value_pairs has every pair (order doesn't matter)"""
        table: HashTable[str, int] = HashTable()
        table["a"] = 1
        table["b"] = 2
        self.assertEqual(sorted(table.key_value_pairs()), [("a", 1), ("b", 2)])


if __name__ == "__main__":
    unittest.main()
