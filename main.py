import sqlite3
import PySimpleGUI as sg

def main():

    # Connect to the database
    db_name = 'database.sqlite'
    conn = connectToDB(db_name)
    initDatabaseTables(conn)

    ### PySimpleGUI ###
    # All the stuff inside your window.
    sg.theme('DarkPurple7')
    layout = [  [
                    sg.Combo(['Update', 'Delete', 'Insert'], key='type_combo', readonly=True, default_value='Update', enable_events=True),
                    sg.Text('row with customer_id', key='combo_text'),
                    sg.InputText(key='customer_id_input', size=10, visible=True)
                ],
                [sg.Text('customer_id | name | email | address', visible=False, key='insert_text')],
                [
                    sg.Combo(['customer_id', 'name', 'email', 'address'], readonly=True, default_value='customer_id', key='update_combo'),
                    sg.Text('new value:', key='new_value_text'),
                    sg.InputText(key='update_text',visible=True, size=10),
                    sg.InputText(key='insert_input_id',visible=False, size=10),
                    sg.InputText(key='insert_input_name',visible=False, size=10),
                    sg.InputText(key='insert_input_email',visible=False, size=10),
                    sg.InputText(key='insert_input_address',visible=False, size=10)
                ],
                [sg.Button('Update', key='apply_btn')],
                [sg.Text('Search a customer by customer_id')],
                [sg.InputText(size=15, key='search_input'), sg.Button('Search', key='search_btn')],
                [sg.Combo(['Get all customers with orders', 'example 2'], key='search_combo', default_value='Get all customers with orders'), sg.Button('Search')],
                [sg.Text('Output for tables')],
                [sg.Multiline(key='multi', size=(50, 10), disabled=True)],
                [sg.Button('Ok'), sg.Button('Cancel')]
            ]

    # Create the Window
    window = sg.Window('Window Title', layout)
    windowLoop(window, conn)
    ### PySimpleGUI END ###

    return None

def windowLoop(window, conn):
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break

        elif event == 'Ok':
            clearFields(window)
            cur = conn.cursor()
            sql = 'SELECT * FROM customers'
            res = cur.execute(sql)
            for row in res:
                window['multi'].print(row)
        elif event == 'type_combo' and values['type_combo'] == 'Update':
            # Update GUI
            hideInsert(window)

            window['customer_id_input'].update(visible=True)
            window['update_combo'].update(visible=True)
            window['update_text'].update(visible=True)
            window['new_value_text'].update(visible=True)
            window['combo_text'].update('row with customer_id')
            window['combo_text'].update('column')
            window['apply_btn'].update('Update')

        elif event == 'type_combo' and values['type_combo'] == 'Delete':
            hideInsert(window)
            hideUpdate(window)
            
            window['combo_text'].update('row with customer_id')
            window['customer_id_input'].update(visible=True)
            window['apply_btn'].update('Delete')

        elif event == 'type_combo' and values['type_combo'] == 'Insert':
            hideUpdate(window)
            hideDelete(window)

            window['combo_text'].update('new column to customers')
            window['apply_btn'].update('Insert')

            window['insert_text'].update(visible=True)
            window['insert_input_id'].update(visible=True)
            window['insert_input_name'].update(visible=True)
            window['insert_input_email'].update(visible=True)
            window['insert_input_address'].update(visible=True)
        
        elif event == 'apply_btn':
            customerID = values['customer_id_input']
            if values['type_combo'] == 'Update':
                newValue = values['update_text']
                column = values['update_combo']
                updateCustomersTable(window, conn, column, newValue, customerID)
            elif values['type_combo'] == 'Insert':
                customerID = values['insert_input_id']
                name = values['insert_input_name']
                email = values['insert_input_email']
                address = values['insert_input_address']
                insertIntoCustomersTable(window, conn, customerID, name, email, address)
            elif values['type_combo'] == 'Delete':
                deleteFromCustomersTable(window, conn, customerID)

        elif event == 'search_btn':
            clearFields(window)
            searchFromCustomers(conn, window, values['search_input'])

    window.close()
    return None

def clearFields(window):
    window['multi'].update('')
    return None

def hideInsert(window):
    window['insert_input_id'].update(visible=False)
    window['insert_input_name'].update(visible=False)
    window['insert_input_email'].update(visible=False)
    window['insert_input_address'].update(visible=False)
    window['insert_text'].update(visible=False)

def hideUpdate(window):
    window['update_combo'].update(visible=False)
    window['update_text'].update(visible=False)
    window['new_value_text'].update(visible=False)

def hideDelete(window):
    window['customer_id_input'].update(visible=False)

def connectToDB(db_name):
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except Exception as e:
        print(e)
    return conn

def updateCustomersTable(window, conn, column, newValue, customerID):
    cur = conn.cursor()

    sql = "UPDATE customers SET {} = '{}' WHERE customer_id = {};".format(column, newValue, customerID)
    cur.execute(sql)
    conn.commit()

    window['multi'].update(f"Customer's {customerID} {column} updated to {newValue}")
    return None

def insertIntoCustomersTable(window, conn, cid, name, email, address):
    cur = conn.cursor()

    cur.execute('INSERT INTO customers(customer_id, name, email, address) VALUES(?, ?, ?, ?);', [cid, name, email, address])
    conn.commit()

    window['multi'].update(f"Added {name} to customers")
    return None

def deleteFromCustomersTable(window, conn, cID):
    cur = conn.cursor()

    cur.execute('DELETE FROM customers WHERE customer_id = ?;', [cID])
    conn.commit()

    window['multi'].update(f"Deleted customer with ID {cID}")
    return None

def searchFromCustomers(conn, window, cID):

    cur = conn.cursor()

    for row in cur.execute('SELECT * FROM customers WHERE customer_id = ?', [cID]):
        window['multi'].print(row)

    return None

def addDataToTable(conn):

    cur = conn.cursor()
    sql = '''
    INSERT INTO customers(
            customer_id,
            name,
            email,
            address
        )
        VALUES 
            (112233, 'Maija', 'Vilkkumaa', 'Skinnarila'),
            (222222, 'Jere', 'Puuro', 'Bunkkeri'),
            (111111, 'Jeri', 'Kopteri' , 'KPC'),
            (987654, 'Pekka', 'Pekkanen', 'Pekkala');
    '''
    sql2 = '''
    INSERT INTO orders(
            order_id
            customer_id
            order_date
            total_cost
        )
        VALUES (1122, 12345, 20200101, 49),
        (2233, 112233, 20191612, 5),
        (3344, 222222, 20191511, 69),
        (5965, 111111, 20193112, 1);
    '''
    sql3 = '''
    INSERT INTO products(
            product_id
            name
            price
        )
        VALUES (7868, 'Tuoli', 25),
        (7869, 'Lamppu', 21),
        (7870, 'Sohva', 120),
        (7871, 'Taso', 9);
    '''
    sql4 = '''
    INSERT INTO order_details(
            order_id
            product_id
            quantity
        )
        VALUES (1122, 7686, 1),
        (2233, 7869, 1),
        (3344, 7870, 1),
        (5965, 7871, 2);
    '''
    sql5 = '''
    INSERT INTO employees(
            employee_id
            name
            email
            salary
        )
        VALUES (9891, 'Olli-pekka', op@lut, 1000),
        (9892, 'Juho', juhis@lut, 1500),
        (9893, 'Jiri', jiri@lut, 10000),
        (9894, 'Merja', merjis@lut, 50);
    '''
    sql6 = '''
    INSERT INTO employee_roles(
            employee_id
            role
        )
        VALUES (9891, 'orja'),
        (9892, 'juoksupoika'),
        (9893, 'pomo'),
        (9894, 'joulupukki');
    '''
    cur.execute(sql)
    ##cur.execute(sql2)
    ##cur.execute(sql3)
    ##cur.execute(sql4)
    ###cur.execute(sql5)
    ###cur.execute(sql6)
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
            order_date DATE NOT NULL,
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