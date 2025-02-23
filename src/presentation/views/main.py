import customtkinter as ctk  # type: ignore
from src.presentation.widgets.tkinter_app_widgets import TkinterApp
from src.presentation.controllers.ProductController import ProductController
from src.infrastructure.JsonProductRepository import JsonProductRepository

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

        # Initialize the JSON product repository
        self.product_repository = JsonProductRepository('../../infrastructure/data/products.json')

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