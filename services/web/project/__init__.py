from flask import Flask
import os
import  json
from time import sleep
from datetime import datetime
import mysql.connector
from .generator import Generator
import threading


app = Flask(__name__)


@app.route("/")
def index():
    return "Hello"

def generate(count:int):
    with mysql.connector.connect(host="db", user="root", password="root", database="db") as db:
        gen = Generator()
        for _ in range(count):
            user = gen.generate_user()

            sql = "INSERT INTO users (birth_day,registration_date,user_login,user_email,firstname,surname,patronymic,sex,job_position,description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (user["birth"], user["reg"], user["login"], user["mail"], user["name"], user["surname"], user["patronymic"], user["sex"], user["job"], user["descr"])

            cursor = db.cursor()
            cursor.execute(sql, val)
            db.commit()

@app.route("/add/<count>")
def add_user(count):
    count = int(count)
    if(count>1):
        r = threading.Thread(name='gen', target=lambda: generate(count))
        r.start()
    else:
        generate(1)
    return "OK"


