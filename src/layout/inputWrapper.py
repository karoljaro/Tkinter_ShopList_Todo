import tkinter as ttk
from tkinter import Misc
from widgets import ListEntry, SubmitBtn

class InputWrapper(ttk.Frame):
    def __init__(self, parent: Misc):
        super().__init__(parent, background='#242424',)

        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=1, uniform="a")
        self.columnconfigure(0, weight=2, uniform="a")

        ListEntry(self).grid(column=0, row=0, sticky="news", padx=(0, 10))
        SubmitBtn(self).grid(column=1, row=0)

        