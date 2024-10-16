from abc import ABC, abstractmethod
from typing import Tuple, Any

class MatrixInterface(ABC):
    @abstractmethod
    def add(self, other: 'MatrixInterface') -> 'MatrixInterface':
        pass

    @abstractmethod
    def multiply(self, other: 'MatrixInterface') -> 'MatrixInterface':
        pass

    @abstractmethod
    def transpose(self) -> 'MatrixInterface':
        pass

    @abstractmethod
    def inverse(self) -> 'MatrixInterface':
        pass

    @abstractmethod
    def determinant(self) -> float:
        pass

    @abstractmethod
    def get(self, row: int, col: int) -> Any:
        pass

    @abstractmethod
    def set(self, row: int, col: int, value: Any) -> None:
        pass

    @abstractmethod
    def shape(self) -> Tuple[int, int]:
        pass
