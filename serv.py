import socket
from threading import Thread

socket_one = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 33124

socket_one.bind(("0.0.0.0", port))
socket_one.listen(2)
def handle_client(connected_socket, num):
    while True:
        received_data = connected_socket.recv(4096)
        if(num == 1):
            connected_socket_two.send(received_data)
        else:
            connected_socket_one.send(received_data)


connected_socket_one, addr = socket_one.accept()
print("Connection from: " + str(addr))
connected_socket_two, addr2 = socket_one.accept()
print("Connection from: " + str(addr2))
# create thread to handle client
t1 = Thread(target=handle_client, args=[connected_socket_one, 1])
t1.start()

t2 = Thread(target=handle_client, args=[connected_socket_two, 2])
t2.start()
while True:
    message = input("Enter a message: ")

#    connected_socket.close()

    if "stop" in message:
        break

socket_one.close()