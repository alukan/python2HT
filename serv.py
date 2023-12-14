import socket
from threading import Thread
import logging

with open('network_game.log', 'w'):
    pass

log_format = '%(asctime)s [%(levelname)s] %(message)s'
socket_one = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logging.basicConfig(filename='network_game.log', level=logging.INFO, format=log_format)
port = 33124

socket_one.bind(("0.0.0.0", port))
socket_one.listen(2)
def handle_client(connected_socket, num):
    while True:
        received_data = connected_socket.recv(4096)
        
        message = f"Received coordinates: {received_data.decode()} from {addresses[num]}"
        if(received_data.decode() == "stop"):
            socket_one.close()
            logging.info("Connection closed")
            break
        #logging.info(message) it creates bug when file is too big
        sockets[1-num].send(received_data)

addresses=["",""]
connected_socket_one, addresses[0] = socket_one.accept()
print("Connection from: " + str(addresses[0]))
logging.info(f"Connection established with {addresses[0]}")
player_one = connected_socket_one.recv(4096)
connected_socket_two, addresses[1] = socket_one.accept()
print("Connection from: " + str(addresses[1]))
logging.info(f"Connection established with {addresses[1]}")
player_two = connected_socket_two.recv(4096)

sockets = [connected_socket_one, connected_socket_two]

connected_socket_one.send(player_two)
connected_socket_two.send(player_one)
# create thread to handle client
t1 = Thread(target=handle_client, args=[connected_socket_one, 0])
t1.start()

t2 = Thread(target=handle_client, args=[connected_socket_two, 1])
t2.start()

logging.info("Network Game Program started.")

socket_one.close()