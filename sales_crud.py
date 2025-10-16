from db_connect import create_connection
from datetime import date
from tabulate import tabulate


def add_sale(customer_id, item_id, quantity, total, payment_method="Cash", amount_paid=None, amount_due=None, payment_status="Pending"):
    print(f"add_sale CALLED: customer_id={customer_id}, item_id={item_id}, quantity={quantity}, total={total}")

    # 1. Early ID and quantity checks
    if not isinstance(customer_id, int) or customer_id <= 0:
        print("Error: Invalid customer ID.")
        return
    if not isinstance(item_id, int) or item_id <= 0:
        print("Error: Invalid item ID.")
        return
    if not isinstance(quantity, int) or quantity <= 0:
        print("Error: Quantity must be a positive integer.")
        return
    if total is None or total < 0:
        print("Error: Total cannot be negative or None.")
        return

    # 2. Set defaults first
    if amount_paid is None:
        amount_paid = total
    if amount_due is None:
        amount_due = total - amount_paid

    # 3. Then check for negative values
    if amount_paid < 0 or amount_due < 0:
        print("Error: Financial values cannot be negative.")
        return

    # 4. DB logic with step-by-step prints
    conn = None
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()

            print("[DEBUG] Querying stock for item_id:", item_id)
            cursor.execute("SELECT quantity_in_stock FROM materials WHERE id = %s", (item_id,))
            result = cursor.fetchone()
            print("[DEBUG] Material row for stock:", result)
            if not result:
                print(f"Error: Material with ID {item_id} not found.")
                return
            current_stock = result[0]
            print(f"[DEBUG] Stock before sale: {current_stock}")
            if current_stock < quantity:
                print(f"Error: Not enough stock. Only {current_stock} units available.")
                return

            # Insert the sale
            sql = '''
                INSERT INTO sales (customer_id, item_id, quantity, sale_date, total,
                                   payment_method, amount_paid, amount_due, payment_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            values = (customer_id, item_id, quantity, date.today(), total,
                      payment_method, amount_paid, amount_due, payment_status)
            print("[DEBUG] Inserting sale:", values)
            cursor.execute(sql, values)

            # Update material stock
            print(f"[DEBUG] Decrementing stock by {quantity} for item_id {item_id}")
            cursor.execute(
                "UPDATE materials SET quantity_in_stock = quantity_in_stock - %s WHERE id = %s",
                (quantity, item_id)
            )
            conn.commit()

            cursor.execute("SELECT quantity_in_stock FROM materials WHERE id=%s", (item_id,))
            new_stock = cursor.fetchone()[0]
            print(f"Sale recorded for customer ID {customer_id} and stock updated.")
            print(f"[DEBUG] Stock after sale: {new_stock}")

    except Exception as e:
        print(f"Database error during add_sale: {e}")
        if conn:
            conn.rollback()
            print("Transaction rolled back due to error.")
    finally:
        if conn:
            conn.close()





def list_sales():
    conn = None
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.order_no, c.customer_name, m.item_name, s.quantity, s.sale_date, s.total,
                       s.payment_method, s.amount_paid, s.amount_due, s.payment_status
                FROM sales s
                JOIN customers c ON s.customer_id = c.customer_id
                JOIN materials m ON s.item_id = m.id
            """)
            rows = cursor.fetchall()
            headers = ["OrderNo", "Customer", "Item", "Qty", "Date", "Total", "Payment", "Paid", "Due", "Status"]
            print(tabulate(rows, headers=headers, tablefmt="grid"))
    except Exception as e:
        print(f"Database error during list_sales: {e}")
    finally:
        if conn:
            conn.close()


def popular_items():
    conn = None
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.item_name, SUM(s.quantity) as total_sold
                FROM sales s JOIN materials m ON s.item_id = m.id
                GROUP BY m.item_name
                ORDER BY total_sold DESC
                LIMIT 5
            """)
            rows = cursor.fetchall()
            print("Top-Selling Items:")
            for item, sold in rows:
                print(f"{item}: {sold} units")
    except Exception as e:
        print(f"Database error during popular_items: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    # Test with valid customer and item IDs
    add_sale(
        customer_id=1,    # Amit Kumar
        item_id=1,        # Cement
        quantity=10,
        total=3900.0,
        payment_method="Cash",
        amount_paid=2000.0,
        amount_due=1900.0,
        payment_status="Partially Paid"
    )
    add_sale(customer_id=1, item_id=1, quantity=10, total=3900.0, payment_method="Cash", amount_paid=2000.0, amount_due=1900.0, payment_status="Partially Paid")
    add_sale(customer_id=2, item_id=2, quantity=5, total=23000.0, payment_method="Credit", amount_paid=23000.0, amount_due=0.0, payment_status="Paid")
    add_sale(customer_id=1, item_id=5, quantity=8, total=360.0, payment_method="Cash", amount_paid=360.0, amount_due=0.0, payment_status="Paid")
    list_sales()
    popular_items()
