import customtkinter as ctk # type: ignore
from tkinter import Misc

class ListEntry(ctk.CTkEntry):
    def __init__(self, master: Misc, **kwargs):
        super().__init__(master, **kwargs)

        self.bind("<Return>", self.onEnter)

    def onEnter(self, *args):
        print("enter")