from dataclasses import dataclass
import socket
import threading
from datetime import datetime


HOST = socket.gethostname()  # The server's hostname or IP address
PORT = 8888  # The port used by the server

@dataclass 
class Client:
    connection: socket
    addr: str
    name: str
    rps_hand: str = ""
    game_phrase: str = ""
    queued_for_rps: bool = False
    accept_connections: bool = True


class Server:
    def __init__(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
        self.s.bind((HOST,PORT))
        self.s.listen()

        self.clients = []
        self.clients_looking_for_rps = []
        
        self.acceptConnections()
        
    def acceptConnections(self):
        '''
        Accepts connections, requests the inputed name from the client.
        Adds the connection and name to list of known clients.
        Starts thread with connection to client to recieve messages from them.
        '''
        while True:
            (conn, addr) = self.s.accept()
            print(f"{addr} connected")

            conn.send("Return_Name".encode('UTF-8'))
            name = conn.recv(1024).decode('UTF-8')

            newClient = Client(conn, addr, name)
            self.clients.append(newClient)

            conn.send("Connection to server successful\n".encode('UTF-8'))
            self.sendMsg(f"{name} joined the chatroom\n")

            print(f"Current Client List: {self.clients}")
            
            thread = threading.Thread(target=self.recieveMsg,args=(newClient,))
            thread.start()

    ### Add encryption for both sending and recieving msgs
    def sendMsg(self,message):
        '''
        Takes in message to be sent
        then encodes the message and sends it to all clients.
        '''
        for client in self.clients:
            client.connection.send(message.encode('UTF-8'))

    def recieveMsg(self, client):
        while True:
            try:
                msg = client.connection.recv(1024).decode('UTF-8')
                phrases = [other_client.game_phrase for other_client in self.clients]
                
                if not client.accept_connections:
                    continue
                elif msg == "INITIATE_RPS#":
                    self.start_rps(client)
                elif (not client.queued_for_rps) and msg in phrases:
                    client.connection.send("OPEN_RPS#".encode('UTF-8'))
                    
                    for player in self.clients_looking_for_rps:
                        if player.game_phrase == msg:
                            client2 = player
                            break
                    hand1 = client2.rps_hand
                    hand2 = client.connection.recv(1024).decode('UTF-8')
                    hands = f"{client2.name} chose: {hand1} and {client.name} chose: {hand2}."

                    match (self.rps_game_turn(hand1,hand2)):
                        case 1:
                            result = f"{client2.name} wins!"
                        case 2:
                            result = f"{client.name} wins!"
                        case _:
                            result = "Its a Tie!"

                    self.sendMsg(hands + "\n" + result + "\n")

                    client2.game_phrase = ""
                    client2.queued_for_rps = False
                    client2.accept_connections = True

                    self.clients_looking_for_rps.remove(client2)

                    client.connection.send("CLOSE_RPS#".encode('UTF-8'))
                    client2.connection.send("CLOSE_RPS#".encode('UTF-8'))
                else:
                    cur_time = "[" + (datetime.now().strftime("%H:%M:%S")) + "]"
                    fmt_msg = f"{cur_time} {client.name}: {msg}"
                    print(fmt_msg)
                    self.sendMsg(fmt_msg+"\n")
            except:
                print(f"Removed: {client.name}")
                self.clients.remove(client)
                client.connection.close()
                self.sendMsg(f"{client.name} left the chatroom")
                break

    def start_rps(self, client):
        self.clients_looking_for_rps.append(client)
        
        client.connection.send("OPEN_RPS#".encode('UTF-8'))

        client.rps_hand = client.connection.recv(1024).decode('UTF-8')
        print(f"Hand: {client.rps_hand}")
                    
        fmt_msg = f"{client.name}: wants to play rock paper scissors. Type 'PLAY {client.name}'"
        print(fmt_msg)
        self.sendMsg(fmt_msg+"\n")
        
        client.game_phrase = f"PLAY {client.name}"
        client.queued_for_rps = True
        client.accept_connections = False

    def rps_game_turn(self,hand1,hand2):
        if hand1 == "Rock":
            if hand2 == "Rock":
                return 0
            elif hand2 == "Paper":
                return 2
            else:
                return 1
        elif hand1 == "Paper":
            if hand2 == "Rock":
                return 1
            elif hand2 == "Paper":
                return 0
            else:
                return 2
        else:
            if hand2 == "Rock":
                return 2
            elif hand2 == "Paper":
                return 1
            else:
                return 0

Server(HOST,PORT)