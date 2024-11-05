import psycopg2


def create_db(curs):
    curs.execute("""
        DROP TABLE phonenums;
        DROP TABLE clients;
        CREATE TABLE clients (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(20) NOT NULL,
            last_name VARCHAR(20) NOT NULL,
            email VARCHAR(30) NOT NULL
        );
        CREATE TABLE phonenums (
            clientID INTEGER REFERENCES clients(id),
            phone VARCHAR(11) NOT NULL
        );
        """)
    conn.commit()


def add_client(curs, f_name, l_name, email, phone=None):
    curs.execute("""
        INSERT INTO clients(first_name, last_name, email) VALUES (%s, %s, %s) RETURNING id;
        """, (f_name, l_name, email))
    current_id = curs.fetchone()[0]
    if phone is not None:
        curs.execute("""
            INSERT INTO phonenums(clientid, phone) VALUES (%s, %s);
            """, (current_id, phone))
    conn.commit()


def add_phonenum(curs, client_id, phone):
    curs.execute("""
                INSERT INTO phonenums(clientid, phone) VALUES (%s, %s);
                """, (client_id, phone))
    conn.commit()


def edit_client(curs, clientid, f_name=None, l_name=None, email=None, phone=None):
    if f_name is not None:
        curs.execute("""
                    UPDATE clients SET first_name=%s WHERE id=%s;
                    """, (f_name, clientid))
    elif l_name is not None:
        curs.execute("""
                    UPDATE clients SET last_name=%s WHERE id=%s;
                    """, (l_name, clientid))
    elif email is not None:
        curs.execute("""
                    UPDATE clients SET email=%s WHERE id=%s;
                    """, (email, clientid))
    elif phone is not None:
        pass
    conn.commit()


def delete_phonenum(curs, client_id, phone):
    curs.execute("""
                DELETE FROM phonenums WHERE clientid=%s AND phone=%s;
                """, (client_id, phone))
    conn.commit()


def delete_client(curs, client_id):
    curs.execute("""
                DELETE FROM phonenums WHERE clientid=%s;
                DELETE FROM clients WHERE id=%s;
                """, (client_id, client_id))
    conn.commit()


def find_client(curs, f_name=None, l_name=None, email=None, phone=None):
    if f_name is not None:
        curs.execute("""
                    SELECT * FROM clients WHERE first_name=%s;
                    """, (f_name,))
    elif l_name is not None:
        curs.execute("""
                    SELECT * FROM clients WHERE last_name=%s;
                    """, (l_name,))
    elif email is not None:
        curs.execute("""
                    SELECT * FROM clients WHERE email=%s;
                    """, (email,))
    elif phone is not None:
        curs.execute("""
                    SELECT * FROM clients WHERE id=(SELECT clientid FROM phonenums WHERE phone = %s);
                    """, (phone,))
    else:
        print("No argument was passed")
    print(curs.fetchall())


with psycopg2.connect(database="netology_db", user="postgres", password="1111") as conn:
    with conn.cursor() as cur:
        create_db(cur)

        add_client(cur, "Sven", "Svensson", "svensven@dbeaver.com", None)
        add_client(cur, "Einar", "Einarsson", "einar2@dbeaver.com", "12345678912")
        add_client(cur, "Astrid", "Astridsdottir", "astridd@dbeaver.com", None)

        add_phonenum(cur, "1", "11223344556")
        add_phonenum(cur, "2", "10012345678")
        add_phonenum(cur, "3", "21343423333")
        add_phonenum(cur, "3", "12467777777")

        edit_client(cur, "1", "Bjorn", None, "bjornsven@dbeaver.com", "12345543211")
        edit_client(cur, "2", None, None, "cooleinar@dbeaver.com")

        delete_phonenum(cur, "2", "10012345678")

        delete_client(cur, "3")

        find_client(cur, "Bjorn", None, None, None)
        find_client(cur, None, None, None, "12345678912")
