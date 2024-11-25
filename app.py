from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ecommerce'

mysql = MySQL(app)

@app.route('/')
def index():
    return redirect(url_for('display_products'))

@app.route('/add_product_page', methods=['GET'])
def add_product_page():
    return render_template('add_product.html')  # Ensure you have this template

@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        
        if name and price and description:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO products (name, price, description) VALUES (%s, %s, %s)", (name, price, description))
            mysql.connection.commit()
            cursor.close()
            flash('Product added successfully!', 'success')
        else:
            flash('All fields are required!', 'danger')
        
        return redirect(url_for('display_products'))

@app.route('/display_products')
def display_products():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    return render_template('display_products.html', products=products)

# Update product route
@app.route('/update_product/<int:id>', methods=['GET', 'POST'])
def update_product_view(id):
    if request.method == 'POST':
        # Handle the update form submission
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']

        # Check if all fields are provided
        if name and price and description:
            cursor = mysql.connection.cursor()
            cursor.execute("""
                UPDATE products
                SET name = %s, price = %s, description = %s
                WHERE id = %s
            """, (name, price, description, id))
            mysql.connection.commit()
            cursor.close()

            # Flash success message and redirect to display products
            flash('Product updated successfully!', 'success')
            return redirect(url_for('display_products'))  # Ensure the POST always ends with a redirect
        else:
            # If fields are missing, redirect back with an error
            flash('All fields are required!', 'danger')
            return redirect(url_for('update_product_view', id=id))  # Rerender form with the same ID

    else:  # Handle GET request to display the update form
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id = %s", [id])
        product = cursor.fetchone()
        cursor.close()

        if product:
            # Render the update form with the product data
            return render_template('update_product.html', product=product)
        else:
            # If the product is not found, redirect back to the product list
            flash('Product not found', 'danger')
            return redirect(url_for('display_products'))  # Always return a response in case of missing product

# Delete product route (add functionality here as needed)
@app.route('/delete_product/<int:id>', methods=['POST'])
def delete_product(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('display_products'))


@app.route('/index')
def index_page():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
