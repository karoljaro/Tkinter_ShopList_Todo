import customtkinter as ctk  # type: ignore
from src.presentation.widgets.tkinter_app_widgets import TkinterApp
from src.presentation.controllers.ProductController import ProductController
from src.infrastructure.JsonProductRepository import JsonProductRepository
import os

class MainApp(ctk.CTk):
    """
    Main application class for the Tkinter-based product management app.
    """
    def __init__(self):
        """
        Initialize the MainApp with the necessary components.
        """
        super().__init__()
        self.title("Product Management")
        self.minsize(640, 600)

        # Set the application icon
        icon_path = os.path.join(os.path.dirname(__file__), '../../../assets/icon.ico')
        self.iconbitmap(icon_path)

        # Initialize the JSON product repository
        file_path = os.path.join(os.path.dirname(__file__), '../../infrastructure/data/products.json')
        self.product_repository = JsonProductRepository(file_path)

        # Initialize the product controller
        self.product_controller = ProductController(self.product_repository)

        # Initialize the TkinterApp with the root window and product controller
        self.app = TkinterApp(self, self.product_controller)

    def run(self):
        """
        Run the Tkinter main loop.
        """
        self.mainloop()

if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()