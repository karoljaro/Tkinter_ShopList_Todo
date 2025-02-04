import customtkinter as ctk # type: ignore
from layout import Body_layout

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._set_appearance_mode("dark")

        # create and config window
        self.create_window()
        Body_layout(self).place(relx=0.5, rely=0.5, anchor="center")

        # run app
        self.mainloop()

    def create_window(self) -> None:
        self.title("Tkinter ShopList Todo")
        self.geometry("800x600")

if __name__ == '__main__':
    App()
