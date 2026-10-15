"""Square matrix with conventional and Strassen multiplication"""

Rows = list[list[float]]

class Matrix:
    """An n x n matrix stored as a list of rows"""

    def __init__(self, n: int) -> None:
        """Makes an n x n matrix of zeros"""
        self.n = n
        self.data: Rows = zeros(n)

    def get(self, i: int, j: int) -> float:
        """Returns the value at row i, column j"""
        return self.data[i][j]

    def set(self, i: int, j: int, value: float) -> None:
        """Sets the value at row i, column j"""
        self.data[i][j] = value

    def add(self, other: "Matrix") -> "Matrix":
        """Returns self + other"""
        return from_rows(add_matrices(self.data, other.data))

    def subtract(self, other: "Matrix") -> "Matrix":
        """Returns self - other"""
        return from_rows(subtract_matrices(self.data, other.data))

    def split(self) -> tuple["Matrix", "Matrix", "Matrix", "Matrix"]:
        """Returns the four quarters (A11, A12, A21, A22)"""
        if self.n % 2 != 0:
            raise ValueError("only split a matrix with even n")
        A11, A12, A21, A22 = split_matrix(self.data)
        return from_rows(A11), from_rows(A12), from_rows(A21), from_rows(A22)

    def multiply(self, other: "Matrix") -> "Matrix | None":
        """Conventional multiply, or None if the sizes don't match"""
        if self.n != other.n:
            return None
        return from_rows(multiply_matrices(self.data, other.data))

    def strassen_multiply(self, other: "Matrix", threshold: int = 1) -> "Matrix | None":
        """Strassen multiply, or None if the sizes don't match (threshold=1 is pure Strassen)"""
        if self.n != other.n:
            return None
        return from_rows(strassen_padded(self.data, other.data, threshold))

    def __add__(self, other: "Matrix") -> "Matrix":
        """Lets you write A + B"""
        return self.add(other)

    def __sub__(self, other: "Matrix") -> "Matrix":
        """Lets you write A - B"""
        return self.subtract(other)

    def __mul__(self, other: "Matrix") -> "Matrix | None":
        """Lets you write A * B (conventional multiply)"""
        return self.multiply(other)


def zeros(n: int) -> Rows:
    """Returns an n x n list of lists of zeros"""
    return [[0.0] * n for _ in range(n)]

def from_rows(rows: Rows) -> Matrix:
    """Makes a Matrix from a square list of rows"""
    for row in rows:
        if len(row) != len(rows):
            raise ValueError("rows must form a square matrix")
    m = Matrix(len(rows))
    for i in range(len(rows)):
        for j in range(len(rows)):
            m.set(i, j, rows[i][j])
    return m


def add_matrices(A: Rows, B: Rows) -> Rows:
    """Returns A + B"""
    n = len(A)
    C = zeros(n)
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] + B[i][j]
    return C


def subtract_matrices(A: Rows, B: Rows) -> Rows:
    """Returns A - B"""
    n = len(A)
    C = zeros(n)
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] - B[i][j]
    return C


def multiply_matrices(A: Rows, B: Rows) -> Rows:
    """Conventional multiply: C[i][j] is row i of A times column j of B"""
    n = len(A)
    C = zeros(n)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C


def split_matrix(A: Rows) -> tuple[Rows, Rows, Rows, Rows]:
    """Splits A into quarters: top left, top right, bottom left, bottom right"""
    half = len(A) // 2
    A11 = [row[:half] for row in A[:half]]
    A12 = [row[half:] for row in A[:half]]
    A21 = [row[:half] for row in A[half:]]
    A22 = [row[half:] for row in A[half:]]
    return A11, A12, A21, A22


def join_matrices(C11: Rows, C12: Rows, C21: Rows, C22: Rows) -> Rows:
    """Joins four quarters back into one matrix (undoes split_matrix)"""
    top = [C11[i] + C12[i] for i in range(len(C11))]
    bottom = [C21[i] + C22[i] for i in range(len(C21))]
    return top + bottom


def strassen(A: Rows, B: Rows, threshold: int = 1) -> Rows:
    """Recursive Strassen for power-of-2 sizes; uses the conventional multiply at threshold or below"""
    if len(A) <= threshold:
        return multiply_matrices(A, B)

    A11, A12, A21, A22 = split_matrix(A)
    B11, B12, B21, B22 = split_matrix(B)

    M1 = strassen(add_matrices(A11, A22), add_matrices(B11, B22), threshold)       # (A11 + A22)(B11 + B22)
    M2 = strassen(add_matrices(A21, A22), B11, threshold)                          # (A21 + A22) B11
    M3 = strassen(A11, subtract_matrices(B12, B22), threshold)                     # A11 (B12 - B22)
    M4 = strassen(A22, subtract_matrices(B21, B11), threshold)                     # A22 (B21 - B11)
    M5 = strassen(add_matrices(A11, A12), B22, threshold)                          # (A11 + A12) B22
    M6 = strassen(subtract_matrices(A21, A11), add_matrices(B11, B12), threshold)  # (A21 - A11)(B11 + B12)
    M7 = strassen(subtract_matrices(A12, A22), add_matrices(B21, B22), threshold)  # (A12 - A22)(B21 + B22)

    C11 = add_matrices(subtract_matrices(add_matrices(M1, M4), M5), M7)  # M1 + M4 - M5 + M7
    C12 = add_matrices(M3, M5)                                           # M3 + M5
    C21 = add_matrices(M2, M4)                                           # M2 + M4
    C22 = add_matrices(add_matrices(subtract_matrices(M1, M2), M3), M6)  # M1 - M2 + M3 + M6

    return join_matrices(C11, C12, C21, C22)


def strassen_padded(A: Rows, B: Rows, threshold: int = 1) -> Rows:
    """Strassen for any n: pads with zeros to a power of 2, multiplies, then trims"""
    n = len(A)
    size = 1
    while size < n:
        size *= 2

    big_A = zeros(size)
    big_B = zeros(size)
    for i in range(n):
        for j in range(n):
            big_A[i][j] = A[i][j]
            big_B[i][j] = B[i][j]

    C = strassen(big_A, big_B, max(threshold, 1))
    return [row[:n] for row in C[:n]]
