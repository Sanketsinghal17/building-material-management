# Building Material Management System

This project manages materials, sales, and analytics for a shop using Python and MySQL.
Progress will be tracked daily here.

## Customer Management Module

This module allows you to add, view, and manage customer information.

### Features

- Add new customers with name, phone number, and address.
- View all customer records in a formatted list.
- (Planned) Edit and delete customer details.

### How to Use

1. **Run the script**  
   Execute `customers_crud.py` with Python:


2. **Sample Usage in Script**
- The script demonstrates adding two customers and then listing all customers present in the database.

3. **Expected Output**
ID | Name | Phone | Address
1 | Amit Kumar | 9991122334 | Delhi
2 | Priya Singh | 9876543210 | Noida


### Code Sample
from customers_crud import add_customer, list_customers, update_customer, delete_customer

add_customer("Rahul Mehra", "9812345678", "Jaipur")
list_customers()
update_customer(1, phone="9111111111")
delete_customer(2)
list_customers()

## Supplier Management Module

This module handles supplier records and links suppliers with materials.

### Features
- Add, view, update, and delete suppliers.
- Link suppliers to materials supplied.

### How to Use

1. **Run the suppliers CRUD script:**
    python suppliers_crud.py

2. **Example operations:**
- Add suppliers.
- Update and delete suppliers.
- List suppliers.

3. **Expected Output Example:**
ID | Name              | Phone       | Address
-----------------------------------------------
1  | Mohan Traders     | 9812211223  | Kolkata
2  | SR Building Supply| 8799912345  | Mumbai

## Materials Module Update

Materials are linked to suppliers with a foreign key to track sourcing.

### Updated Add Material Function
Add a material specifying supplier ID:

add_material("Cement", 50.0, "kg", 1000, supplier_id=1)

## Sales Module Update

Sales now use customer_id foreign key for data integrity and show customer and item names in listings.

### How to Use

add_sale(customer_id=1, item_id=1, quantity=10, total=3900.0,
         payment_method="Cash", amount_paid=2000.0, amount_due=1900.0,
         payment_status="Partially Paid")
list_sales()

### Improved Listing
Sales are displayed in a formatted table with meaningful columns like Customer, Item, Quantity, Date, etc.

## Inventory Alerts & Low Stock Notifications

This feature helps monitor the stock levels of materials. It alerts you when any material's quantity in stock drops below a threshold.

### How to Use

show_low_stock()      #Shows all items with quantity <= 20
show_low_stock(10)    # Custom threshold, e.g. items with quantity <= 10

### Expected Output Example:

Low Stock Alert!
Cement: 15 units left
Bricks: 7 units left

## Sales Analytics

Analytics tools provide a quick overview of your shop’s sales performance, highlighting top-selling products.

### How to Use

popular_items()       # Lists top 5 selling materials

### Expected Output Example:

Top-Selling Items:
Bricks: 120 units
Tiles (Box of 10): 95 units
Cement: 80 units

## Validation & Error Handling
All CRUD operations now include input validation and transaction-safe error handling.
- Customers: validates non-empty name and 10-digit phone before insert/update.
- Suppliers: validates non-empty name and 10-digit phone before insert/update.
- Materials: validates non-empty name and non-negative price/quantity.
- Sales: validates IDs, quantity > 0, non-negative amounts; checks stock before sale; inserts sale and decrements stock in a single transaction with rollback on failure.

## Search Features
Quick search using partial names:
- Suppliers:
    from suppliers_crud import search_supplier
    search_supplier("Moh")
- Materials:
    from materials_crud import search_material
    search_material("Cem")


## Running the App (CLI examples)
- Customers
    from customers_crud import add_customer, list_customers, update_customer, delete_customer
    add_customer("Test User", "1234567890", "Test Address")
    list_customers()
    update_customer(1, name="Test User Updated")
    delete_customer(1)
- Suppliers
    from suppliers_crud import add_supplier, list_suppliers, search_supplier
    add_supplier("Mohan Traders", "9812211223", "Kolkata")
    list_suppliers()
    search_supplier("Moh")
- Materials
    from materials_crud import add_material, list_materials, search_material, show_low_stock
    add_material("Cement", 390.0, "quintal", 100, 1)
    list_materials()
    search_material("Cem")
    show_low_stock(20)
- Sales
    from sales_crud import add_sale, list_sales, popular_items
    add_sale(1, 1, 10, 3900.0, "Cash", amount_paid=2000.0, amount_due=1900.0, payment_status="Partially Paid")
    list_sales()
    popular_items()


## Testing
This project uses pytest.

### Install
pip install pytest

### Run all tests
pytest


### Run a single test file
If tests are in the root:
    pytest test_customers.py

If tests are inside a tests/ folder:
    pytest tests/test_customers.py


### Notes
- Some tests open a fresh DB connection after an update/delete to ensure committed state is visible.
- Use a separate test database to avoid altering production data.

## Day 9 Progress
- Added validation and error handling across Customers, Suppliers, Materials, Sales.
- Implemented search for Suppliers and Materials.
- Wrote basic unit tests for Customers.
- Fixed transaction visibility in tests by using fresh connections after write operations.

## Dashboard Section
Show how to run it with different arguments:

python dashboard.py
python dashboard.py --threshold 10 --days 30

## Low-stock Reporting
Exporting a CSV and notifications:

    from materials_crud import export_low_stock_csv, notify_low_stock
    export_low_stock_csv(threshold=10)
    notify_low_stock(20)
    Or, if you have the CLI:

python materials_tools.py export --threshold 15
python materials_tools.py notify --threshold 10

## Analytics Section
Daily/period/top customers via CLI:

python analytics_cli.py daily --days 7
python analytics_cli.py period --start 2025-10-01 --end 2025-10-31
python analytics_cli.py top --limit 5

Or, direct function use:

    from analytics import sales_by_day, revenue_period, top_customers
    sales_by_day(7)
    revenue_period("2025-10-01", "2025-10-31")
    top_customers(5)

