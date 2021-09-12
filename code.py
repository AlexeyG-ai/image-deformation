import tkinter as tk
from point_grid import PointGrid
from dragpoint_beta import DragPoint
from functools import partial
from transformations import MaskTransform
from matrix import Matrix


def change_point(matr, grid, mask, point_num, event, point):
	mask[point_num] = tuple(int(el - 100) for el in point.get_pos())

	transform = MaskTransform(
		size=(300, 300),
		mask=mask
	)

	converted = tuple(map(transform, sum(matr, ())))
	converted = Matrix.fit_to_size(
		converted, size=Matrix.get_size(matr)
	)

	grid.update(converted)

def create_coords_grid(start_coords, end_coords, size):
	m, n = size
	x1, y1 = start_coords
	x2, y2 = end_coords
	dx, dy = (x2 - x1) / (m - 1), (y2 - y1) / (n - 1)

	matr = []
	for i in range(n):
		row = []
		for j in range(m):
			row.append((x1 + dx * j, y1 + dy * i))
		matr.append(row)

	return Matrix.convert(matr)

if __name__ == "__main__":
	root = tk.Tk()
	cnv = tk.Canvas(root, width=500, height=500, bg="white")
	mask = [(0, 0), (0, 300), (300, 300), (300, 0)]

	matrix = create_coords_grid(
		start_coords=(0, 0),
		end_coords=(300, 300),
		size=(10, 10)
	)

	grid = PointGrid(
		canvas=cnv,
		coords=matrix,
		point={"size": 4, "options": {"fill": "red", "width": 0}},
		line={"options": {"fill": "blue"}}
	)
	grid.set_pos((100, 100))
	grid.update(matrix)
	
	point = partial(DragPoint, canvas=cnv, size=16, color="orange")
	onmove_template = partial(partial, change_point, matrix, grid, mask)
	add = lambda p1, p2: tuple(map(sum, zip(p1, p2)))
	add_grid_pos = partial(add, (100, 100)) 

	p1 = point(
		pos=add_grid_pos(matrix[-1][-1]),
		onmove=onmove_template(2)
	)

	p2 = point(
		pos=add_grid_pos(matrix[0][0]),
		onmove=onmove_template(0)
	)

	p3 = point(
		pos=add_grid_pos(matrix[0][-1]),
		onmove=onmove_template(3)
	)

	p4 = point(
		pos=add_grid_pos(matrix[-1][0]),
		onmove=onmove_template(1)
	)

	cnv.pack()
	root.mainloop()