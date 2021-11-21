import mysql.connector
from .generator import generate_user

def create_table():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="db"
    )
    cursor = db.cursor()
    cursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")

def add_user(count: int):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="db"
    )

    for _ in range(count):
        user = generate_user()

        sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
        val = (user["name"], user["mail"])

        cursor = db.cursor()
        cursor.execute(sql, val)
        db.commit()

        print(cursor.rowcount, "record inserted.")
