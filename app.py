from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "flash message"

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="murugan@0026",
    database="inventory"
)
cursor = db.cursor()

# ---------------- ROUTES ----------------

# Homepage - Warehouse Locations
@app.route('/')
def location():
    cur = db.cursor()
    cur.execute("SELECT * FROM locations")
    data = cur.fetchall()
    cur.close()
    return render_template('locations.html', locations=data)

# Insert new warehouse location
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']

        cur = db.cursor()
        cur.execute("INSERT INTO locations (name, address, phone) VALUES (%s, %s, %s)", (name, address, phone))
        db.commit()
        flash("Warehouse location added successfully") 
        return redirect(url_for('location'))

# Insert new product
@app.route('/pinsert', methods=['POST'])
def pinsert():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        warehouse_id = request.form['warehouse_id']

        cur = db.cursor()
        cur.execute("INSERT INTO products (name, quantity, price, warehouse_id) VALUES (%s, %s, %s, %s)",
                    (name, quantity, price, warehouse_id))
        db.commit()
        flash("Product added successfully")
        return redirect(url_for('product'))

# Products page
@app.route('/product')
def product():
    cur = db.cursor()
    cur.execute("SELECT * FROM products")
    data = cur.fetchall()
    cur.close()
    return render_template('products.html', products=data)

# Movement page
@app.route('/movement')
def movement():
    return render_template('movement.html')

# Balance Report page
@app.route('/balance')
def balance():
    return render_template('balance.html')

# -----------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
