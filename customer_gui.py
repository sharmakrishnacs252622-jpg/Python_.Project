import tkinter as tk
from tkinter import ttk, messagebox
from menu_data import MENU
from order import Order
import database
from PIL import Image, ImageTk
import os


class CustomerApp:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.order = Order()
        self.image_refs = []

        self.root = tk.Tk()
        self.root.title(f"🍽 Welcome {username}")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f0f2f5")

        self.table_var = tk.IntVar(value=1)

        # ---------------- HEADER ----------------
        header = tk.Frame(self.root, bg="#1e88e5", height=60)
        header.pack(fill=tk.X)

        tk.Label(header,
                 text="Restaurant Ordering System",
                 bg="#1e88e5",
                 fg="white",
                 font=("Arial", 18, "bold")).pack(side=tk.LEFT, padx=20)

        tk.Label(header,
                 text="Table No:",
                 bg="#1e88e5",
                 fg="white").pack(side=tk.RIGHT, padx=5)

        tk.Spinbox(header,
                   from_=1, to=20,
                   textvariable=self.table_var,
                   width=5).pack(side=tk.RIGHT)

        # ---------------- MAIN FRAME ----------------
        main_frame = tk.Frame(self.root, bg="#f0f2f5")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ---------------- LEFT: MENU ----------------
        left_frame = tk.Frame(main_frame, bg="white", bd=2, relief="groove")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(left_frame,
                 text="📋 Menu",
                 font=("Arial", 16, "bold"),
                 bg="white").pack(pady=10)

        notebook = ttk.Notebook(left_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Image mapping
        image_map = {
            "Samosa": "images/samosa.png",
            "Paneer Tikka": "images/paneer_tikka.png",
            "Chicken 65": "images/chicken65.png",
            "Butter Chicken": "images/butter_chicken.png",
            "Chicken Biryani": "images/biryani.png"
        }

        for category, items in MENU.items():
            tab = tk.Frame(notebook, bg="white")
            notebook.add(tab, text=category)

            row = 0
            col = 0

            for item in items:
                raw_name = item[0]
                price = item[1]

                # Remove emoji and extra text
                name = raw_name
                for emoji in ["🥟 ", "🧀 ", "🍗 ", "🍛 ", "🍚 ", "🥬 ", "🫘 ", "🫓 ", "🧄 ", "🧈 ", "🍡 ", "🍮 ", "🍨 ", "🍵 ", "🥭 ", "🧂 "]:
                    name = name.replace(emoji, "")

                name = name.replace(" (2 pcs)", "")

                img_path = image_map.get(name)

                photo = None
                if img_path:
                    full_path = os.path.join(os.getcwd(), img_path)
                    if os.path.exists(full_path):
                        img = Image.open(full_path)
                        img = img.resize((100, 100))
                        photo = ImageTk.PhotoImage(img)
                        self.image_refs.append(photo)

                card = tk.Frame(tab, bg="white", bd=1, relief="solid")
                card.grid(row=row, column=col, padx=15, pady=15)

                if photo:
                    tk.Label(card, image=photo, bg="white").pack()

                tk.Label(card,
                         text=name,
                         font=("Arial", 10, "bold"),
                         bg="white").pack()

                tk.Label(card,
                         text=f"₹{price}",
                         fg="green",
                         bg="white").pack()

                tk.Button(card,
                          text="Add",
                          bg="#43a047",
                          fg="white",
                          command=lambda n=name, p=price: self.add_item(n, p)
                          ).pack(pady=5)

                col += 1
                if col == 3:
                    col = 0
                    row += 1

        # ---------------- RIGHT: ORDER PANEL ----------------
        right_frame = tk.Frame(main_frame, bg="white", bd=2, relief="groove")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(right_frame,
                 text="🛒 Your Order",
                 font=("Arial", 16, "bold"),
                 bg="white").pack(pady=10)

        self.listbox = tk.Listbox(right_frame,
                                  font=("Courier", 11),
                                  height=15)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.total_label = tk.Label(right_frame,
                                    text="Total: ₹0.00",
                                    font=("Arial", 14, "bold"),
                                    fg="#d32f2f",
                                    bg="white")
        self.total_label.pack(pady=10)

        btn_frame = tk.Frame(right_frame, bg="white")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame,
                  text="🗑 Clear",
                  bg="#e53935",
                  fg="white",
                  width=12,
                  command=self.clear_order).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame,
                  text="✅ Place Order",
                  bg="#1e88e5",
                  fg="white",
                  width=15,
                  command=self.place_order).pack(side=tk.LEFT, padx=5)

        self.root.mainloop()

    # ---------------- FUNCTIONS ----------------

    def add_item(self, name, price):
        self.order.add_item(name, price)
        self.refresh()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        for line in self.order.get_items_summary():
            self.listbox.insert(tk.END, line)
        self.total_label.config(text=f"Total: ₹{self.order.total:.2f}")

    def clear_order(self):
        self.order.clear()
        self.refresh()

    def place_order(self):
        if not self.order.items:
            messagebox.showwarning("Empty Order", "Your order is empty!")
            return

        database.add_order(
            self.user_id,
            self.table_var.get(),
            self.order.items,
            self.order.total
        )

        messagebox.showinfo("Order Placed", "Order placed successfully!")

        self.order.clear()
        self.refresh()