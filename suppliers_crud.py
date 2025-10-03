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
