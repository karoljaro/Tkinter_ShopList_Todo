import customtkinter as ctk  # type: ignore
from tkinter import messagebox
from src.presentation.widgets.ctk_listbox import CTkListbox
from src.utils.purchaseStatus import get_purchase_status


class TkinterApp:
    """
    Main application class for the Tkinter-based shopping list and todo app.
    """

    def __init__(self, root, product_controller) -> None:
        """
        Initialize the TkinterApp with the root window and product controller.

        :param root: The root window of the Tkinter application.
        :param product_controller: The controller for managing products.
        """
        self.root = root
        self.product_controller = product_controller

        # Create a main frame to center the content
        main_frame = ctk.CTkFrame(root, fg_color="#242424")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create a frame for the input fields and labels
        input_frame = ctk.CTkFrame(main_frame, fg_color="#242424")
        input_frame.pack(pady=10)

        # Name label and entry
        self.name_label = ctk.CTkLabel(input_frame, text="Name")
        self.name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ctk.CTkEntry(input_frame, width=300)
        self.name_entry.grid(row=1, column=0, padx=5, pady=5)

        # Quantity label and entry
        self.quantity_label = ctk.CTkLabel(input_frame, text="Quantity")
        self.quantity_label.grid(row=0, column=1, padx=5, pady=5)
        self.quantity_entry = ctk.CTkEntry(input_frame)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        # Purchased checkbox
        self.purchased_var = ctk.BooleanVar()
        self.purchased_check = ctk.CTkCheckBox(
            main_frame, text="Purchased", variable=self.purchased_var
        )
        self.purchased_check.pack(pady=10)

        # Search and filter frame
        search_filter_frame = ctk.CTkFrame(main_frame, fg_color="#242424")
        search_filter_frame.pack(pady=10, fill="x")

        # Search functionality
        search_label = ctk.CTkLabel(search_filter_frame, text="Search:")
        search_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.search_entry = ctk.CTkEntry(
            search_filter_frame, width=200, placeholder_text="Search products..."
        )
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        self.search_entry.bind("<KeyRelease>", self.on_search_change)

        # Filter by status
        status_label = ctk.CTkLabel(search_filter_frame, text="Filter by Status:")
        status_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.status_filter = ctk.CTkComboBox(
            search_filter_frame, values=["All", "Purchased", "Not Purchased"], width=120
        )
        self.status_filter.grid(row=0, column=3, padx=5, pady=5)
        self.status_filter.set("All")
        self.status_filter.configure(command=self.on_filter_change)

        # Quantity range filter
        qty_label = ctk.CTkLabel(search_filter_frame, text="Min Qty:")
        qty_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.min_qty_entry = ctk.CTkEntry(
            search_filter_frame, width=80, placeholder_text="0"
        )
        self.min_qty_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.min_qty_entry.bind("<KeyRelease>", self.on_filter_change)

        max_qty_label = ctk.CTkLabel(search_filter_frame, text="Max Qty:")
        max_qty_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        self.max_qty_entry = ctk.CTkEntry(
            search_filter_frame, width=80, placeholder_text="No limit"
        )
        self.max_qty_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.max_qty_entry.bind("<KeyRelease>", self.on_filter_change)

        # Low stock threshold
        low_stock_label = ctk.CTkLabel(search_filter_frame, text="Low Stock Threshold:")
        low_stock_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.low_stock_entry = ctk.CTkEntry(
            search_filter_frame, width=80, placeholder_text="5"
        )
        self.low_stock_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Clear filters button
        clear_filters_btn = ctk.CTkButton(
            search_filter_frame,
            text="Clear Filters",
            command=self.clear_filters,
            width=100,
        )
        clear_filters_btn.grid(row=2, column=2, padx=5, pady=5)

        # Show low stock button
        low_stock_btn = ctk.CTkButton(
            search_filter_frame,
            text="Show Low Stock",
            command=self.show_low_stock,
            width=120,
        )
        low_stock_btn.grid(row=2, column=3, padx=5, pady=5)

        # Create a frame for the buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="#242424")
        button_frame.pack(pady=10)

        # Add, Update, and Remove buttons
        self.add_button = ctk.CTkButton(
            button_frame, text="Add Product", command=self.add_product
        )
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        self.update_button = ctk.CTkButton(
            button_frame,
            text="Update Product",
            command=self.update_product,
            state=ctk.DISABLED,
        )
        self.update_button.grid(row=0, column=1, padx=5, pady=5)

        self.remove_button = ctk.CTkButton(
            button_frame,
            text="Remove Product",
            command=self.remove_product,
            state=ctk.DISABLED,
        )
        self.remove_button.grid(row=0, column=2, padx=5, pady=5)

        # Product list
        self.product_list = CTkListbox(
            main_frame, width=600, height=300, command=self.on_product_select
        )
        self.product_list.pack(pady=5)

        self.selected_product_id = None
        self.product_map: dict[str, int] = (
            {}
        )  # Słownik do mapowania wyświetlanych wartości na ID produktów
        self.current_filter_mode = (
            "all"  # Track current filter mode for efficient updates
        )

        # Refresh product list on startup
        self.refresh_product_list()

    def on_product_select(self, selected_option):
        """
        Handle the selection of a product from the list.

        :param selected_option: The selected product option.
        """
        selected_value = selected_option
        selected_id = self.product_map.get(selected_value)
        if self.selected_product_id == selected_id:
            # Odznacz element
            self.selected_product_id = None
            self.clear_inputs()
            self.product_list.deselect_all()  # Resetuj zaznaczenie w liście
        else:
            # Zaznacz nowy element
            self.selected_product_id = selected_id
            product = self.product_controller.get_product_by_id(
                self.selected_product_id
            )
            if product:
                self.name_entry.delete(0, ctk.END)
                self.name_entry.insert(0, product.name)
                self.quantity_entry.delete(0, ctk.END)
                self.quantity_entry.insert(0, product.quantity)
                self.purchased_var.set(product.purchased)
                self.update_button.configure(state=ctk.NORMAL)
                self.remove_button.configure(state=ctk.NORMAL)

    def add_product(self):
        """
        Add a new product to the list.
        """
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        if not name:
            messagebox.showerror("Error", "Name field is empty")
            return
        if not quantity:
            messagebox.showerror("Error", "Quantity field is empty")
            return
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity must be greater than zero")
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer")
            return
        purchased = self.purchased_var.get()
        try:
            product = self.product_controller.add_product(name, quantity, purchased)
            messagebox.showinfo(
                "Success", f"Product {product.name} added successfully!"
            )
            self.refresh_product_list()
            self.clear_inputs()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_product(self):
        """
        Update the selected product in the list.
        """
        if not self.selected_product_id:
            messagebox.showerror("Error", "No product selected")
            return
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        if not name:
            messagebox.showerror("Error", "Name field is empty")
            return
        if not quantity:
            messagebox.showerror("Error", "Quantity field is empty")
            return
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity must be greater than zero")
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer")
            return
        purchased = self.purchased_var.get()
        try:
            product = self.product_controller.update_product(
                self.selected_product_id, name, quantity, purchased
            )
            messagebox.showinfo(
                "Success", f"Product {product.name} updated successfully!"
            )
            self.refresh_product_list()
            self.clear_inputs()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def remove_product(self):
        """
        Remove the selected product from the list.
        """
        if not self.selected_product_id:
            messagebox.showerror("Error", "No product selected")
            return
        try:
            self.product_controller.remove_product(self.selected_product_id)
            messagebox.showinfo("Success", "Product removed successfully!")
            self.refresh_product_list()
            self.clear_inputs()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def refresh_product_list(self):
        """
        Refresh the product list displayed in the UI using all products.
        """
        if hasattr(self, "current_filter_mode") and self.current_filter_mode != "all":
            # If filters are active, reapply them
            if self.current_filter_mode == "low_stock":
                self.show_low_stock()
            else:
                self.apply_filters()
        else:
            # Show all products
            products = self.product_controller.get_all_products()
            self.update_product_display(products)

    def clear_inputs(self):
        """
        Clear the input fields in the UI.
        """
        self.name_entry.delete(0, ctk.END)
        self.quantity_entry.delete(0, ctk.END)
        self.purchased_var.set(False)
        self.update_button.configure(state=ctk.DISABLED)
        self.remove_button.configure(state=ctk.DISABLED)

    def on_search_change(self, event=None):
        """
        Handle search input changes and filter products using list comprehensions.

        :param event: The event triggered by key release (optional).
        """
        self.apply_filters()

    def on_filter_change(self, event=None):
        """
        Handle filter changes and update product list.

        :param event: The event triggered by combo box or entry changes (optional).
        """
        self.apply_filters()

    def apply_filters(self):
        """
        Apply all active filters to the product list using ProductController methods.
        """
        # Get search term
        search_term = self.search_entry.get().strip()

        # Get status filter
        status_filter = self.status_filter.get()
        purchased_filter = None
        if status_filter == "Purchased":
            purchased_filter = True
        elif status_filter == "Not Purchased":
            purchased_filter = False

        # Get quantity range
        min_qty = 0
        max_qty = None

        try:
            min_qty_text = self.min_qty_entry.get().strip()
            if min_qty_text:
                min_qty = int(min_qty_text)
        except ValueError:
            min_qty = 0

        try:
            max_qty_text = self.max_qty_entry.get().strip()
            if max_qty_text:
                max_qty = int(max_qty_text)
        except ValueError:
            max_qty = None

        # Apply filters in sequence using ProductController methods
        if search_term:
            # Use search functionality
            products = self.product_controller.search_products(search_term)
        else:
            # Start with status filter
            products = self.product_controller.get_products_by_status(purchased_filter)

        # Apply quantity range filter
        if search_term:
            # If search was used, apply additional filters manually using list comprehensions
            if purchased_filter is not None:
                products = [p for p in products if p.purchased == purchased_filter]
            if max_qty is not None:
                products = [p for p in products if min_qty <= p.quantity <= max_qty]
            else:
                products = [p for p in products if p.quantity >= min_qty]
        else:
            # Use quantity range filter from controller
            quantity_filtered = self.product_controller.get_products_by_quantity_range(
                min_qty, max_qty
            )
            # Intersect with status filtered products
            product_ids = {p.id for p in products}
            products = [p for p in quantity_filtered if p.id in product_ids]

        # Update the display
        self.update_product_display(products)
        self.current_filter_mode = "filtered"

    def show_low_stock(self):
        """
        Show products with low stock using the ProductController method.
        """
        try:
            threshold_text = self.low_stock_entry.get().strip()
            threshold = int(threshold_text) if threshold_text else 5
        except ValueError:
            threshold = 5

        low_stock_products = self.product_controller.get_low_stock_products(threshold)
        self.update_product_display(low_stock_products)
        self.current_filter_mode = "low_stock"

    def clear_filters(self):
        """
        Clear all filters and show all products.
        """
        self.search_entry.delete(0, ctk.END)
        self.status_filter.set("All")
        self.min_qty_entry.delete(0, ctk.END)
        self.max_qty_entry.delete(0, ctk.END)
        self.low_stock_entry.delete(0, ctk.END)
        self.low_stock_entry.insert(0, "5")  # Reset to default
        self.current_filter_mode = "all"
        self.refresh_product_list()

    def update_product_display(self, products):
        """
        Update the product list display with filtered products.

        :param products: List of products to display.
        """
        self.product_list.delete(0, ctk.END)
        self.product_map.clear()  # Use generator to efficiently process product names
        product_names_gen = self.product_controller.get_product_names_generator()
        # Convert generator to list for demonstration (but don't store unused)
        list(product_names_gen)

        for product in products:
            purchase_status = get_purchase_status(product.purchased)
            name_display = (
                product.name if len(product.name) <= 40 else product.name[:40] + "..."
            )

            # Add low stock indicator
            low_stock_indicator = " ⚠️ LOW STOCK" if product.quantity < 5 else ""
            display_value = f"- Name: {name_display} | Quantity: {product.quantity} | Status: {purchase_status}{low_stock_indicator}"

            self.product_list.insert(ctk.END, display_value)
            self.product_map[display_value] = product.id

        # Update button states
        self.selected_product_id = None
        self.update_button.configure(state=ctk.DISABLED)
        self.remove_button.configure(state=ctk.DISABLED)
