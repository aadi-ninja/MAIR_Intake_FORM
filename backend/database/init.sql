-- Create database
CREATE DATABASE mair_db;

-- Connect to the database (run this separately or in psql)
-- \c mair_db

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(200),
    role VARCHAR(50) NOT NULL,  -- admin, approver, user, developer
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create request types enum
CREATE TYPE request_type_enum AS ENUM ('NEW_REQUEST', 'CHANGE_REQUEST', 'BUG_FIX');

-- Create status enum
CREATE TYPE status_enum AS ENUM (
    'SUBMITTED',
    'ACKNOWLEDGED', 
    'IN_REVIEW',
    'SENT_FOR_APPROVAL',
    'APPROVED',
    'REJECTED',
    'IN_PROGRESS',
    'COMPLETED'
);

-- Create requests table
CREATE TABLE requests (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    request_type request_type_enum NOT NULL,
    business_unit VARCHAR(100),
    priority VARCHAR(50),  -- HIGH, MEDIUM, LOW
    status status_enum DEFAULT 'SUBMITTED',
    submitted_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create attachments table
CREATE TABLE attachments (
    id SERIAL PRIMARY KEY,
    request_id INTEGER REFERENCES requests(id) ON DELETE CASCADE,
    file_name VARCHAR(255),
    file_path TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create WSJF table
CREATE TABLE wsjf (
    id SERIAL PRIMARY KEY,
    request_id INTEGER UNIQUE REFERENCES requests(id) ON DELETE CASCADE,
    user_business_value INTEGER,  -- 1-9
    time_criticality INTEGER,  -- 1-9
    risk_reduction INTEGER,  -- 1-9
    job_size INTEGER,  -- 1-9
    wsjf_score DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create status history table
CREATE TABLE status_history (
    id SERIAL PRIMARY KEY,
    request_id INTEGER REFERENCES requests(id) ON DELETE CASCADE,
    old_status status_enum,
    new_status status_enum NOT NULL,
    changed_by INTEGER REFERENCES users(id),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create comments table
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    request_id INTEGER REFERENCES requests(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id),
    comment_text TEXT NOT NULL,
    parent_comment_id INTEGER REFERENCES comments(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create approvals table
CREATE TABLE approvals (
    id SERIAL PRIMARY KEY,
    request_id INTEGER REFERENCES requests(id) ON DELETE CASCADE,
    assigned_to INTEGER REFERENCES users(id),
    status VARCHAR(50) DEFAULT 'PENDING',  -- PENDING, APPROVED, REJECTED, MORE_INFO_REQUESTED
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_requests_submitted_by ON requests(submitted_by);
CREATE INDEX idx_requests_status ON requests(status);
CREATE INDEX idx_requests_request_type ON requests(request_type);
CREATE INDEX idx_comments_request_id ON comments(request_id);
CREATE INDEX idx_status_history_request_id ON status_history(request_id);
CREATE INDEX idx_approvals_request_id ON approvals(request_id);
CREATE INDEX idx_approvals_assigned_to ON approvals(assigned_to);

-- Insert sample users
INSERT INTO users (username, email, full_name, role) VALUES
    ('admin', 'admin@mair.local', 'System Admin', 'admin'),
    ('john_approver', 'john@mair.local', 'John Approver', 'approver'),
    ('jane_dev', 'jane@mair.local', 'Jane Developer', 'developer'),
    ('user1', 'user1@mair.local', 'User One', 'user');
