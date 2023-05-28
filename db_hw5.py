import psycopg2


def create_db(conn, cur):
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



def add_client(conn, cur, client_id, first_name, last_name, email, phones=None):
    cur.execute("""
    INSERT INTO customers(client_id, first_name, last_name, email) VALUES (%s, %s, %s, %s);
    """, (client_id, first_name, last_name, email))
    cur.execute("""
    SELECT * FROM customers;
    """)
    print(cur.fetchall())
    cur.execute("""
    INSERT INTO phones (client_id, phone) VALUES (%s, %s);
    """, (client_id, phones))
    cur.execute("""
    SELECT * FROM phones;
    """)
    print(cur.fetchall())

def add_phone(conn, cur,  client_id, phone):
    cur.execute("""
    UPDATE phones SET phone=%s WHERE client_id=%s;
     """, (phone, client_id))

def change_client(conn, cur, client_id, first_name=None, last_name=None, email=None, phones=None):
    current_user = cur.execute("""
    SELECT * FROM customers
    WHERE client_id = %s
    """, (client_id,))
    # print(cur.fetchall())
    if first_name is None:
        first_name = current_user[1]
    if last_name is None:
        last_name = current_user[2]
    if email is None:
        email = current_user[3]
    print(cur.fetchall())
    cur.execute("""
    UPDATE customers 
    SET first_name = %s, last_name = %s, email = %s WHERE client_id = %s
    """, (first_name, last_name, email, client_id))
    cur.execute("""
        UPDATE phones SET phone=%s WHERE client_id=%s;
        """, (phones, client_id))
    cur.execute("""
        SELECT * FROM phones;
        """)
    print(cur.fetchall())




def delete_phone(conn, cur, client_id):
    cur.execute("""
    UPDATE phones SET phone=%s WHERE client_id=%s;
    """, ('Noll', client_id))
    cur.execute("""
    SELECT * FROM phones;
    """)
    print(cur.fetchall())

def delete_client(conn, cur, client_id):
    cur.execute("""
    DELETE FROM phones WHERE client_id=%s;
    """, (client_id,))
    cur.execute("""
    SELECT FROM phones;
    """)
    print(cur.fetchall())
    cur.execute("""
    DELETE FROM customers WHERE client_id=%s;
    """, (client_id,))
    cur.execute("""
    SELECT * FROM customers;
    """)
    print(cur.fetchall())


def find_client(conn, cur, first_name=None, last_name=None, email=None, phone=None):
    cur.execute("""
    SELECT * FROM customers c JOIN phones p ON c.client_id = p.client_id WHERE first_name=%s AND last_name=%s AND
    email=%s AND phone=%s;
    """, (first_name, last_name, email, phone))
    print(cur.fetchall())



with psycopg2.connect(database="create_t", user="postgres", password="123456") as conn:
    with conn.cursor() as cur:
        create_db(conn, cur)
        add_client(conn, cur, 1, 'Anna', 'Romanova', 'anna.petrova@mail.ru', '+79034321233')
        add_client(conn, cur, 2, 'Maksim', 'Maksimov', 'max.maksimov@gmail.com', '+79012116739')
        add_client(conn, cur, 3, 'Ivan', 'Ivanov', 'vanivanov@gmail.com')
        add_client(conn, cur, 4, 'Nino', 'Vaganov', 'ninovag@mail.ru', '+79095431233')
        add_phone(conn, cur, 3, '+79094321233')
        change_client(conn, cur, 4, first_name='Ivan', last_name='Petrov', email='ivan.petrov@gmail.com', phones='+79236543312')
        change_client(conn, cur, 1, 'Lena', 'Romanova', 'lenaRomanova@mail.ru', '+79034321233')
        change_client(conn, cur, 4, first_name='Ivan', last_name='Petrov', email='ivan.petrov@gmail.com', phones='+79650449022')
        delete_phone(conn, cur, 1)
        delete_client(conn, cur, 2)
        find_client(conn, cur, 'Maksim', 'Maksimov', 'max.maksimov@gmail.com', '+79012116739')
        find_client(conn, cur, 'Ivan', 'Ivanov', 'vanivanov@gmail.com', '+79094321233')



conn.close()

