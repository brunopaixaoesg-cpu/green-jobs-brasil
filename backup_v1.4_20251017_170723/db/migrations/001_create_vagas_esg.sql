-- Migration 001: Criar tabela de Vagas ESG
-- Data: 2025-10-11
-- Descrição: Sistema de vagas verdes com ODS tags e matching

-- Tabela principal de vagas
CREATE TABLE IF NOT EXISTS vagas_esg (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cnpj TEXT NOT NULL,
    titulo TEXT NOT NULL,
    descricao TEXT,
    
    -- Classificação ESG
    ods_tags TEXT, -- JSON array: [7, 13, 15]
    habilidades_requeridas TEXT, -- JSON array: ["ISO 14001", "GRI", "Carbon Footprint"]
    
    -- Requisitos
    nivel_experiencia TEXT CHECK(nivel_experiencia IN ('junior', 'pleno', 'senior', 'especialista')),
    tipo_contratacao TEXT CHECK(tipo_contratacao IN ('CLT', 'PJ', 'temporario', 'estagio', 'freelance')),
    
    -- Localização e Remuneração
    localizacao_uf TEXT,
    localizacao_cidade TEXT,
    salario_min REAL,
    salario_max REAL,
    remoto BOOLEAN DEFAULT 0,
    hibrido BOOLEAN DEFAULT 0,
    
    -- Status e Metadata
    status TEXT DEFAULT 'ativa' CHECK(status IN ('ativa', 'pausada', 'fechada', 'cancelada')),
    vagas_disponiveis INTEGER DEFAULT 1,
    candidaturas_recebidas INTEGER DEFAULT 0,
    
    -- Informações Adicionais
    beneficios TEXT, -- JSON array
    requisitos_adicionais TEXT,
    diferenciais TEXT,
    
    -- Timestamps
    criada_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    atualizada_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_em DATETIME, -- Data de encerramento
    
    -- Foreign Key
    FOREIGN KEY (cnpj) REFERENCES empresas_verdes(cnpj) ON DELETE CASCADE
);

-- Índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_vagas_cnpj ON vagas_esg(cnpj);
CREATE INDEX IF NOT EXISTS idx_vagas_status ON vagas_esg(status);
CREATE INDEX IF NOT EXISTS idx_vagas_criada_em ON vagas_esg(criada_em DESC);
CREATE INDEX IF NOT EXISTS idx_vagas_remoto ON vagas_esg(remoto);
CREATE INDEX IF NOT EXISTS idx_vagas_uf ON vagas_esg(localizacao_uf);

-- Tabela de candidaturas (relacionamento vaga-profissional)
CREATE TABLE IF NOT EXISTS candidaturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vaga_id INTEGER NOT NULL,
    profissional_id INTEGER, -- Será criado na próxima migration
    
    -- Status da candidatura
    status TEXT DEFAULT 'pendente' CHECK(status IN ('pendente', 'em_analise', 'aprovada', 'rejeitada', 'finalizada')),
    
    -- Match score
    match_score REAL, -- 0-100
    
    -- Mensagem do candidato
    mensagem_candidato TEXT,
    curriculo_url TEXT,
    
    -- Feedback da empresa
    feedback_empresa TEXT,
    motivo_rejeicao TEXT,
    
    -- Timestamps
    candidatou_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    atualizada_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (vaga_id) REFERENCES vagas_esg(id) ON DELETE CASCADE
);

-- Índices para candidaturas
CREATE INDEX IF NOT EXISTS idx_candidaturas_vaga ON candidaturas(vaga_id);
CREATE INDEX IF NOT EXISTS idx_candidaturas_status ON candidaturas(status);
CREATE INDEX IF NOT EXISTS idx_candidaturas_score ON candidaturas(match_score DESC);

-- Trigger para atualizar timestamp
CREATE TRIGGER IF NOT EXISTS update_vaga_timestamp 
AFTER UPDATE ON vagas_esg
BEGIN
    UPDATE vagas_esg SET atualizada_em = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_candidatura_timestamp 
AFTER UPDATE ON candidaturas
BEGIN
    UPDATE candidaturas SET atualizada_em = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger para atualizar contador de candidaturas
CREATE TRIGGER IF NOT EXISTS increment_candidaturas 
AFTER INSERT ON candidaturas
BEGIN
    UPDATE vagas_esg 
    SET candidaturas_recebidas = candidaturas_recebidas + 1 
    WHERE id = NEW.vaga_id;
END;

-- View para vagas ativas com informações da empresa
CREATE VIEW IF NOT EXISTS view_vagas_ativas AS
SELECT 
    v.*,
    e.razao_social,
    e.nome_fantasia,
    e.porte,
    e.municipio as empresa_municipio,
    e.uf as empresa_uf,
    e.score_verde as empresa_score_verde,
    e.ods_tags as empresa_ods_tags
FROM vagas_esg v
LEFT JOIN empresas_verdes e ON v.cnpj = e.cnpj
WHERE v.status = 'ativa'
ORDER BY v.criada_em DESC;

-- Dados de exemplo para teste
INSERT INTO vagas_esg (
    cnpj, titulo, descricao, ods_tags, habilidades_requeridas,
    nivel_experiencia, tipo_contratacao, localizacao_uf, localizacao_cidade,
    salario_min, salario_max, remoto, status, vagas_disponiveis
) VALUES 
(
    '00.000.000/0001-91', -- Substituir por CNPJ real do banco
    'Analista de Sustentabilidade Pleno',
    'Buscamos profissional para desenvolver e implementar estratégias ESG, elaborar relatórios de sustentabilidade e apoiar na gestão de indicadores ambientais.',
    '[7, 12, 13]', -- ODS: Energia Limpa, Consumo Responsável, Ação Climática
    '["ISO 14001", "GRI Standards", "Inventário GEE", "Excel Avançado"]',
    'pleno',
    'CLT',
    'SP',
    'São Paulo',
    6000.00,
    9000.00,
    1, -- Remoto
    'ativa',
    2
);

-- Comentário final
-- Esta migration cria a infraestrutura completa para o sistema de vagas ESG
-- Próxima migration: 002_create_profissionais_esg.sql
