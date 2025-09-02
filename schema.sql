CREATE TABLE entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    sentiment VARCHAR(50),
    score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

