CREATE TABLE point_of_sales (
    id SERIAL PRIMARY KEY,

-- Store names
    siret VARCHAR(14),
    store_name TEXT NOT NULL,
    store_name_normalized TEXT,
    
-- Address fields
    street_number VARCHAR(10),
    street TEXT,
    -- zip_code limited to 6 characters for French postal codes
    zip_code VARCHAR(6),
    city TEXT,
    
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    
-- Technical fields
    is_deleted BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL
);

-- Indexes for the search and filter processes
CREATE INDEX idx_pos_siret ON point_of_sales(siret);
CREATE INDEX idx_pos_zip_code ON point_of_sales(zip_code);