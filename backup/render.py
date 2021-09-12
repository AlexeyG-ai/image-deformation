import tkinter as tk
from collections import namedtuple
from threading import Thread
from time import sleep


class FieldRender:
	canvas_settings = namedtuple('CanvasSettings', ['width', 'height', 'fill'])

	def __init__(self, *, canvas_size=(1000, 1000), canvas_bg="white"):
		self._init_ui_objects(
			canvas=self.canvas_settings(
				width=canvas_size[0],
				height=canvas_size[1],
				fill=canvas_bg
			)
		)

		self._start_pos = (0, 0)
		self._runtime_thread = None

	def set_start_pos(self, x, y):
		assert isinstance(x, int) and isinstance(y, int)
		self._start_pos = (x, y)

	def _init_ui_objects(self, *, canvas):
		root = tk.Tk()
		
		self._cnv = tk.Canvas(
			root,
			width=canvas.width, height=canvas.height,
			bg=canvas.fill
		)
		self._root = root

		self._cnv.pack()

	def draw_point(self, pos, c=10, *, fill="blue"):
		pos1 = (
			pos[0] - c // 2 + self._start_pos[0],
			pos[1] - c // 2 + self._start_pos[1],
		)
	
		pos2 = (
			pos[0] + c // 2 + self._start_pos[0],
			pos[1] + c // 2 + self._start_pos[1],
		)
	
		self._cnv.create_rectangle(
			*pos1, *pos2,
			fill=fill,
			width=0
		)

	def draw_line(self, p1, p2, *, fill="blue"):
		self._cnv.create_line(
			p1[0] + self._start_pos[0], p1[1] + self._start_pos[1],
			p2[0] + self._start_pos[0], p2[1] + self._start_pos[1],
			fill=fill
		)

	def draw_matr(self, matr, matr_size, *, color="blue"):
		# DRAW POINTS
		for point in matr:
			self.draw_point(point, fill=color)
		
		# DRAW HORIZONTAL LINES
		for ind, point in enumerate(matr):
			if ind % matr_size == 0:
				continue
		
			self.draw_line(matr[ind - 1], point, fill=color)
		
		# DRAW VERTICAL LINES
		for ind, point in enumerate(matr[:-matr_size]):
			self.draw_line(point, matr[ind + matr_size], fill=color)

	def run(self):
		self._root.mainloop()