import pygame
import socket
from threading import Thread
# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 700))
clock = pygame.time.Clock()
running = True

circle_pos = pygame.Vector2(screen.get_width() / 3, screen.get_height() / 3)
other_player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

def handle_server(connected_socket):
    while True:
        received_data = connected_socket.recv(4096).decode().split("; ")
        other_player_pos.x = float(received_data[0])
        other_player_pos.y = float(received_data[1])
        if(not running):
            break

socket_one = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 33124
server_address = '127.0.0.1'

socket_one.connect((server_address, port))

t1 = Thread(target=handle_server, args=[socket_one])
t1.start()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # if left arrow key is pressed, move circle to the left
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        circle_pos.x -= 5
        socket_one.send((f"{circle_pos.x}; {circle_pos.y}").encode())

    # if right arrow key is pressed, move circle to the right
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        circle_pos.x += 5
        socket_one.send((f"{circle_pos.x}; {circle_pos.y}").encode())

    if pygame.key.get_pressed()[pygame.K_UP]:
        circle_pos.y -= 5
        socket_one.send((f"{circle_pos.x}; {circle_pos.y}").encode())

    # if right arrow key is pressed, move circle to the right
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        circle_pos.y += 5
        socket_one.send((f"{circle_pos.x}; {circle_pos.y}").encode())

    pygame.draw.circle(screen, "green", circle_pos, 40)

    pygame.draw.circle(screen, "red", other_player_pos, 40)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()