from db_connect import create_connection
import re

def add_customer(name, phone, address):
    if not name.strip():
        print("Error: Customer name cannot be empty.")
        return
    if not re.match(r"^\d{10}$", phone):
        print("Error: Phone number must be exactly 10 digits.")
        return
    conn = None
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO customers (customer_name, phone, address) VALUES (%s, %s, %s)",
                (name, phone, address)
            )
            conn.commit()
            print(f"Customer added: {name}")
    except Exception as e:
        print(f"Database error during add_customer: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()


def list_customers():
    conn = None
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT customer_id, customer_name, phone, address FROM customers")
            rows = cursor.fetchall()
            print("ID | Name       | Phone       | Address")
            print("--------------------------------------------")
            for row in rows:
                print(row)
    except Exception as e:
        print(f"Database error during list_customers: {e}")
    finally:
        if conn:
            conn.close()

def update_customer(customer_id, name=None, phone=None, address=None):
    if phone is not None and not re.match(r"^\d{10}$", phone):
        print("Error: Phone number must be exactly 10 digits.")
        return
    if name is not None and not name.strip():
        print("Error: Customer name cannot be empty.")
        return
    
    conn = None
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            updates = []
            values = []
            if name:
                updates.append("customer_name=%s")
                values.append(name)
            if phone:
                updates.append("phone=%s")
                values.append(phone)
            if address:
                updates.append("address=%s")
                values.append(address)
            if not updates:
                print("Nothing to update.")
                return
            query = "UPDATE customers SET " + ", ".join(updates) + " WHERE customer_id=%s"
            values.append(customer_id)
            cursor.execute(query, tuple(values))
            conn.commit()
            print(f"Customer {customer_id} updated.")
    except Exception as e:
        print(f"Database error during update_customer: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def delete_customer(customer_id):
    conn = None
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customers WHERE customer_id=%s", (customer_id,))
            conn.commit()
            print(f"Customer {customer_id} deleted.")
    except Exception as e:
        print(f"Database error during delete_customer: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def search_customer(name):
    conn = None
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT customer_id, customer_name, phone, address FROM customers WHERE customer_name LIKE %s", (f"%{name}%",))
            rows = cursor.fetchall()
            print("ID | Name       | Phone       | Address")
            print("--------------------------------------------")
            for row in rows:
                print(row)
    except Exception as e:
        print(f"Database error during search_customer: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    add_customer("Amit Kumar", "9991122334", "Delhi")
    add_customer("Priya Singh", "9876543210", "Noida")
    list_customers()
