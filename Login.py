import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import sqlite3

# --- Colors & Window Setup ---
DARK, LIGHT, CREAM = "#3e2723", "#8d6e63", "#fff8e1"
root = ctk.CTk()
root.title("☕ Café Login")
root.geometry("900x600")
root.config(bg=DARK)

def save_customer(name, phone, email):
    DB_PATH = r"C:\Users\AR FAST\OneDrive\Desktop\Project python\smart_cafe.db"
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)",
                (name, phone, email))
    conn.commit()
    conn.close()
# --- Login Function ---
def login(role):
    user, pwd = user_ent.get().strip(), pass_ent.get().strip()
    phone, mail = phone_ent.get().strip(), mail_ent.get().strip()
    if not all([user, pwd, phone, mail]):
        messagebox.showwarning("Missing Info", "Please fill all fields!")
        return
    if role == "Admin":
        if pwd != "admin123":
            messagebox.showerror("Access Denied", "Wrong admin password!")
            return
        messagebox.showinfo("Login", f"Welcome {role}, {user}!\nPhone: {phone}\nEmail: {mail}")
        root.destroy()
        import Admin
        import importlib   #reload admin modules while running
        importlib.reload(Admin)
        Admin.AdminPanel(tk.Tk())    #Admin is module , .AdminPanel is class or method of Admin file , jime tk.Tk() window parameter pass horaha hai
        tk.mainloop()
    else:
        save_customer(user, phone, mail)
        with open("current_user.txt", "w") as f:
            f.write(user)

        messagebox.showinfo("Login", f"Welcome {user}!\nEnjoy your café experience ☕")
        root.destroy()
        import cafe_app
        
# --- Helper to Create Entry Row ---
def entry_row(label, show=""):
    ctk.CTkLabel(root, text=label, fg_color=DARK, text_color=LIGHT, font=("Segoe UI", 11)).pack()
    e = ctk.CTkEntry(root, fg_color=CREAM, text_color=DARK, font=("Segoe UI", 11),  show=show)
    e.pack(pady=5, ipadx=10, ipady=4)
    return e

# --- Title & Fields ---
ctk.CTkLabel(root, text="Welcome to Smart Café", fg_color=DARK, text_color=CREAM,
         font=("Segoe UI", 16, "bold")).pack(pady=15)

user_ent = entry_row("Username")
pass_ent = entry_row("Password", show="*")
phone_ent = entry_row("Phone Number")
mail_ent = entry_row("Email")

# --- Role Buttons ---
ctk.CTkLabel(root, text="Login as:", fg_color=DARK, text_color=LIGHT, font=("Segoe UI", 11)).pack(pady=10)
for role in ["Customer", "Admin"]:
    ctk.CTkButton(root, text=role, fg_color=LIGHT, text_color=CREAM, font=("Segoe UI", 12, "bold"),
               width=12, command=lambda r=role: login(r)).pack(pady=5)

ctk.CTkLabel(root, text="Enjoy your café experience!", fg_color=DARK, text_color=LIGHT,
         font=("Segoe UI", 10, "italic")).pack(side="bottom", pady=15)

root.mainloop()