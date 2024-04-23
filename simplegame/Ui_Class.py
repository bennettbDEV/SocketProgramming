import tkinter as tk
import tkinter.messagebox
import customtkinter

class Game_Ui(customtkinter.CTk):
    def __init__(self, title, size):

        # main setup
        super().__init__()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(size[0],size[1])

        # main grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)

        self.grid_rowconfigure(0, weight=1)

        # widgets
        #self.popup = Popup(self)
        self.side_bar = Sidebar(self)
        self.main = Main(self)

        self.mainloop()
    
    def start_dialog(self):
        '''
        Will create a popup object, which asks the user for their name
        and will return the String result.
        '''
        pass 
    def start_rps(self):
        '''
        Will create a Rockpaperscissors object, which has an additional window for the game
        '''
        pass 
    def receive_msg(self):
        '''
        Takes in a string message and adds a chat message to the main text box
        '''
        pass
    def send_msg(self):
        '''
        Takes in a string to send to other users
        '''
        pass

    
class Popup(customtkinter.CTkInputDialog):
    '''
    still needs funtionality
    '''
    def __init__(self, parent):
        super().__init__(parent)
        self.open_input_dialog_event()
        
    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Enter your name:", title="CTkInputDialog")
        print("Username:", dialog.get_input())
        self.quit()      

class Sidebar(customtkinter.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)
        # sidebar grid layout
        sidebar_frame = customtkinter.CTkFrame(parent, width=100, corner_radius=0)

        # Placing the sidebar at (0,0)
        sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.make_widgets(sidebar_frame)

    def make_widgets(self, sidebar_frame):
        # Create Label widget
        header = customtkinter.CTkLabel(sidebar_frame, text="Games", font=customtkinter.CTkFont(size=20, weight="bold"))
        
        # Create button widgets
        sidebar_button_1 = customtkinter.CTkButton(sidebar_frame, command=self.sidebar_button1_event)
        sidebar_button_1.configure(text="Rock, Paper, Scissors")   
        sidebar_button_2 = customtkinter.CTkButton(sidebar_frame, command=self.sidebar_button2_event)
        sidebar_button_2.configure(state="disabled", text="More games soon")

        # Placing widgets
        header.pack(pady = (5,15))
        sidebar_button_1.pack(pady = 6)
        sidebar_button_2.pack(pady = 6)

    def sidebar_button1_event(self):
        print("sidebar_button1 click")
    def sidebar_button2_event(self):
        print("sidebar_button2 click")

class Main(customtkinter.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        main_frame = customtkinter.CTkFrame(parent, width=100, corner_radius=0)
        main_frame.grid(row=0, column=1, sticky="nsew")

        main_frame.grid_columnconfigure(0, weight=6)
        main_frame.grid_columnconfigure(1, weight=1)

        main_frame.grid_rowconfigure(0, weight=6)
        main_frame.grid_rowconfigure(1, weight=1)

        self.make_widgets(main_frame)

    def make_widgets(self, main_frame):
        
        # Creating widgets
        entry = customtkinter.CTkEntry(main_frame, placeholder_text="Type your message here...")
        main_button_1 = customtkinter.CTkButton(master=main_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        main_button_1.configure(text="Send")
        textbox = customtkinter.CTkTextbox(main_frame, width=250)
        textbox.insert("0.0", "Textbox")

        # Placing widgets
        entry.grid(row=1, column=0, padx=(20, 0), pady=5, sticky = "we")
        main_button_1.grid(row=1, column=1, padx=(20, 20), pady=5)
        textbox.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="nsew")



Game_Ui("Simple Game", (600,500))