import socket

def recieveMsg(connection):
    '''
    Takes in connection socket and recieves message from client
    Returns the text recieved as a string
    if recieving data fails, returns "Invalid input"
    
    '''
    data = connection.recv(1024)
    if not data:
        return "Invalid input"
    return (str(data)[2:-1])
def sendMsg(connection, message):
    '''
    Takes in connection socket and the message to be sent
    '''
    connection.sendall((message).encode('UTF-8'))
    
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
def play_game(connection):
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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM ) as s:
    
    s.bind((HOST,PORT))
    s.listen()
    (conn, addr) = s.accept()
    with conn:
        print(f"{addr} connected")
        sendMsg(conn, "Send 'game' at anytime to initite the game")
        while True:
            recieved_message = recieveMsg(conn)
            if recieved_message == "game":
                play_game(conn)
            print("Client: " + recieved_message)
            message = input()
            sendMsg(conn,message)
                                
        s.close()
        