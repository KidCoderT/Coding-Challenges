from math import cos, dist, inf, radians, sin
import sys
import pyglet
from random import randint
from pyglet.window import key, mouse

window = pyglet.window.Window(600, 600, visible=True)
window.set_caption('#145 2D Raycasting')

# Batched rendering
batch = pyglet.graphics.Batch()
border = pyglet.graphics.OrderedGroup(0)
main = pyglet.graphics.OrderedGroup(1)


def random_vec():
	return [randint(0, window.width), randint(0, window.height)]

class Boundary:
	def __init__(self, a: tuple[int], b: tuple[int]) -> None:
		self.a = a
		self.b = b
		self.line = pyglet.shapes.Line(
			self.a[0],
			self.a[1],
			self.b[0],
			self.b[1],
			batch=batch,
			group=border
		)

class Ray:
	def __init__(self, pos: list[int], angle: int) -> None:
		self.pos = pos
		self.dir = [cos(angle), sin(angle)]

	def set_direction(self, x, y):
		self.dir[0] = x - self.pos[0]
		self.dir[1] = y - self.pos[1]

	def draw(self):
		a, b = self.pos, [self.pos[0] + self.dir[0], self.pos[1] + self.dir[1]]

		line = pyglet.shapes.Line(
			a[0],
			a[1],
			b[0],
			b[1],
			batch=batch,
			group=border
		)
		line.draw()

	def cast(self, wall: Boundary):
		x1, y1, x2, y2 = wall.a[0], wall.a[1], wall.b[0], wall.b[1]
		x3, y3, x4, y4 = self.pos[0], self.pos[1], self.pos[0] + \
			self.dir[0], self.pos[1] + self.dir[1]

		denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
		if denominator == 0:
			return None

		t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
		u = - ((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

		if 0 < t < 1 and u > 0:
			return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


class Particle:
	def __init__(self) -> None:
		self.pos = [window.width / 2, window.height / 2]
		self.shape = pyglet.shapes.Circle(
			self.pos[0],
			self.pos[1],
			10,
			batch=batch,
			group=main
		)
		self.walls = [Boundary(random_vec(), random_vec()) for i in range(4)]
		self.rays = [Ray(self.pos, radians(angle)) for angle in range(0, 360, 2)]

		self.walls.append(
			Boundary((0, 0), (0, window.height))
		)
		self.walls.append(
			Boundary((0, 0), (window.width, 0))
		)
		self.walls.append(
			Boundary((window.width, 0), (window.width, window.height))
		)
		self.walls.append(
			Boundary((0, window.height), (window.width, window.height))
		)

	def update(self, mx, my):
		self.pos[0] = mx
		self.pos[1] = my
		self.shape.x = self.pos[0]
		self.shape.y = self.pos[1]
	
	def draw(self):
		for ray in self.rays:
			closest = None
			record = float('inf')
			for wall in self.walls:
				pt = ray.cast(wall)
				if pt is None: continue
				
				new_record = dist(self.pos, pt)
				if new_record < record:
					record = new_record
					closest = pt
			
			if closest is not None:
				a, b = ray.pos, closest

				line = pyglet.shapes.Line(
					a[0],
					a[1],
					b[0],
					b[1],
					batch=batch,
					group=border
				)
				line.draw()

particle = Particle()

@window.event
def on_key_press(symbol, modifier):
	pass
	# if symbol == key.W or symbol == key.UP:
	# 	player_paddle.is_up = True
	# if symbol == key.S or symbol == key.DOWN:
	# 	player_paddle.is_down = True


@window.event
def on_key_release(symbol, modifier):
	pass
	# if symbol == key.W or symbol == key.UP:
	# 	player_paddle.is_up = False
	# if symbol == key.S or symbol == key.DOWN:
	# 	player_paddle.is_down = False


@window.event
def on_mouse_motion(x, y, dx, dy):
	# ray.set_direction(x + dx, y + dy)
	particle.update(x + dx, y + dy)


def update(dt):
	pass


@window.event
def on_draw():
	window.clear()
	batch.draw()
	particle.draw()

pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()
