import customtkinter as ctk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import Database

#====================== FUNCTION TO GET MENU FRAME ==========================
def get_menu_frame(parent):
    """
    Creates and returns the menu management frame (for Admin Panel).
    Includes TreeView + Add/Edit/Delete functionality.
    """
    menu_frame = Frame(parent, bg="#DFCCAF")

    # ====== TREEVIEW FRAME ======
    menu_table_frame = Frame(menu_frame)
    menu_table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar = ttk.Scrollbar(menu_table_frame, orient="vertical")
    scrollbar.pack(side=RIGHT, fill=Y)

    menu_tree = ttk.Treeview(
        menu_table_frame,
        columns=("ID", "NAME", "CATEGORY", "PRICE"),
        show='headings',
        height=15,
        yscrollcommand=scrollbar.set
    )
    menu_tree.heading("ID", text="ID")
    menu_tree.heading("NAME", text="NAME")
    menu_tree.heading("CATEGORY", text="CATEGORY")
    menu_tree.heading("PRICE", text="PRICE (Rs)")
    menu_tree.column("ID", width=50, anchor=CENTER)
    menu_tree.column("NAME", width=200)
    menu_tree.column("CATEGORY", width=150)
    menu_tree.column("PRICE", width=100, anchor=E)
    menu_tree.pack(side=LEFT, fill="both", expand=True)
    scrollbar.config(command=menu_tree.yview)

    # ======================= FORM SECTION ================================
    form_frame = Frame(menu_frame, bg="#DFCCAF")
    form_frame.pack(pady=10)

    Label(form_frame, text="Name:", bg="#DFCCAF").grid(row=0, column=0, padx=5)
    name_entry = Entry(form_frame)
    name_entry.grid(row=0, column=1, padx=5)

    Label(form_frame, text="Category:", bg="#DFCCAF").grid(row=0, column=2, padx=5)
    category_entry = Entry(form_frame)
    category_entry.grid(row=0, column=3, padx=5)

    Label(form_frame, text="Price:", bg="#DFCCAF").grid(row=0, column=4, padx=5)
    price_entry = Entry(form_frame)
    price_entry.grid(row=0, column=5, padx=5)

    # ============================= HELPER FUNCTIONS ===============================
    def load_menu():
        menu_tree.delete(*menu_tree.get_children())
        rows = Database.get_menu_items()
        for row in rows:
            menu_tree.insert("", END, values=row)

    def clear_entries():
        name_entry.delete(0, END)
        category_entry.delete(0, END)
        price_entry.delete(0, END)

    def add_item():
        name = name_entry.get().strip()
        category = category_entry.get().strip()
        price = price_entry.get().strip()

        if not (name and category and price):
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return

        try:
            Database.add_menu_item(name, category, float(price))
            messagebox.showinfo("Success", f"{name} added successfully!")
            clear_entries()
            load_menu()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add item.\n{e}")

    def edit_item():
        selected = menu_tree.focus()
        if not selected:
            messagebox.showwarning("Selection Error", "Select an item to edit.")
            return

        values = menu_tree.item(selected, "values")
        item_id = values[0]

        name = name_entry.get().strip() or values[1]
        category = category_entry.get().strip() or values[2]
        price = price_entry.get().strip() or values[3]

        try:
            Database.update_menu_item(item_id, name, category, float(price))
            messagebox.showinfo("Updated", f"Item ID {item_id} updated!")
            clear_entries()
            load_menu()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update item.\n{e}")

    def delete_item():
        selected = menu_tree.focus()
        if not selected:
            messagebox.showwarning("Selection Error", "Select an item to delete.")
            return

        values = menu_tree.item(selected, "values")
        item_id = values[0]

        confirm = messagebox.askyesno("Confirm Delete", f"Delete {values[1]}?")
        if confirm:
            try:
                Database.delete_menu_item(item_id)
                messagebox.showinfo("Deleted", f"{values[1]} deleted successfully.")
                load_menu()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete.\n{e}")

    # ------------------------------ BUTTONS-----------------------------------
    button_frame = Frame(menu_frame, bg="#DFCCAF")
    button_frame.pack(pady=10)
    
    Button(button_frame, text="Add Item", bg="#27AE60", fg="white", width=15, command=add_item).pack(side=LEFT, padx=5)
    Button(button_frame, text="Edit Item", bg="#2980B9", fg="white", width=15, command=edit_item).pack(side=LEFT, padx=5)
    Button(button_frame, text="Delete Item", bg="#C0392B", fg="white", width=15, command=delete_item).pack(side=LEFT, padx=5)
    
    # Load initial data
    load_menu()

    return menu_frame

if __name__== "__main__": #this block only runs if we open GUI.py directly
    root=ctk.CTk()
    root.title("SMART CAFE MENU (Standalone)")
    get_menu_frame(root).pack(fill="both", expand=True)
    root.mainloop()



