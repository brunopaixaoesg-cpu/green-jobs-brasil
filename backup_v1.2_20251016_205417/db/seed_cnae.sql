-- Seed data for gjb.cnae_green table
-- Load CNAE green classification data

\copy gjb.cnae_green(cnae, titulo, categoria, ods_raw, prioridade, observacoes) FROM 'etl/cnae_green_seed.csv' WITH (FORMAT CSV, HEADER true, DELIMITER ',', QUOTE '"', ESCAPE '"', ENCODING 'UTF8');

-- Update statistics after data load
ANALYZE gjb.cnae_green;