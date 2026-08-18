import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database import get_db

def customeradd(name,mobile):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM customers")
    count = cursor.fetchone()[0]
    customer_code = f"C{count + 1:03d}"
    cursor.execute("INSERT INTO customers (customer_code,name, mobile) VALUES (?,?, ?)", (customer_code,name, mobile))
    conn.commit()
    customer_id = cursor.lastrowid
    conn.close()
    return customer_id

def addUdhhar(customer_id, item_name, quantity, price, due_date):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO udhaar
        (customer_id, item_name, quantity, amount, due_date)
        VALUES (?, ?, ?, ?, ?)
    """, (customer_id, item_name, quantity, price, due_date))

    conn.commit()
    conn.close()

def add_payment(customer_id, payment_amount):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO payments (customer_id, amount)
        VALUES (?, ?)
    """, (customer_id, payment_amount))
    conn.commit()
    conn.close()

def total_payment_amount(customer_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM payments
        WHERE customer_id = ?
    """, (customer_id,))
    total_payment = cursor.fetchone()[0]
    conn.close()
    return total_payment


def pending_history(customer_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, amount, payment_date
        FROM payments
        WHERE customer_id = ?
        ORDER BY id DESC
    """, (customer_id,))
    payments = cursor.fetchall()
    conn.close()
    return payments

def customer_udhar_history(customer_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, item_name, quantity, amount, due_date, created_at
        FROM udhaar
        WHERE customer_id = ?
        ORDER BY id DESC
    """, (customer_id,))
    udhaar = cursor.fetchall()
    conn.close()
    return udhaar

def total_udhar_amount(customer_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM udhaar
        WHERE customer_id = ?
    """, (customer_id,))
    total_amount = cursor.fetchone()[0]
    conn.close()
    return total_amount

def get_all_customers():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            c.id, 
            c.name, 
            c.mobile, 

            COALESCE((
                SELECT SUM(u.amount)
                FROM udhaar u
                WHERE u.customer_id = c.id
            ), 0) AS total_udhaar, 

            COALESCE((
                SELECT SUM(p.amount)
                FROM payments p
                WHERE p.customer_id = c.id
            ), 0) AS total_paid

        FROM customers c
        WHERE c.status = 'pending'
        ORDER BY c.name ASC
    """)

    customers = cursor.fetchall()
    conn.close()
    return customers
def update_customer(customer_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE customers
        SET status = 'completed'
        WHERE id = ?
    """, (customer_id,))
    conn.commit()
    conn.close()


def get_by_customer_id(customer_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, customer_code, name, mobile, status
        FROM customers
        WHERE id = ?
    """, (customer_id,))

    customer = cursor.fetchone()

    conn.close()

    return customer

def get_all_completedcustomers():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            c.id, 
            c.customer_code, 
            c.name, 
            c.mobile, 

            COALESCE((
                SELECT SUM(u.amount)
                FROM udhaar u
                WHERE u.customer_id = c.id
            ), 0) AS total_udhaar, 

            COALESCE((
                SELECT SUM(p.amount)
                FROM payments p
                WHERE p.customer_id = c.id
            ), 0) AS total_paid,

            COALESCE((
                SELECT SUM(u.amount)
                FROM udhaar u
                WHERE u.customer_id = c.id
            ), 0)
            -
            COALESCE((
                SELECT SUM(p.amount)
                FROM payments p
                WHERE p.customer_id = c.id
            ), 0) AS remaining

        FROM customers c
        WHERE c.status = 'completed'
        ORDER BY c.name ASC
    """)

    customers = cursor.fetchall()
    conn.close()

    return customers



def get_all_pendingcustomers():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.id,
            c.customer_code,
            c.name,
            c.mobile,

            COALESCE((
                SELECT SUM(u.amount)
                FROM udhaar u
                WHERE u.customer_id = c.id
            ), 0) AS total_udhaar,

            COALESCE((
                SELECT SUM(p.amount)
                FROM payments p
                WHERE p.customer_id = c.id
            ), 0) AS total_paid,

            (
                COALESCE((
                    SELECT SUM(u.amount)
                    FROM udhaar u
                    WHERE u.customer_id = c.id
                ), 0)
                -
                COALESCE((
                    SELECT SUM(p.amount)
                    FROM payments p
                    WHERE p.customer_id = c.id
                ), 0)
            ) AS pending,

            (
                SELECT MAX(p.payment_date)
                FROM payments p
                WHERE p.customer_id = c.id
            ) AS last_transaction

        FROM customers c

        WHERE
            (
                COALESCE((
                    SELECT SUM(u.amount)
                    FROM udhaar u
                    WHERE u.customer_id = c.id
                ), 0)
                -
                COALESCE((
                    SELECT SUM(p.amount)
                    FROM payments p
                    WHERE p.customer_id = c.id
                ), 0)
            ) > 0

        ORDER BY c.name ASC
    """)

    customers = cursor.fetchall()
    conn.close()

    return customers


def total_count_customer():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM customers")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def total_count_completedcustomer():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM customers where status = 'completed'")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def total_pending_customer():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM customers where status = 'pending'")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def total_pending_amount():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(
            COALESCE((SELECT SUM(u.amount)
                      FROM udhaar u
                      WHERE u.customer_id = c.id), 0)
            -
            COALESCE((SELECT SUM(p.amount)
                      FROM payments p
                      WHERE p.customer_id = c.id), 0)
        )
        FROM customers c
        WHERE c.status = 'pending'
    """)

    result = cursor.fetchone()[0] or 0

    conn.close()
    return result

def get_all_history():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.name AS customer_name,
            DATE(u.created_at) AS date,
            TIME(u.created_at) AS time,
            'Udhaar' AS type,
            u.item_name AS description,
            u.amount AS amount,
            0 AS paid,
            u.amount AS remaining
        FROM udhaar u
        JOIN customers c ON u.customer_id = c.id

        UNION ALL

        SELECT
            c.name AS customer_name,
            DATE(p.payment_date) AS date,
            TIME(p.payment_date) AS time,
            'Payment' AS type,
            'Payment Received' AS description,
            p.amount AS amount,
            p.amount AS paid,
            0 AS remaining
        FROM payments p
        JOIN customers c ON p.customer_id = c.id

        ORDER BY date DESC, time DESC
    """)

    history = cursor.fetchall()
    conn.close()

    return history

def shopkeeper_login(email,password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shopkeepers WHERE email = ? AND password = ?", (email, password))
    shopkeeper = cursor.fetchone()
    conn.close()
    return shopkeeper

def get_shopkeeper_by_id(shopkeeper_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shopkeepers WHERE id = ?", (shopkeeper_id,))
    shopkeeper = cursor.fetchone()
    conn.close()
    return shopkeeper

def update_profile(shopkeeper_id, shopkeeper_name, shop_name, mobile_number, email):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE shopkeepers
        SET shopkeeper_name = ?,
            shop_name = ?,
            phone_number = ?,
            email = ?
        WHERE id = ?
    """, (
        shopkeeper_name,
        shop_name,
        mobile_number,
        email,
        shopkeeper_id
    ))

    conn.commit()
    conn.close()

def change_password(shopkeeper_id, current_password, new_password):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE shopkeepers SET password = ? WHERE id = ?",
        (new_password, shopkeeper_id)
    )

    conn.commit()
    conn.close()

    return True