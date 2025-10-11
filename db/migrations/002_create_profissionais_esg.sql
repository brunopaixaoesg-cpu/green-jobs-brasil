-- =====================================================
-- Migration 002: Criar Tabela de Profissionais ESG
-- Data: 2025-01-11
-- Descrição: Sistema de cadastro de profissionais verdes
-- =====================================================

-- Tabela principal de profissionais ESG
CREATE TABLE IF NOT EXISTS profissionais_esg (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Dados pessoais
    email TEXT UNIQUE NOT NULL,
    nome_completo TEXT NOT NULL,
    telefone TEXT,
    linkedin_url TEXT,
    portfolio_url TEXT,
    
    -- Localização
    localizacao_uf TEXT,
    localizacao_cidade TEXT,
    aceita_remoto BOOLEAN DEFAULT 1,
    disponivel_mudanca BOOLEAN DEFAULT 0,
    
    -- Experiência profissional
    anos_experiencia_total INTEGER,
    anos_experiencia_esg INTEGER,
    cargo_atual TEXT,
    empresa_atual TEXT,
    
    -- Formação
    formacao_nivel TEXT CHECK(formacao_nivel IN ('medio', 'tecnico', 'superior', 'pos-graduacao', 'mestrado', 'doutorado')),
    formacao_area TEXT,
    instituicao TEXT,
    
    -- ODS e ESG
    ods_interesse TEXT, -- JSON array: [7, 12, 13, 15]
    ods_experiencia TEXT, -- JSON array com anos: {"7": 3, "13": 5}
    habilidades_esg TEXT, -- JSON array: ["ISO 14001", "Relatório GRI", etc]
    certificacoes TEXT, -- JSON array: [{"nome": "ISO 14001", "ano": 2023}]
    
    -- Preferências de trabalho
    areas_interesse TEXT, -- JSON array: ["Energia Renovável", "Gestão de Resíduos"]
    nivel_desejado TEXT CHECK(nivel_desejado IN ('junior', 'pleno', 'senior', 'especialista', 'gerencial')),
    tipo_contratacao_desejado TEXT, -- JSON array: ["CLT", "PJ"]
    pretensao_salarial_min REAL,
    pretensao_salarial_max REAL,
    
    -- Documentos
    curriculo_url TEXT,
    carta_apresentacao TEXT,
    
    -- Bio e descrição
    resumo_profissional TEXT,
    motivacao_esg TEXT, -- Por que trabalhar com ESG
    
    -- Status e controle
    status TEXT DEFAULT 'ativo' CHECK(status IN ('ativo', 'inativo', 'pausado')),
    perfil_completo BOOLEAN DEFAULT 0, -- Se preencheu todos dados importantes
    aceita_contato BOOLEAN DEFAULT 1,
    disponibilidade TEXT CHECK(disponibilidade IN ('imediata', '30dias', '60dias', '90dias', 'indefinida')),
    
    -- Métricas
    visualizacoes_perfil INTEGER DEFAULT 0,
    candidaturas_enviadas INTEGER DEFAULT 0,
    matches_recebidos INTEGER DEFAULT 0,
    
    -- Timestamps
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    ultimo_acesso DATETIME
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_prof_email ON profissionais_esg(email);
CREATE INDEX IF NOT EXISTS idx_prof_status ON profissionais_esg(status);
CREATE INDEX IF NOT EXISTS idx_prof_uf ON profissionais_esg(localizacao_uf);
CREATE INDEX IF NOT EXISTS idx_prof_remoto ON profissionais_esg(aceita_remoto);
CREATE INDEX IF NOT EXISTS idx_prof_nivel ON profissionais_esg(nivel_desejado);

-- Tabela de experiências profissionais detalhadas
CREATE TABLE IF NOT EXISTS experiencias_profissionais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profissional_id INTEGER NOT NULL,
    
    empresa TEXT NOT NULL,
    cargo TEXT NOT NULL,
    descricao TEXT,
    
    data_inicio DATE NOT NULL,
    data_fim DATE, -- NULL se emprego atual
    emprego_atual BOOLEAN DEFAULT 0,
    
    ods_relacionados TEXT, -- JSON array
    conquistas TEXT, -- Principais conquistas
    
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (profissional_id) REFERENCES profissionais_esg(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_exp_profissional ON experiencias_profissionais(profissional_id);

-- Tabela de formação acadêmica
CREATE TABLE IF NOT EXISTS formacoes_academicas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profissional_id INTEGER NOT NULL,
    
    nivel TEXT CHECK(nivel IN ('medio', 'tecnico', 'superior', 'pos-graduacao', 'mestrado', 'doutorado')),
    curso TEXT NOT NULL,
    instituicao TEXT NOT NULL,
    
    ano_inicio INTEGER,
    ano_conclusao INTEGER,
    em_andamento BOOLEAN DEFAULT 0,
    
    descricao TEXT,
    
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (profissional_id) REFERENCES profissionais_esg(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_formacao_profissional ON formacoes_academicas(profissional_id);

-- Trigger para atualizar timestamp
CREATE TRIGGER IF NOT EXISTS update_profissional_timestamp 
AFTER UPDATE ON profissionais_esg
BEGIN
    UPDATE profissionais_esg SET atualizado_em = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger para verificar perfil completo
CREATE TRIGGER IF NOT EXISTS check_perfil_completo 
AFTER UPDATE ON profissionais_esg
BEGIN
    UPDATE profissionais_esg 
    SET perfil_completo = (
        CASE 
            WHEN NEW.nome_completo IS NOT NULL 
                AND NEW.email IS NOT NULL 
                AND NEW.telefone IS NOT NULL
                AND NEW.localizacao_uf IS NOT NULL
                AND NEW.ods_interesse IS NOT NULL
                AND NEW.habilidades_esg IS NOT NULL
                AND NEW.anos_experiencia_esg IS NOT NULL
                AND NEW.resumo_profissional IS NOT NULL
                AND NEW.curriculo_url IS NOT NULL
            THEN 1 
            ELSE 0 
        END
    )
    WHERE id = NEW.id;
END;

-- Inserir profissionais de exemplo para testes
INSERT INTO profissionais_esg (
    email, nome_completo, telefone, linkedin_url,
    localizacao_uf, localizacao_cidade, aceita_remoto,
    anos_experiencia_total, anos_experiencia_esg,
    cargo_atual, formacao_nivel, formacao_area,
    ods_interesse, ods_experiencia, habilidades_esg, certificacoes,
    areas_interesse, nivel_desejado, tipo_contratacao_desejado,
    pretensao_salarial_min, pretensao_salarial_max,
    resumo_profissional, motivacao_esg,
    status, perfil_completo, disponibilidade
) VALUES 
(
    'maria.silva@email.com',
    'Maria Silva Santos',
    '(11) 98765-4321',
    'https://linkedin.com/in/mariasilva',
    'SP',
    'São Paulo',
    1,
    8,
    5,
    'Analista de Sustentabilidade Sênior',
    'pos-graduacao',
    'Gestão Ambiental',
    '[7, 13]',
    '{"7": 5, "13": 3}',
    '["ISO 14001", "Relatório GRI", "Carbon Footprint", "Energia Renovável"]',
    '[{"nome": "ISO 14001 Lead Auditor", "ano": 2021}, {"nome": "GRI Certified", "ano": 2022}]',
    '["Energia Renovável", "Gestão de Carbono", "Relatórios de Sustentabilidade"]',
    'senior',
    '["CLT", "PJ"]',
    8000.00,
    12000.00,
    'Profissional com 8 anos de experiência, sendo 5 anos focados em sustentabilidade e ESG. Especialista em energia renovável e gestão de carbono.',
    'Acredito que a transição energética é fundamental para o futuro do planeta e quero fazer parte dessa transformação.',
    'ativo',
    1,
    'imediata'
),
(
    'joao.santos@email.com',
    'João Pedro Santos',
    '(21) 97654-3210',
    'https://linkedin.com/in/joaopedro',
    'RJ',
    'Rio de Janeiro',
    1,
    4,
    2,
    'Coordenador de Projetos Ambientais',
    'superior',
    'Engenharia Ambiental',
    '[12, 15]',
    '{"12": 2, "15": 2}',
    '["Gestão de Resíduos", "Logística Reversa", "PNRS", "Economia Circular"]',
    '[{"nome": "Gestão de Resíduos Sólidos", "ano": 2023}]',
    '["Gestão de Resíduos", "Economia Circular", "Reciclagem"]',
    'pleno',
    '["CLT"]',
    6000.00,
    9000.00,
    'Engenheiro Ambiental com experiência em gestão de resíduos sólidos e projetos de economia circular.',
    'Trabalhar com resíduos e economia circular me motiva a criar soluções práticas para problemas ambientais.',
    'ativo',
    1,
    '30dias'
),
(
    'ana.costa@email.com',
    'Ana Paula Costa',
    '(11) 96543-2109',
    NULL,
    'SP',
    'Campinas',
    1,
    2,
    1,
    'Assistente de ESG',
    'superior',
    'Administração',
    '[7, 8, 12]',
    '{"8": 1}',
    '["ESG", "Relatórios de Sustentabilidade", "Excel Avançado", "Power BI"]',
    '[]',
    '["ESG", "Relatórios", "Análise de Dados"]',
    'junior',
    '["CLT", "PJ"]',
    3500.00,
    5500.00,
    'Jovem profissional iniciando carreira em ESG, com grande interesse em análise de dados e relatórios de sustentabilidade.',
    'Quero contribuir para um mundo mais sustentável através de dados e análises que guiem decisões empresariais.',
    'ativo',
    1,
    'imediata'
);

-- Adicionar experiências de exemplo
INSERT INTO experiencias_profissionais (
    profissional_id, empresa, cargo, descricao,
    data_inicio, data_fim, emprego_atual,
    ods_relacionados, conquistas
) VALUES
(
    1,
    'Solar Energy do Brasil',
    'Analista de Sustentabilidade Sênior',
    'Liderança de projetos de energia solar fotovoltaica e elaboração de relatórios de sustentabilidade.',
    '2020-01-01',
    NULL,
    1,
    '[7, 13]',
    'Reduzi 35% das emissões de carbono através de projetos de energia renovável. Implementei sistema de rastreamento de ODS alinhado ao GRI.'
),
(
    2,
    'EcoRecicla S/A',
    'Coordenador de Projetos Ambientais',
    'Gestão de projetos de reciclagem e logística reversa para grandes corporações.',
    '2021-06-01',
    NULL,
    1,
    '[12, 15]',
    'Implementei programa de logística reversa que recuperou 2 mil toneladas de resíduos. Aumentei taxa de reciclagem em 40%.'
);

-- Verificação
SELECT 'Migration 002 executada com sucesso!' as message;
SELECT 'Total de profissionais criados: ' || COUNT(*) as result FROM profissionais_esg;
SELECT 'Total de experiências criadas: ' || COUNT(*) as result FROM experiencias_profissionais;
