from db_connect import create_connection

def add_supplier(name, phone, address):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO suppliers (supplier_name, phone, address) VALUES (%s, %s, %s)",
            (name, phone, address)
        )
        conn.commit()
        print(f"Supplier added: {name}")
        conn.close()

def list_suppliers():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT supplier_id, supplier_name, phone, address FROM suppliers")
        rows = cursor.fetchall()
        print("ID | Name          | Phone       | Address")
        print("----------------------------------------------")
        for row in rows:
            print(row)
        conn.close()
        
def update_supplier(supplier_id, name=None, phone=None, address=None):
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
        if not updates:
            print("Nothing to update.")
            return
        sql = "UPDATE suppliers SET " + ", ".join(updates) + " WHERE supplier_id=%s"
        values.append(supplier_id)
        cursor.execute(sql, tuple(values))
        conn.commit()
        print(f"Supplier {supplier_id} updated.")
        conn.close()

def delete_supplier(supplier_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM suppliers WHERE supplier_id=%s", (supplier_id,))
        conn.commit()
        print(f"Supplier {supplier_id} deleted.")
        conn.close()


if __name__ == "__main__":
    add_supplier("Mohan Traders", "9812211223", "Kolkata")
    add_supplier("SR Building Supply", "8799912345", "Mumbai")
    update_supplier(1, phone="9000000000", address="Delhi")

    # Delete supplier
    delete_supplier(2)
    list_suppliers()
