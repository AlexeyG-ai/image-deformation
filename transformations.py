from abc import ABC, abstractmethod


class Transformation(ABC):
	@abstractmethod
	def change_x(self, p):
		"""Изменяет положение точки по оси X"""
		pass

	@abstractmethod
	def change_y(self, p):
		"""Изменяет положение точки по оси Y"""
		pass

	def __call__(self, p):
		return (
			self.change_x(p),
			self.change_y(p),
		)


class AffineTransform(Transformation):
	"""Афинные преобразования.
	coef_matr: tuple[float|int] - матрица с коефециентами
	start_pos: tuple[int] - коэфециенты отклонения
	"""

	def change_x(self, p):
		return self.coef[0] * p[0] + self.coef[1] * p[1] + self.pos[0]

	def change_y(self, p):
		return self.coef[2] * p[0] + self.coef[3] * p[1] + self.pos[1]

	def __init__(self, coef_matr, start_pos=(0, 0)):
		self.coef = coef_matr
		self.pos = start_pos

class OneAxisTransformY(Transformation):
	"""Искажение пространства при переносе 1 точки по оси Y"""

	def change_x(self, p):
		coef = p[0] / self._size[0]
		return self._affine1(p)[0] * (1 - coef) + self._affine2(p)[0] * coef

	def change_y(self, p):
		coef = p[1] / self._size[1]
		return self._affine1(p)[1] * (1 - coef) + self._affine2(p)[1] * coef

	def __init__(self, size, endpoint_y):
		self._affine1 = AffineTransform((
			1, 0,
			(endpoint_y - size[1]) / size[0], 1
		))

		self._affine2 = AffineTransform((
			1, 0,
			0, 1,
		))

		self._size = size

class OneAxisTransformX(Transformation):
	"""Искажение пространства при переносе 1 точки по оси X"""

	def change_x(self, p):
		coef = p[0] / self._size[0]
		return self._affine1(p)[0] * (1 - coef) + self._affine2(p)[0] * coef

	def change_y(self, p):
		coef = p[1] / self._size[1]
		return self._affine1(p)[1] * (1 - coef) + self._affine2(p)[1] * coef

	def __init__(self, size, endpoint_x):
		self._affine1 = AffineTransform((
			1, (endpoint_x - size[0]) / size[1],
			0, 1
		))

		self._affine2 = AffineTransform((
			1, 0,
			0, 1,
		))

		self._size = size

class OnePointTransform(Transformation):
	"""Искажение пространства при переносе 1 точки"""

	def change_x(self, p):
		coef = p[0] / self._size[0]
		return self._affine1(p)[0] * (1 - coef) + self._affine2(p)[0] * coef

	def change_y(self, p):
		coef = p[1] / self._size[1]
		return self._affine1(p)[1] * (1 - coef) + self._affine2(p)[1] * coef

	def __init__(self, size, current_coords):
		dx = current_coords[0] - size[0]
		dy = current_coords[1] - size[1]		

		self._affine1 = AffineTransform((
			1, 0,
			0, 1
		))

		self._affine2 = AffineTransform(
			(
				1, dx / size[1],
				dy / size[0], 1
			)
		)

		self._size = size

class MaskTransform(Transformation):
	def change_x(self, p):
		coef = p[0] / self._size[0]
		return self._affine1(p)[0] * (1 - coef) + self._affine2(p)[0] * coef

	def change_y(self, p):
		coef = p[1] / self._size[1]
		return self._affine1(p)[1] * (1 - coef) + self._affine2(p)[1] * coef

	def __init__(self, size, mask):
		p0, p1, p2, p3 = mask

		self._affine1 = AffineTransform(
			(
				1, (p1[0] - p0[0]) / size[1],
				(p3[1] - p0[1]) / size[0], 1
			),
			p0
		)

		self._affine2 = AffineTransform(
			(
				1, (p2[0] - p3[0]) / size[1],
				(p2[1] - p1[1]) / size[0], 1
			),
			(p3[0] - size[0], p1[1] - size[1])
		)

		self._size = size