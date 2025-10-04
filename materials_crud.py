from db_connect import create_connection

def add_material(item_name, price_per_unit, unit_type, quantity, supplier_id):
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
        conn.close()


def list_materials():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, item_name, price_per_unit, unit_type, quantity_in_stock FROM materials")
        rows = cursor.fetchall()
        print("ID | Name                 | Price   | Unit    | Quantity")
        print("---|----------------------|---------|---------|---------")
        for row in rows:
            print(f"{row[0]:<3}| {row[1]:<20} | {row[2]:<7} | {row[3]:<7} | {row[4]}")
        conn.close()

def update_material(id, price=None, quantity=None):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        if price is not None:
            cursor.execute("UPDATE materials SET price_per_unit=%s WHERE id=%s", (price, id))
        if quantity is not None:
            cursor.execute("UPDATE materials SET quantity_in_stock=%s WHERE id=%s", (quantity, id))
        conn.commit()
        print(f"Material ID {id} updated!")
        conn.close()

def delete_material(id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM materials WHERE id=%s", (id,))
        conn.commit()
        print(f"Material ID {id} deleted!")
        conn.close()
        
def show_low_stock(threshold=20):
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
        conn.close()


if __name__ == "__main__":
    # Add sample materials
    materials = [
        ("Cement", 390.00, "quintal", 100),
        ("Steel Rod", 4600.00, "quintal", 30),
        ("Sand", 115.00, "quintal", 250),
        ("Bricks", 9.00, "piece", 8000),
        ("Concrete Blocks", 45.00, "piece", 2000),
        ("Crushed Stone Chips", 70.00, "quintal", 180),
        ("Plywood", 1200.00, "sheet", 250),
        ("Marble Slab", 1500.00, "slab", 100),
        ("Paint (20L)", 2100.00, "tin", 40),
        ("Tiles (Box of 10)", 650.00, "box", 300),
    ]
    for m in materials:
        add_material(*m)
    
    # List all materials
    list_materials()
    
    show_low_stock()        # uses default threshold of 20
    show_low_stock(10)      # custom threshold if you want


    # Example for updating material (uncomment to use)
    # update_material(1, price=400.00)       # update price of material with ID 1
    # update_material(1, quantity=90)        # update quantity of material with ID 1

    # Example for deleting material (uncomment to use)
    # delete_material(10)                    # delete material with ID 10
