from math import cos, sin
from random import randint
import sys
import pygame
from pygame.math import Vector2

def p5_map(n, start_1, stop_1, start_2, stop_2):
	return ((n - start_1)/(stop_1 - start_1)) * (stop_2 - start_2) + start_2

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("#4 2D Raycasting")

class Boundary:
	def __init__(self, pos_1, pos_2):
		self.a = Vector2(*pos_1)
		self.b = Vector2(*pos_2)
	
	def render(self):
		pygame.draw.line(DISPLAY, (255, 255, 255), self.a, self.b)

class Ray:
	def __init__(self, start :Vector2, angle):
		self.pos = start
		self.direction = Vector2(cos(angle), sin(angle))
	
	def setDirection(self, x, y):
		self.direction.x = x - self.pos.x
		self.direction.y = y - self.pos.y
		self.direction.normalize()

	def cast(self, boundaries):
		sm_distace = None

		
		for boundary in boundaries:
			(x1, x2, y1, y2) = (boundary.a.x, boundary.b.x, boundary.a.y, boundary.b.y)
			(x3, x4, y3, y4) = (self.pos.x, self.pos.x + self.direction.x, self.pos.y, self.pos.y + self.direction.y)

			denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

			if denominator == 0:
				return None

			t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
			u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

			if 1 > t > 0 and u > 0:
				point = Vector2(
					x1 + t * (x2 - x1),
					y1 + t * (y2 - y1)
				)

				if sm_distace is None:
					sm_distace = point
				else:
					if self.pos.distance_to(point) < self.pos.distance_to(sm_distace):
						sm_distace = point
		
		return sm_distace

	def render(self):
		pygame.draw.line(DISPLAY, (255, 255, 255), self.pos, self.pos + self.direction)

class Particle:
	def __init__(self):
		self.boundaries = []
		for _ in range(5):
			self.boundaries.append(
				Boundary(
					(randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT)),
					(randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT))
				)
			)
		self.boundaries.append(
			Boundary(
				(0, 0),
				(SCREEN_WIDTH, 0)
			)
		)
		self.boundaries.append(
			Boundary(
				(0, SCREEN_HEIGHT),
				(SCREEN_WIDTH, SCREEN_HEIGHT)
			)
		)
		self.boundaries.append(
			Boundary(
				(0, 0),
				(0, SCREEN_HEIGHT)
			)
		)
		self.boundaries.append(
			Boundary(
				(SCREEN_WIDTH, 0),
				(SCREEN_WIDTH, SCREEN_HEIGHT)
			)
		)
		
		self.pos = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

		self.rays = []
		for angle in range(0, 360, 3):
			self.rays.append(Ray(self.pos, angle))
	
	def update(self):
		mx, my = pygame.mouse.get_pos()
		self.pos.x = mx
		self.pos.y = my
	
	def render(self):
		pygame.draw.circle(DISPLAY, (255, 255, 255), self.pos, 5)

		for ray in self.rays:
			ray.render()
			point = ray.cast(self.boundaries)
			if point is not None:
				pygame.draw.line(DISPLAY, (255, 255, 255), ray.pos, point, 2)

		for boundary in self.boundaries:
			boundary.render()

particle = Particle()

clock = pygame.time.Clock()

while True:
	DISPLAY.fill((0, 0, 0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	particle.update()
	particle.render()

	pygame.display.update()
	clock.tick(60)
