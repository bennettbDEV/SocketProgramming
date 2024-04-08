import socket

HOST = "<IPADDRESS>"  # The server's hostname or IP address
PORT = 9999  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM ) as s:

    s.connect((HOST, PORT))
    while True:
        message = input()
        s.sendall(message.encode('UTF-8'))
        data = s.recv(1024)
        print("Echo: " + (str(data)[1:]) )
        if(message == "end"):
            break
    s.close()
    


