import sqlite3

def connectToDB(db_name):
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except Exception as e:
        print(e)
    return conn

