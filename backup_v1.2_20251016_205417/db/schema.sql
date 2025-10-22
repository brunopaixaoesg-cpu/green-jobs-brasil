-- Green Jobs Brasil Database Schema
-- PostgreSQL Schema for GJB Green Scan System

-- Create schema
CREATE SCHEMA IF NOT EXISTS gjb;

-- Create enum types
CREATE TYPE gjb.prioridade_enum AS ENUM ('Core', 'Adjacente');

-- Table: gjb.cnae_green
-- Master table for green CNAEs classification
CREATE TABLE gjb.cnae_green (
    cnae TEXT PRIMARY KEY,
    titulo TEXT NOT NULL,
    categoria TEXT NOT NULL,
    ods_raw TEXT,
    ods_tags INTEGER[] GENERATED ALWAYS AS (
        CASE 
            WHEN ods_raw IS NULL OR ods_raw = '' THEN ARRAY[]::INTEGER[]
            ELSE string_to_array(regexp_replace(ods_raw, '[^0-9,]', '', 'g'), ',')::INTEGER[]
        END
    ) STORED,
    prioridade gjb.prioridade_enum NOT NULL DEFAULT 'Adjacente',
    observacoes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table: gjb.empresas_verdes
-- Main companies table with green classification
CREATE TABLE gjb.empresas_verdes (
    cnpj TEXT PRIMARY KEY,
    razao_social TEXT NOT NULL,
    nome_fantasia TEXT,
    cnae_principal TEXT NOT NULL,
    cnaes_secundarias TEXT[],
    porte TEXT,
    uf TEXT NOT NULL,
    municipio TEXT,
    situacao_cadastral TEXT,
    data_abertura DATE,
    score_verde INTEGER CHECK (score_verde >= 0 AND score_verde <= 100),
    ods_tags INTEGER[],
    fonte_atualizacao TEXT DEFAULT 'ETL_RFB',
    atualizado_em TIMESTAMPTZ DEFAULT NOW(),
    
    -- Foreign key constraint
    FOREIGN KEY (cnae_principal) REFERENCES gjb.cnae_green(cnae)
);

-- Table: gjb.empresa_cnae
-- Junction table for company-CNAE relationships
CREATE TABLE gjb.empresa_cnae (
    cnpj TEXT NOT NULL,
    codigo_cnae TEXT NOT NULL,
    PRIMARY KEY (cnpj, codigo_cnae),
    
    -- Foreign key constraints
    FOREIGN KEY (cnpj) REFERENCES gjb.empresas_verdes(cnpj) ON DELETE CASCADE,
    FOREIGN KEY (codigo_cnae) REFERENCES gjb.cnae_green(cnae)
);

-- Indexes for performance optimization
-- UF and main CNAE filtering
CREATE INDEX idx_empresas_verdes_uf_cnae ON gjb.empresas_verdes(uf, cnae_principal);

-- CNAE and company size filtering
CREATE INDEX idx_empresa_cnae_codigo_porte ON gjb.empresa_cnae(codigo_cnae);
CREATE INDEX idx_empresas_verdes_porte ON gjb.empresas_verdes(porte);

-- GIN indexes for array columns
CREATE INDEX idx_empresas_verdes_cnaes_secundarias ON gjb.empresas_verdes USING GIN(cnaes_secundarias);
CREATE INDEX idx_empresas_verdes_ods_tags ON gjb.empresas_verdes USING GIN(ods_tags);
CREATE INDEX idx_cnae_green_ods_tags ON gjb.cnae_green USING GIN(ods_tags);

-- Text search indexes
CREATE INDEX idx_empresas_verdes_razao_social ON gjb.empresas_verdes USING GIN(to_tsvector('portuguese', razao_social));
CREATE INDEX idx_empresas_verdes_nome_fantasia ON gjb.empresas_verdes USING GIN(to_tsvector('portuguese', nome_fantasia));

-- Additional performance indexes
CREATE INDEX idx_empresas_verdes_municipio ON gjb.empresas_verdes(municipio);
CREATE INDEX idx_empresas_verdes_situacao ON gjb.empresas_verdes(situacao_cadastral);
CREATE INDEX idx_empresas_verdes_score ON gjb.empresas_verdes(score_verde DESC);
CREATE INDEX idx_empresas_verdes_data_abertura ON gjb.empresas_verdes(data_abertura);

-- Comments for documentation
COMMENT ON SCHEMA gjb IS 'Green Jobs Brasil - Schema for green companies classification system';
COMMENT ON TABLE gjb.cnae_green IS 'Master table for green CNAEs with ODS mapping and priority classification';
COMMENT ON TABLE gjb.empresas_verdes IS 'Companies classified as green with scoring and ODS tags';
COMMENT ON TABLE gjb.empresa_cnae IS 'Junction table mapping companies to their CNAEs (primary and secondary)';
COMMENT ON COLUMN gjb.cnae_green.ods_tags IS 'Generated array of ODS numbers extracted from ods_raw field';
COMMENT ON COLUMN gjb.empresas_verdes.score_verde IS 'Green score: 0-100 based on CNAE priority and company status';