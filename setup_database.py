import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE custom_table
             (id INTEGER PRIMARY KEY, name TEXT NOT NULL, description TEXT NOT NULL)''')
c.execute("INSERT INTO custom_table (name, description) VALUES ('Item1', 'Description1')")
c.execute("INSERT INTO custom_table (name, description) VALUES ('Item2', 'Description2')")
conn.commit()
conn.close()
import sqlite3

# Connect to the database (it will create the file if it doesn't exist)
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create the custom_table
c.execute('''CREATE TABLE IF NOT EXISTS custom_table
             (id INTEGER PRIMARY KEY, name TEXT NOT NULL, description TEXT NOT NULL)''')

# Insert sample data into custom_table
c.execute("INSERT INTO custom_table (name, description) VALUES ('Item1', 'Description1')")
c.execute("INSERT INTO custom_table (name, description) VALUES ('Item2', 'Description2')")

# Create the users table
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)''')

# Insert a sample user (for testing purposes)
# You should hash passwords in a real application, this is just for simplicity
c.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('demouser', 'ThisIsForWPClass')")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database tables created successfully and sample data inserted.")
