import tkinter as ttk
from tkinter import Misc
from widgets import ListEntry

class Body_layout(ttk.Frame):
    def __init__(self, master: Misc):
        # Body_layout config
        super().__init__(master, width=400, height=400, background="#242424")
        self.pack_propagate(False)
        self.rowconfigure((0, 1), weight=1, uniform='a')
        self.columnconfigure(0, weight=1)
        self.pack(expand=True, fill='both')

        # Widgets
        ListEntry(self).pack()