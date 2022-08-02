import sqlite3
connection = sqlite3.connect("Sales.db")
connection.execute("INSERT INTO USER (USER_NAME,USER_PASSWORD,ACCOUNT_TYPE,PHONE_NUMBER,EMAIL) VALUES('admin','12345','0','7022990061','admin@123.com')")
connection.commit()
