from dataclasses import dataclass, field
from matrix import Matrix


@dataclass
class PointSettings:
	size: int
	options: dict = field(default_factory=dict)


@dataclass
class LineSettings:
	options: dict = field(default_factory=dict)


class PointGrid:
	def __init__(self, canvas, coords, point, line):
		self._point_sets = PointSettings(**point)
		self._line_sets = LineSettings(**line)
		self._canvas = canvas
		self._grid_pos = (0, 0)

		coords = Matrix.convert(coords)
		m, n = Matrix.get_size(coords)
		self._points = self._init_points(m * n)
		self._vert_lines = self._init_lines(m * (n - 1))
		self._hor_lines = self._init_lines((m - 1) * n)

		self.update(coords)

	def _init_points(self, count):
		return tuple(self._canvas.create_rectangle(0, 0, 1, 1, **self._point_sets.options) for _ in range(count))

	def _init_lines(self, count):
		return tuple(self._canvas.create_line(0, 0, 1, 1, **self._line_sets.options) for _ in range(count))

	def _update_points(self, points, coords):
		coords = sum(coords, tuple())
		for point_id, point_pos in zip(self._points, coords):
			self._set_point_pos(point_id, point_pos)

	def _update_lines(self, lines, coords):
		m, n = Matrix.get_size(coords)
		coords = sum(coords, tuple())
		for ind, line_id in enumerate(lines):
			self._set_line_pos(line_id, coords[ind], coords[ind + m])

	def _set_line_pos(self, line_id, p1, p2):
		p1 = map(sum, zip(self._grid_pos, p1))
		p2 = map(sum, zip(self._grid_pos, p2))
		self._canvas.coords(line_id, *p1, *p2)

	def _set_point_pos(self, point_id, point_pos):
		x, y = map(sum, zip(self._grid_pos, point_pos))
		size = self._point_sets.size
		self._canvas.coords(
			point_id,
			x - size, y - size,
			x + size, y + size
		)

	def update(self, coords: tuple):
		coords = Matrix.convert(coords)
		self._update_points(self._points, coords)
		self._update_lines(self._vert_lines, coords)
		self._update_lines(self._hor_lines, Matrix.rotate_right(coords))

	def set_pos(self, coords: tuple):
		self._grid_pos = coords