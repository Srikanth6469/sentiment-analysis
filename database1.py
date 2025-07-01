import sqlite3
import hashlib
import datetime
from flask import session
from flask import Flask, request, send_file
import io
import plotly.graph_objs as go
import pymysql
import mysql.connector
from dotenv import load_dotenv
load_dotenv()
from dotenv import load_dotenv
load_dotenv()


# def db_connect():
#     _conn = pymysql.connect(host="localhost", user="root",
#                             passwd="123", db="toxic")
#     c = _conn.cursor()

#     return c, _conn



import mysql.connector
import mysql.connector

# def db_connect():
#     conn = mysql.connector.connect(
#         host="localhost",
#         database="toxic",
#         user="root",
#         password="1234",
#     )
#     return conn.cursor(), conn  # ✅ return both cursor and connection





import os
import MySQLdb
load_dotenv()

def db_connect():
    try:
        _conn = MySQLdb.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER", "root"),
            passwd=os.environ.get("DB_PASSWORD", "1234"),
            db=os.environ.get("DB_NAME", "toxic"),
            port=int(os.environ.get("DB_PORT", 3306))
        )
        return _conn.cursor(), _conn
    except Exception as e:
        print("❌ Database connection failed:", e)
        raise


# ✅ CALL the function here with ()
cursor, conn = db_connect()

cursor.execute("SHOW TABLES;")
print(cursor.fetchall())

conn.close()


# -------------------------------Registration-----------------------------------------------------------------


    


def inc_reg(username,password,email,mobile):
    try:
        c, conn = db_connect()
        print(username,password,email,mobile)
        id="0"
        status = "pending"
        j = c.execute("insert into user (id,username,password,email,mobile,status) values ('"+id +
                      "','"+username+"','"+password+"','"+email+"','"+mobile+"','"+status+"')")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))
    






# # -------------------------------Registration End-----------------------------------------------------------------
# # -------------------------------Loginact Start-----------------------------------------------------------------


def ins_loginact(username, password):
    try:
        c, conn = db_connect()
        c.execute("SELECT * FROM user WHERE username=%s AND password=%s", (username, password))
        user = c.fetchone()
        conn.close()
        print(user)  # Debugging
        return user is not None
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    print(db_connect())
