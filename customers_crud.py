from db_connect import create_connection

def add_customer(name, phone, address):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO customers (customer_name, phone, address) VALUES (%s, %s, %s)",
            (name, phone, address)
        )
        conn.commit()
        print(f"Customer added: {name}")
        conn.close()

def list_customers():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT customer_id, customer_name, phone, address FROM customers")
        rows = cursor.fetchall()
        print("ID | Name       | Phone       | Address")
        print("--------------------------------------------")
        for row in rows:
            print(row)
        conn.close()

if __name__ == "__main__":
    add_customer("Amit Kumar", "9991122334", "Delhi")
    add_customer("Priya Singh", "9876543210", "Noida")
    list_customers()
