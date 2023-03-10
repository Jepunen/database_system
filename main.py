import sqlite3
import PySimpleGUI as sg

def main():

    # Connect to the database
    db_name = 'database.sqlite'
    conn = connectToDB(db_name)

    sg.theme('DarkPurple7')

    # All the stuff inside your window.
    layout = [  [sg.Text('Some text on Row 1')],
                [sg.Output(s=(30,5))],
                [sg.Button('Ok'), sg.Button('Cancel')] ]

    # Create the Window
    window = sg.Window('Window Title', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        print('You entered ', values[0])
        if event
    window.close()

    return None


def connectToDB(db_name):
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except Exception as e:
        print(e)
    return conn


def addDataToTable(conn, table, data):

    cur = conn.cursor()

    if table == "Student":
        cur.execute(f'''
        INSERT INTO 
            Student(
                FirstName,
                LastName,
                StudentID,
                GPA,
                Email
            )
        VALUES (?,?,?,?,?)
        ''', data
    )

    return None


def initDatabaseTables(conn):
    customers = '''
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            address TEXT
        );
    '''
    
    orders = '''
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            total_cost FLOAT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );
    '''
    
    products = '''
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price FLOAT NOT NULL
        );
    '''

    orderDetails = '''
        CREATE TABLE order_details (
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            PRIMARY KEY (order_id, product_id),
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
    '''

    employees = '''
        CREATE TABLE employees (
            employee_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            salary FLOAT NOT NULL
        );
    '''

    employee_roles = '''
        CREATE TABLE employee_roles (
            employee_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            PRIMARY KEY (employee_id, role),
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
        );
    '''
    
    cur = conn.cursor()

    cur.execute(customers)
    cur.execute(orders)
    cur.execute(products)
    cur.execute(orderDetails)
    cur.execute(employees)
    cur.execute(employee_roles)

    conn.commit()

    return cur.lastrowid

main()