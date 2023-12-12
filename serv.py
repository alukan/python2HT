import socket

socket_one = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 33123

socket_one.bind(("0.0.0.0", port))
socket_one.listen(1)
while True:
    ch = False
    connected_socket, addr = socket_one.accept()
    print("Connection from: " + str(addr))
    name = input ("Input your name ")
    connected_socket.send(name.encode())
    sec_name = connected_socket.recv(4096).decode()
    print(f"You are chatting with {sec_name}")
    while True:
        received_data = connected_socket.recv(4096)
        mess = received_data.decode()
        print(f"{sec_name}: {mess}")
        ans = input(f"{name}: ")
        connected_socket.send(ans.encode())

        if "stop" in mess or "stop" in ans:
            connected_socket.close()
            if "stop all" in mess or "stop all" in ans:
                ch = True
            break
    if ch:
        break
socket_one.close()