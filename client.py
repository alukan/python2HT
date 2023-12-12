import socket

socket_one = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 33123
server_address = '127.0.0.1'

socket_one.connect((server_address, port))
buffer_size = 4096
name = input ("Input your name ")
socket_one.send(name.encode())
sec_name = socket_one.recv(buffer_size).decode()
print(f"You are chatting with {sec_name}")
while True:
    ans = input(f"{name}: ")
    socket_one.send(ans.encode())
    mess = socket_one.recv(buffer_size).decode()
    print(f"{sec_name}: {mess}")
    if "stop" in mess or "stop" in ans:
            socket_one.close()
            break