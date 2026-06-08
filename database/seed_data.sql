USE smart_store_ai;

INSERT INTO users (id, name, email, role) VALUES
(1, 'Ari Customer', 'ari@example.com', 'customer'),
(2, 'Mina Customer', 'mina@example.com', 'customer'),
(3, 'Admin User', 'admin@example.com', 'admin');

INSERT INTO products (id, name, category, price, rating, stock) VALUES
(1, 'Wireless Mouse', 'Accessories', 19.99, 4.8, 45),
(2, 'Mechanical Keyboard', 'Accessories', 69.99, 4.7, 20),
(3, 'Laptop Bag', 'Bags', 34.99, 4.6, 30),
(4, 'Noise Canceling Headset', 'Audio', 89.99, 4.9, 15),
(5, 'USB-C Hub', 'Accessories', 29.99, 4.5, 25),
(6, 'Portable SSD', 'Storage', 99.99, 4.8, 18),
(7, 'Gaming Laptop', 'Computers', 1199.99, 4.7, 8),
(8, 'Webcam HD', 'Accessories', 39.99, 4.4, 22);

INSERT INTO orders (user_id, product_id, quantity, order_date) VALUES
(1, 1, 1, '2026-06-01'),
(1, 5, 1, '2026-06-02'),
(1, 3, 1, '2026-06-03'),
(2, 4, 1, '2026-06-01'),
(2, 6, 1, '2026-06-04'),
(2, 1, 2, '2026-06-05');
