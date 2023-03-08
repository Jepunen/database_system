import sqlite3

def main():
    db_name = 'database.sqlite'
    conn = connectToDB(db_name)

    create_student(conn, ("Kalle",))

    return None


def connectToDB(db_name):
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except Exception as e:
        print(e)
    return conn


def create_student(conn, student):
    sql = ''' INSERT INTO Student(FirstName)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, student)
    conn.commit()

    everything = cur.execute('SELECT * FROM Student')
    for row in everything:
        print(row[0])
    print(everything)

    return cur.lastrowid

main()