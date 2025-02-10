from tkinter import Misc
import customtkinter as ctk # type: ignore

class SubmitBtn(ctk.CTkButton):
    def __init__(self, master: Misc, **kwargs):
        super().__init__(master, text="Dodaj", command=self.onSubmit, **kwargs)
        self.configure(state="disabled")
    def onSubmit(self):
        print("Submit btn")



