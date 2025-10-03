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


---

