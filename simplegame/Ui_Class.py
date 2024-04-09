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
        self.grid_columnconfigure((1,2,3), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # widgets
        self.side_bar = Sidebar(self)
        self.main = Main(self)

        self.mainloop()

class Sidebar(customtkinter.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)

        # sidebar grid layout
        #self.sidebar_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0)
        self.grid(row=0, column=0, rowspan=4, sticky="nsew")
        
        self.make_widgets()

    def make_widgets(self):
        # Create Label widget
        header = customtkinter.CTkLabel(self, text="Games", font=customtkinter.CTkFont(size=20, weight="bold"))
        
        # Create button widgets
        sidebar_button_1 = customtkinter.CTkButton(self, command=self.sidebar_button1_event)
        sidebar_button_1.configure(text="Rock, Paper, Scissors")   
        sidebar_button_2 = customtkinter.CTkButton(self, command=self.sidebar_button2_event)
        sidebar_button_2.configure(state="disabled", text="More games soon")

        # Placing widgets
        header.grid(row=0, column=0, padx=20, pady=(20, 10))
        sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

    def sidebar_button1_event(self):
        print("sidebar_button1 click")
    def sidebar_button2_event(self):
        print("sidebar_button2 click")

class Main(customtkinter.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.grid(row=0, column=1, rowspan = 3, columnspan=4,sticky="nsew")
        self.make_widgets()

    def make_widgets(self):
        # Creating widgets
        entry = customtkinter.CTkEntry(self, placeholder_text="Type your message here")
        main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        main_button_1.configure(text="Send")
        textbox = customtkinter.CTkTextbox(self, width=250)
        textbox.insert("0.0", "Textbox")

        # Placing widgets
        entry.grid(row=3, column=1, columnspan=3, padx=(20, 0), pady=(20, 20), sticky="nsew")
        main_button_1.grid(row=3, column=4, padx=(20, 20), pady=(20, 20), sticky="nsew")
        textbox.grid(row=0, column=1, columnspan=4, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")

Game_Ui("Simple Game", (600,500))