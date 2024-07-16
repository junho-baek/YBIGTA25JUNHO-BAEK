from __future__ import annotations
import copy


"""
TODO:
- __setitem__ 구현하기
- __pow__ 구현하기 (__matmul__을 활용해봅시다)
- __repr__ 구현하기
"""


class Matrix:
    MOD = 1000

    def __init__(self, matrix: list[list[int]]) -> None:
        self.matrix = matrix

    @staticmethod
    def full(n: int, shape: tuple[int, int]) -> Matrix:
        return Matrix([[n] * shape[1] for _ in range(shape[0])])

    @staticmethod
    def zeros(shape: tuple[int, int]) -> Matrix:
        return Matrix.full(0, shape)

    @staticmethod
    def ones(shape: tuple[int, int]) -> Matrix:
        return Matrix.full(1, shape)

    @staticmethod
    def eye(n: int) -> Matrix:
        matrix = Matrix.zeros((n, n))
        for i in range(n):
            matrix[i, i] = 1
        return matrix

    @property
    def shape(self) -> tuple[int, int]:
        return (len(self.matrix), len(self.matrix[0]))

    def clone(self) -> Matrix:
        return Matrix(copy.deepcopy(self.matrix))

    def __getitem__(self, key: tuple[int, int]) -> int:
        return self.matrix[key[0]][key[1]]

    def __setitem__(self, key: tuple[int, int], value: int) -> None:
        # 구현하세요!
        # 주어진 값에 대해 1000으로 나눈 나머지를 저장합니다.
        self.matrix[key[0]][key[1]] = value % Matrix.MOD
        
    def __matmul__(self, matrix: Matrix) -> Matrix:
        x, m = self.shape
        m1, y = matrix.shape
        assert m == m1

        result = self.zeros((x, y))

        for i in range(x):
            for j in range(y):
                for k in range(m):
                    result[i, j] += self[i, k] * matrix[k, j]

        return result

    def __pow__(self, n: int) -> Matrix:
        # 구현하세요!
        # 행렬의 거듭제곱을 분할 정복 방식으로 효율적으로 계산합니다.
        if n == 1:
            # n이 1인 경우 각 원소에 대해 __setitem__을 통해 모듈러 연산 적용
            result = self.clone()
            for i in range(result.shape[0]):
                for j in range(result.shape[1]):
                    result[i, j] = result[i, j]
            return result

        if n % 2 == 0:
            # n이 짝수인 경우
            half_pow = self ** (n // 2)
            full_pow = half_pow @ half_pow
        else:
            # n이 홀수인 경우
            half_pow = self ** (n // 2)
            full_pow = half_pow @ half_pow @ self

        # 각 원소에 대해 모듈러 연산 적용
        for i in range(full_pow.shape[0]):
            for j in range(full_pow.shape[1]):
                full_pow[i, j] = full_pow[i, j] % Matrix.MOD

        return full_pow

    def __repr__(self) -> str:
        # 구현하세요!
        # 행렬을 문자열로 변환하여 출력합니다.
        rows = []
        for row in self.matrix:
            string_row = []
            for element in row:
                string_row.append(str(element))
            rows.append(' '.join(string_row))
        return '\n'.join(rows)