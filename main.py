import pygame
import sys
import math

pygame.init()

screen_width = 800
screen_height = 600

black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('ball')

angle = 0

radius = 10

angular_speed = 0.1
rad_speed = 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    x = screen_width // 2 + radius * math.cos(angle)
    y = screen_height // 2 + radius * math.sin(angle)
    radius += rad_speed
    if (rad_speed > 0) and radius > 300:
        rad_speed = -rad_speed
        angular_speed = -angular_speed
    elif (rad_speed < 0) and radius < 20:
        rad_speed = -rad_speed
        angular_speed = -angular_speed
    angle += angular_speed

    screen.fill(black)

    pygame.draw.line(screen, white, (screen_width // 2, screen_height // 2), (int(x), int(y)), 2)

    pygame.draw.circle(screen, white, (int(x), int(y)), 20)

    pygame.display.flip()

    pygame.time.Clock().tick(60)