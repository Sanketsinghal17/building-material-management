import pytest
from customers_crud import add_customer, list_customers, update_customer, delete_customer
from db_connect import create_connection

@pytest.fixture(scope='module')
def db_conn():
    conn = create_connection()
    yield conn
    conn.close()

def test_add_customer_valid(db_conn):
    # Add a valid customer
    add_customer("Test User", "1234567890", "Test Address")
    cursor = db_conn.cursor()
    cursor.execute("SELECT customer_name FROM customers WHERE phone=%s", ("1234567890",))
    result = cursor.fetchone()
    assert result is not None
    assert result[0] == "Test User"

def test_add_customer_invalid_phone(db_conn):
    # This should not add to database and print error
    add_customer("User Invalid", "abc123", "Anywhere")
    cursor = db_conn.cursor()
    cursor.execute("SELECT customer_name FROM customers WHERE customer_name=%s", ("User Invalid",))
    result = cursor.fetchone()
    assert result is None  # Customer should not have been inserted

def test_update_customer(db_conn):
    cursor = db_conn.cursor()
    cursor.execute("SELECT customer_id FROM customers WHERE phone=%s", ("1234567890",))
    cust_id = cursor.fetchone()[0]
    update_customer(cust_id, name="Test User Updated")
    # CLOSE the cursor and start a fresh one for SELECT
    db_conn.commit()  # Make sure if needed, though commit is inside update_customer
    cursor = db_conn.cursor()
    cursor.execute("SELECT customer_name FROM customers WHERE customer_id=%s", (cust_id,))
    result = cursor.fetchone()
    assert result[0] == "Test User Updated"


def test_delete_customer(db_conn):
    # 1. Fetch customer ID
    cursor = db_conn.cursor()
    cursor.execute("SELECT customer_id FROM customers WHERE phone=%s", ("1234567890",))
    cust_id = cursor.fetchone()[0]
    
    # 2. Delete customer in separate transaction
    delete_customer(cust_id)
    
    # 3. Close and open a fresh connection for verification
    db_conn.close()
    fresh_conn = create_connection()
    fresh_cursor = fresh_conn.cursor()
    fresh_cursor.execute("SELECT * FROM customers WHERE customer_id=%s", (cust_id,))
    result = fresh_cursor.fetchone()
    fresh_conn.close()
    
    # 4. Now check result
    assert result is None