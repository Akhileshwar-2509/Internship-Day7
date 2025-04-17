import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to database
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

# Create table (if not exists)
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    quantity INTEGER,
    price REAL
)
""")

# Insert sample data
sample_data = [
    ('Apples', 10, 2.0),
    ('Bananas', 15, 1.5),
    ('Oranges', 8, 2.5),
    ('Apples', 5, 2.0),
    ('Bananas', 10, 1.5),
    ('Oranges', 12, 2.5),
    ('Mangoes', 6, 3.0),
    ('Mangoes', 4, 3.0),
]
cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sample_data)
conn.commit()

# Query 1: Total quantity and revenue by product
query1 = """
SELECT product, SUM(quantity) AS total_qty, SUM(quantity * price) AS revenue
FROM sales GROUP BY product
"""
df1 = pd.read_sql_query(query1, conn)
print("\n🛍 Total Quantity and Revenue by Product:\n", df1)

# Query 2: Average price per product
query2 = "SELECT product, AVG(price) AS avg_price FROM sales GROUP BY product"
df2 = pd.read_sql_query(query2, conn)
print("\n📊 Average Price per Product:\n", df2)

# Query 3: Top-selling product by quantity
query3 = """
SELECT product, SUM(quantity) AS total_qty
FROM sales GROUP BY product ORDER BY total_qty DESC LIMIT 1
"""
df3 = pd.read_sql_query(query3, conn)
print("\n🥇 Top-Selling Product by Quantity:\n", df3)

# Query 4: Total sales revenue (single value)
query4 = "SELECT SUM(quantity * price) AS total_revenue FROM sales"
df4 = pd.read_sql_query(query4, conn)
print("\n💰 Total Sales Revenue:\n", df4)

# Plot 1: Bar chart of revenue by product
df1.plot(kind='bar', x='product', y='revenue', title="Revenue by Product", legend=False, color='skyblue')
plt.ylabel('Revenue')
plt.tight_layout()
plt.savefig("sales_revenue_bar.png")
plt.show()

# Plot 2: Bar chart of quantity sold
df1.plot(kind='bar', x='product', y='total_qty', title="Quantity Sold by Product", color='orange', legend=False)
plt.ylabel('Quantity Sold')
plt.tight_layout()
plt.savefig("sales_quantity_bar.png")
plt.show()

# Plot 3: Average price per product
df2.plot(kind='bar', x='product', y='avg_price', title="Average Price per Product", color='green', legend=False)
plt.ylabel('Average Price')
plt.tight_layout()
plt.savefig("avg_price_bar.png")
plt.show()

# Plot 4: Pie chart of revenue share
plt.figure(figsize=(6, 6))
plt.pie(df1['revenue'], labels=df1['product'], autopct='%1.1f%%', startangle=140)
plt.title("Revenue Share by Product")
plt.savefig("revenue_share_pie.png")
plt.show()

conn.close()
