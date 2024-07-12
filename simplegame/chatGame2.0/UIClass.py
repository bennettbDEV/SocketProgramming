import customtkinter
from tkinter import StringVar

class UIClass(customtkinter.CTk):
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
        self.username = self.start_dialog()
        
        self.side_bar = Sidebar(self)
        self.main = Main(self)
        self.rps = None
        #self.destroy()

    def start_dialog(self):
        '''
        Will create a popup object, which asks the user for their name
        and will return the String result.
        '''
        # Eventually, override the _cancel_event, and _on_closing functions to terminate the entire program
        dialog = customtkinter.CTkInputDialog(text="Enter your name:", title="Login")
        username = dialog.get_input()
        self.quit()  
        return username
    
    def start_chatBox(self):
        self.mainloop()
    
    def start_rps(self):
        '''
        Will create a Rockpaperscissors object, which has an additional window for the game
        '''
        
        self.main.entry.configure(state="disabled")
        self.side_bar.rps_button.configure(state="disabled")   
        if self.rps is None or not self.rps.winfo_exists():
            self.rps = RockPaperScissors()  # create window if its None or destroyed
        else:
            self.rps.focus()  # if window exists focus it

    
class Sidebar(customtkinter.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)
        # sidebar grid layout
        sidebar_frame = customtkinter.CTkFrame(parent, width=100, corner_radius=0)

        # Placing the sidebar at (0,0)
        sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.make_widgets(sidebar_frame)

        self.queued = False
        self.game_choice = ""

    def make_widgets(self, sidebar_frame):
        # Create Label widget
        header = customtkinter.CTkLabel(sidebar_frame, text="Games", font=customtkinter.CTkFont(size=20, weight="bold"))
        
        # Create button widgets
        self.rps_button = customtkinter.CTkButton(sidebar_frame, command=self.rps_button_event)
        self.rps_button.configure(text="Rock, Paper, Scissors")   
        sidebar_button_2 = customtkinter.CTkButton(sidebar_frame, command=self.sidebar_button2_event)
        sidebar_button_2.configure(state="disabled", text="More games soon")

        # Placing widgets
        header.pack(pady = (5,15))
        self.rps_button.pack(pady = 6)
        sidebar_button_2.pack(pady = 6)

    def rps_button_event(self):
        self.game_choice="INITIATE_RPS#"
        self.queued = True

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

        self.entry = customtkinter.CTkEntry(main_frame, placeholder_text="Type your message here...")
        self.textbox = customtkinter.CTkTextbox(main_frame, width=250)

        self.queued = False
        self.entry_text = ""

        self.make_widgets(main_frame)

    def make_widgets(self, main_frame):
        
        # Creating widgets
        main_button_1 = customtkinter.CTkButton(master=main_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.send_entry)
        main_button_1.configure(text="Send")

        #self.textbox.insert("0.0", "!")
        self.textbox.configure(state="disabled")

        # Placing widgets
        self.entry.grid(row=1, column=0, padx=(20, 0), pady=5, sticky = "we")
        main_button_1.grid(row=1, column=1, padx=(20, 20), pady=5)
        self.textbox.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="nsew")

    def send_entry(self):
        self.entry_text = self.entry.get()
        self.queued = True
        self.entry.delete(0, "end")

    def write_msg(self, text):
        self.textbox.configure(state="normal")
        self.textbox.insert("end",text)
        self.textbox.yview("end")
        self.textbox.configure(state="disabled")

class RockPaperScissors(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("400x200")
        self.minsize(400,200)
        self.maxsize(400,200)
        self.title("Rock Paper Scissors")
        
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0,2), weight=1)
        self.grid_rowconfigure(1, weight=2)

        self.queued = False
        self.hand = ""

        self.string_result = StringVar(master=self, value="")
        self.make_widgets()
        
    def make_widgets(self):

        self.title = customtkinter.CTkLabel(self, text="Select your hand", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.results = customtkinter.CTkLabel(self, textvariable=self.string_result, font=customtkinter.CTkFont(size=14, weight="bold"))

        self.rock_button = customtkinter.CTkButton(self, text="Rock", command=self.rock_button_callbck)
        self.paper_button = customtkinter.CTkButton(self, text="Paper", command=self.paper_button_callbck)
        self.scissors_button = customtkinter.CTkButton(self, text="Scissors", command=self.scissors_button_callbck)
        
        self.title.grid(row=0,column=0,columnspan=3)
        self.results.grid(row=2,column=0,columnspan=3)

        self.rock_button.grid(row=1,column=0,padx=(20,10), pady=1)
        self.paper_button.grid(row=1,column=1,padx=10, pady=1)
        self.scissors_button.grid(row=1,column=2,padx=(10,20), pady=1)

    def rock_button_callbck(self):
        self.hand = "Rock"
        self.queued = True
    def paper_button_callbck(self):
        self.hand = "Paper"
        self.queued = True
    def scissors_button_callbck(self):
        self.hand = "Scissors"
        self.queued = True
    