from datetime import date, timedelta, datetime
from tabulate import tabulate
from db_connect import create_connection

def sales_by_day(limit_days=7):
    """Outputs per-day sales totals and revenue for the given number of recent days."""
    """
    Show total revenue per day for the last N days (including today).
    """
    if not isinstance(limit_days, int) or limit_days <= 0:
        print("limit_days must be a positive integer")
        return
    conn = None
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            since = date.today() - timedelta(days=limit_days - 1)
            cursor.execute("""
                SELECT DATE(sale_date) as day, IFNULL(SUM(total),0) as revenue
                FROM sales
                WHERE sale_date >= %s
                GROUP BY DATE(sale_date)
                ORDER BY day DESC
            """, (since,))
            rows = cursor.fetchall()
            if rows:
                print(tabulate(rows, headers=["Day", "Revenue"], tablefmt="grid"))
            else:
                print("No sales found in the selected period.")
    except Exception as e:
        print(f"Error in sales_by_day: {e}")
    finally:
        if conn:
            conn.close()

def revenue_period(start_date_str, end_date_str):
    """
    Show totals for a date range [start, end] inclusive.
    Dates must be in YYYY-MM-DD format.
    """
    conn = None
    try:
        # Validate and convert
        start_dt = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_dt = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        if start_dt > end_dt:
            print("start_date cannot be after end_date")
            return

        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    IFNULL(SUM(total),0) as total_revenue,
                    IFNULL(SUM(amount_paid),0) as total_paid,
                    IFNULL(SUM(amount_due),0) as total_due
                FROM sales
                WHERE sale_date BETWEEN %s AND %s
            """, (start_dt, end_dt))
            row = cursor.fetchone()
            print(tabulate([row], headers=["Revenue", "Paid", "Due"], tablefmt="grid"))
    except ValueError:
        print("Dates must be in YYYY-MM-DD format")
    except Exception as e:
        print(f"Error in revenue_period: {e}")
    finally:
        if conn:
            conn.close()

def top_customers(limit=5):
    """Lists the top N customers by total revenue."""
    if not isinstance(limit, int) or limit <= 0:
        print("limit must be a positive integer")
        return
    conn = None
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.customer_name, IFNULL(SUM(s.total),0) as revenue
                FROM sales s
                JOIN customers c ON s.customer_id = c.customer_id
                GROUP BY c.customer_name
                ORDER BY revenue DESC
                LIMIT %s
            """, (limit,))
            rows = cursor.fetchall()
            if rows:
                print(tabulate(rows, headers=["Customer", "Revenue"], tablefmt="grid"))
            else:
                print("No customer sales data available.")
    except Exception as e:
        print(f"Error in top_customers: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # Quick demo runs (comment/uncomment as needed)
    sales_by_day(7)
    revenue_period("2025-10-01", "2025-10-31")
    top_customers(5)
