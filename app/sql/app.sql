/* =========================================================
   Order Service - MySQL DDL
   Enterprise Grade Schema
   ========================================================= */

-- Create Database
CREATE DATABASE IF NOT EXISTS orderdb
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE orderdb;

-- =========================================================
-- USERS TABLE
-- =========================================================
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(200) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'USER',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_users_username (username)
);

-- =========================================================
-- ORDERS TABLE
-- =========================================================
CREATE TABLE orders (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'CREATED',
    total_amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_orders_user_id (user_id),
    INDEX idx_orders_status (status)
);

-- =========================================================
-- ORDER ITEMS TABLE
-- =========================================================
CREATE TABLE order_items (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_order_items_order_id (order_id),

    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id)
        REFERENCES orders(id)
        ON DELETE CASCADE
);

-- =========================================================
-- OPTIONAL: SAMPLE DATA (FOR TESTING)
-- =========================================================
INSERT INTO users (username, password, role)
VALUES ('admin', 'encrypted_password_here', 'ADMIN');

-- =========================================================
-- END OF DDL
-- =========================================================
