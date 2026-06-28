import sqlite3
def connect():
    conn=sqlite3.connect("smart_cafe.db")
    return conn
def create_tables():
    conn=connect()
    cursor=conn.cursor()
# ====================MENU TABLE================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS menu_items(
                   item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   category TEXT,
                   price REAL
                   )
    """)
    
#======================CUSTOMERS TABLE=========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers(
                   customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   phone TEXT,
                   email TEXT)

    """)
#======================SALES====================================
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales(
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    sale_date TEXT,
    sale_hour INTEGER,
    total_amount REAL,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
)
""")
#====================ORDER ITEMS===================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items(
                   order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   sale_id INTEGER,
                   item_id INTEGER,
                   quantity INTEGER,
                   subtotal REAL,
                   FOREIGN KEY(sale_id) REFERENCES sales(sale_id),
                   FOREIGN KEY(item_id) REFERENCES menu_items(item_id))
    """)

#------------------------------- AI--------------------------
def is_discount_enabled():
    con = connect()
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS discount_control(state INTEGER)")
    result = cur.execute("SELECT state FROM discount_control").fetchone()
    if result is None:
        cur.execute("INSERT INTO discount_control(state) VALUES (0)")
        con.commit()
        con.close()
        return False
    con.close()
    return bool(result[0])

def set_discount_state(state):
    con = connect()
    cur = con.cursor()
    cur.execute("UPDATE discount_control SET state=?", (1 if state else 0,))
    con.commit()
    con.close()
#---------------------------close------------------------------
#==============================Cafe Menu ====================================
def insert_menu_data():
    menu_data=[
        ("Latte","Coffee",1299),
        ("Cappuccino","Coffee",999),
        ("Espresso","Coffee",1099),
        ("Black Coffee","Coffee",599),
        ("Mocha","Coffee",690),
        ("Americano","Coffee",890),
        ("Macchiato","Coffee",1399),
        ("Plain Fries","Snacks",400),
        ("Pizza fries","Snacks",640),
        ("Cheese Sandwich","Snacks",790),
        ("Croissant","Snacks",990),
        ("Cookies","Snacks",350),
        ("Chicken Burger","Fast Food",770),
        ("Beef Burger","Fast Food",800),
        ("Fried Chicken","Fast Food",1200),
        ("Wings","Fast Food",640),
        ("Pizza","Italian",1799),
        ("Red Sause Pasta","Italian",1299),
        ("White Sause Pasta","Italian",1400),
        ("Barbars Pasta","Italian",1999),
        ("Ice cream","Deserts",250),
        ("Brownies","Deserts",250),
        ("Cake","Deserts",1700),
        ("Pudding","Deserts",700)
    ]

# Clear old menu data before inserting
    conn=connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM menu_items")
# now inserting new data

    cursor.executemany("INSERT INTO menu_items (name,category,price) VALUES(?,?,?)",menu_data)
    conn.commit()
    conn.close()

#====================fetch menu items==================================
def get_menu_items():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu_items")
    rows = cursor.fetchall()
    conn.close()
    return rows
#===================add menu items===================================
def add_menu_item(name, category, price):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO menu_items (name, category, price) VALUES (?, ?, ?)",
        (name, category, price)
    )
    conn.commit()
    conn.close()
#===================update menu items=============================
def update_menu_item(item_id, name, category, price):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE menu_items SET name=?, category=?, price=? WHERE item_id=?", 
                   (name, category, price, item_id))
    conn.commit()
    conn.close()
#======================delete menu items==============================
def delete_menu_item(item_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM menu_items WHERE item_id=?", (item_id,))
    conn.commit()
    conn.close()
#=======================SALES==========================================  
# ye function aik complete bill insert karta hai order_details table mai 
from datetime import datetime
def record_sale(total_amount, cart_items):#cart_items = [
   # {'name': 'Burger', 'qty': 2, 'price': 150},
   # {'name': 'Fries', 'qty': 1, 'price': 50}]  # cart items aik list of dictionary return karay ga
    conn = connect()
    cur = conn.cursor()
    from datetime import date
    today = date.today().isoformat()
    # 1) insert sale
    cur.execute("INSERT INTO sales(sale_date, total_amount) VALUES (?,?)",
                (today, total_amount))
    sale_id = cur.lastrowid     #sale id auto increment hai lekin humein kaise pata chalay ga ke jo abhi sale insert hui hai uski ID kia hai , isliye lastrowid use kia
    # 2) insert items
    for item in cart_items:   #yaha item se muraad aik dictionary hai , cart_items aik list of dictionary hai ,to sari dictionaries ke liye loop chalay ga 
        name = item['name']   #{'name':"burger","qty":'2','price':590}  so item['name']=burger so name=burger
        qty = item['qty']   #qty=2
        cur.execute("SELECT item_id FROM menu_items WHERE name=?", (name,))
        item_id = cur.fetchone()[0]
        subtotal = qty * item['price']
        cur.execute("""INSERT INTO order_items(sale_id, item_id, quantity, subtotal)
                       VALUES (?,?,?,?)""", (sale_id, item_id, qty, subtotal))
    conn.commit()
    conn.close()
#ye function AI feature 3 mai use hoga jaha list box mai ye average sales or hour araha hai
def get_average_sales():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT sale_hour, AVG(total_amount) FROM sales GROUP BY sale_hour")  #Jo sales same hour par hui hain unko aik group banao, aur phir har group ka average total_amount nikaalo.
    averages = dict(cur.fetchall())  # {hour: avg_sales}
    con.close()
    return averages  #{10: 400.0,11:78}

DEMO_MODE = True
def is_slow_hour():
    if DEMO_MODE:
        return True
    con = connect()
    cur = con.cursor()
    now = datetime.now()

    # Total sales so far this hour
    cur.execute("SELECT SUM(total_amount) FROM sales WHERE sale_date=? AND sale_hour=?",
                (now.strftime("%Y-%m-%d"), now.hour))
    current_sales = cur.fetchone()[0] or 0
    
    # Average sales for this hour (from past data)
    cur.execute("SELECT AVG(total_amount) FROM sales WHERE sale_hour=?", (now.hour,))
    avg_sales = cur.fetchone()[0] or 0
    
    con.close()
    
    # Compare and decide
    if avg_sales > 0 and current_sales < 0.7 * avg_sales:  # 30% below normal
        return True
    else:
        return False

def calculate_discounted_total(total_amount):
    if is_slow_hour():
        discount_rate = 0.15                   # 15% off
        discounted = total_amount * (1 - discount_rate)
        return discounted, discount_rate
    else:
        return total_amount, 0



