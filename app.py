from flask import Flask, render_template, request, redirect, session, flash
from db_config import get_db_connection

app = Flask(__name__)
app.secret_key = 'secret123'

@app.route('/')
def home():
    return redirect('/login')


# -------------------- LOGIN --------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (uname, pwd))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect('/products')
        else:
            flash("Invalid credentials.")
            return redirect('/login')

    return render_template('login.html')


# -------------------- LOGOUT --------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# -------------------- DASHBOARD (Optional) --------------------
@app.route('/dashboard')
def dashboard():
    if 'role' not in session:
        return redirect('/login')
    return render_template('dashboard.html', role=session['role'])


# -------------------- ADD PRODUCT --------------------
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if session.get('role') != 'distributor':
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        purchase = float(request.form['purchase_price'])
        company = request.form['company']
        img = request.form['image_url']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (name, price, purchase_price, company, image_url)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, price, purchase, company, img))
        conn.commit()
        conn.close()
        flash("Product added successfully!")
        return redirect('/products')

    return render_template('add_product.html')


# -------------------- VIEW PRODUCTS --------------------
@app.route('/products')
def products():
    if 'role' not in session:
        return redirect('/login')

    search = request.args.get('search', '')
    company = request.args.get('company', '')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT DISTINCT company FROM products")
    companies = [row['company'] for row in cursor.fetchall()]

    if search:
        cursor.execute("SELECT * FROM products WHERE name LIKE %s", ('%' + search + '%',))
    elif company:
        cursor.execute("SELECT * FROM products WHERE company=%s", (company,))
    else:
        cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()
    conn.close()

    return render_template('products.html', products=products, companies=companies, selected_company=company)


# -------------------- DELETE PRODUCT --------------------
@app.route('/delete_product/<int:id>')
def delete_product(id):
    if session.get('role') != 'distributor':
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash("Product deleted successfully.")
    return redirect('/products')


# -------------------- COLLECTIONS (FOR SALESMAN) --------------------
@app.route('/collections', methods=['GET', 'POST'])
def collections():
    if session.get('role') != 'salesman':
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        user_id = request.form['user_id']
        amount = float(request.form['amount'])

        # Update due amount
        cursor.execute("UPDATE collections SET amount = amount - %s WHERE id = %s", (amount, user_id))

        # Optional: insert into collections log/history table
        # cursor.execute("INSERT INTO collection_logs (user_id, collected_amount, date) VALUES (%s, %s, NOW())", (user_id, amount))

        conn.commit()
        flash("Amount collected successfully.")
        return redirect('/collections')

    # Fetch customer dues
    cursor.execute("SELECT id, username, amount FROM collections")
    customers = cursor.fetchall()
    conn.close()

    return render_template('collections.html', customers=customers)





# -------------------- ADD DUE -----------------
@app.route('/add_due', methods=['GET', 'POST'])
def add_due():
    if session.get('role') != 'distributor':
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        user_id = request.form['user_id']
        username = request.form['username']
        amount = float(request.form['amount'])

        # Insert or update
        cursor.execute("""
            INSERT INTO collections (id, username, amount)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE amount = amount + VALUES(amount)
        """, (user_id, username, amount))

        conn.commit()
        conn.close()
        flash("Due amount updated.")
        return redirect('/add_due')

    # Get customers
    cursor.execute("SELECT id, username FROM users WHERE role = 'retailer'")
    customers = cursor.fetchall()
    conn.close()

    return render_template('add_due.html', customers=customers)







@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if session.get('role') != 'distributor':
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        purchase = float(request.form['purchase_price'])
        company = request.form['company']
        image_url = request.form['image_url']

        cursor.execute("""
            UPDATE products
            SET name=%s, price=%s, purchase_price=%s, company=%s, image_url=%s
            WHERE id=%s
        """, (name, price, purchase, company, image_url, product_id))

        conn.commit()
        conn.close()
        flash("Product updated successfully.")
        return redirect('/products')

    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    conn.close()

    if not product:
        return "Product not found", 404

    return render_template('edit_product.html', product=product)






# -------------------- MAIN --------------------
if __name__ == '__main__':
    app.run(debug=True)