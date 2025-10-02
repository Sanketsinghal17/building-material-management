from db_connect import create_connection
from datetime import date
from tabulate import tabulate

def add_sale(customer_id, item_id, quantity, total, payment_method="Cash", amount_paid=None, amount_due=None, payment_status="Pending"):
    from datetime import date
    if amount_paid is None:
        amount_paid = total
    if amount_due is None:
        amount_due = total - amount_paid

    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        sql = '''
            INSERT INTO sales (customer_id, item_id, quantity, sale_date, total,
                               payment_method, amount_paid, amount_due, payment_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        values = (customer_id, item_id, quantity, date.today(), total,
                  payment_method, amount_paid, amount_due, payment_status)
        cursor.execute(sql, values)
        conn.commit()
        print(f"Sale recorded for customer ID {customer_id}.")
        conn.close()


def list_sales():
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
    list_sales()


