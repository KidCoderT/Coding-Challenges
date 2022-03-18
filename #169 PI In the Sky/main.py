from re import U
import sys
import pygame
import random

pygame.init()

width, height = 900, 750
DISPLAY = pygame.display.set_mode((width, height))
pygame.display.set_caption("PI In the SKY")


def load(url):
	img = pygame.image.load(url)
	img = pygame.transform.scale(img, (60, 60))
	img.convert()
	return img


IMAGE = {
	"0": [load(f"Pies/Pie_{color}-00.png") for color in ["Blue", "Orange", "Pink", "Yellow"]],
	"1": [load(f"Pies/Pie_{color}-01.png") for color in ["Blue", "Orange", "Pink", "Yellow"]],
	"2": [load(f"Pies/Pie_{color}-02.png") for color in ["Blue", "Orange", "Pink", "Yellow"]],
	"3": [load(f"Pies/Pie_{color}-03.png") for color in ["Blue", "Orange", "Pink", "Yellow"]],
	"4": [load(f"Pies/Pie_{color}-04.png") for color in ["Blue", "Orange", "Pink", "Yellow"]],
	"5": [load(f"Pies/Pie_{color}-05.png") for color in ["Blue", "Orange", "Pink", "Yellow"]],
	"6": [load(f"Pies/Pie_{color}-06.png") for color in ["Blue", "Orange", "Pink", "Yellow"]],
	"7": [load(f"Pies/Pie_{color}-07.png") for color in ["Blue", "Orange", "Pink", "Yellow"]],
	"8": [load(f"Pies/Pie_{color}-08.png") for color in ["Blue", "Orange", "Pink", "Yellow"]],
	"9": [load(f"Pies/Pie_{color}-09.png") for color in ["Blue", "Orange", "Pink", "Yellow"]]
}

clock = pygame.time.Clock()

START = 0
PLAYING = 1
GAMEOVER = -1
state = START

pi = ""
with open("one-million.txt", 'r', encoding='utf-8') as f:
	for line in f:
		pi = pi + line[:-2]


class Pie:
	radius = 30

	def __init__(self) -> None:
		self.x = random.randint(15 + self.radius, width - 15 - self.radius)
		self.y = random.randint(-100, -30)
		self.num = random.randint(0, 9)
		self.img = random.choice(IMAGE[str(self.num)])

		self.vel_y = 1

	def update(self):
		self.y += self.vel_y
		if self.y > -30:
			self.vel_y += 0.19

	def render(self):
		DISPLAY.blit(self.img, (self.x - self.radius, self.y - self.radius))


class Plate:
	plate = pygame.image.load("Plate.png")

	def __init__(self) -> None:
		self.rect = pygame.Rect(0, height - 25, 80, 20)
		self.hitbox = pygame.Rect(0, height - 55, 70, 30)
		self.rect.centerx = width / 2
		self.hitbox.centerx = width / 2

	def update(self):
		mx, _ = pygame.mouse.get_pos()
		self.rect.centerx = mx
		if self.rect.left < 15:
			self.rect.x = 15
		elif self.rect.right > width - 25:
			self.rect.x = width - 25 - self.rect.width

		self.hitbox.centerx = self.rect.centerx

	def catches(self, pie: Pie):
		if self.hitbox.collidepoint(pie.x, pie.y):
			return True
		return False

	def render(self):
		# pygame.draw.rect(DISPLAY, (0, 0, 0), self.rect)
		# pygame.draw.rect(DISPLAY, (70, 70, 70), self.hitbox)
		DISPLAY.blit(self.plate, self.rect.topleft)


plate = Plate()
pies = []
digits = "3."
chance = 0.05

PI_FONT = pygame.font.Font("Bungee-Regular.ttf", 30)
logo = pygame.transform.scale(pygame.image.load(
	"Pi-in-the-sky-Logo.png"), (1500 * 0.4, 883 * 0.4))
logo_rect = pygame.Rect(0, 0, logo.get_width() + 20, logo.get_height() + 20)
logo_rect.centerx = width / 2
logo_rect.centery = height / 2 - 60

info_text = PI_FONT.render("Pres any key to continue", False, (112, 50, 126))

def reset():
	global digits, chance, pies, plate
	digits = "3."
	chance = 0.05
	pies = []
	plate = Plate()

while True:
	DISPLAY.fill((135, 222, 249))
	if random.random() <= chance:
		pies.append(Pie())

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if state == START:
				state = PLAYING
				reset()
			elif state == GAMEOVER:
				state = PLAYING

	if state == START:
		pygame.draw.rect(DISPLAY, (161, 235, 255), logo_rect)
		DISPLAY.blit(logo, (width / 2 - logo.get_width() / 2,
					 height / 2 - logo.get_height() / 2 - 60))
		DISPLAY.blit(
			info_text, (width / 2 - info_text.get_width() / 2, logo_rect.bottom + 40))

	elif state == PLAYING:
		plate.render()
		plate.update()

		to_remove = []

		for pie in pies:
			pie.render()
			pie.update()

			if plate.catches(pie):
				to_remove.append(pie)
				if pi[len(digits) - 2] == str(pie.num):
					digits += str(pie.num)
				else:
					state = GAMEOVER
			elif pie.y > height + 30:
				to_remove.append(pie)

		for pie in to_remove:
			try: pies.remove(pie)
			except: pass

		_3 = PI_FONT.render("PI", False, (0, 0, 0))
		DISPLAY.blit(_3, (width - 10 - _3.get_width(), 20))

		_rl = list(["3"] + list(digits[2:]))
		for i, num in enumerate(_rl[-12:]):
			r = PI_FONT.render(num, False, (0, 0, 0))
			DISPLAY.blit(r, (width - 15 - r.get_width(), 60 + i * 35))

		next = PI_FONT.render(pi[len(digits) - 2], False, (50, 150, 50))
		DISPLAY.blit(next, (width - 15 - next.get_width(),
							60 + min(len(digits) - 1, 12) * 35))

		score = PI_FONT.render(f"score: {len(digits) - 2}", False, (0, 0, 0))
		DISPLAY.blit(score, (15, 20))

		if len(digits) - 2 == 5 and chance == 0.05:
			chance += 0.02
		elif len(digits) - 2 == 10 and chance == 0.07:
			chance += 0.03
		elif len(digits) - 2 == 20 and chance == 0.1:
			chance += 0.07
	elif state == GAMEOVER:
		pygame.draw.rect(DISPLAY, (161, 235, 255), logo_rect)
		DISPLAY.blit(logo, (width / 2 - logo.get_width() / 2,
                      height / 2 - logo.get_height() / 2 - 60))
		DISPLAY.blit(
			info_text, (width / 2 - info_text.get_width() / 2, logo_rect.bottom + 40))
		title = PI_FONT.render("GAME OVER", False, (0, 0, 0))
		DISPLAY.blit(
			title, (width / 2 - title.get_width() / 2, logo_rect.bottom + 90))

		score = PI_FONT.render(f"score: {len(digits) - 2}", False, (0, 0, 0))
		DISPLAY.blit(score, (width / 2 - score.get_width() / 2, 40))

	pygame.display.update()
	clock.tick(60)
