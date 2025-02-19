import tkinter as tk
from tkinter import messagebox
from src.presentation.controllers.ProductController import ProductController

class TkinterApp:
    def __init__(self, root, product_controller):
        self.root = root
        self.product_controller = product_controller
        self.root.title("Product Management")

        self.name_label = tk.Label(root, text="Name")
        self.name_label.pack()
        self.name_entry = tk.Entry(root)
        self.name_entry.pack()

        self.quantity_label = tk.Label(root, text="Quantity")
        self.quantity_label.pack()
        self.quantity_entry = tk.Entry(root)
        self.quantity_entry.pack()

        self.purchased_label = tk.Label(root, text="Purchased")
        self.purchased_label.pack()
        self.purchased_var = tk.BooleanVar()
        self.purchased_check = tk.Checkbutton(root, variable=self.purchased_var)
        self.purchased_check.pack()

        self.add_button = tk.Button(root, text="Add Product", command=self.add_product)
        self.add_button.pack()

        self.update_button = tk.Button(root, text="Update Product", command=self.update_product)
        self.update_button.pack()

        self.remove_button = tk.Button(root, text="Remove Product", command=self.remove_product)
        self.remove_button.pack()

        self.list_button = tk.Button(root, text="List Products", command=self.list_products)
        self.list_button.pack()

        self.product_list = tk.Listbox(root, width=150)
        self.product_list.pack()

    def add_product(self):
        name = self.name_entry.get()
        quantity = int(self.quantity_entry.get())
        purchased = self.purchased_var.get()
        try:
            product = self.product_controller.add_product(name, quantity, purchased)
            messagebox.showinfo("Success", f"Product {product.name} added successfully!")
            self.refresh_product_list()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_product(self):
        selected_product = self.product_list.get(tk.ACTIVE)
        if not selected_product:
            messagebox.showerror("Error", "No product selected")
            return
        product_id = selected_product.split()[0]
        name = self.name_entry.get()
        quantity = int(self.quantity_entry.get())
        purchased = self.purchased_var.get()
        try:
            product = self.product_controller.update_product(product_id, name, quantity, purchased)
            messagebox.showinfo("Success", f"Product {product.name} updated successfully!")
            self.refresh_product_list()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def remove_product(self):
        selected_product = self.product_list.get(tk.ACTIVE)
        if not selected_product:
            messagebox.showerror("Error", "No product selected")
            return
        product_id = selected_product.split()[0]
        try:
            self.product_controller.remove_product(product_id)
            messagebox.showinfo("Success", "Product removed successfully!")
            self.refresh_product_list()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def list_products(self):
        self.refresh_product_list()

    def refresh_product_list(self):
        self.product_list.delete(0, tk.END)
        products = self.product_controller.get_all_products()
        for product in products:
            self.product_list.insert(tk.END, f"{product.id} {product.name} {product.quantity} {product.purchased}")

if __name__ == "__main__":
    root = tk.Tk()
    product_controller = ProductController()
    app = TkinterApp(root, product_controller)
    root.mainloop()