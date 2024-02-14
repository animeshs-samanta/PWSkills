import sqlite3

con = sqlite3.connect("User.db")
print("Database opened successfully")

con.execute("create table loginInformation(userId INTEGER PRIMARY KEY AUTOINCREMENT, userName VARCHAR(225) UNIQUE NOT NULL,password VARCHAR(225)  NOT NULL)")

print("Table Create successfully")
con.close()