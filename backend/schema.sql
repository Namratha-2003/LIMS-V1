-- PostgreSQL schema for LIMS Deviation module (7 tables)
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20),
    portal_password_hash TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS srfs (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    srf_number VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS srf_equipments (
    id SERIAL PRIMARY KEY,
    srf_id INT NOT NULL REFERENCES srfs(id) ON DELETE CASCADE,
    equipment_name VARCHAR(100) NOT NULL,
    equipment_serial VARCHAR(100),
    calibration_due DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS deviations (
   id SERIAL PRIMARY KEY,
   srf_id INT NOT NULL REFERENCES srfs(id) ON DELETE CASCADE,
   equipment_id INT NOT NULL REFERENCES srf_equipments(id) ON DELETE CASCADE,
   deviation_type VARCHAR(50) NOT NULL CHECK (
       deviation_type IN ('OOT','DAMAGED','MISSING_STANDARD','GB_FAILURE')
   ),
   description TEXT,
   status VARCHAR(30) DEFAULT 'OPEN' CHECK (
       status IN ('OPEN','IN_REVIEW','CUSTOMER_ACCEPTED','CUSTOMER_REJECTED','RESOLVED','CLOSED')
   ),
   raised_by INT NOT NULL,  -- user_id (lab staff / QA)
   resolved_by INT,
   customer_action_note TEXT,
   resolution_notes TEXT,
   created_at TIMESTAMP DEFAULT NOW(),
   updated_at TIMESTAMP DEFAULT NOW(),
   resolved_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    equipment_id INT NOT NULL REFERENCES srf_equipments(id) ON DELETE CASCADE,
    deviation_id INT REFERENCES deviations(id) ON DELETE SET NULL,
    job_type VARCHAR(50) NOT NULL,   -- CALIBRATION, REPAIR, RETURN
    status VARCHAR(30) DEFAULT 'PENDING' CHECK (
        status IN ('PENDING','IN_PROGRESS','COMPLETED','FAILED')
    ),
    assigned_to INT,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,  -- recipient (customer or staff user id)
    deviation_id INT REFERENCES deviations(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    channel VARCHAR(20) NOT NULL CHECK (channel IN ('EMAIL','SMS','PORTAL')),
    status VARCHAR(20) DEFAULT 'PENDING' CHECK (status IN ('PENDING','SENT','FAILED')),
    created_at TIMESTAMP DEFAULT NOW(),
    sent_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS certifications (
    id SERIAL PRIMARY KEY,
    srf_id INT NOT NULL REFERENCES srfs(id) ON DELETE CASCADE,
    equipment_id INT NOT NULL REFERENCES srf_equipments(id) ON DELETE CASCADE,
    deviation_id INT REFERENCES deviations(id) ON DELETE SET NULL,
    certificate_number VARCHAR(100) UNIQUE,
    issued_date TIMESTAMP,
    expiry_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
