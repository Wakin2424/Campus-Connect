CREATE TABLE payment (
    payment_id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50) UNIQUE NOT NULL,
    user_id INT REFERENCES Auth_customuser(id) ON DELETE CASCADE,
    product_id INT REFERENCES product(product_id) ON DELETE SET NULL,
    payment_method VARCHAR(50) NOT NULL,  -- mpesa, paypal, contact_seller
    price DECIMAL(10,2) NOT NULL,
    amount INT DEFAULT 1,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Status validation
    CONSTRAINT valid_payment_status 
    CHECK (status IN ('pending', 'complete', 'cancelled'))
);
CREATE TABLE address (
    address_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Auth_customuser(id) ON DELETE CASCADE,
    address1 VARCHAR(255) NOT NULL,
    address2 VARCHAR(255),
    contact VARCHAR(50) NOT NULL,
    city VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
