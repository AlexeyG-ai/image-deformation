from render import FieldRender
from transformations import MaskTransform, AffineTransform
from dragpoint_beta import DragPoint

SIZE = (300, 300)
CELLS = 10
src_matr = [(x, y) for x in range(0, SIZE[0] + 1, SIZE[0] // (CELLS - 1)) for y in range(0, SIZE[1] + 1, SIZE[1] // (CELLS - 1))]

p0 = (-100, -150)
p1 = (-150, 450)
p2 = (600, 600)
p3 = (350, -50)

# transform = MaskTransform(
# 	size=SIZE,
# 	mask=(
# 		(0, -50), (-50, 350),
# 		(400, 400), (450, -100)
# 	)
# )

transform = AffineTransform(
	(
 		1, 0.2,
 		0, 1
 	)
)

changed_matr = list(map(transform, src_matr))

render = FieldRender(canvas_size=(500, 500))
render.set_start_pos(100, 100)
# render.draw_matr(src_matr, CELLS, color="grey")
# render.draw_matr(changed_matr, CELLS, color="blue")

# render.draw_point(
# 	(-50, 0),
# 	fill="green",
# )

class PointGrid:
	def __init__(self, canvas, coords, size = 5, start_pos = (0, 0)):
		self._canvas = canvas
		self._start_pos = start_pos
		self._size = size
		self._coords = coords

		self._init_points()
		self._init_lines()

	def _init_points(self):
		coords = sum(self._coords, ())
		self._points = tuple(map(self._create_point, coords))

	def _create_point(self, pos):
		x, y = map(sum, zip(self._start_pos, pos))
		return self._canvas.create_rectangle(
			x - self._size, y - self._size,
			x + self._size, y + self._size,
			fill="#00f", width=0
		)

	def _init_lines(self):
		coords = sum(self._coords, ())
		w = len(self._coords[0])

		self._hor_lines = tuple(self._create_line(coords[ind - 1], pos) for ind, pos in enumerate(coords) if ind % w)
		self._vert_lines = tuple(self._create_line(pos, coords[ind + w]) for ind, pos in enumerate(coords[:-w]))

	def _create_line(self, pos1, pos2):
		pos1, pos2 = tuple(map(sum, zip(self._start_pos, pos)) for pos in (pos1, pos2))
		return self._canvas.create_line(
			*pos1, *pos2
		)

	def _set_point_pos(self, point_id, point_pos):
		x, y = map(sum, zip(self._start_pos, point_pos))
		self._canvas.coords(
			point_id,
			x - self._size, y - self._size,
			x + self._size, y + self._size
		)

	def _set_line_pos(self, line_id, pos1, pos2):
		pos1 = map(sum, zip(self._start_pos, pos1))
		pos2 = map(sum, zip(self._start_pos, pos2))
		self._canvas.coords(
			line_id,
			*pos1, *pos2
		)

	def update_coordinates(self, coords):
		w = len(coords[0])
		coords = sum(coords, ())
		self._coords = coords

		# SET POINTS
		for point_id, pos in zip(self._points, coords):
			self._set_point_pos(point_id, pos)

		# SET HORIZONTAL LINES
		for ind, line_id in enumerate(self._hor_lines):
			delta = ind // (w - 1)
			self._set_line_pos(line_id, coords[ind + delta], coords[ind + delta + 1])

		for ind, line_id in enumerate(self._vert_lines):
			self._set_line_pos(line_id, coords[ind], coords[ind + w])



matr = (
	((0, 0), (30, 0), (60, 0)),
	((0, 30), (30, 30), (60, 30)),
	((0, 60), (30, 90), (60, 60))
)

grid = PointGrid(
	canvas=render._cnv,
	coords=matr,
	start_pos=(100, 100)
)

grid.update_coordinates(
	(
		((0, 0), (30, 0), (60, 0)),
		((0, 30), (30, 30), (60, 30)),
		((0, 60), (30, 90), (60, 60))
	)
)

def set_point_pos(point_ind, point_coords, grid):
	grid = [list(row) for row in grid]
	i, j = point_ind // len(grid[0]), point_ind % len(grid[0])
	grid[i][j] = point_coords
	return tuple([tuple(row) for row in grid])

p1 = DragPoint(
	canvas=render._cnv,
	pos=(100, 100),
	size=10,
	color="green",
	onmove=lambda pos: grid.update_coordinates(set_point_pos(0, (pos.x - 100, pos.y - 100), grid._coords))
)

render.run()