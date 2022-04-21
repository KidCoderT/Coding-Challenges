import sys
import pygame

width, height = 720, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("#167 Prime Spirula")
window.fill((0, 0, 0))


def is_prime(num):
    for i in range(2, num):
        if num % i == 0:
            return False
    return True


num = 1
direction = 0

total_steps = 1
done_steps = 1
repeat = 1

STEP_SIZE = 5

dot = pygame.Vector2(width / 2, height / 2)
total_spiral = int((width / STEP_SIZE) * (height / STEP_SIZE))

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if num < total_spiral:
        if is_prime(num):
            pygame.draw.circle(window, (255, 255, 255), dot.xy, STEP_SIZE * 0.3)

        if direction == 0:
            dot.x += STEP_SIZE
        elif direction == 1:
            dot.y -= STEP_SIZE
        elif direction == 2:
            dot.x -= STEP_SIZE
        else:
            dot.y += STEP_SIZE

        if done_steps % total_steps == 0:
            direction = (direction + 1) % 4
            repeat += 1
            if repeat % 2 == 0:
                total_steps += 1
        done_steps += 1

        num += 1

        pygame.display.update()

    clock.tick(60)
