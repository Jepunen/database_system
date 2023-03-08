import sqlite3

def main():
    db_name = 'database.sqlite'
    conn = connectToDB(db_name)

    initDatabaseTables(conn)

    return None


def connectToDB(db_name):
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except Exception as e:
        print(e)
    return conn


def initDatabaseTables(conn):
    student = '''
        CREATE TABLE IF NOT EXISTS
            Student(
                FirstName,
                LastName,
                StudentID,
                GPA,
                Email
            );
    '''
    
    course = '''
        CREATE TABLE IF NOT EXISTS 
            Course (
                CourseID,
                points,
                Length,
                TeacherID
            );
    '''
    
    teacher = '''
        CREATE TABLE IF NOT EXISTS 
            Teacher (
                TeacherID,
                FirstName,
                LastName,
                Email
            );
    '''
    
    cur = conn.cursor()

    cur.execute(student)
    cur.execute(course)
    cur.execute(teacher)

    conn.commit()

    return cur.lastrowid

main()