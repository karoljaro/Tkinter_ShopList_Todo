from tkinter import Misc
import customtkinter as ctk # type: ignore

class SubmitBtn(ctk.CTkButton):
    def __init__(self, master: Misc):
        super().__init__(master, text="Submit", command=self.onSubmit)

    def onSubmit(self):
        print("Submit btn")
