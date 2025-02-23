import customtkinter as ctk  # type: ignore
from tkinter import messagebox
from src.presentation.widgets.ctk_listbox import CTkListbox
from src.utils.purchaseStatus import get_purchase_status

class TkinterApp:
    def __init__(self, root, product_controller) -> None:
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
        self.purchased_check = ctk.CTkCheckBox(main_frame, text="Purchased", variable=self.purchased_var)
        self.purchased_check.pack(pady=10)

        # Create a frame for the buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="#242424")
        button_frame.pack(pady=10)

        # Add, Update, and Remove buttons
        self.add_button = ctk.CTkButton(button_frame, text="Add Product", command=self.add_product)
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        self.update_button = ctk.CTkButton(button_frame, text="Update Product", command=self.update_product, state=ctk.DISABLED)
        self.update_button.grid(row=0, column=1, padx=5, pady=5)

        self.remove_button = ctk.CTkButton(button_frame, text="Remove Product", command=self.remove_product, state=ctk.DISABLED)
        self.remove_button.grid(row=0, column=2, padx=5, pady=5)

        # Product list
        self.product_list = CTkListbox(main_frame, width=600, height=300, command=self.on_product_select)
        self.product_list.pack(pady=5)

        self.selected_product_id = None
        self.product_map = {}  # Słownik do mapowania wyświetlanych wartości na ID produktów

        # Refresh product list on startup
        self.refresh_product_list()

    def on_product_select(self, selected_option):
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
            product = self.product_controller.get_product_by_id(self.selected_product_id)
            if product:
                self.name_entry.delete(0, ctk.END)
                self.name_entry.insert(0, product.name)
                self.quantity_entry.delete(0, ctk.END)
                self.quantity_entry.insert(0, product.quantity)
                self.purchased_var.set(product.purchased)
                self.update_button.configure(state=ctk.NORMAL)
                self.remove_button.configure(state=ctk.NORMAL)

    def add_product(self):
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
            messagebox.showinfo("Success", f"Product {product.name} added successfully!")
            self.refresh_product_list()
            self.clear_inputs()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_product(self):
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
            product = self.product_controller.update_product(self.selected_product_id, name, quantity, purchased)
            messagebox.showinfo("Success", f"Product {product.name} updated successfully!")
            self.refresh_product_list()
            self.clear_inputs()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def remove_product(self):
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
        self.product_list.delete(0, ctk.END)
        self.product_map.clear()  # Wyczyść mapowanie
        products = self.product_controller.get_all_products()
        for product in products:
            purchase_status = get_purchase_status(product.purchased)
            name_display = product.name if len(product.name) <= 40 else product.name[:40] + "..."
            display_value = f"- Name: {name_display} | Quantity: {product.quantity} | Status: {purchase_status}"
            self.product_list.insert(ctk.END, display_value)
            self.product_map[display_value] = product.id  # Mapuj wyświetlaną wartość na ID produktu
        self.selected_product_id = None
        self.update_button.configure(state=ctk.DISABLED)
        self.remove_button.configure(state=ctk.DISABLED)

    def clear_inputs(self):
        self.name_entry.delete(0, ctk.END)
        self.quantity_entry.delete(0, ctk.END)
        self.purchased_var.set(False)
        self.update_button.configure(state=ctk.DISABLED)
        self.remove_button.configure(state=ctk.DISABLED)