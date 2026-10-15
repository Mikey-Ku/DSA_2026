"""Tests for the Matrix class and both multiplication algorithms"""

import random
import unittest

from matrix import Matrix, Rows, from_rows


class MatrixTest(unittest.TestCase):
    """Checks each matrix operation, then Strassen against the conventional multiply"""

    def test_new_matrix_is_zeros(self) -> None:
        """Matrix(n) is n x n and full of zeros"""
        m = Matrix(3)
        self.assertEqual(m.n, 3)
        self.assertEqual(m.data, [[0, 0, 0], [0, 0, 0], [0, 0, 0]])

    def test_get_and_set(self) -> None:
        """A value that is set can be read back, and the rest stay 0"""
        m = Matrix(2)
        m.set(0, 1, 5)
        self.assertEqual(m.get(0, 1), 5)
        self.assertEqual(m.get(0, 0), 0)

    def test_from_rows_must_be_square(self) -> None:
        """A list of rows that isn't square raises a ValueError"""
        with self.assertRaises(ValueError):
            from_rows([[1, 2, 3], [4, 5, 6]])

    def test_add_and_subtract(self) -> None:
        """+ and - work entry by entry"""
        a = from_rows([[1, 2], [3, 4]])
        b = from_rows([[5, 6], [7, 8]])
        self.assertEqual((a + b).data, [[6, 8], [10, 12]])
        self.assertEqual((b - a).data, [[4, 4], [4, 4]])

    def test_split(self) -> None:
        """split gives the top left, top right, bottom left and bottom right quarters"""
        m = from_rows([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ])
        a11, a12, a21, a22 = m.split()
        self.assertEqual(a11.data, [[1, 2], [5, 6]])
        self.assertEqual(a12.data, [[3, 4], [7, 8]])
        self.assertEqual(a21.data, [[9, 10], [13, 14]])
        self.assertEqual(a22.data, [[11, 12], [15, 16]])

    def test_split_odd_size(self) -> None:
        """An odd size can't be split in half, so it raises a ValueError"""
        with self.assertRaises(ValueError):
            Matrix(3).split()

    def test_multiply_by_hand(self) -> None:
        """A 2 x 2 example worked out by hand"""
        a = from_rows([[1, 3], [7, 5]])
        b = from_rows([[6, 8], [4, 2]])
        expected = [[18, 14], [62, 66]]
        self.assertEqual(data_of(a * b), expected)
        self.assertEqual(data_of(a.strassen_multiply(b)), expected)

    def test_different_sizes(self) -> None:
        """Multiplying different sized matrices gives None"""
        self.assertIsNone(Matrix(2).multiply(Matrix(3)))
        self.assertIsNone(Matrix(2).strassen_multiply(Matrix(3)))

    def test_strassen_matches_conventional(self) -> None:
        """Random matrices of many sizes, including odd ones that need padding"""
        for n in [1, 2, 3, 4, 5, 7, 8, 16, 33]:
            a = random_matrix(n)
            b = random_matrix(n)
            self.assertEqual(data_of(a.strassen_multiply(b)), data_of(a.multiply(b)), f"n = {n}")

    def test_every_threshold_matches(self) -> None:
        """The hybrid gives the same answer whatever size it switches at"""
        a = random_matrix(32)
        b = random_matrix(32)
        expected = data_of(a.multiply(b))
        for threshold in [1, 2, 4, 8, 16, 32, 64]:
            result = data_of(a.strassen_multiply(b, threshold))
            self.assertEqual(result, expected, f"threshold = {threshold}")


def random_matrix(n: int) -> Matrix:
    """Makes an n x n matrix of random whole numbers from -10 to 10"""
    return from_rows([[float(random.randint(-10, 10)) for _ in range(n)] for _ in range(n)])


def data_of(product: Matrix | None) -> Rows:
    """Returns the rows of a product, which should not be None"""
    assert product is not None
    return product.data


if __name__ == "__main__":
    unittest.main()
