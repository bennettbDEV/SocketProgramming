import socket
import threading

def acceptConnections():
    '''
    Accepts connections, requests the inputed name from the client.
    Adds the connection and name to list of known clients.
    Starts thread with connection to client to recieve messages from them.
    '''
    while True:
        (conn, addr) = s.accept()
        print(f"{addr} connected")

        conn.send("Return_Name".encode('UTF-8'))
        name = conn.recv(1024).decode('UTF-8')

        names.append(name)
        clients.append(conn)

        conn.send("Connection to server successful\n".encode('UTF-8'))
        sendMsg(f"{name} joined the chatroom\n")
        
        thread = threading.Thread(target=recieveMsg,args=(conn,))
        thread.start()

### Add encryption for both sending and recieving msgs
def sendMsg(message):
    '''
    Takes in message to be sent
    then encodes the message and sends it to all clients.
    '''
    for client in clients:
        client.send(message.encode('UTF-8'))
def recieveMsg(client):
    while True:
        try:
            msg = client.recv(1024).decode('UTF-8')
            fmt_msg = f"{names[clients.index(client)]}: {msg}"
            print(fmt_msg)
            sendMsg(fmt_msg+"\n")
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            names.remove(name)
            break

def choose_hand(input):
    if input == "rock" or input == "r":
        return 0
    elif input == "paper" or input == "p":
        return 1
    elif input == "scissors" or input == "s":
        return 2
    else:
        return -1
def game_turn(hand1,hand2):
    if hand1 == 0:
        if hand2 == 0:
            return "Tie"
        elif hand2 == 1:
            return "Player2 wins"
        else:
            return "Player1 wins"
    elif hand1 == 1:
        if hand2 == 0:
            return "Player1 wins"
        elif hand2 == 1:
            return "Tie"
        else:
            return "Player2 wins"
    else:
        if hand2 == 0:
            return "Player1 wins"
        elif hand2 == 1:
            return "Tie"
        else:
            return "Player2 wins"
def play_game(conn):

    sendMsg(conn,"Play rock paper scissors? Answer Y/N")
    firstmessage = recieveMsg(conn)
    print("Client msg: " + firstmessage)
            
    if firstmessage.lower() in ('y','yes','sure','ok','yeah'):
        print("Game started")
        print("You are Player1")
        sendMsg(conn,"You are Player2. Enter 'rock', 'paper', or 'scissors'")
        player1_hand = input("Enter 'rock', 'paper', or 'scissors'")
                
        while choose_hand(player1_hand) not in range(3):
            print("Invalid input,")
            sendMsg(conn, "Waiting for Player1 to choose")
            player1_hand = input("Enter 'rock', 'paper', or 'scissors'")
        player2_hand = recieveMsg(conn)
        
        while choose_hand(player2_hand) not in range(3):
            sendMsg(conn, "Invalid input")
            player2_hand = recieveMsg(conn)
        hands = ("Player1 chose: " + player1_hand + " and Player2 chose: " + player2_hand + ". ")
        result = game_turn(choose_hand(player1_hand),choose_hand(player2_hand))
                    
        print(hands + "\n" + result)
        # Sending -1 at the end of a message indicates the client doesn't need to send another message
        sendMsg(conn, (hands + result + "-1"))
    return True



HOST = socket.gethostname()  # The server's hostname or IP address
PORT = 8888  # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
        
s.bind((HOST,PORT))
s.listen()

#Replace seperate lists for clients and names to a single dictionary/hashtable
clients = []
names = []

acceptConnections()
