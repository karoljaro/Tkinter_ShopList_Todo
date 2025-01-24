import customtkinter as ctk # type: ignore
from tkinter import Misc

class ListEntry(ctk.CTkEntry):
    def __init__(self, master: Misc):
        super().__init__(master)