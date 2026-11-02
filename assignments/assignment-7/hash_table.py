"""An associative array implemented as a hash map with separate chaining.

An associative array stores key/value pairs and supports three operations:
insert (set), lookup (get), and remove.

This implementation hashes each key to a bucket index in the range [0, m).
Keys that hash to the same bucket (a collision) are stored together in that
bucket's list.
"""

from typing import Generic, Hashable, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")

PRIMES = [
    53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317,
    196613, 393241, 786433, 1572869, 3145739, 6291469, 12582917, 25165843,
    50331653, 100663319, 201326611, 402653189, 805306457, 1610612741,
]

#Load factor = n/m
MAX_LOAD_FACTOR = 0.75


class Entry(Generic[K, V]):
    """One key/value pair in a bucket's list"""

    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value


class HashTable(Generic[K, V]):
    """Associative array: a list of buckets, each bucket a list of entries"""

    def __init__(self) -> None:
        # Start with the smallest prime number of buckets and no pairs
        self.prime_index = 0  # which prime we are on
        self.buckets: list[list[Entry[K, V]]] = empty_buckets(PRIMES[0])
        self.num_entries = 0

    def bucket_index(self, key: K) -> int:
        """Division hashing: h(k) = k mod m"""
        # hash() turns the key into an integer, mod squeezes it into 0 to m - 1
        return hash(key) % len(self.buckets)

    def find_entry(self, key: K) -> "Entry[K, V] | None":
        """Looks through the key's bucket for its entry, or returns None"""
        # A key can only be in its own bucket, so search just that chain
        for entry in self.buckets[self.bucket_index(key)]:
            if entry.key == key:
                return entry
        return None

    def rehash(self) -> None:
        """Moves every entry into the next prime number of buckets"""
        # Grow to the next prime
        old_buckets = self.buckets
        self.prime_index += 1
        self.buckets = empty_buckets(PRIMES[self.prime_index])

        # m changed, so k mod m changes so every entry must be reinserted
        for bucket in old_buckets:
            for entry in bucket:
                self.buckets[self.bucket_index(entry.key)].append(entry)

    def set(self, key: K, value: V) -> None:
        """Insert: adds the pair, or replaces the value if the key is already there"""
        # Key already stored, replace its value
        entry = self.find_entry(key)
        if entry is not None:
            entry.value = value
            return

        # New key: add it to the end of its bucket's chain
        self.buckets[self.bucket_index(key)].append(Entry(key, value))
        self.num_entries += 1

        # Too many pairs per bucket makes chains long, so grow
        too_full = self.num_entries / len(self.buckets) > MAX_LOAD_FACTOR
        if too_full and self.prime_index + 1 < len(PRIMES):
            self.rehash()

    def contains(self, key: K) -> bool:
        """True if the key is stored"""
        return self.find_entry(key) is not None

    def get(self, key: K) -> "V | None":
        """Lookup: the key's value, or None if it isn't stored"""
        entry = self.find_entry(key)
        return entry.value if entry is not None else None

    def remove(self, key: K) -> bool:
        """Remove: deletes the key's pair. True if it was there"""
        # Find the key in its bucket and pop it out of that chain
        bucket = self.buckets[self.bucket_index(key)]
        for position, entry in enumerate(bucket):
            if entry.key == key:
                bucket.pop(position)
                self.num_entries -= 1
                return True
        return False

    def size(self) -> int:
        """Number of pairs stored (n)"""
        return self.num_entries

    def key_value_pairs(self) -> list[tuple[K, V]]:
        """Every (key, value) pair in the table"""
        return [(entry.key, entry.value) for bucket in self.buckets for entry in bucket]


    def __setitem__(self, key: K, value: V) -> None:
        self.set(key, value)

    def __getitem__(self, key: K) -> "V | None":
        return self.get(key)

    def __contains__(self, key: K) -> bool:
        return self.contains(key)

    def __len__(self) -> int:
        return self.size()


def empty_buckets(m: int) -> list[list[Entry]]:
    """m empty buckets"""
    return [[] for _ in range(m)]
