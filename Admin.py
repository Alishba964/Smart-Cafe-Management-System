from tkinter import *
import customtkinter as ctk
from tkinter import ttk, messagebox
from GUI import get_menu_frame
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Toplevel
import Database

class AdminPanel():
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Cafe Management - Admin")
        self.root.geometry("900x550")
        self.root.config(bg="#DFCCAF")

        # Sidebar frame
        self.sidebar = Frame(self.root, bg="#3C2F2F",width=200)
        self.sidebar.pack(side=LEFT, fill=Y)

        # Main content frame
        self.main_frame = Frame(self.root, bg="#DFCCAF")
        self.main_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        # Sidebar Buttons
        self.manage_menu_btn = Button(self.sidebar,text="Manage Menu",bg="#6F4436",fg="#F5E9D2",
            font=("Arial", 12, "bold"),relief=FLAT, command=self.show_manage_menu
        )
        self.manage_menu_btn.pack(fill=X, pady=(50, 10), padx=10)

        self.analytics_btn = Button(self.sidebar,text="Analytics",bg="#6F4436",fg="#F5E9D2",
            font=("Arial", 12, "bold"),relief=FLAT,command=self.show_analytics
        )
        self.analytics_btn.pack(fill=X, pady=10, padx=10)

        self.logout_btn = Button(self.sidebar,text="Logout",bg="#854442",fg="#F5E9D2",
        font=("Arial", 12, "bold"),relief=FLAT,command=self.logout
        )
        self.logout_btn.pack(fill=X, pady=(10), padx=10)
        
        self.home_btn=Button(self.sidebar,text="Home",bg="#854442",fg="#F5E9D2",
                             font=("Arial",12,"bold"),relief=FLAT,command=self.show_welcome_screen)
        self.home_btn.pack(fill=X,pady=10,padx=10)
        # Default screen
        self.show_welcome_screen()

    # ========================
    # HELPER FUNCTIONS
    # ========================

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    # #HOTSELLER================
    def get_hot_seller(self):
        conn = Database.connect()
        cur = conn.cursor()
        from datetime import date
        today = date.today().isoformat()  #2025-11-17

        cur.execute("""
        SELECT menu_items.name, SUM(oi.quantity) AS total_sold
        FROM order_items oi
        JOIN sales ON oi.sale_id = sales.sale_id
        JOIN menu_items ON oi.item_id = menu_items.item_id
        WHERE sales.sale_date = ?
        GROUP BY menu_items.name
        ORDER BY total_sold DESC
        LIMIT 1
    """, (today,))
        row = cur.fetchone()
        conn.close()
        if row:
            item, count = row
            return f"⭐ Hot Seller Today: {item} ({count} sold)"
        else:
            return "No sales recorded today."
        
    def show_welcome_screen(self):
        self.clear_main_frame()
        Label(self.main_frame,text="‧𓍢☕ ׂ 𓈒 ⋆ ۪WELCOME, ADMIN‧𓍢☕ ׂ 𓈒 ⋆ ۪",bg="#DFCCAF",font=("Arial", 22, "bold"),fg="#3C2F2F"
        ).pack(pady=100)
        Label(self.main_frame,text="Select an option from the left panel",bg="#DFCCAF",font=("Arial", 14)
        ).pack(pady=10)
        label_hot = Label(self.main_frame, text="", font=("Arial", 14), bg="#DFCCAF", fg="#3C2F2F")
        label_hot.pack(pady=10)
        label_hot.config(text= self.get_hot_seller())
    def show_manage_menu(self):
        self.clear_main_frame()
        Label(self.main_frame,text="Manage Menu",bg="#DFCCAF",font=("Arial", 20, "bold"),fg="#145A32"
        ).pack(pady=20)

        # Load TreeView menu from GUI.py
        menu_section = get_menu_frame(self.main_frame)
        menu_section.pack(fill=BOTH, expand=True, padx=20, pady=10)

    #-----------------------Show analytics---------------------------------
    def show_analytics(self):
        self.clear_main_frame()
        import Database  # we’ll use your Database functions

        # ========== HEADER ==========
        Label(self.main_frame, text="📊 SALES & ANALYTICS", 
              bg="#DFCCAF", font=("Arial", 20, "bold"), fg="#3C2F2F").pack(pady=15)

        Label(self.main_frame, text="───────────────────────────────",
              bg="#DFCCAF", fg="#3C2F2F").pack(pady=10)

        # ========== AI FEATURE 1: DYNAMIC DISCOUNT ==========
        Label(self.main_frame, text="🤖 Dynamic Discounts", 
              bg="#DFCCAF", font=("Arial", 16, "bold"), fg="#3C2F2F").pack(pady=10)

        current_state = Database.is_discount_enabled()
        self.status_label = Label(self.main_frame, 
                                  text=f"Dynamic Discount is {'ON' if current_state else 'OFF'}",
                                  bg="#DFCCAF", 
                                  fg="green" if current_state else "red",
                                  font=("Arial", 14, "bold"))
        self.status_label.pack(pady=10)

        def toggle_discount():
            new_state = not Database.is_discount_enabled()
            Database.set_discount_state(new_state)
            self.status_label.config(
                text=f"Dynamic Discount is {'ON' if new_state else 'OFF'}",
                fg="green" if new_state else "red"
            )
            messagebox.showinfo("Discount Status", f"Dynamic Discount turned {'ON' if new_state else 'OFF'}!")

        Button(self.main_frame, text="Toggle Discount", 
               bg="#6F4436", fg="#F5E9D2", 
               font=("Arial", 12, "bold"), 
               command=toggle_discount).pack(pady=10)
        
       # graph(view daily sales)
        Button(self.main_frame, text="📈 View Daily Sales",
        bg="#6F4436", fg="#F5E9D2",
        font=("Arial", 12, "bold"),
        command=show_daily_sales).pack(pady=15)

        # ========== AI FEATURE 2: SALES HOUR INSIGHT ==========
        Label(self.main_frame, text="🤖Smart Hour Detection", 
              bg="#DFCCAF", font=("Arial", 16, "bold"), fg="#3C2F2F").pack(pady=10)

        def check_slow_hour():
            if Database.is_slow_hour():
                messagebox.showinfo("AI Insight 💡", "☕ This is a slow hour. You may enable discounts.")
            else:
                messagebox.showinfo("AI Insight 💡", "✨ Sales are normal right now.")

        Button(self.main_frame, text="Check Current Hour Performance", 
               bg="#6F4436", fg="#F5E9D2",
               font=("Arial", 12, "bold"), 
               command=check_slow_hour).pack(pady=10)

        # ========== AI FEATURE 3: AVERAGE SALES REPORT ==========
        Label(self.main_frame, text="Hourly Average Sales", 
              bg="#DFCCAF", font=("Arial", 16, "bold"), fg="#3C2F2F").pack(pady=10)

        averages = Database.get_average_sales()
        if averages:
            frame = Frame(self.main_frame, bg="#DFCCAF", width=400)
            frame.pack(pady=5)
            # Scrollbar
            scrollbar = Scrollbar(frame, orient="vertical")
            scrollbar.pack(side="right", fill="y")
             # Listbox
            listbox = Listbox(frame, yscrollcommand=scrollbar.set, font=("Arial", 12), bg="#F3F0EB", fg="#3C2F2F", width=50)
            listbox.pack(side="left", fill="both", expand=True)
            # Configure scrollbar
            scrollbar.config(command=listbox.yview)
            for hour, avg in averages.items():
                text=f"Hour {hour}: Avg ₨{avg:.2f}"
                listbox.insert(END, text.center(100)) 
        else:
            Label(self.main_frame, text="No sales data available yet.", 
                  bg="#DFCCAF", font=("Arial", 12, "italic")).pack()
#---------------------------------------------------------------------------------------------

    def logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.root.destroy()
    

# ##-------------graph------------------
DB_PATH = "smart_cafe.db"
def show_daily_sales():
    dash = Toplevel()
    dash.title("📅 Daily Sales Overview")
    dash.geometry("800x500")
    dash.config(bg="#F5E9D2")
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        SELECT sale_date, SUM(total_amount)
        FROM sales
        GROUP BY sale_date
        ORDER BY sale_date
    """)
    data = cur.fetchall()
    con.close()
    if not data:
        Label(dash, text="No sales data available yet.",
              font=("Segoe UI", 14, "bold"), bg="#F5E9D2", fg="#6F4436").pack(pady=200)
        return
    dates, totals = zip(*data)

    
    #===== Matplotlib Chart =====
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(dates, totals, color="#6F4436", marker="o", linewidth=2)
    ax.set_title("Daily Sales Trend", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Total Sales (Rs.)", fontsize=11)
    ax.tick_params(axis='x', rotation=30)

    # ===== Embed in Tkinter =====
    canvas = FigureCanvasTkAgg(fig, master=dash)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=30)

# ============ MAIN ============

if __name__ == "__main__":
    root = ctk.CTk()
    app = AdminPanel(root)
    root.mainloop()
    

  