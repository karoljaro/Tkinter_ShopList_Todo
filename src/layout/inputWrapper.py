import tkinter as ttk
from tkinter import Misc, StringVar, IntVar
from widgets import ListEntry, SubmitBtn, QuantityEntry

class InputWrapper(ttk.Frame):
    def __init__(self, parent: Misc):
        super().__init__(parent, background='#242424')

        # Grid config
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure(0, weight=2, uniform="a")
        self.columnconfigure(1, weight=2, uniform="a")
        self.columnconfigure(2, weight=1, uniform="a")

        self.entry_var = StringVar()
        self.entry_var.trace_add("write", self.inputValid)

        self.quantity_var = IntVar()
        self.quantity_var.trace_add("write", self.inputValid)

        ListEntry(self, textvariable=self.entry_var).grid(column=0, row=0, sticky="news", padx=(0, 10))
        QuantityEntry(self, width=150, step_size=1).grid(column=1, row=0, sticky="news", padx=(0,10))
        
        self.submit_btn = SubmitBtn(self)
        self.submit_btn.grid(column=2, row=0)

        


    def inputValid(self, *args):
        print(self.winfo_width())
        self.submit_btn.configure(state="normal" if self.entry_var.get().strip() and self.quantity_var.get() >= 0 else "disabled")
        