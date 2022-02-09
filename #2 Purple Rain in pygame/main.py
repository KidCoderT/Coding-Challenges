import random
import pygame
import sys

def p5_map(n, start_1, stop_1, start_2, stop_2):
	return ((n - start_1)/(stop_1 - start_1)) * (stop_2 - start_2) + start_2

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 720
DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("#2 Purple Rain!")

class Drop:
	def __init__(self):
		self.x = random.randint(0, SCREEN_WIDTH)
		self.y = random.randint(-200, SCREEN_HEIGHT + 200)
		self.z = random.randint(0, 40)
		self.y_speed = p5_map(self.z, 0, 40, 10, 20)
		self.length = p5_map(self.z, 0, 40, 5, 25)
	
	def update(self):
		self.y += self.y_speed

		if self.y > SCREEN_HEIGHT:
			self.y = -random.randint(100, 200)
			self.z = random.randint(0, 40)
			self.y_speed = p5_map(self.z, 0, 40, 10, 20)
			self.length = p5_map(self.z, 0, 40, 5, 25)
		
		self.y_speed += 0.2

	def render(self):
		pygame.draw.line(DISPLAY, (138, 43, 226), (self.x, self.y), (self.x, self.y + 20), 2)

drops = [Drop() for i in range(500)]
clock = pygame.time.Clock()

while True:
	DISPLAY.fill((230, 230, 250))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	
	for drop in drops:
		drop.update()
		drop.render()
	
	pygame.display.update()
	clock.tick(60)
