-- Finance Dashboard Database Schema
-- Database: PostgreSQL
-- Author: Senior Full-Stack Engineer

-- 1. Create Enums for fixed types
CREATE TYPE transaction_type AS ENUM ('income', 'expense');

-- 2. Create Roles Table
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Create Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role_id INTEGER REFERENCES roles(id) ON DELETE SET NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Create Categories Table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type transaction_type NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, type)
);

-- 5. Create Transactions Table
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    amount DECIMAL(15, 2) NOT NULL CHECK (amount > 0),
    type transaction_type NOT NULL,
    transaction_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Create Audit Logs Table
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(50) NOT NULL, -- e.g., 'CREATE', 'UPDATE', 'DELETE', 'LOGIN'
    entity_name VARCHAR(50) NOT NULL, -- e.g., 'transactions', 'users'
    entity_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address VARCHAR(45),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------------------
-- INDEXES FOR PERFORMANCE
-- ------------------------------------------------------------------------

-- Users performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role_id ON users(role_id);

-- Transactions performance (filtering and analytics)
CREATE INDEX idx_transactions_user_id ON transactions(user_id);
CREATE INDEX idx_transactions_category_id ON transactions(category_id);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_type ON transactions(type);
CREATE INDEX idx_transactions_user_date ON transactions(user_id, transaction_date);

-- Audit logs performance
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);

-- ------------------------------------------------------------------------
-- SAMPLE DATA (SEEDING)
-- ------------------------------------------------------------------------

-- Seed Roles
INSERT INTO roles (name, description) VALUES 
('Admin', 'Full administrative access to all data and users'),
('Analyst', 'Can view all transaction data and dashboard analytics'),
('Viewer', 'Can only view the dashboard summary');

-- Seed Default Categories
INSERT INTO categories (name, type, is_default) VALUES 
('Salary', 'income', TRUE),
('Investment', 'income', TRUE),
('Freelance', 'income', TRUE),
('Rent', 'expense', TRUE),
('Food', 'expense', TRUE),
('Transport', 'expense', TRUE),
('Utilities', 'expense', TRUE),
('Entertainment', 'expense', TRUE),
('Healthcare', 'expense', TRUE);
