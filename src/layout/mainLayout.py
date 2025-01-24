import tkinter as ttk
from tkinter import Misc
from layout.inputWrapper import InputWrapper

class Body_layout(ttk.Frame):
    def __init__(self, master: Misc):
        # Body_layout config
        super().__init__(master, width=400, height=400, background="red")
        self.pack_propagate(False)

        self.rowconfigure((0, 1), weight=1, uniform='a')
        self.columnconfigure(0, weight=1)

        self.pack(expand=True, fill='both')

        input_wrapper = InputWrapper(self)
        input_wrapper.grid(column=0, row=0, sticky="news")

        
        