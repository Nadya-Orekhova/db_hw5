import psycopg2


def create_db(conn):
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS customers(
        client_id INTEGER UNIQUE PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(60),
        email VARCHAR(100)
        );""")
    cur.execute("""CREATE TABLE IF NOT EXISTS phones(
        id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES customers(client_id),
        phone VARCHAR(12)
        );""")
    conn.commit()


def add_client(conn, client_id, first_name, last_name, email, phones=None):
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO customers(client_id, first_name, last_name, email) VALUES (%s, %s, %s, %s);
    """, (client_id, first_name, last_name, email))
    conn.commit()
    cur.execute("""
    SELECT * FROM customers;
    """)
    print(cur.fetchall())
    cur.execute("""
    INSERT INTO phones (client_id, phone) VALUES (%s, %s);
    """, (client_id, phones))
    conn.commit()
    cur.execute("""
    SELECT * FROM phones;
    """)
    print(cur.fetchall())

def add_phone(conn, client_id, phone):
    cur = conn.cursor()
    cur.execute("""
    UPDATE phones SET phone=%s WHERE client_id=%s;
     """, (phone, client_id))
    conn.commit()

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    cur = conn.cursor()
    cur.execute("""
    UPDATE customers SET first_name=%s, last_name=%s, email=%s WHERE client_id=%s;
    """, (first_name, last_name, email, client_id))
    cur.execute("""
    SELECT * FROM customers;
    """)
    print(cur.fetchall())
    cur.execute("""
    SELECT * FROM phones;
    """)
    print(cur.fetchall())

def delete_phone(conn,client_id):
    cur = conn.cursor()
    cur.execute("""
    UPDATE phones SET phone=%s WHERE client_id=%s;
    """, ('Noll', client_id))
    cur.execute("""
    SELECT * FROM phones;
    """)
    print(cur.fetchall())

def delete_client(conn, client_id):
    cur = conn.cursor()
    cur.execute("""
    DELETE FROM phones WHERE client_id=%s;
    """, (client_id,))
    cur.execute("""
    SELECT FROM phones;
    """)
    print(cur.fetchall())
    cur = conn.cursor()
    cur.execute("""
    DELETE FROM customers WHERE client_id=%s;
    """, (client_id,))
    cur.execute("""
    SELECT * FROM customers;
    """)
    print(cur.fetchall())


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    cur = conn.cursor()
    cur.execute("""
    SELECT * FROM customers c JOIN phones p ON c.client_id = p.client_id WHERE first_name=%s OR last_name=%s 
    OR email=%s OR phone=%s;
    """, (first_name, last_name, email, phone))
    print(cur.fetchall())



with psycopg2.connect(database="create_t", user="postgres", password="123456") as conn:
    create_db(conn)
    add_client(conn, 1, 'Anna', 'Romanova', 'anna.petrova@mail.ru', '+79034321233')
    add_client(conn, 2, 'Maksim', 'Maksimov', 'max.maksimov@gmail.com', '+79012116739')
    add_client(conn, 3, 'Ivan', 'Ivanov', 'vanivanov@gmail.com')
    add_client(conn, 4, 'Nino', 'Vaganov', 'ninovag@mail.ru', '+79096542311')
    add_phone(conn, 3, '+79094321233')
    change_client(conn, 4, first_name='Ivan', last_name='Petrov', email='ivan.petrov@gmail.com', phones='+79650449022')
    # delete_phone(conn, 1)
    delete_client(conn, 2)
    find_client(conn, last_name='Ivan')
    find_client(conn, first_name='Ivanov')
    find_client(conn, email='vanivanov@gmail.com')
    find_client(conn, phone='+79094321233')

conn.close()

