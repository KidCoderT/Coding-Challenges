import random
import pygame
import sys

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("#1 Starfield!")

def p5_map(n, start_1, stop_1, start_2, stop_2):
	return ((n - start_1)/(stop_1 - start_1)) * (stop_2 - start_2) + start_2

class Star:
	def __init__(self):
		self.x = random.randint(-SCREEN_WIDTH, SCREEN_WIDTH)
		self.y = random.randint(-SCREEN_HEIGHT, SCREEN_HEIGHT)
		self.z = random.randint(0, SCREEN_WIDTH)
		self.pz = self.z
	
	def update(self, speed):
		self.z -= speed
		if self.z < 1:
			self.z = SCREEN_WIDTH
			self.x = random.randint(-SCREEN_WIDTH, SCREEN_WIDTH)
			self.y = random.randint(-SCREEN_HEIGHT, SCREEN_HEIGHT)
			self.pz = self.z
	
	def render(self, translation):
		sx = p5_map(self.x/self.z, 0, 1, 0, SCREEN_WIDTH)
		sy = p5_map(self.y/self.z, 0, 1, 0, SCREEN_HEIGHT)

		# r = p5_map(self.z, 0, SCREEN_WIDTH, 8, 0)
		# pygame.draw.circle(DISPLAY, (255, 255, 255), (sx + translation[0], sy + translation[1]), r)

		px = p5_map(self.x / self.pz, 0, 1, 0, SCREEN_WIDTH)
		py = p5_map(self.y / self.pz, 0, 1, 0, SCREEN_HEIGHT)

		pygame.draw.line(DISPLAY, (255, 255, 255), (sx + translation[0], sy + translation[1]), (px + translation[0], py + translation[1]))

		self.pz = self.z

stars = [Star() for _ in range(800)]
max_speed = 30
speed = 0

translation = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

while True:

	speed = p5_map(pygame.mouse.get_pos()[0], 0, SCREEN_WIDTH, -max_speed, max_speed)
	DISPLAY.fill((0, 0, 0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	
	for star in stars:
		star.update(speed)
		star.render(translation)
	
	pygame.display.update()
