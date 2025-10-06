from db_connect import create_connection
import re
from tabulate import tabulate

def add_supplier(name, phone, address):
    if not name.strip():
        print("Error: Supplier name cannot be empty.")
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
                "INSERT INTO suppliers (supplier_name, phone, address) VALUES (%s, %s, %s)",
                (name, phone, address)
            )
            conn.commit()
            print(f"Supplier added: {name}")
    except Exception as e:
        print(f"Database error during add_supplier: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def list_suppliers():
    conn = None
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT supplier_id, supplier_name, phone, address FROM suppliers")
            rows = cursor.fetchall()
            print("ID | Name          | Phone       | Address")
            print("----------------------------------------------")
            for row in rows:
                print(row)
    except Exception as e:
        print(f"Database error during list_suppliers: {e}")
    finally:
        if conn:
            conn.close()

def search_supplier(name):
    conn = None
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT supplier_id, supplier_name, phone, address FROM suppliers WHERE supplier_name LIKE %s",
                (f"%{name}%",)
            )
            rows = cursor.fetchall()
            if rows:
                print(tabulate(rows, headers=["ID", "Name", "Phone", "Address"], tablefmt="grid"))
            else:
                print(f"No suppliers found matching: {name}")
    except Exception as e:
        print(f"Database error during search_supplier: {e}")
    finally:
        if conn:
            conn.close()

def update_supplier(supplier_id, name=None, phone=None, address=None):
    if phone is not None and not re.match(r"^\d{10}$", phone):
        print("Error: Phone number must be exactly 10 digits.")
        return
    if name is not None and not name.strip():
        print("Error: Supplier name cannot be empty.")
        return

    if not any([name, phone, address]):
        print("Nothing to update.")
        return

    conn = None
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            updates = []
            values = []
            if name:
                updates.append("supplier_name=%s")
                values.append(name)
            if phone:
                updates.append("phone=%s")
                values.append(phone)
            if address:
                updates.append("address=%s")
                values.append(address)
            sql = "UPDATE suppliers SET " + ", ".join(updates) + " WHERE supplier_id=%s"
            values.append(supplier_id)
            cursor.execute(sql, tuple(values))
            conn.commit()
            print(f"Supplier {supplier_id} updated.")
    except Exception as e:
        print(f"Database error during update_supplier: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def delete_supplier(supplier_id):
    conn = None
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM suppliers WHERE supplier_id=%s", (supplier_id,))
            conn.commit()
            print(f"Supplier {supplier_id} deleted.")
    except Exception as e:
        print(f"Database error during delete_supplier: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    add_supplier("Mohan Traders", "9812211223", "Kolkata")
    add_supplier("SR Building Supply", "8799912345", "Mumbai")
    update_supplier(1, phone="9000000000", address="Delhi")

    # Delete supplier
    delete_supplier(2)
    list_suppliers()
    print("\nSearch Results for 'Moh':")
    search_supplier("Moh")
