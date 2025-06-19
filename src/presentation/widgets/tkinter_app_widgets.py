import customtkinter as ctk  # type: ignore
from tkinter import messagebox
from src.presentation.widgets.ctk_listbox import CTkListbox
from src.utils.purchaseStatus import get_purchase_status
from typing import List


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

        # AI Fix Name button
        self.fix_name_button = ctk.CTkButton(
            button_frame,
            text="✨ Fix Name",
            command=self.fix_name,
            fg_color="#5a4a6f",
            hover_color="#7a6a8f",
        )
        self.fix_name_button.grid(row=0, column=3, padx=5, pady=5)  # AI Learn button
        self.learn_button = ctk.CTkButton(
            button_frame,
            text="🧠 Add to Dictionary",
            command=self.add_to_dictionary,
            fg_color="#4a6f5a",
            hover_color="#6a8f7a",
        )
        self.learn_button.grid(row=0, column=4, padx=5, pady=5)

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
        Add a new product to the list with AI name normalization and smart suggestions.
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
        # BEFORE adding the product, check if AI has suggestions
        try:
            # Use new advanced AI checking
            suggestions_analysis = self.product_controller.check_name_for_suggestions(
                name
            )

            if suggestions_analysis["has_any_suggestions"]:
                # Show AI suggestions dialog and let user choose
                self._show_smart_ai_suggestions_for_add_product(
                    name, quantity, purchased, suggestions_analysis
                )
                return  # Exit here, the dialog will handle adding the product

        except Exception as e:
            # If AI check fails, continue with normal add
            print(f"AI suggestion check failed: {e}")

        # No AI suggestions needed or AI failed, proceed with normal add
        self._add_product_final(name, quantity, purchased)

    def _add_product_final(self, name: str, quantity: int, purchased: bool):
        """
        Final step to add product with AI normalization.
        """
        try:
            # Use AI normalization
            product, normalization_info = self.product_controller.add_product_with_ai(
                name, quantity, purchased
            )

            # Create success message
            success_msg = f"Product '{product.name}' added successfully!"

            # Show AI improvements
            if normalization_info["improved"]:
                changes = ", ".join(normalization_info["changes"])
                success_msg += f"\n🤖 AI improved: '{normalization_info['original']}' → '{normalization_info['normalized']}'"
                success_msg += f"\nChanges: {changes}"

            # Show similar products warning
            if normalization_info["similar_products"]:
                similar_names = [
                    name for name, score in normalization_info["similar_products"][:2]
                ]
                success_msg += f"\n⚠️ Similar products found: {', '.join(similar_names)}"

            messagebox.showinfo("Success", success_msg)
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
            )  # Add low stock indicator
            low_stock_indicator = " ⚠️ LOW STOCK" if product.quantity < 5 else ""
            display_value = f"- Name: {name_display} | Quantity: {product.quantity} | Status: {purchase_status}{low_stock_indicator}"
            self.product_list.insert(ctk.END, display_value)
            self.product_map[display_value] = product.id

        # Update button states
        self.selected_product_id = None
        self.update_button.configure(state=ctk.DISABLED)
        self.remove_button.configure(state=ctk.DISABLED)

    def fix_name(self):
        """
        Fix the current product name using advanced AI with smart suggestions.
        """
        current_name = self.name_entry.get()
        if not current_name:
            messagebox.showwarning("Warning", "Please enter a product name first.")
            return

        try:
            # Use advanced AI analysis
            suggestions_analysis = self.product_controller.check_name_for_suggestions(
                current_name
            )

            if suggestions_analysis["has_any_suggestions"]:
                # Show AI suggestions dialog
                self._show_smart_ai_suggestions_dialog(
                    current_name, suggestions_analysis
                )
            else:
                # No suggestions found, just normalize normally
                normalization_info = self.product_controller.normalize_product_name(
                    current_name
                )

                if normalization_info["improved"]:
                    self.name_entry.delete(0, ctk.END)
                    self.name_entry.insert(0, normalization_info["normalized"])

                    changes = ", ".join(normalization_info["changes"])
                    message = f"✨ Name improved!\n\nBefore: '{normalization_info['original']}'\nAfter: '{normalization_info['normalized']}'\n\nChanges: {changes}"

                    if self.selected_product_id:
                        message += "\n\nUpdate this product now?"
                        result = messagebox.askyesno("AI Name Fix", message)
                        if result:
                            self.update_product()
                            return

                    messagebox.showinfo("AI Name Fix", message)
                else:
                    messagebox.showinfo(
                        "AI Name Fix", f"✅ Name '{current_name}' is already perfect!"
                    )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fix name: {str(e)}")

    def _show_smart_ai_suggestions_dialog(self, original_name: str, analysis: dict):
        """
        Show smart AI suggestions dialog for the Fix Name button.
        """
        import tkinter as tk
        from tkinter import ttk

        dialog = tk.Toplevel(self.root)
        dialog.title("🤖 Smart AI Name Fix")
        dialog.geometry("550x450")
        dialog.transient(self.root)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        main_frame = ttk.Frame(dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="🧠 AI Name Improvement Suggestions",
            font=("Arial", 14, "bold"),
        )
        title_label.pack(pady=(0, 10))

        # Original name
        orig_frame = ttk.Frame(main_frame)
        orig_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(orig_frame, text="Current name:", font=("Arial", 10, "bold")).pack(
            anchor=tk.W
        )
        orig_label = ttk.Label(
            orig_frame, text=f"'{original_name}'", font=("Arial", 11), foreground="blue"
        )
        orig_label.pack(anchor=tk.W, padx=(20, 0))

        # Suggestions frame with scrollbar
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        canvas = tk.Canvas(canvas_frame, height=200)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Store selected corrections
        selected_corrections = {}

        ttk.Label(
            scrollable_frame,
            text="Choose improvements for each word:",
            font=("Arial", 10, "bold"),
        ).pack(anchor=tk.W, pady=(0, 10))

        words_analysis = analysis["words"]
        for word, word_data in words_analysis.items():
            if word_data["has_suggestions"]:
                word_frame = ttk.LabelFrame(
                    scrollable_frame, text=f"Word: '{word}'", padding="8"
                )
                word_frame.pack(fill=tk.X, pady=5, padx=5)

                var = tk.StringVar(value=word)  # Default to original word
                selected_corrections[word] = var

                # Original word option
                rb_original = ttk.Radiobutton(
                    word_frame,
                    text=f"✋ Keep '{word}' (original)",
                    variable=var,
                    value=word,
                )
                rb_original.pack(anchor=tk.W, pady=2)

                # AI suggestions
                suggestions = word_data["suggestions"]
                for suggestion, confidence in suggestions[:4]:  # Show top 4
                    if suggestion != word:  # Don't show if it's the same as original
                        confidence_pct = int(confidence * 100)
                        emoji = (
                            "🎯"
                            if confidence > 0.8
                            else "💡" if confidence > 0.7 else "🤔"
                        )
                        rb_suggestion = ttk.Radiobutton(
                            word_frame,
                            text=f"{emoji} '{suggestion}' ({confidence_pct}% confidence)",
                            variable=var,
                            value=suggestion,
                        )
                        rb_suggestion.pack(anchor=tk.W, pady=2)

                        # Auto-select the best suggestion if confidence is very high
                        if confidence > 0.85 and suggestion != word:
                            var.set(suggestion)

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(15, 0))

        def apply_corrections():
            # Build corrected name
            words = original_name.split()
            corrected_words = []
            learned_corrections = []

            for word in words:
                word_lower = word.lower()
                if word_lower in selected_corrections:
                    chosen = selected_corrections[word_lower].get()
                    # Preserve original capitalization pattern if keeping original
                    if chosen == word_lower:
                        corrected_words.append(word)
                    else:
                        corrected_words.append(chosen)
                        # Track what AI learned
                        if chosen != word_lower:
                            learned_corrections.append(f"'{word_lower}' → '{chosen}'")
                            self.product_controller.add_learned_typo(word_lower, chosen)
                else:
                    corrected_words.append(word)

            corrected_name = " ".join(corrected_words)

            # Apply proper capitalization
            normalization_info = self.product_controller.normalize_product_name(
                corrected_name
            )
            final_name = normalization_info["normalized"]

            # Update name field
            self.name_entry.delete(0, ctk.END)
            self.name_entry.insert(0, final_name)

            dialog.destroy()

            # Show what AI learned if any
            if learned_corrections:
                learn_msg = "🧠 AI learned:\n" + "\n".join(learned_corrections) + "\n\n"
            else:
                learn_msg = ""

            # Show result and ask about auto-update
            if final_name != original_name:
                message = f"{learn_msg}✨ AI applied corrections!\n\nBefore: '{original_name}'\nAfter: '{final_name}'"

                if self.selected_product_id:
                    message += "\n\nUpdate this product now?"
                    result = messagebox.askyesno("AI Corrections Applied", message)
                    if result:
                        self.update_product()
                        return

                messagebox.showinfo("AI Corrections Applied", message)
            else:
                messagebox.showinfo("AI Corrections", "No corrections were applied.")

        def cancel():
            dialog.destroy()

        # Style the buttons
        apply_btn = ttk.Button(
            buttons_frame, text="✅ Apply Corrections", command=apply_corrections
        )
        apply_btn.pack(side=tk.LEFT, padx=(0, 8))

        cancel_btn = ttk.Button(buttons_frame, text="❌ Cancel", command=cancel)
        cancel_btn.pack(side=tk.LEFT)

    def _show_ai_suggestions_dialog(self, original_name: str, suggestions_data: List):
        """
        Show dialog with AI suggestions for word corrections.
        """
        import tkinter as tk
        from tkinter import ttk

        dialog = tk.Toplevel(self.root)
        dialog.title("🤖 AI Suggestions")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        main_frame = ttk.Frame(dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="AI found possible corrections:",
            font=("Arial", 12, "bold"),
        )
        title_label.pack(pady=(0, 10))

        # Original name
        orig_label = ttk.Label(
            main_frame, text=f"Original: '{original_name}'", font=("Arial", 10)
        )
        orig_label.pack(pady=(0, 10))

        # Suggestions frame
        suggestions_frame = ttk.Frame(main_frame)
        suggestions_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Store selected corrections
        selected_corrections = {}

        for word, suggestions in suggestions_data:
            word_frame = ttk.LabelFrame(
                suggestions_frame, text=f"Word: '{word}'", padding="5"
            )
            word_frame.pack(fill=tk.X, pady=5)

            var = tk.StringVar(value=word)  # Default to original word
            selected_corrections[word] = var

            # Original word option
            rb_original = ttk.Radiobutton(
                word_frame, text=f"Keep '{word}' (original)", variable=var, value=word
            )
            rb_original.pack(anchor=tk.W)

            # AI suggestions
            for suggestion, confidence in suggestions[:3]:  # Show top 3
                confidence_pct = int(confidence * 100)
                rb_suggestion = ttk.Radiobutton(
                    word_frame,
                    text=f"'{suggestion}' ({confidence_pct}% confidence)",
                    variable=var,
                    value=suggestion,
                )
                rb_suggestion.pack(anchor=tk.W)

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))

        def apply_corrections():
            # Build corrected name
            words = original_name.split()
            corrected_words = []

            for word in words:
                word_lower = word.lower()
                if word_lower in selected_corrections:
                    chosen = selected_corrections[word_lower].get()
                    # Preserve original capitalization pattern if keeping original
                    if chosen == word_lower:
                        corrected_words.append(word)
                    else:
                        corrected_words.append(chosen)
                        # Learn this correction for future use
                        if chosen != word_lower:
                            self.product_controller.add_learned_typo(word_lower, chosen)
                else:
                    corrected_words.append(word)

            corrected_name = " ".join(corrected_words)

            # Apply proper capitalization
            normalization_info = self.product_controller.normalize_product_name(
                corrected_name
            )
            final_name = normalization_info["normalized"]

            # Update name field
            self.name_entry.delete(0, ctk.END)
            self.name_entry.insert(0, final_name)

            dialog.destroy()

            # Show result and ask about auto-update
            if final_name != original_name:
                message = f"✨ AI applied corrections!\n\nBefore: '{original_name}'\nAfter: '{final_name}'"

                if self.selected_product_id:
                    message += "\n\nUpdate this product now?"
                    result = messagebox.askyesno("AI Corrections Applied", message)
                    if result:
                        self.update_product()
                        return

                messagebox.showinfo("AI Corrections Applied", message)
            else:
                messagebox.showinfo("AI Corrections", "No corrections were applied.")

        def cancel():
            dialog.destroy()

        ttk.Button(
            buttons_frame, text="Apply Corrections", command=apply_corrections
        ).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Cancel", command=cancel).pack(side=tk.LEFT)

    def _show_smart_ai_suggestions_for_add_product(
        self, original_name: str, quantity: int, purchased: bool, analysis: dict
    ):
        """
        Show advanced AI suggestions dialog for the add product flow.
        """
        import tkinter as tk
        from tkinter import ttk

        dialog = tk.Toplevel(self.root)
        dialog.title("🤖 Smart AI Suggestions - Add Product")
        dialog.geometry("550x500")
        dialog.transient(self.root)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        main_frame = ttk.Frame(dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="🧠 AI found potential improvements!",
            font=("Arial", 14, "bold"),
        )
        title_label.pack(pady=(0, 10))

        # Original name
        orig_frame = ttk.Frame(main_frame)
        orig_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(orig_frame, text="Product name:", font=("Arial", 10, "bold")).pack(
            anchor=tk.W
        )
        orig_label = ttk.Label(
            orig_frame, text=f"'{original_name}'", font=("Arial", 11), foreground="blue"
        )
        orig_label.pack(anchor=tk.W, padx=(20, 0))

        # Suggestions frame with scrollbar
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        canvas = tk.Canvas(canvas_frame, height=200)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Store selected corrections
        selected_corrections = {}

        ttk.Label(
            scrollable_frame,
            text="Choose corrections for each word:",
            font=("Arial", 10, "bold"),
        ).pack(anchor=tk.W, pady=(0, 10))

        words_analysis = analysis["words"]
        for word, word_data in words_analysis.items():
            if word_data["has_suggestions"]:
                word_frame = ttk.LabelFrame(
                    scrollable_frame, text=f"Word: '{word}'", padding="8"
                )
                word_frame.pack(fill=tk.X, pady=5, padx=5)

                var = tk.StringVar(value=word)  # Default to original word
                selected_corrections[word] = var

                # Original word option
                rb_original = ttk.Radiobutton(
                    word_frame,
                    text=f"✋ Keep '{word}' (original)",
                    variable=var,
                    value=word,
                )
                rb_original.pack(anchor=tk.W, pady=2)

                # AI suggestions
                suggestions = word_data["suggestions"]
                for suggestion, confidence in suggestions[:4]:  # Show top 4
                    if suggestion != word:  # Don't show if it's the same as original
                        confidence_pct = int(confidence * 100)
                        emoji = (
                            "🎯"
                            if confidence > 0.8
                            else "💡" if confidence > 0.7 else "🤔"
                        )
                        rb_suggestion = ttk.Radiobutton(
                            word_frame,
                            text=f"{emoji} '{suggestion}' ({confidence_pct}% confidence)",
                            variable=var,
                            value=suggestion,
                        )
                        rb_suggestion.pack(anchor=tk.W, pady=2)

                        # Auto-select the best suggestion if confidence is very high
                        if confidence > 0.85 and suggestion != word:
                            var.set(suggestion)

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(15, 0))

        def add_with_smart_corrections():
            # Build corrected name
            words = original_name.split()
            corrected_words = []
            learned_corrections = []

            for word in words:
                word_lower = word.lower()
                if word_lower in selected_corrections:
                    chosen = selected_corrections[word_lower].get()
                    # Preserve original capitalization pattern if keeping original
                    if chosen == word_lower:
                        corrected_words.append(word)
                    else:
                        corrected_words.append(chosen)
                        # Track what AI learned
                        if chosen != word_lower:
                            learned_corrections.append(f"'{word_lower}' → '{chosen}'")
                            self.product_controller.add_learned_typo(word_lower, chosen)
                else:
                    corrected_words.append(word)

            corrected_name = " ".join(corrected_words)

            # Close dialog first
            dialog.destroy()

            # Show what AI learned if any
            if learned_corrections:
                learn_msg = "🧠 AI learned:\n" + "\n".join(learned_corrections)
                messagebox.showinfo("AI Learning", learn_msg)

            # Add product with corrected name
            self._add_product_final(corrected_name, quantity, purchased)

        def add_without_corrections():
            dialog.destroy()
            # Add product with original name
            self._add_product_final(original_name, quantity, purchased)

        def cancel():
            dialog.destroy()
            # Don't add anything

        # Style the buttons
        apply_btn = ttk.Button(
            buttons_frame,
            text="✅ Apply AI suggestions & Add",
            command=add_with_smart_corrections,
        )
        apply_btn.pack(side=tk.LEFT, padx=(0, 8))

        keep_btn = ttk.Button(
            buttons_frame, text="📝 Add as-is", command=add_without_corrections
        )
        keep_btn.pack(side=tk.LEFT, padx=(0, 8))

        cancel_btn = ttk.Button(buttons_frame, text="❌ Cancel", command=cancel)
        cancel_btn.pack(side=tk.LEFT)

    def add_to_dictionary(self):
        """
        Add a custom word correction to AI dictionary.
        """
        import tkinter as tk
        from tkinter import ttk

        dialog = tk.Toplevel(self.root)
        dialog.title("🧠 Add to AI Dictionary")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            main_frame, text="Teach AI a new correction:", font=("Arial", 12, "bold")
        )
        title_label.pack(pady=(0, 15))

        # Typo field
        ttk.Label(main_frame, text="Incorrect word (typo):").pack(anchor=tk.W)
        typo_entry = ttk.Entry(main_frame, width=30)
        typo_entry.pack(fill=tk.X, pady=(5, 10))

        # Correct field
        ttk.Label(main_frame, text="Correct word:").pack(anchor=tk.W)
        correct_entry = ttk.Entry(main_frame, width=30)
        correct_entry.pack(fill=tk.X, pady=(5, 15))

        # Pre-fill with current name if available
        current_name = self.name_entry.get()
        if current_name:
            typo_entry.insert(0, current_name)

        def add_correction():
            typo = typo_entry.get().strip()
            correct = correct_entry.get().strip()

            if not typo or not correct:
                messagebox.showerror("Error", "Both fields are required!")
                return

            if typo.lower() == correct.lower():
                messagebox.showerror(
                    "Error", "Typo and correct word cannot be the same!"
                )
                return

            try:
                self.product_controller.add_learned_typo(typo, correct)
                messagebox.showinfo("Success", f"✅ AI learned: '{typo}' → '{correct}'")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add correction: {str(e)}")

        def cancel():
            dialog.destroy()

        # Buttons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            buttons_frame, text="Add to Dictionary", command=add_correction
        ).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Cancel", command=cancel).pack(side=tk.LEFT)
