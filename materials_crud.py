import csv
from db_connect import create_connection
from tabulate import tabulate
from datetime import datetime


def add_material(item_name, price_per_unit, unit_type, quantity, supplier_id):
    conn = None
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            sql = """
                INSERT INTO materials (item_name, price_per_unit, unit_type, quantity_in_stock, supplier_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (item_name, price_per_unit, unit_type, quantity, supplier_id)
            cursor.execute(sql, values)
            conn.commit()
            print(f"Material {item_name} added with supplier ID {supplier_id}!")
    except Exception as e:
        print(f"Database error during add_material: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def list_materials():
    conn = None
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, item_name, price_per_unit, unit_type, quantity_in_stock FROM materials")
            rows = cursor.fetchall()
            print("ID | Name                 | Price   | Unit    | Quantity")
            print("---|----------------------|---------|---------|---------")
            for row in rows:
                print(f"{row[0]:<3}| {row[1]:<20} | {row[2]:<7} | {row[3]:<7} | {row[4]}")
    except Exception as e:
        print(f"Database error during list_materials: {e}")
    finally:
        if conn:
            conn.close()

def search_material(name):
    conn = None
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, item_name, price_per_unit, unit_type, quantity_in_stock FROM materials WHERE item_name LIKE %s",
                (f"%{name}%",)
            )
            rows = cursor.fetchall()
            if rows:
                print(tabulate(rows, headers=["ID", "Name", "Price", "Unit", "Quantity"], tablefmt="grid"))
            else:
                print(f"No materials found matching: {name}")
    except Exception as e:
        print(f"Database error during search_material: {e}")
    finally:
        if conn:
            conn.close()

def update_material(id, price=None, quantity=None):
    conn = None
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            if price is not None:
                cursor.execute("UPDATE materials SET price_per_unit=%s WHERE id=%s", (price, id))
            if quantity is not None:
                cursor.execute("UPDATE materials SET quantity_in_stock=%s WHERE id=%s", (quantity, id))
            conn.commit()
            print(f"Material ID {id} updated!")
    except Exception as e:
        print(f"Database error during update_material: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def delete_material(id):
    conn = None
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM materials WHERE id=%s", (id,))
            conn.commit()
            print(f"Material ID {id} deleted!")
    except Exception as e:
        print(f"Database error during delete_material: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def show_low_stock(threshold=20):
    conn = None
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT item_name, quantity_in_stock FROM materials WHERE quantity_in_stock <= %s",
                (threshold,)
            )
            rows = cursor.fetchall()
            if rows:
                print("Low Stock Alert!")
                for item, qty in rows:
                    print(f"{item}: {qty} units left")
            else:
                print("All stocks are sufficient.")
    except Exception as e:
        print(f"Database error during show_low_stock: {e}")
    finally:
        if conn:
            conn.close()

def export_low_stock_csv(path=None, threshold=20):
    """Exports low stock materials (below threshold) to a CSV file."""
    """
    Export low stock materials to a CSV.
    Columns: item_name, quantity_in_stock, unit_type, supplier_id
    """
    conn = None
    try:
        if path is None:
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = f"low_stock_{threshold}_{stamp}.csv"

        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT item_name, quantity_in_stock, unit_type, supplier_id
                FROM materials
                WHERE quantity_in_stock <= %s
                ORDER BY quantity_in_stock ASC, item_name ASC
            """, (threshold,))
            rows = cursor.fetchall()

            if not rows:
                print(f"No items at or below threshold {threshold}. CSV not created.")
                return None

            with open(path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["item_name", "quantity_in_stock", "unit_type", "supplier_id"])
                writer.writerows(rows)

            print(f"Low stock report saved to {path}")
            return path
    except Exception as e:
        print(f"Error during export_low_stock_csv: {e}")
        return None
    finally:
        if conn:
            conn.close()

def notify_low_stock(threshold=20, channel="stdout"):
    """
    Notification stub. For now, prints to stdout.
    Extend later to email/Slack/SMS by implementing those channels.
    """
    conn = None
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT item_name, quantity_in_stock
                FROM materials
                WHERE quantity_in_stock <= %s
                ORDER BY quantity_in_stock ASC, item_name ASC
            """, (threshold,))
            rows = cursor.fetchall()

            if not rows:
                print(f"No low-stock items at or below {threshold}.")
                return

            if channel == "stdout":
                print(f"Low-stock items (≤{threshold}):")
                for name, qty in rows:
                    print(f"- {name}: {qty} units remaining")
            else:
                # Placeholder for future channels (e.g., 'email', 'slack')
                print(f"[{channel}] Notification channel not configured yet.")
    except Exception as e:
        print(f"Error during notify_low_stock: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    materials = [
        ("Cement", 390.00, "quintal", 100, 1),
        ("Steel Rod", 4600.00, "quintal", 30, 2),
        ("Sand", 115.00, "quintal", 250, 1),
        ("Bricks", 9.00, "piece", 8000, 3),
        ("Concrete Blocks", 45.00, "piece", 2000, 2),
        ("Crushed Stone Chips", 70.00, "quintal", 180, 3),
        ("Plywood", 1200.00, "sheet", 250, 1),
        ("Marble Slab", 1500.00, "slab", 100, 2),
        ("Paint (20L)", 2100.00, "tin", 40, 3),
        ("Tiles (Box of 10)", 650.00, "box", 300, 1),
    ]
    for m in materials:
        add_material(*m)
    
    list_materials()
    
    print("\nSearch Results for 'Cem':")
    search_material("Cem")
    show_low_stock()
    show_low_stock(10)
    from materials_crud import export_low_stock_csv, notify_low_stock
    export_low_stock_csv(threshold=20)          # creates timestamped CSV
    export_low_stock_csv("low_stock.csv", 10)   # custom path and threshold
    notify_low_stock(15)                        # prints low stock list

