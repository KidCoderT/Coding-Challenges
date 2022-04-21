from math import cos, dist, inf, radians, sin
import sys
import pyglet
from random import randint
from pyglet.window import key, mouse

width, height = 700, 700
window = pyglet.window.Window(width*2, height, visible=True)
window.set_caption('#146 Raycast Rendering')

# Batched rendering
batch = pyglet.graphics.Batch()
border = pyglet.graphics.OrderedGroup(0)
main = pyglet.graphics.OrderedGroup(1)

VISIBILITY = 40


def random_vec():
    return [randint(0, width), randint(0, height)]


def p5_map(n, start_1, stop_1, start_2, stop_2):
    return ((n - start_1)/(stop_1 - start_1)) * (stop_2 - start_2) + start_2


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

    def render(self, walls):
        closest = None
        record = float('inf')
        for wall in walls:
            pt = self.cast(wall)
            if pt is None:
                continue

            new_record = dist(self.pos, pt)
            if new_record < record:
                record = new_record
                closest = pt

        if closest is not None:
            a, b = self.pos, closest

            line = pyglet.shapes.Line(
                a[0],
                a[1],
                b[0],
                b[1],
                batch=batch,
                group=border
            )
            line.draw()

        return record

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
        self.pos = [width / 2, height / 2]
        self.shape = pyglet.shapes.Circle(
            self.pos[0],
            self.pos[1],
            10,
            batch=batch,
            group=main
        )
        self.walls = [Boundary(random_vec(), random_vec()) for i in range(4)]
        self.rays = [Ray(self.pos, radians(angle))
                     for angle in range(0, VISIBILITY, 1)]
        self.move_forward = False
        self.move_back = False

        self.walls.append(
            Boundary((0, 0), (0, height))
        )
        self.walls.append(
            Boundary((0, 0), (width, 0))
        )
        self.walls.append(
            Boundary((width, 0), (width, height))
        )
        self.walls.append(
            Boundary((0, height), (width, height))
        )

        self.scenes = [None for i in range(VISIBILITY)]

    def update(self, mx, my):
        self.pos[0] = mx
        self.pos[1] = my
        if self.pos[0] >= width:
            self.pos[0] = width

        self.shape.x = self.pos[0]
        self.shape.y = self.pos[1]

    def draw(self):
        for i, ray in enumerate(self.rays):
            scene = ray.render(self.walls)
            self.scenes[i] = scene

        w = width / VISIBILITY
        for i, scene in enumerate(self.scenes):
            try:
                v = 255 - int(scene)
                color = (v, v, v)
            except:
                color = (0, 0, 0)
            rect = pyglet.shapes.Rectangle(
                width + i*w, 0, w, height, color)
            rect.draw()


particle = Particle()


@window.event
def on_key_press(symbol, modifier):
    pass
    if symbol == key.W or symbol == key.UP:
        particle.move_forward = True
    if symbol == key.S or symbol == key.DOWN:
        particle.move_back = True


@window.event
def on_key_release(symbol, modifier):
    if symbol == key.W or symbol == key.UP:
        particle.move_forward = False
    if symbol == key.S or symbol == key.DOWN:
        particle.move_back = False


@window.event
def on_mouse_motion(x, y, dx, dy):
    # ray.set_direction(x + dx, y + dy)
    particle.update(x + dx, y + dy)


def update(dt):
    # particle.update(dt)
    pass


@window.event
def on_draw():
    window.clear()
    batch.draw()
    particle.draw()


pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()
