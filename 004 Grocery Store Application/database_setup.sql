-- Create Database
CREATE DATABASE IF NOT EXISTS grocery_store;
USE grocery_store;

-- Create UOM (Unit of Measurement) Table
CREATE TABLE IF NOT EXISTS uom (
    uom_id INT AUTO_INCREMENT PRIMARY KEY,
    uom_name VARCHAR(50) NOT NULL UNIQUE
);

-- Insert default UOM values
INSERT INTO uom (uom_name) VALUES
('kg'),
('liter'),
('piece'),
('dozen'),
('gram'),
('ml'),
('packet');

-- Create Products Table
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    uom_id INT NOT NULL,
    price_per_unit DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (uom_id) REFERENCES uom(uom_id)
);

-- Insert sample products
INSERT INTO products (name, uom_id, price_per_unit) VALUES
('Tomato', 1, 50.00),
('Potato', 1, 30.00),
('Onion', 1, 40.00),
('Milk', 2, 60.00),
('Bread', 3, 35.00),
('Eggs', 4, 72.00),
('Rice', 1, 80.00),
('Oil', 2, 150.00);

-- Create Orders Table
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    datetime DATETIME NOT NULL
);

-- Create Order Details Table
CREATE TABLE IF NOT EXISTS order_details (
    order_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
