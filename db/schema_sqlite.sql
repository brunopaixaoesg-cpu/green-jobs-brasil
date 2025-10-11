-- Green Jobs Brasil Database Schema - SQLite Version
-- SQLite Schema for GJB Green Scan System

-- Table: cnae_green
-- Master table for green CNAEs classification
CREATE TABLE IF NOT EXISTS cnae_green (
    cnae TEXT PRIMARY KEY,
    titulo TEXT NOT NULL,
    categoria TEXT NOT NULL,
    ods_raw TEXT,
    ods_tags TEXT, -- JSON array as text in SQLite
    prioridade TEXT CHECK (prioridade IN ('Core', 'Adjacente')) NOT NULL DEFAULT 'Adjacente',
    observacoes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table: empresas_verdes
-- Main companies table with green classification
CREATE TABLE IF NOT EXISTS empresas_verdes (
    cnpj TEXT PRIMARY KEY,
    razao_social TEXT NOT NULL,
    nome_fantasia TEXT,
    cnae_principal TEXT NOT NULL,
    cnaes_secundarias TEXT, -- JSON array as text
    porte TEXT,
    uf TEXT NOT NULL,
    municipio TEXT,
    situacao_cadastral TEXT,
    data_abertura DATE,
    score_verde INTEGER CHECK (score_verde >= 0 AND score_verde <= 100),
    ods_tags TEXT, -- JSON array as text
    fonte_atualizacao TEXT DEFAULT 'ETL_RFB',
    atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraint
    FOREIGN KEY (cnae_principal) REFERENCES cnae_green(cnae)
);

-- Table: empresa_cnae
-- Junction table for company-CNAE relationships
CREATE TABLE IF NOT EXISTS empresa_cnae (
    cnpj TEXT NOT NULL,
    codigo_cnae TEXT NOT NULL,
    PRIMARY KEY (cnpj, codigo_cnae),
    
    -- Foreign key constraints
    FOREIGN KEY (cnpj) REFERENCES empresas_verdes(cnpj) ON DELETE CASCADE,
    FOREIGN KEY (codigo_cnae) REFERENCES cnae_green(cnae)
);

-- Indexes for performance optimization
CREATE INDEX IF NOT EXISTS idx_empresas_verdes_uf_cnae ON empresas_verdes(uf, cnae_principal);
CREATE INDEX IF NOT EXISTS idx_empresa_cnae_codigo ON empresa_cnae(codigo_cnae);
CREATE INDEX IF NOT EXISTS idx_empresas_verdes_porte ON empresas_verdes(porte);
CREATE INDEX IF NOT EXISTS idx_empresas_verdes_municipio ON empresas_verdes(municipio);
CREATE INDEX IF NOT EXISTS idx_empresas_verdes_situacao ON empresas_verdes(situacao_cadastral);
CREATE INDEX IF NOT EXISTS idx_empresas_verdes_score ON empresas_verdes(score_verde DESC);
CREATE INDEX IF NOT EXISTS idx_empresas_verdes_data_abertura ON empresas_verdes(data_abertura);