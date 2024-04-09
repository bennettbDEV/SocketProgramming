import tkinter as tk
import tkinter.messagebox
import customtkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        self.title("Simple Game")
        
        self.geometry(f"{1080}x{580}")

        # configure grid layout (3x3)
        self.grid_columnconfigure((1,2,3), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Games", font=customtkinter.CTkFont(size=20, weight="bold"))

        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_1.configure(text="Rock, Paper, Scissors")   

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_2.configure(state="disabled", text="More games soon")

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Type your message here")
        self.entry.grid(row=3, column=1, columnspan=3, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=4, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.main_button_1.configure(text="Send")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, columnspan=4, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # set default values
        self.textbox.insert("0.0", "Textbox")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Enter your name:", title="CTkInputDialog")
        print("Username:", dialog.get_input())

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()