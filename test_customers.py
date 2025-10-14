import pytest
from customers_crud import add_customer, list_customers, update_customer, delete_customer
from suppliers_crud import add_supplier, list_suppliers, update_supplier, delete_supplier
from db_connect import create_connection

@pytest.fixture(scope='function')
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
    
def test_add_supplier_valid(db_conn):
    """Should allow proper supplier addition and persist to database."""
    add_supplier("Test Supplier", "9123456780", "Test City")
    cursor = db_conn.cursor()
    cursor.execute("SELECT supplier_name, phone FROM suppliers WHERE phone=%s", ("9123456780",))
    result = cursor.fetchone()
    assert result is not None
    assert result[0] == "Test Supplier"
    assert result[1] == "9123456780"

def test_add_supplier_invalid_phone(db_conn):
    """Should block addition of supplier with invalid phone number."""
    add_supplier("Invalid Supplier", "badnum", "Nowhere")
    cursor = db_conn.cursor()
    cursor.execute("SELECT supplier_name FROM suppliers WHERE supplier_name=%s", ("Invalid Supplier",))
    result = cursor.fetchone()
    assert result is None  # Should NOT be inserted

def test_update_supplier(db_conn):
    # Setup: ensure supplier exists for this test
    add_supplier("Supplier To Update", "9123456880", "Initial City")
    cursor = db_conn.cursor()
    cursor.execute("SELECT supplier_id FROM suppliers WHERE phone=%s", ("9123456880",))
    row = cursor.fetchone()
    cursor.close()
    assert row is not None, "No supplier found to update with phone 9123456880"
    supp_id = row[0]

    update_supplier(supp_id, phone="9800000000")
    db_conn.commit()

    # New cursor for new query
    cursor2 = db_conn.cursor()
    cursor2.execute("SELECT phone FROM suppliers WHERE supplier_id=%s", (supp_id,))
    result = cursor2.fetchone()
    cursor2.close()
    assert result is not None, "No supplier found with updated id"
    assert result[0] == "9800000000"

def test_delete_supplier(db_conn):
    # Setup: ensure supplier exists
    add_supplier("Supplier To Delete", "9755555555", "Delete City")
    cursor = db_conn.cursor()
    cursor.execute("SELECT supplier_id FROM suppliers WHERE phone=%s", ("9755555555",))
    row = cursor.fetchone()
    cursor.close()
    assert row is not None, "Test supplier for delete not present"
    supp_id = row[0]

    delete_supplier(supp_id)

    fresh_conn = create_connection()
    fresh_cursor = fresh_conn.cursor()
    fresh_cursor.execute("SELECT * FROM suppliers WHERE supplier_id=%s", (supp_id,))
    result = fresh_cursor.fetchone()
    fresh_cursor.close()
    fresh_conn.close()
    assert result is None
