import argparse
from db_connect import create_connection
from tabulate import tabulate
from datetime import date, timedelta

from datetime import date, timedelta

def show_dashboard(low_stock_threshold=20, last_n_days=0):
    conn = None
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()

            # Total counts
            cursor.execute("SELECT COUNT(*) FROM customers")
            customer_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM suppliers")
            supplier_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM materials")
            material_count = cursor.fetchone()[0]

            # Compute filter date if needed
            if last_n_days and last_n_days > 0:
                since = date.today() - timedelta(days=last_n_days)
                cursor.execute("SELECT IFNULL(SUM(total),0) FROM sales WHERE sale_date >= %s", (since,))
                total_revenue = cursor.fetchone()[0]
                cursor.execute("SELECT IFNULL(SUM(amount_due),0) FROM sales WHERE amount_due > 0 AND sale_date >= %s", (since,))
                unpaid_amount = cursor.fetchone()[0]
            else:
                cursor.execute("SELECT IFNULL(SUM(total),0) FROM sales")
                total_revenue = cursor.fetchone()[0]
                cursor.execute("SELECT IFNULL(SUM(amount_due),0) FROM sales WHERE amount_due > 0")
                unpaid_amount = cursor.fetchone()[0]

            # Low stock count
            cursor.execute("SELECT COUNT(*) FROM materials WHERE quantity_in_stock <= %s", (low_stock_threshold,))
            low_stock_count = cursor.fetchone()[0]

            # Top-selling items (apply same date filter if provided)
            if last_n_days and last_n_days > 0:
                cursor.execute("""
                    SELECT m.item_name, SUM(s.quantity) as total_sold
                    FROM sales s JOIN materials m ON s.item_id = m.id
                    WHERE s.sale_date >= %s
                    GROUP BY m.item_name
                    ORDER BY total_sold DESC
                    LIMIT 5
                """, (since,))
            else:
                cursor.execute("""
                    SELECT m.item_name, SUM(s.quantity) as total_sold
                    FROM sales s JOIN materials m ON s.item_id = m.id
                    GROUP BY m.item_name
                    ORDER BY total_sold DESC
                    LIMIT 5
                """)
            popular_items = cursor.fetchall()

            print("\n===== Business Dashboard Summary =====")
            print(tabulate([
                ["Customers", customer_count],
                ["Suppliers", supplier_count],
                ["Materials", material_count],
                ["Total Revenue", total_revenue],
                ["Total Unpaid", unpaid_amount],
                [f"Low Stock Items (≤{low_stock_threshold})", low_stock_count]
            ], headers=["Metric", "Value"], tablefmt="grid"))
            print("\nTop 5 Selling Items:")
            if popular_items:
                print(tabulate(popular_items, headers=["Item", "Total Sold"], tablefmt="grid"))
            else:
                print("No sales data available.")
    except Exception as e:
        print(f"Error generating dashboard: {e}")
    finally:
        if conn:
            conn.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=int, default=20, help="Low stock threshold")
    parser.add_argument("--days", type=int, default=0, help="Limit sales totals to last N days (0 = all time)")
    args = parser.parse_args()

    show_dashboard(low_stock_threshold=args.threshold, last_n_days=args.days)

if __name__ == "__main__":
    main()
