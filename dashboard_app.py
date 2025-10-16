import streamlit as st
import pandas as pd
from db_connect import create_connection
from customers_crud import add_customer, list_customers
from suppliers_crud import add_supplier, list_suppliers
from materials_crud import add_material, show_low_stock
from sales_crud import add_sale, list_sales

st.title("Building Material Management Dashboard")

menu = st.sidebar.selectbox(
    "Choose Action",
    ("Add Customer", "Add Supplier", "Add Material", "Make Sale", "Show Customers", "Show Suppliers", "Show Materials", "Show Low Stock", "Show Sales")
)

if menu == "Add Customer":
    name = st.text_input("Customer name")
    phone = st.text_input("Phone")
    address = st.text_input("Address")
    if st.button("Add Customer"):
        add_customer(name, phone, address)
        st.success("Customer added!")

if menu == "Add Supplier":
    name = st.text_input("Supplier name")
    phone = st.text_input("Phone")
    address = st.text_input("Address")
    if st.button("Add Supplier"):
        add_supplier(name, phone, address)
        st.success("Supplier added!")

if menu == "Add Material":
    name = st.text_input("Material name")
    price = st.number_input("Price per unit", min_value=0.0, step=1.0, format="%.2f")
    unit = st.text_input("Unit type")
    qty = st.number_input("Quantity", min_value=1, step=1)
    supp_id = st.number_input("Supplier ID", min_value=1, step=1)
    if st.button("Add Material"):
        add_material(name, price, unit, qty, supp_id)
        st.success("Material added!")

if menu == "Make Sale":
    cust_id = st.number_input("Customer ID", min_value=1, step=1)
    item_id = st.number_input("Material ID", min_value=1, step=1)
    qty = st.number_input("Quantity", min_value=1, step=1)
    total = st.number_input("Total Price", min_value=0.0, step=1.0)
    if st.button("Make Sale"):
        add_sale(int(cust_id), int(item_id), int(qty), float(total))
        st.success("Sale recorded!")

if menu == "Show Customers":
    conn = create_connection()
    df = pd.read_sql("SELECT * FROM customers", conn)
    st.write(df)
    conn.close()

if menu == "Show Suppliers":
    st.write("All suppliers:")
    list_suppliers()

if menu == "Show Materials":
    import pandas as pd
    from db_connect import create_connection
    conn = create_connection()
    df = pd.read_sql("SELECT * FROM materials", conn)
    st.write(df)
    conn.close()

if menu == "Show Low Stock":
    threshold = st.number_input("Stock threshold", min_value=1, step=1)
    if st.button("Show Low Stock"):
        st.write(show_low_stock(threshold))

if menu == "Show Sales":
    st.write("All sales:")
    list_sales()
    
    
