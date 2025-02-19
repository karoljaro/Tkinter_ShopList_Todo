import tkinter as tk
from src.presentation.tkinter.tkinter_app import TkinterApp
from src.presentation.controllers.ProductController import ProductController
from src.infrastructure.JsonProductRepository import JsonProductRepository

def main():
    root = tk.Tk()
    product_repository = JsonProductRepository('src/infrastructure/data/products.json')
    product_controller = ProductController(product_repository)
    app = TkinterApp(root, product_controller)
    root.mainloop()

if __name__ == "__main__":
    main()