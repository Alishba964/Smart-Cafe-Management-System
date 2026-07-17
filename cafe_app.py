import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from Database import get_menu_items
from datetime import datetime,timedelta  
import customtkinter as ctk
# -------------------- COLORS & ROOT --------------------
DARK, LIGHT, CREAM = "#3C2F2F", "#DFCCAF", "#fff8e1"
root = ctk.CTk()
root.title("☕ Smart Café")
root.geometry("900x520")
root.config(bg=DARK)

cart = []
total = tk.DoubleVar(value=0)  # linked with tkinter widgets and update them automatically
DB_PATH = r"C:\Users\AR FAST\OneDrive\Desktop\Smart Cafe Management System\smart_cafe.db"

def get_current_user(): # this fuction is for show account
    try:
        with open("current_user.txt", "r") as f:  # reads saved username
            return f.read().strip()
    except FileNotFoundError:
        return None

def get_user_info(username):
    conn = sqlite3.connect(DB_PATH)  # connect to your café database
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS customers (name TEXT, phone TEXT, email TEXT)")
    cur.execute("SELECT name, phone, email FROM customers WHERE name=?", (username,))
    data = cur.fetchone()
    conn.close()
    return data

def show_account():
    """Displays the logged-in customer's account info"""
    for w in mid.winfo_children():
        w.destroy()

    username = get_current_user()
    if not username:
        ctk.CLabel(mid, text="⚠ No user logged in!", bg=LIGHT, fg=DARK,
                 font=("Segoe UI", 13, "bold")).pack(pady=50)
        return

    info = get_user_info(username)
    if not info:
        tk.Label(mid, text="No account info found.", fg_color=LIGHT, text_color=DARK,
                 font=("Segoe UI", 13, "bold")).pack(pady=50)
        return

    name, phone, email = info
    tk.Label(mid, text="👤 Your Account", bg=LIGHT, fg=CREAM,
             font=("Segoe UI", 15, "bold")).pack(pady=20)
    tk.Label(mid, text=f"Name: {name}", bg=LIGHT, fg=DARK,
             font=("Segoe UI", 12)).pack(pady=5)
    tk.Label(mid, text=f"Phone: {phone}", bg=LIGHT, fg=DARK,
             font=("Segoe UI", 12)).pack(pady=5)
    tk.Label(mid, text=f"Email: {email}", bg=LIGHT, fg=DARK,
             font=("Segoe UI", 12)).pack(pady=5)

# -------------------- CART FUNCTIONS --------------------
def add_to_cart(name, price):
    for item in cart:
        if item["name"] == name:
            item["qty"] += 1
            break
    else:
        cart.append({"name": name, "qty": 1, "price": price})
    update_cart()

def update_cart():
    box.delete(0, "end")  #.delete(start,end) #delete aik tkinter ka method hai
    total_amount = 0     #agar delete na karein to naye item add honay par puranay walay bhi dubara sath ajaye gai
    for item in cart:   #sab delete honay ke baad aik loop chalaya takay phir se list box mai sab insert
        subtotal = item["qty"] * item["price"]
        total_amount += subtotal
        box.insert("end", f"{item['name']} x{item['qty']} → Rs.{subtotal:.2f}") #naye item ko last mai append karo
    lbl.config(text=f"Total: Rs.{total_amount:.2f}")


# -------------------- LAYOUT FRAMES --------------------
left = tk.Frame(root, bg=LIGHT, width=150)
left.pack(side="left", fill="y")

tk.Frame(root, bg=DARK, width=2).pack(side="left", fill="y")

mid = tk.Frame(root, bg=LIGHT)
mid.pack(side="left", fill="both", expand=True)

tk.Frame(root, bg=DARK, width=2).pack(side="left", fill="y")

right = tk.Frame(root, bg=CREAM, width=250)
right.pack(side="right", fill="y")

# -------------------- MENU TREE --------------------
def show_menu_tree():
    for w in mid.winfo_children():
        w.destroy()
    menu_table_frame = tk.Frame(mid, bg=LIGHT)
    menu_table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar = ttk.Scrollbar(menu_table_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    menu_tree = ttk.Treeview(
        menu_table_frame,
        columns=("ID", "NAME", "CATEGORY", "PRICE"),
        show='headings',
        height=20,
        yscrollcommand=scrollbar.set
    )
    menu_tree.heading("ID", text="ID")
    menu_tree.heading("NAME", text="NAME")
    menu_tree.heading("CATEGORY", text="CATEGORY")
    menu_tree.heading("PRICE", text="PRICE (Rs)")

    menu_tree.column("ID", width=50, anchor="center")
    menu_tree.column("NAME", width=200)
    menu_tree.column("CATEGORY", width=150)
    menu_tree.column("PRICE", width=100, anchor="center")

    menu_tree.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=menu_tree.yview)

    rows = get_menu_items()
    for row in rows:
        menu_tree.insert("","end",values=row)

    root.menu_tree = menu_tree

    tk.Button(mid, text="🛒 Add to Cart", bg=DARK, fg=CREAM, font=("Segoe UI", 11, "bold"),
              relief="flat", command=lambda: add_selected_to_cart(menu_tree)).pack(pady=10)

def add_selected_to_cart(menu_tree):
    selected = menu_tree.focus()  #.focus() gives an iid(internal item identifier)
    if not selected:
        messagebox.showwarning("Selection Error", "Please select an item from the menu.")
        return
    v = menu_tree.item(selected, "values")
    name = v[1]
    price = float(v[3])
    add_to_cart(name, price)

# -------------------- DEALS & DISCOUNTS --------------------
def show_deals():
    for w in mid.winfo_children():
        w.destroy()

    # Outer frame to center deals
    deals_frame_outer = tk.Frame(mid, bg=LIGHT)
    deals_frame_outer.pack(expand=True, fill="both", padx=10, pady=10)

    def create_deal(frame, deal_name, items, price, discount):
        discounted_price = price - (price * discount / 100)
        t = f"{deal_name}\n\n" + "\n".join(items) + f"\n\n💰 Rs.{discounted_price:.0f} (Save {discount}%)"
        lbl = tk.Label(frame, text=t, fg=CREAM, bg=DARK, font=('Segoe UI', 12, 'bold'),
                       justify='center', wraplength=180, height=8)
        lbl.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Button(
            frame,
            text="Add to Cart",
            bg=LIGHT,   # lighter theme color
            fg=DARK,
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            command=lambda: add_to_cart(deal_name, discounted_price)
        ).pack(pady=10)

    deals = [
        ("☕ Morning Combo", ["Latte", "Croissant", "Cookies"], 1799, 10),
        ("🍕 Italian Feast", ["Pizza", "White Sauce Pasta", "Barbars Pasta"], 2899, 15),
        ("🍔 Fast Food Fix", ["Beef Burger", "Wings", "Plain Fries"], 1999, 12),
        ("🍝 Pasta Lovers", ["Red Sauce Pasta", "Barbars Pasta", "Mocha"], 3299, 18),
        ("🍨 Sweet Treat", ["Cake", "Brownies", "Ice Cream"], 2100, 20),
        ("🥤 Coffee Lovers", ["Cappuccino", "Macchiato", "Cookies"], 2499, 15)
    ]

    # Grid layout: 2 rows x 3 columns
    for i, (name, items, price, discount) in enumerate(deals):
        frame = tk.Frame(deals_frame_outer, bg=CREAM, width=220, height=240,
                         highlightbackground=DARK, highlightthickness=3)
        frame.grid(row=i // 3, column=i % 3, padx=20, pady=20)
        create_deal(frame, name, items, price, discount)

    # # Center the entire grid
    for col in range(3):
        deals_frame_outer.grid_columnconfigure(col, weight=1)

# -------------------- HOME SCREEN --------------------
#=========countdown=============
from datetime import datetime

def update_countdown():
    global countdown_label

    if countdown_label is None:
        return
    
    now = datetime.now()
    end_of_hour = now.replace(minute=59, second=59, microsecond=0)
    remaining = end_of_hour - now

    minutes, seconds = divmod(remaining.seconds, 60)  #divmod(a,b)  it does a//b,a%b
    text = f"⏳ Discount ends in {minutes:02d}:{seconds:02d}"

    countdown_label.config(text=text)

    countdown_label.after(1000, update_countdown)
#========================
def show_home():
    global countdown_label

    for w in mid.winfo_children():
        w.destroy()

    # Welcome label
    tk.Label(mid, text="‧☕ ׂ 𓈒 ⋆ ۪  Welcome Customer ☕ ׂ 𓈒 ⋆ ۪ ‧",
             bg=LIGHT, fg=CREAM, font=("Arial", 22, "bold")).pack(pady=40)

    # Check discount status
    if Database.is_discount_enabled():

        # --- Happy Hour Banner ---
        banner = tk.Label(mid,text="🎉 HAPPY HOUR ACTIVE — DISCOUNT IS ON! 🎉",bg="#8d6e63",fg="#2f4f2f",
                            font=("Arial", 18, "bold"),pady=10,padx=20)
        banner.pack(pady=10)
        # --- Countdown Timer ---
        countdown_label = tk.Label(mid,text="",font=("Arial", 14, "bold"),bg=LIGHT,fg="#2f4f2f" )
        countdown_label.pack(pady=10)
        update_countdown()
    else:
        countdown_label = None
# -------------------- SIDEBAR BUTTONS --------------------
for t,cmd in [("Home",show_home),("Menu", show_menu_tree), ("Deals", show_deals), ("Account", show_account)]:
    tk.Button(left, text=t, bg=DARK, fg=CREAM, font=("Segoe UI", 12, "bold"),
              relief="flat", width=12, command=cmd).pack(pady=20)

# -------------------- CART PANEL --------------------
tk.Label(right, text="🛒 Cart", bg=CREAM, fg=DARK, font=("Segoe UI", 15, "bold")).pack(pady=10)
box = tk.Listbox(right, bg="white", fg=DARK, font=("Segoe UI", 10))
box.pack(padx=10, pady=5, fill="both", expand=True)
lbl = tk.Label(right, text="Total: Rs.0", bg=CREAM, fg=DARK, font=("Segoe UI", 12, "bold"))
lbl.pack(pady=10)

from datetime import datetime
import Database
def confirm_order():
    if not cart:
        messagebox.showwarning("Empty Cart", "Add some items before confirming!")
        return
    total_amount = sum(item['qty'] * item['price'] for item in cart)
    
    #AI discount apply here

    if Database.is_discount_enabled():
        final_total, discount = Database.calculate_discounted_total(total_amount)
    else:
        final_total = total_amount
        discount = 0


    receipt="SMART CAFE BILL\n\n"
    for item in cart:
        receipt+=f"{item['name']} x {item['qty']} = Rs{item['qty']* item['price']:.2f}\n"
    if discount > 0:
        receipt += f"\nAI Hour Based Discount: {discount*100:.0f}% applied!"
        receipt += f"\nOLD Total: Rs.{total_amount:.2f}"
        receipt += f"\nNEW Total: Rs.{final_total:.2f}"
    else:
        receipt += f"\nTotal: Rs.{total_amount:.2f}"

    messagebox.showinfo("Receipt", receipt)

    # record sale
    from Database import record_sale
    record_sale(final_total, cart)


    cart.clear()
    update_cart()
    box.delete(0,"end")  # force clear visual listbox too
    lbl.config(text="Total: Rs.0")
tk.Button(right, text="Confirm Order", bg=DARK, fg=CREAM, relief="flat",
          font=("Segoe UI", 11, "bold"), command=confirm_order).pack(pady=5)

show_home()
root.mainloop()



