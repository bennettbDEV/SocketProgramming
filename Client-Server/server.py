import socket

HOST = "<IPADDRESS>"  # The server's hostname or IP address
PORT = 9999  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM ) as s:
    s.bind((HOST,PORT))
    s.listen()
    (conn, addr) = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data: break
            print("Client msg: " + (str(data)[1:]))
            conn.sendall(data)
        s.close()

game_dict = {
    "rock": 0,
    "paper": 1,
    "scissors": 2
    }