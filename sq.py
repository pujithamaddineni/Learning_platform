import sqlite3

# Connect to your database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Show tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

# Show users
cursor.execute("SELECT * FROM students;")
users = cursor.fetchall()

print("\nUsers:")
for user in users:
    print(user)

conn.close()
