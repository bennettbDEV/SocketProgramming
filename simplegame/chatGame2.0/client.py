import socket
import threading
import time
import UIClass


HOST = "###.###.###.###"  # The server's hostname or IP address
PORT = 8888  # The port used by the server

class Client:
    def __init__(self, host, port):
        self.ui = UIClass.UIClass("chat",(500,400))
        self.name = self.ui.username

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
        self.s.connect((host,port))
        self.running = True

        self.ui.protocol("WM_DELETE_WINDOW", self.stop)

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
                msg = self.s.recv(1024).decode('UTF-8')
                # Replace the "return name" to get clients name with RPyC 
                if msg == "Return_Name":
                    self.s.send(self.name.encode('UTF-8'))
                else:
                    self.ui.main.write_msg(msg)
            except ConnectionAbortedError:
                break
            except:
                self.stop()
                break
                    
    def send_msg(self):
        while self.running:
            time.sleep(.25)
            if(self.ui.main.queued):
                msg = self.ui.main.entry_text
                self.s.send(msg.encode('UTF-8'))
                self.ui.main.queued = False

    def stop(self):
        self.running = False
        self.ui.destroy()
        self.s.close()
        exit(0)

Client(HOST,PORT)
