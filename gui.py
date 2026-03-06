import tkinter as tk
from tkinter import ttk, messagebox
from menu_data import MENU
from order import Order
import database  

class RestaurantOrderSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("🍽️ Restaurant Order ")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#f8f0e3")

        self.order = Order()

        # --- Top frame with Admin button ---
        top_frame = tk.Frame(root, bg="#f8f0e3")
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(top_frame, text="🔧 Admin Panel", font=("Arial", 10),
                  bg="#ff9800", fg="white", command=self.open_admin).pack(side=tk.RIGHT)

        # Left Frame: Menu
        left_frame = tk.Frame(root, bg="#f8f0e3", padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(left_frame, text="📋 Menu", font=("Arial", 18, "bold"),
                 bg="#f8f0e3", fg="#5d3a1a").pack(pady=5)

        notebook = ttk.Notebook(left_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Arial", 11, "bold"), padding=[10, 5])

        for category, items in MENU.items():
            tab = tk.Frame(notebook, bg="#ffffff")
            notebook.add(tab, text=category)

            for item, price in items:
                btn_text = f"{item}\n${price:.2f}"
                btn = tk.Button(tab, text=btn_text, font=("Arial", 10),
                                bg="#4caf50", fg="white", activebackground="#45a049",
                                width=18, height=2,
                                command=lambda i=item, p=price: self.add_to_order(i, p))
                btn.pack(pady=5, padx=10)

        # Right Frame: Order
        right_frame = tk.Frame(root, bg="#e6d5b8", padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(right_frame, text="🛒 Your Order", font=("Arial", 18, "bold"),
                 bg="#e6d5b8", fg="#5d3a1a").pack(pady=5)

        order_frame = tk.Frame(right_frame, bg="#e6d5b8")
        order_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(order_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.order_listbox = tk.Listbox(order_frame, yscrollcommand=scrollbar.set,
                                        font=("Courier", 11), bg="#fff9f0",
                                        selectbackground="#f0b27a", height=12)
        self.order_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.order_listbox.yview)

        self.total_var = tk.StringVar()
        self.total_var.set("Total: $0.00")
        tk.Label(right_frame, textvariable=self.total_var, font=("Arial", 14, "bold"),
                 bg="#e6d5b8", fg="#b34b1a").pack(pady=10)

        btn_frame = tk.Frame(right_frame, bg="#e6d5b8")
        btn_frame.pack()

        tk.Button(btn_frame, text="✅ Place Order", font=("Arial", 11),
                  bg="#2196F3", fg="white", padx=10, pady=5,
                  command=self.place_order).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="🗑️ Clear Order", font=("Arial", 11),
                  bg="#f44336", fg="white", padx=10, pady=5,
                  command=self.clear_order).pack(side=tk.LEFT, padx=5)

        self.refresh_order_display()

    def add_to_order(self, item, price):
        self.order.add_item(item, price)
        self.refresh_order_display()

    def refresh_order_display(self):
        self.order_listbox.delete(0, tk.END)
        for line in self.order.get_items_summary():
            self.order_listbox.insert(tk.END, line)
        self.total_var.set(f"Total: ${self.order.total:.2f}")

    def clear_order(self):
        self.order.clear()
        self.refresh_order_display()

    def place_order(self):
        if not self.order.items:
            messagebox.showwarning("Empty Order", "Your order is empty!")
            return
        # Save to database
        database.add_order(self.order.items, self.order.total)
        # Show confirmation
        items_list = "\n".join([f"{name} x{data['qty']} (${data['qty']*data['price']:.2f})"
                                for name, data in self.order.items.items()])
        msg = f"Order placed!\n\n{items_list}\n\nTotal: ${self.order.total:.2f}\n\nThank you!"
        messagebox.showinfo("Order Confirmation", msg)
        self.clear_order()

    def open_admin(self):
        """Open the admin panel in a new window."""
        import admin_gui
        admin_gui.AdminPanel(tk.Toplevel(self.root))