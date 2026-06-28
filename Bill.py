from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

def generate_bill(cart,root):
    if not cart:
        messagebox.showwarning("Cart Empty","Please add items to cart first!")
        return
    # Main window
    bill_window=Toplevel(root)
    bill_window.title("Bill/Receipt")
    bill_window.geometry("400x500")
    
    # Label
    Label(bill_window,text="SMART CAFE BILL",font=("Arial",14,"bold")).pack(pady=10)

    Label(bill_window, text="---------------------------").pack(pady=5)

    #Bill Treeveiw
    bill_tree=ttk.Treeview(bill_window,columns=("NAME","QTY","PRICE","TOTAL"),show="headings")
    bill_tree.heading("NAME", text="NAME")
    bill_tree.heading("QTY", text="QTY")
    bill_tree.heading("PRICE", text="PRICE")
    bill_tree.heading("TOTAL", text="TOTAL")
    bill_tree.pack(fill="both", expand=True, padx=10, pady=10)

    total_amount=0
    for item in cart:
        subtotal=item["qty"]*item['price']
        total_amount+=subtotal
        bill_tree.insert("", END, values=(item["name"], item["qty"], item["price"], subtotal))
    Label(bill_window, text="---------------------------").pack(pady=5)
    Label(bill_window, text=f"Total: Rs. {total_amount:.2f}", font=("Arial", 12, "bold")).pack(pady=10)
    Button(bill_window, text="Close", command=bill_window.destroy).pack(pady=10)
    
    #============================RECEIPT==============================
    
    # Generating Receipt button
    def print_receipt():
        now = datetime.now()
        date_time = now.strftime("%d-%m-%Y  %I:%M %p")
        receipt_text="SMART CAFE BILL\n\n"
        receipt_text += f"Date & Time: {date_time}\n"
        for item in cart:
            receipt_text+=f"{item['name']} x {item['qty']} = Rs. {item['qty']*item['price']}\n"
        receipt_text += f"\nTotal: Rs. {total_amount:.2f}"
        messagebox.showinfo("Receipt", receipt_text)
    Button(bill_window, text="Print Receipt", command=print_receipt).pack(pady=5)

    return bill_window


