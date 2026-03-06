import tkinter as tk
from tkinter import messagebox
import database


class AuthWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🍽 Restaurant Login")
        self.root.geometry("350x300")
        self.root.resizable(False, False)

        # Heading
        tk.Label(self.root,
                 text="Login System",
                 font=("Arial", 16, "bold")).pack(pady=10)

        # Username
        tk.Label(self.root, text="Username").pack(pady=5)
        self.entry_user = tk.Entry(self.root, width=25)
        self.entry_user.pack()

        # Password
        tk.Label(self.root, text="Password").pack(pady=5)
        self.entry_pass = tk.Entry(self.root, show="*", width=25)
        self.entry_pass.pack()

        # Buttons
        tk.Button(self.root,
                  text="Login",
                  width=15,
                  bg="#4caf50",
                  fg="white",
                  command=self.login).pack(pady=10)

        tk.Button(self.root,
                  text="Register",
                  width=15,
                  bg="#2196F3",
                  fg="white",
                  command=self.register).pack()

        self.root.mainloop()

    # ---------------- LOGIN FUNCTION ----------------

    def login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        if not username or not password:
            messagebox.showwarning("Warning", "Please enter username and password")
            return

        #  Admin Login
        if username == "admin" and password == "admin123":
            self.root.destroy()
            from admin_gui import AdminPanel
            AdminPanel()
            return

        #  Normal User Login
        user_id = database.login_user(username, password)

        if user_id:
            self.root.destroy()
            from customer_gui import CustomerApp
            CustomerApp(user_id, username)
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

    # ---------------- REGISTER FUNCTION ----------------

    def register(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        if not username or not password:
            messagebox.showwarning("Warning", "Username and Password required")
            return

        if database.register_user(username, password):
            messagebox.showinfo("Success", "Registered Successfully! Now Login.")
        else:
            messagebox.showerror("Error", "Username already exists")