import socket

HOST = "10.135.13.123"  # The server's hostname or IP address
PORT = 8888  # The port used by the server

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM ) as s:

        s.connect((HOST, PORT))
        while True:
            data = s.recv(1024)
            message_recieved = str(data)[1:]
            # if the message contains a -1 at the end, then wait for another message instead of sending one
            if(message_recieved[-3:-1] != "-1"):
                print("Host: " + message_recieved)
                message = input()
                s.sendall(message.encode('UTF-8'))
            else:
                print("Host: " + (message_recieved[:-3]))
            if(message == "end"):
                break
        s.close()

if __name__ == "__main__":
    main()
    