import sqlite3
import PySimpleGUI as sg

def main():

    # Connect to the database
    db_name = 'database.sqlite'
    conn = connectToDB(db_name)

    sg.theme('DarkPurple7')

    # All the stuff inside your window.
    layout = [  [
                    sg.Combo(['Update', 'Delete', 'Insert'], key='type_combo', readonly=True, default_value='Update', enable_events=True),
                    sg.Text('column'),
                    sg.Combo(['customer_id', 'name', 'email', 'address'], readonly=True, default_value='customer_id')
                ],
                [sg.Text('Output for tables')],
                [sg.Multiline(key='multi', size=(30, 10), disabled=True)],
                [sg.Button('Ok'), sg.Button('Cancel')]
            ]

    # Create the Window
    window = sg.Window('Window Title', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break

        elif event == 'Ok':
            cur = conn.cursor()
            sql = 'SELECT * FROM customers'
            res = cur.execute(sql)
            for row in res:
                window['multi'].print(row)
        elif event == 'type_combo':
            continue

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


def addDataToTable(conn):

    cur = conn.cursor()
    sql = '''
    INSERT INTO customers(
            customer_id,
            name,
            email,
            address
        )
        VALUES (012345, 'Jorma', 'Email', 'Osoite');
    '''
    cur.execute(sql)
    conn.commit()

    return None


def initDatabaseTables(conn):
    customers = '''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            address TEXT
        );
    '''
    
    orders = '''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            total_cost FLOAT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );
    '''
    
    products = '''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price FLOAT NOT NULL
        );
    '''

    orderDetails = '''
        CREATE TABLE IF NOT EXISTS order_details (
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            PRIMARY KEY (order_id, product_id),
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
    '''

    employees = '''
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            salary FLOAT NOT NULL
        );
    '''

    employee_roles = '''
        CREATE TABLE IF NOT EXISTS employee_roles (
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