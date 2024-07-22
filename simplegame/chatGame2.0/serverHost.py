import socket
import threading
import rsa
from datetime import datetime
from dataclasses import dataclass


HOST = socket.gethostname()  # The server's hostname or IP address
PORT = 8888  # The port used by the server

@dataclass 
class Client:
    connection: socket
    addr: str
    public_key: rsa.PublicKey
    name: str
    rps_hand: str = ""
    game_phrase: str = ""
    queued_for_rps: bool = False

class Server:
    def __init__(self, host, port):
        self.pub_key, self.priv_key = rsa.newkeys(1024)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
        self.s.bind((host,port))
        self.s.listen()

        self.clients = []
        self.clients_looking_for_rps = []
        
        self.acceptConnections()
        
    def acceptConnections(self):
        '''
        Accepts connections, exchange public keys, then requests the inputed name from the client.
        Adds the connection and name to list of known clients.
        Starts thread with connection to client to recieve messages from them.
        '''
        while True:
            (conn, addr) = self.s.accept()

            try:
                conn.send(self.pub_key.save_pkcs1("PEM"))
                client_pub = rsa.PublicKey.load_pkcs1(conn.recv(1024))
            except:
                print("Couldn't exchange private keys")
                continue

            print(f"{addr} connected")

            conn.send(rsa.encrypt("Return_Name".encode('UTF-8'), client_pub))
            name = rsa.decrypt(conn.recv(1024), self.priv_key).decode('UTF-8')

            newClient = Client(conn, addr, client_pub, name)
            self.clients.append(newClient)

            conn.send(rsa.encrypt("Connection to server successful\n".encode('UTF-8'), client_pub))
            self.sendMsg(f"{name} joined the chatroom\n")

            print(f"Current Client List: {self.clients}")
            
            thread = threading.Thread(target=self.recieveMsg,args=(newClient,))
            thread.start()

    def sendMsg(self,message):
        '''
        Takes in message to be sent
        then encrypts the message and sends it to all clients.
        '''
        print("> " + message)
        for client in self.clients:
            client.connection.send(rsa.encrypt(message.encode('UTF-8'), client.public_key))

    def recieveMsg(self, client):
        while True:
            try:
                msg = rsa.decrypt(client.connection.recv(1024), self.priv_key).decode('UTF-8')
                phrases = [other_client.game_phrase for other_client in self.clients]
                
                if client.queued_for_rps and msg == "CANCEL":
                    self.cancel_rps(client)
                    self.sendMsg(f"{client.name} cancelled the rock paper scissors challenge.\n")
                elif client.queued_for_rps:
                    continue
                elif msg == "INITIATE_RPS#":
                    self.start_rps_host(client)
                elif msg in phrases:
                    self.start_rps_p2(client, msg)
                else:
                    cur_time = "[" + (datetime.now().strftime("%H:%M:%S")) + "]"
                    fmt_msg = f"{cur_time} {client.name}: {msg}"
                    self.sendMsg(fmt_msg+"\n")
            except:
                print(f"Removed: {client.name}")
                self.clients.remove(client)
                client.connection.close()
                self.sendMsg(f"{client.name} left the chatroom")
                break

    def start_rps_host(self, client):
        self.clients_looking_for_rps.append(client)
        
        client.connection.send(rsa.encrypt("OPEN_RPS#".encode('UTF-8'), client.public_key))

        client.rps_hand = rsa.decrypt(client.connection.recv(1024), self.priv_key).decode('UTF-8')
        if client.rps_hand == "CANCEL":
            client.connection.send(rsa.encrypt("CLOSE_RPS#".encode('UTF-8'), client.public_key))
            return
            
        print(f"Hand: {client.rps_hand}")
                    
        fmt_msg = f"{client.name}: wants to play rock paper scissors. Type 'Play {client.name}'"
        self.sendMsg(fmt_msg+"\n")
        
        client.game_phrase = f"Play {client.name}"
        client.queued_for_rps = True

    def start_rps_p2(self,client,msg):
        client.connection.send(rsa.encrypt("OPEN_RPS#".encode('UTF-8'), client.public_key))
                    
        for player in self.clients_looking_for_rps:
            if player.game_phrase == msg:
                client2 = player
                break

        self.sendMsg(f"{client.name} accepted {client2.name}'s challenge!\n")

        hand1 = client2.rps_hand
        hand2 = rsa.decrypt(client.connection.recv(1024), self.priv_key).decode('UTF-8')
        if hand2 == "CANCEL":
            self.cancel_rps(client)
            self.cancel_rps(client2)
            self.sendMsg(f"{client.name} cancelled the rock paper scissors challenge.\n")
            return

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

        self.clients_looking_for_rps.remove(client2)

        client.connection.send(rsa.encrypt("CLOSE_RPS#".encode('UTF-8'), client.public_key))
        client2.connection.send(rsa.encrypt("CLOSE_RPS#".encode('UTF-8'), client2.public_key))

    def cancel_rps(self, client):
        client.queued_for_rps = False
        if client in self.clients_looking_for_rps:
            self.clients_looking_for_rps.remove(client)
        client.connection.send(rsa.encrypt("CLOSE_RPS#".encode('UTF-8'), client.public_key))
        client.game_phrase = ""

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