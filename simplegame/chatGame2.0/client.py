import socket
import threading
import time
import rsa
import UIClass


HOST = "####.####.####.####"  # The server's hostname or IP address
PORT = 8888  # The port used by the server

class Client:
    def __init__(self, host, port):
        self.ui = UIClass.UIClass("Chat",(500,400))
        self.name = self.ui.username

        # generate pub/priv keys for encrpytion
        self.pub_key, self.priv_key = rsa.newkeys(1024)
        self.server_pub = None

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
        self.s.connect((host,port))

        # exchange public keys
        self.server_pub = rsa.PublicKey.load_pkcs1(self.s.recv(1024))
        self.s.send(self.pub_key.save_pkcs1("PEM"))

        self.running = True
        self.rps_running = False

        self.ui.protocol("WM_DELETE_WINDOW", self.stop)

        # additional threads to allow sending + recieving at same time
        recieve_thread = threading.Thread(target=self.recieve_msg)
        send_thread = threading.Thread(target=self.send_msg)
        
        recieve_thread.start()
        send_thread.start()
        self.run_gui()
        
    def run_gui(self):
        self.ui.start_chatBox()

    def recieve_msg(self):
        while self.running:
            try:
                msg = rsa.decrypt(self.s.recv(1024), self.priv_key).decode('UTF-8')
                # Maybe use RPyC here...
                if msg == "Return_Name":
                    self.s.send(rsa.encrypt(self.name.encode('UTF-8'), self.server_pub))
                elif msg == "OPEN_RPS#":
                    self.rps_running = True
                    self.ui.start_rps()
                elif msg == "CLOSE_RPS#":
                    self.rps_running = False
                    self.ui.stop_rps()
                else:
                    self.ui.main.write_msg(msg)
            except ConnectionAbortedError:
                break
            except:
                self.stop()
                break
                    
    def send_msg(self):
        while self.running:
            time.sleep(.10)
            if(self.ui.main.queued):
                msg = self.ui.main.entry_text
                self.s.send(rsa.encrypt(msg.encode('UTF-8'), self.server_pub))
                self.ui.main.queued = False
            elif(self.ui.side_bar.queued):
                msg = self.ui.side_bar.game_choice
                self.s.send(rsa.encrypt(msg.encode('UTF-8'), self.server_pub))
                self.ui.side_bar.queued = False
            elif(self.rps_running and self.ui.rps.queued):
                msg = self.ui.rps.hand
                self.s.send(rsa.encrypt(msg.encode('UTF-8'), self.server_pub))
                self.ui.rps.queued = False

    def stop(self):
        self.running = False
        self.ui.destroy()
        self.s.close()
        exit(0)

Client(HOST,PORT)
