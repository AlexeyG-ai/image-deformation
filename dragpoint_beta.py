class DragEvent:
	def __init__(self, instance):
		self._instance = instance
		self._onclick_listeners = [self._drag_onclick]
		self._onmousemove_listeners = [self._drag_onmousemove]
		self._init_listeners()

	def _init_listeners(self):
		cnv = self._instance._canvas
		tag = self._instance._item_id

		cnv.tag_bind(tag, "<Button-1>", self._onclick_manager)
		cnv.tag_bind(tag, "<B1-Motion>", self._onmousemove_manager)

	def _onclick_manager(self, event):
		for listener in self._onclick_listeners:
			listener(event, self._instance)

	def _onmousemove_manager(self, event):
		for listener in self._onmousemove_listeners:
			listener(event, self._instance)

	def _drag_onclick(self, event, point):
		self._instance_start_pos = self._instance.get_pos()
		self._event_start_pos = (event.x, event.y)

	def _drag_onmousemove(self, event, point):
		start_x, start_y = self._event_start_pos
		dx, dy = event.x - start_x, event.y - start_y
		obj_x, obj_y = self._instance_start_pos

		self._instance.set_pos((obj_x + dx, obj_y + dy))

class DragPoint:
	def __init__(self, canvas, pos, size, color, *, onclick=None, onmove=None):
		self._canvas = canvas
		self.color = color
		self._init_on_canvas()
		self.set_pos(pos)
		self.set_size(size)
		self._drag_event = DragEvent(self)

		if onclick is not None:
			self._drag_event._onclick_listeners.append(onclick)

		if onmove is not None:
			self._drag_event._onmousemove_listeners.append(onmove)

	def _init_on_canvas(self):
		"""Инициализирует обьект на холсте"""
		self._item_id = self._canvas.create_rectangle(0, 0, 40, 40)
		self._canvas.itemconfig(self._item_id, fill=self.color, width=0)

	def _get_coords(self):
		"""Получение координат точек, по которым строится фигура"""
		return self._canvas.coords(self._item_id)

	def _set_coords(self, pos, size):
		"""Высчитывает и устанавливает координаты точек для отрисовки фигуры.
		pos: tuple[int] - положение обьекта
		size: int - размер обьекта
		"""
		x, y = pos
		self._canvas.coords(
			self._item_id, 
			x - size // 2, y - size // 2,
			x + size // 2, y + size // 2
		)

	def get_pos(self):
		"""Возвращает позицию обьекта"""
		x1, y1, x2, y2 = self._get_coords()
		return (
			(x1 + x2) // 2,
			(y1 + y2) // 2
		)

	def set_pos(self, pos):
		"""Устанавливает позицию обьекта"""
		self._set_coords(pos=pos, size=self.get_size())

	def get_size(self):
		"""Возвращает размер (ширина / высота) обьекта"""
		x1, _, x2, _ = self._get_coords()
		return x2 - x1

	def set_size(self, size):
		"""Устанавливает размеры обьекта"""
		self._set_coords(pos=self.get_pos(), size=size)