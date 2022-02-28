import pygame
import sys

def p5_map(n, start_1, stop_1, start_2, stop_2):
	return ((n - start_1)/(stop_1 - start_1)) * (stop_2 - start_2) + start_2

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 900
DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("#3 Solar System (2D)!")
TRANSLATION = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

class CelestialBody:
	def __init__(self, r: float, d: float, angle: float = 0.0):
		self.radius = r
		self.angle = angle
		self.distance = d
		self.bodies = []
	
	def spawn_moons(self, total_number_of_moons, radius: list , distance: list ):
		for i in range(total_number_of_moons):
			r = radius[i]
			d = distance[i]
			self.bodies.append(CelestialBody(self.radius * r, self.radius + d))
	
	def render(self):
		pygame.draw.circle(DISPLAY, (255, 255, 255), (0 + TRANSLATION[0], 0 + TRANSLATION[1]), self.radius)
		
		for body in self.bodies:
			body.render()

sun = CelestialBody(80, 0)
sun.spawn_moons(5, [0.1, 0.3, 0.8, 0.6, 0.45], [10, 50, 100, 150, 200])

clock = pygame.time.Clock()

while True:
	DISPLAY.fill((0, 0, 0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	
	sun.render()
	
	pygame.display.update()
	clock.tick(60)

