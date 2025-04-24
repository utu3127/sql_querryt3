# import pandas as pd
# import sqlite3

# Step 1: Load your CSV
# df = pd.read_csv("furniture_with_features.csv")

# Step 2: Create an in-memory SQLite database
# conn = sqlite3.connect(":memory:")  # You can use "furniture.db" to save to file

# Step 3: Load data into SQL table
# df.to_sql("furniture", conn, index=False, if_exists="replace")

# # Step 4: Run SQL queries
# query = """
# SELECT productTitle, SUM(sold) AS total_sold
# FROM furniture
# GROUP BY productTitle
# ORDER BY total_sold DESC
# LIMIT 5;
# """
# query = """ SELECT tagText, AVG(sold) FROM furniture GROUP BY tagText; """
# query = """ SELECT * FROM top_products_view LIMIT 5; """
# query = """ 
# SELECT productTitle, sold
# FROM furniture
# WHERE sold > (SELECT AVG(sold) FROM furniture);
# """

# result = pd.read_sql_query(query, conn)
# print("🏆 Top 5 Best-Selling Products:\n", result)

# # Step 5: Save all used queries into a file
# with open("queries.sql", "w") as f:
#     f.write(query)





import pandas as pd
import sqlite3

# Load the dataset
df = pd.read_csv("furniture_with_features.csv")

# Create SQLite connection
conn = sqlite3.connect(":memory:")
df.to_sql("furniture", conn, index=False, if_exists="replace")

cursor = conn.cursor()

# 1. Average sold by tagText
print("\n🔹 1. Average sold by tagText")
q1 = "SELECT tagText, AVG(sold) AS avg_sold FROM furniture GROUP BY tagText;"
print(pd.read_sql_query(q1, conn))

# 2. Products with above average sales (Subquery)
print("\n🔹 2. Products with above-average sales")
q2 = """
SELECT productTitle, sold
FROM furniture
WHERE sold > (SELECT AVG(sold) FROM furniture);
"""
print(pd.read_sql_query(q2, conn))

# 3. Create a view
print("\n🔹 3. Creating view for top-selling products")
cursor.execute("""
CREATE VIEW IF NOT EXISTS top_products_view AS
SELECT productTitle, SUM(sold) AS total_sold
FROM furniture
GROUP BY productTitle;
""")

# 4. Index creation (optimization)
print("\n🔹 4. Creating index on price")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_price ON furniture(price);")

# 5. View the results from the view
print("\n🔹 5. View: Top products (from view)")
q5 = "SELECT * FROM top_products_view ORDER BY total_sold DESC LIMIT 5;"
print(pd.read_sql_query(q5, conn))

