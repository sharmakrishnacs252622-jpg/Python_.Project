import tkinter as tk
from tkinter import ttk, messagebox
import database


class AdminPanel:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🍽 Admin Dashboard")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f4f6f9")

        # -------- Header --------
        header = tk.Frame(self.root, bg="#2c3e50", height=60)
        header.pack(fill=tk.X)

        tk.Label(header,
                 text="Restaurant Admin Panel",
                 bg="#2c3e50",
                 fg="white",
                 font=("Arial", 18, "bold")).pack(pady=10)

        # -------- Notebook --------
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_tab("pending")
        self.create_tab("accepted")
        self.create_tab("completed")

        self.root.mainloop()

    # ---------------- CREATE TAB ----------------

    def create_tab(self, status):
        tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tab, text=status.capitalize())

        columns = ("User", "Table", "Items", "Total", "Time")
        tree = ttk.Treeview(tab, columns=columns, show="headings")
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for col in columns:
            tree.heading(col, text=col)

        tree.column("User", width=120, anchor="center")
        tree.column("Table", width=80, anchor="center")
        tree.column("Items", width=400)
        tree.column("Total", width=100, anchor="center")
        tree.column("Time", width=150, anchor="center")

        self.load_data(tree, status)

        btn_frame = tk.Frame(tab, bg="white")
        btn_frame.pack(pady=5)

        # -------- Buttons --------
        if status == "completed":

            tk.Button(btn_frame,
                      text="Delete Selected",
                      bg="#e74c3c",
                      fg="white",
                      width=15,
                      command=lambda: self.delete_selected(tree)
                      ).pack(side=tk.LEFT, padx=5)

            tk.Button(btn_frame,
                      text="Delete All",
                      bg="#c0392b",
                      fg="white",
                      width=12,
                      command=self.delete_all_completed
                      ).pack(side=tk.LEFT, padx=5)

        elif status != "completed":

            tk.Button(btn_frame,
                      text="Update Status",
                      bg="#27ae60",
                      fg="white",
                      width=15,
                      command=lambda: self.update_status(tree, status)
                      ).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame,
                  text="Refresh",
                  bg="#3498db",
                  fg="white",
                  width=10,
                  command=lambda: self.refresh_tab(tree, status)
                  ).pack(side=tk.LEFT, padx=5)

    # ---------------- LOAD DATA ----------------

    def load_data(self, tree, status):
        for row in tree.get_children():
            tree.delete(row)

        orders = database.get_orders_by_status(status)

        for order in orders:
            items_text = ""
            for name, data in order["items"].items():
                items_text += f"{name} x{data['qty']}, "

            tree.insert("", "end",
                        values=(
                            order["username"],
                            order["table_number"],
                            items_text.rstrip(", "),
                            f"₹{order['total']:.2f}",
                            order["created_at"][:16]
                        ))

    # ---------------- UPDATE STATUS ----------------

    def update_status(self, tree, current_status):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select Order", "Please select an order!")
            return

        item = tree.item(selected[0])
        user = item["values"][0]
        table = item["values"][1]

        orders = database.get_orders_by_status(current_status)

        for order in orders:
            if order["username"] == user and order["table_number"] == table:
                if current_status == "pending":
                    database.update_status(order["id"], "accepted")
                    messagebox.showinfo("Success", "Order Accepted!")

                elif current_status == "accepted":
                    database.update_status(order["id"], "completed")
                    messagebox.showinfo("Success", "Order Completed!")

        self.refresh_all()

    # ---------------- DELETE FUNCTIONS ----------------

    def delete_selected(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select Order", "Please select an order!")
            return

        if not messagebox.askyesno("Confirm", "Delete selected order?"):
            return

        item = tree.item(selected[0])
        user = item["values"][0]
        table = item["values"][1]

        orders = database.get_orders_by_status("completed")

        for order in orders:
            if order["username"] == user and order["table_number"] == table:
                database.delete_order(order["id"])

        self.refresh_all()

    def delete_all_completed(self):
        if not messagebox.askyesno("Confirm", "Delete ALL completed orders?"):
            return

        database.delete_completed_orders()
        self.refresh_all()

    # ---------------- REFRESH ----------------

    def refresh_tab(self, tree, status):
        self.load_data(tree, status)

    def refresh_all(self):
        self.root.destroy()
        AdminPanel()