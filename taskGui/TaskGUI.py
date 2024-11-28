from tkinter import Frame
from tkinter.ttk import Combobox


class TaskGUI:
    def __init__(self, main):
        self.main = main
        main.title("Task GUI")
        self.main.geometry("1280x720")

        # Frame
        self.frame = Frame(self.main, background="gray24")
        self.frame.pack(fill="both", expand=True)

        # Create Combobox
        self.cmb= Combobox(self.frame, values=("Vali kujund", "Ring", "Ristkülik"))
        self.cmb.current(0) # vali kujund
        self.cmb["state"] = "readonly"
        self.cmb.grid(row=0, column=0,padx=5, pady=5, columnspan=5,sticky="ew")
