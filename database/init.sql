-- Script de inicialización para PostgreSQL
-- Proyecto06 - Base de Datos

-- Crear esquema si no existe
CREATE SCHEMA IF NOT EXISTS proyecto06;

-- Tabla de Usuarios
CREATE TABLE IF NOT EXISTS proyecto06.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Productos
CREATE TABLE IF NOT EXISTS proyecto06.products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    price INTEGER NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Auditoría
CREATE TABLE IF NOT EXISTS proyecto06.audit_logs (
    id SERIAL PRIMARY KEY,
    entity_type VARCHAR(50),
    entity_id INTEGER,
    action VARCHAR(20),
    old_values JSONB,
    new_values JSONB,
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices para mejorar performance
CREATE INDEX idx_users_username ON proyecto06.users(username);
CREATE INDEX idx_users_email ON proyecto06.users(email);
CREATE INDEX idx_products_name ON proyecto06.products(name);
CREATE INDEX idx_products_available ON proyecto06.products(is_available);
CREATE INDEX idx_audit_entity ON proyecto06.audit_logs(entity_type, entity_id);

-- Crear vistas útiles
CREATE OR REPLACE VIEW proyecto06.active_users AS
SELECT * FROM proyecto06.users WHERE is_active = TRUE;

CREATE OR REPLACE VIEW proyecto06.available_products AS
SELECT id, name, description, price, created_at 
FROM proyecto06.products 
WHERE is_available = TRUE;

-- Datos de ejemplo
INSERT INTO proyecto06.users (username, email) VALUES
    ('admin', 'admin@proyecto06.com'),
    ('demo_user', 'demo@proyecto06.com')
ON CONFLICT DO NOTHING;

INSERT INTO proyecto06.products (name, description, price) VALUES
    ('Producto 1', 'Descripción del producto 1', 9999),
    ('Producto 2', 'Descripción del producto 2', 19999),
    ('Producto 3', 'Descripción del producto 3', 29999)
ON CONFLICT DO NOTHING;

-- Logs iniciales
INSERT INTO proyecto06.audit_logs (entity_type, action, created_by) VALUES
    ('database', 'initialized', 'system'),
    ('migration', 'completed', 'system');

COMMIT;
