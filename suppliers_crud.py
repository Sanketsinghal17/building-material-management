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

if __name__ == "__main__":
    add_supplier("Mohan Traders", "9812211223", "Kolkata")
    add_supplier("SR Building Supply", "8799912345", "Mumbai")
    list_suppliers()
