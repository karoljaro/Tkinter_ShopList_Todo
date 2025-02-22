import customtkinter as ctk # type: ignore
from src.presentation.widgets.tkinter_app_widgets import TkinterApp
from src.presentation.controllers.ProductController import ProductController
from src.infrastructure.JsonProductRepository import JsonProductRepository

def main():
    root = ctk.CTk()
    product_repository = JsonProductRepository('../../infrastructure/data/products.json')
    product_controller = ProductController(product_repository)
    app = TkinterApp(root, product_controller)
    root.mainloop()

if __name__ == "__main__":
    main()