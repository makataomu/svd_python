from typing import List, Tuple
from matrix_interface import MatrixInterface

class Matrix(MatrixInterface):
    def __init__(self, data: List[List[float]]) -> None:
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if data else 0

    def shape(self) -> Tuple[int, int]:
        return (self.rows, self.cols)

    def get(self, row: int, col: int) -> float:
        """вроде так лучше получать значения, чем через индексы"""
        return self.data[row][col]

    def set(self, row: int, col: int, value: float) -> None:
        self.data[row][col] = value

    def add(self, other: 'MatrixInterface') -> 'MatrixInterface':
        """сложение с проверкой на одинаковый размер"""
        if self.shape() != other.shape():
            raise ValueError("Matrices must have the same dimensions to add")
        result = [
            [self.get(i, j) + other.get(i, j) for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def multiply(self, other: 'MatrixInterface') -> 'MatrixInterface':
        """при умножении axb на cxd надо, чтобы b=c"""
        if self.cols != other.shape()[0]:
            raise ValueError("Invalid matrix dimensions for multiplication")
        result = [
            [sum(self.get(i, k) * other.get(k, j)
                for k in range(self.cols))
                for j in range(other.shape()[1])]
                  for i in range(self.rows)
        ]
        return Matrix(result)

    def transpose(self) -> 'MatrixInterface':
        result = [
            [self.get(j, i) for j in range(self.rows)]
            for i in range(self.cols)
        ]
        return Matrix(result)

    def determinant(self) -> float:
        if self.rows == 1:
            return self.data[0][0]
        elif self.rows == 2:
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]
        else:
            # laplace expansion
            det = 0.0
            for c in range(self.cols):
                cofactor_matrix = self.minor(0, c)
                det += ((-1) ** c) * self.data[0][c] * cofactor_matrix.determinant()
            return det

    def minor(self, row: int, col: int) -> 'Matrix':
        """получение минорной матрицы за счет удаления указанных строки и колонки"""
        minor_matrix = [
            [self.data[i][j] for j in range(self.cols) if j != col]
            for i in range(self.rows) if i != row
        ]
        return Matrix(minor_matrix)

    def cofactor_matrix(self) -> 'Matrix':
        cofactors = [
            [((-1) ** (i + j)) * self.minor(i, j).determinant() for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(cofactors)

    def inverse(self) -> 'MatrixInterface':
        det = self.determinant()
        if det == 0:
            raise ValueError("Matrix is singular and cannot be inverted.")

        cofactors = self.cofactor_matrix()
        adjugate = cofactors.transpose()
        inverse_matrix = adjugate.scalar_multiply(1 / det)
        return inverse_matrix

    def scalar_multiply(self, scalar: float) -> 'Matrix':
        result = [
            [scalar * self.get(i, j) for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)


    def __str__(self) -> str:
        return '\n'.join(['\t'.join(map(str, row)) for row in self.data])
