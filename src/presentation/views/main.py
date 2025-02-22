import customtkinter as ctk  # type: ignore
from src.presentation.widgets.tkinter_app_widgets import TkinterApp
from src.presentation.controllers.ProductController import ProductController
from src.infrastructure.JsonProductRepository import JsonProductRepository

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Product Management")

        self.product_repository = JsonProductRepository('../../infrastructure/data/products.json')
        self.product_controller = ProductController(self.product_repository)
        self.app = TkinterApp(self, self.product_controller)

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()