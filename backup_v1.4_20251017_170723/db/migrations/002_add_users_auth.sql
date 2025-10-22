-- Migration 002: Sistema de Autenticação
-- Adiciona tabela de usuários com suporte a JWT

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    user_type TEXT NOT NULL CHECK(user_type IN ('empresa', 'profissional', 'admin')),
    is_active BOOLEAN DEFAULT 1,
    is_verified BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Relacionamentos opcionais
    empresa_id TEXT, -- CNPJ da empresa (se user_type = 'empresa')
    profissional_id INTEGER, -- ID do profissional (se user_type = 'profissional')
    
    FOREIGN KEY (empresa_id) REFERENCES empresas_verdes(cnpj),
    FOREIGN KEY (profissional_id) REFERENCES profissionais_esg(id)
);

-- Tabela de tokens de refresh (opcional para logout/revogação)
CREATE TABLE IF NOT EXISTS refresh_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    token TEXT UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    revoked BOOLEAN DEFAULT 0,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela de log de autenticação
CREATE TABLE IF NOT EXISTS auth_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    action TEXT NOT NULL, -- 'login', 'logout', 'failed_login', 'password_reset'
    ip_address TEXT,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_type ON users(user_type);
CREATE INDEX IF NOT EXISTS idx_refresh_tokens_user ON refresh_tokens(user_id);
CREATE INDEX IF NOT EXISTS idx_refresh_tokens_token ON refresh_tokens(token);
CREATE INDEX IF NOT EXISTS idx_auth_logs_user ON auth_logs(user_id);

-- Inserir usuário admin padrão (senha: admin123)
-- Hash bcrypt de 'admin123'
INSERT OR IGNORE INTO users (email, hashed_password, full_name, user_type, is_active, is_verified)
VALUES (
    'admin@greenjobs.com.br',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU.6YrDqKleu',
    'Administrador Sistema',
    'admin',
    1,
    1
);
