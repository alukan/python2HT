import pygame
import socket
import json
from threading import Thread
# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 700))
clock = pygame.time.Clock()
running = True

try:
    with open("client2_pos.json", "r") as json_file:
        loaded_data = json.load(json_file)
    circle_pos = pygame.Vector2(loaded_data["x"], loaded_data["y"])
except:
    circle_pos = pygame.Vector2(50, 50)

other_player_pos = pygame.Vector2(0, 0)

def handle_server(connected_socket):
    while running:
        received_data = connected_socket.recv(4096).decode().split("; ")
        other_player_pos.x = float(received_data[0])
        other_player_pos.y = float(received_data[1])

socket_one = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 33124
server_address = '127.0.0.1'

socket_one.connect((server_address, port))
socket_one.send((f"{circle_pos.x}; {circle_pos.y}").encode())
received_data = socket_one.recv(4096).decode().split("; ")
other_player_pos.x = float(received_data[0])
other_player_pos.y = float(received_data[1])
t1 = Thread(target=handle_server, args=[socket_one])
t1.start()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("client2_pos.json", "w") as json_file:
                data = {
                    "x":  circle_pos.x,
                    "y":  circle_pos.y
                }
                json.dump(data, json_file)
            socket_one.send(("stop").encode())
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