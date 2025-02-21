import customtkinter as ctk  # type: ignore
from tkinter import messagebox
from CTkListbox import CTkListbox  # type: ignore

class TkinterApp:
    def __init__(self, root, product_controller):
        self.root = root
        self.product_controller = product_controller
        self.root.title("Product Management")

        self.name_label = ctk.CTkLabel(root, text="Name")
        self.name_label.pack(pady=5)
        self.name_entry = ctk.CTkEntry(root)
        self.name_entry.pack(pady=5)

        self.quantity_label = ctk.CTkLabel(root, text="Quantity")
        self.quantity_label.pack(pady=5)
        self.quantity_entry = ctk.CTkEntry(root)
        self.quantity_entry.pack(pady=5)

        self.purchased_var = ctk.BooleanVar()
        self.purchased_check = ctk.CTkCheckBox(root,text="Purchased", variable=self.purchased_var)
        self.purchased_check.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Add Product", command=self.add_product)
        self.add_button.pack(pady=5)

        self.update_button = ctk.CTkButton(root, text="Update Product", command=self.update_product)
        self.update_button.pack(pady=5)

        self.remove_button = ctk.CTkButton(root, text="Remove Product", command=self.remove_product)
        self.remove_button.pack(pady=5)

        self.product_list = CTkListbox(root, width=400, command=self.on_product_select)
        self.product_list.pack(pady=5)

        self.selected_product_id = None

        # Refresh product list on startup
        self.refresh_product_list()

    def on_product_select(self, selected_option):
        self.selected_product_id = selected_option.split()[0]

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
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer")
            return
        purchased = self.purchased_var.get()
        try:
            product = self.product_controller.add_product(name, quantity, purchased)
            messagebox.showinfo("Success", f"Product {product.name} added successfully!")
            self.refresh_product_list()
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
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer")
            return
        purchased = self.purchased_var.get()
        try:
            product = self.product_controller.update_product(self.selected_product_id, name, quantity, purchased)
            messagebox.showinfo("Success", f"Product {product.name} updated successfully!")
            self.refresh_product_list()
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
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def refresh_product_list(self):
        self.product_list.delete(0, ctk.END)
        products = self.product_controller.get_all_products()
        for product in products:
            self.product_list.insert(ctk.END, f"{product.id} {product.name} {product.quantity} {product.purchased}")
        self.selected_product_id = None