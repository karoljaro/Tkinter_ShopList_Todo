import tkinter as ttk
from tkinter import Misc
import customtkinter as ctk # type: ignore

class Body_layout(ttk.Frame):
    def __init__(self, parent: Misc):
        super().__init__(parent, width=400, height=400, background="black")
        self.pack_propagate(False)

        self.btn = ctk.CTkButton(self, text="Click me", command=self.onClick)

        self.btn.pack()
        self.pack()

    def onClick(self):
        print('Click')
