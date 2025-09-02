CREATE TABLE journals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entry TEXT,
    sentiment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone VARCHAR(20),
    amount DECIMAL(10,2),
    checkout_id VARCHAR(255),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
