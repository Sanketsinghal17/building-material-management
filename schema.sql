CREATE DATABASE IF NOT EXISTS building_materials;
USE building_materials;

CREATE TABLE IF NOT EXISTS materials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(50) NOT NULL,
    price_per_unit DECIMAL(10,2) NOT NULL,
    unit_type VARCHAR(20) DEFAULT 'quintal',
    quantity_in_stock INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS sales (
    order_no INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(50),
    item_id INT,
    quantity INT,
    sale_date DATE,
    total DECIMAL(12,2),
    payment_method VARCHAR(20) DEFAULT 'Cash',
    amount_paid DECIMAL(12,2) DEFAULT 0,
    amount_due DECIMAL(12,2) DEFAULT 0,
    payment_status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (item_id) REFERENCES materials(id)
);

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(30) UNIQUE,
    password VARCHAR(100),
    role VARCHAR(20) DEFAULT 'staff'
);

/* Optional for Day 3 or later */
CREATE TABLE IF NOT EXISTS payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_no INT,
    payment_date DATE,
    payment_method VARCHAR(20),
    paid_amount DECIMAL(12,2),
    FOREIGN KEY (order_no) REFERENCES sales(order_no)
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(50) NOT NULL,
    phone VARCHAR(15),
    address VARCHAR(255)
);

