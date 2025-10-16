import pytest
from customers_crud import add_customer, list_customers, update_customer, delete_customer
from suppliers_crud import add_supplier, list_suppliers, update_supplier, delete_supplier
from materials_crud import add_material, update_material, delete_material, show_low_stock
from sales_crud import add_sale, list_sales
from db_connect import create_connection

def ensure_test_data(db_conn):
    cursor = db_conn.cursor()
    try:
        # Disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        cursor.execute("TRUNCATE TABLE sales")
        cursor.execute("TRUNCATE TABLE materials")
        cursor.execute("TRUNCATE TABLE customers")
        cursor.execute("TRUNCATE TABLE suppliers")
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")
        # Now add fresh test data
        cursor.execute("""
            INSERT INTO suppliers (supplier_id, supplier_name, phone, address)
            VALUES (1, 'Test Supplier', '1234567890', 'Test Address')
        """)
        cursor.execute("""
            INSERT INTO customers (customer_id, customer_name, phone, address)
            VALUES (1, 'Test Customer', '9876543210', 'Test Address')
        """)
        cursor.execute("""
            INSERT INTO materials (id, item_name, price_per_unit, unit_type, quantity_in_stock, supplier_id)
            VALUES (1, 'Test Material', 50.0, 'pcs', 100, 1)
        """)
        db_conn.commit()
    finally:
        cursor.close()


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

def test_add_material_valid(db_conn):
    # Safely remove all prior "Test Material" before insert to avoid confusion
    cursor = db_conn.cursor(buffered=True)
    cursor.execute("DELETE FROM materials WHERE item_name=%s", ("Test Material",))
    db_conn.commit()

    add_material("Test Material", 250.0, "kg", 50, supplier_id=1)
    cursor.execute("SELECT item_name, quantity_in_stock FROM materials WHERE item_name=%s ORDER BY id DESC LIMIT 1", ("Test Material",))
    row = cursor.fetchone()
    cursor.close()
    assert row is not None
    assert row[0] == "Test Material"
    assert row[1] == 50



def test_update_material(db_conn):
    add_material("Material For Update", 120.0, "kg", 10, supplier_id=1)
    cursor = db_conn.cursor(buffered=True)
    cursor.execute("SELECT id FROM materials WHERE item_name=%s", ("Material For Update",))
    row = cursor.fetchone()
    assert row is not None
    mat_id = row[0]
    cursor.close()

    update_material(mat_id, price=99.0)
    db_conn.commit()

    cursor2 = db_conn.cursor(buffered=True)
    cursor2.execute("SELECT price_per_unit FROM materials WHERE id=%s", (mat_id,))
    result = cursor2.fetchone()
    cursor2.close()
    assert result is not None
    assert float(result[0]) == 99.0


def test_delete_material(db_conn):
    add_material("Material For Delete", 10.0, "kg", 2, supplier_id=1)
    cursor = db_conn.cursor(buffered=True)
    cursor.execute("SELECT id FROM materials WHERE item_name=%s", ("Material For Delete",))
    row = cursor.fetchone()
    assert row is not None
    mat_id = row[0]
    cursor.close()

    delete_material(mat_id)

    fresh_conn = create_connection()
    fresh_cursor = fresh_conn.cursor(buffered=True)
    fresh_cursor.execute("SELECT * FROM materials WHERE id=%s", (mat_id,))
    result = fresh_cursor.fetchone()
    fresh_cursor.close()
    fresh_conn.close()
    assert result is None


def test_show_low_stock(db_conn):
    from materials_crud import add_material, show_low_stock
    add_material("LowStockTest", 30.0, "kg", 3, supplier_id=1)
    items = show_low_stock(5)
    assert items is not None, "show_low_stock should not return None"
    names = [item['item_name'] for item in items if 'item_name' in item]
    assert "LowStockTest" in names
    
def test_add_sale_valid(db_conn):
    ensure_test_data(db_conn)
    add_sale(customer_id=1, item_id=1, quantity=5, total=250.0, payment_method="Cash", amount_paid=150.0, amount_due=100.0, payment_status="Partial")
    cursor = db_conn.cursor(buffered=True, dictionary=True)
    cursor.execute("SELECT * FROM sales WHERE customer_id=%s AND item_id=%s ORDER BY order_no DESC LIMIT 1", (1, 1))
    sale = cursor.fetchone()
    cursor.close()
    assert sale is not None
    assert sale["quantity"] == 5
    assert float(sale["total"]) == 250.0
    assert sale["payment_method"] == "Cash"
    assert float(sale["amount_paid"]) == 150.0
    assert float(sale["amount_due"]) == 100.0
    assert sale["payment_status"] == "Partial"

def test_stock_decrement_on_sale(db_conn):
    ensure_test_data(db_conn)
    cursor = db_conn.cursor(buffered=True, dictionary=True)
    cursor.execute("SELECT quantity_in_stock FROM materials WHERE id=%s", (1,))
    before = cursor.fetchone()['quantity_in_stock']
    add_sale(customer_id=1, item_id=1, quantity=3, total=150.0)
    cursor.execute("SELECT quantity_in_stock FROM materials WHERE id=%s", (1,))
    after = cursor.fetchone()['quantity_in_stock']
    cursor.close()
    assert after == before - 3




def test_add_sale_invalid_customer(db_conn):
    ensure_test_data(db_conn)
    add_sale(customer_id=-1, item_id=1, quantity=2, total=100)
    cursor = db_conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM sales WHERE customer_id=-1")
    row = cursor.fetchone()
    cursor.close()
    assert row is None

def test_add_sale_invalid_item(db_conn):
    ensure_test_data(db_conn)
    add_sale(customer_id=1, item_id=-1, quantity=2, total=100)
    cursor = db_conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM sales WHERE item_id=-1")
    row = cursor.fetchone()
    cursor.close()
    assert row is None

def test_add_sale_insufficient_stock(db_conn):
    ensure_test_data(db_conn)
    cursor = db_conn.cursor(buffered=True)
    cursor.execute("SELECT quantity_in_stock FROM materials WHERE id=%s", (1,))
    stock = cursor.fetchone()
    quantity = stock[0] + 100 if stock and stock[0] is not None else 9999
    add_sale(customer_id=1, item_id=1, quantity=quantity, total=9999)
    cursor.execute("SELECT * FROM sales WHERE quantity=%s ORDER BY order_no DESC LIMIT 1", (quantity,))
    row = cursor.fetchone()
    cursor.close()
    assert row is None

def test_list_sales_output(db_conn, capsys):
    ensure_test_data(db_conn)
    add_sale(customer_id=1, item_id=1, quantity=1, total=50)
    list_sales()
    captured = capsys.readouterr()
    assert "Customer" in captured.out
    assert "Qty" in captured.out
