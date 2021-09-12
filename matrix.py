from typing import Iterable
from collections import namedtuple
from itertools import zip_longest


class Matrix:
	@classmethod
	def convert(cls, iterable_object: Iterable) -> tuple:
		"""Конвертация в кортеж для удобной работы с матрицей"""
		assert isinstance(iterable_object, Iterable), "Аргумент должен быть итерируемым обьектом!"
		assert all(isinstance(row, Iterable) for row in iterable_object), "Элементы аргумента должны быть итерируемыми обьектами!"
		converted = tuple(map(tuple, iterable_object))

		assert cls.is_valid(converted), "Столбцы должны быть одинаковой длины!"
		return converted

	@classmethod
	def is_valid(cls, matr: tuple) -> bool:
		"""Проверка рамров матрицы"""
		return len(set(map(len, matr))) == 1

	@classmethod
	def get_size(cls, matr: tuple) -> tuple:
		"""Размеры матрицы"""
		return (len(matr[0]), len(matr))

	@classmethod
	def print(cls, matr: tuple):
		"""Выводит матрицу на экран в отформатированном виде"""
		cols = tuple(zip_longest(*matr))
		max_lens = tuple(max(map(lambda el: len(str(el)), col)) for col in cols)
		
		for row in matr:
			print(*tuple(str(el).ljust(max_lens[ind], " ") for ind, el in enumerate(row)))

	@classmethod
	def rotate_right(cls, matr: tuple):
		return tuple(zip_longest(*matr[::-1]))

	@classmethod
	def fit_to_size(cls, iterable: Iterable, size: tuple):
		"""Переводит список элементов размера m + n в матрицу размеров (m x n)"""
		m, n = size
		return Matrix.convert(tuple(iterable[x:x + m] for x in range(0, len(iterable), m)))