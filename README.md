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
from customers_crud import add_customer, list_customers

add_customer("Rahul Mehra", "9812345678", "Jaipur")
list_customers()


---

