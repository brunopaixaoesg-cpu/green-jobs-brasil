# 🧹 LOG DE LIMPEZA - Green Jobs Brasil
**Data:** 23/10/2025  
**Objetivo:** Remover arquivos obsoletos e focar no MVP funcional

## 📋 ARQUIVOS REMOVIDOS

### 1. Backups Antigos (3 pastas)
- [ ] backup_v1.2_20251016_205417/ (completa)
- [ ] backup_v1.2_20251016_220737/ (completa) 
- [ ] backup_v1.4_20251017_170723/ (completa)

### 2. Arquivos PostgreSQL/Render (Falhou)
- [ ] populate_render.py
- [ ] populate_direct.py ⚠️ (credenciais expostas)
- [ ] api/db.py (confuso SQLite + PostgreSQL)

### 3. Scripts Experimentais
- [ ] scrapers_poc/ (pasta completa)
- [ ] start_mobile.py
- [ ] verificar_dados.py

### 4. Documentação Obsoleta  
- [ ] RELATORIO_*.md (8+ arquivos)
- [ ] VERSION_*.md (múltiplas versões)
- [ ] backup_*.txt

### 5. Testes Duplicados
- [ ] teste_* (manter apenas teste_fluxo_completo.py)

## ✅ ARQUIVOS MANTIDOS (Core)
- api/sqlite_api_clean.py ⭐
- api/seed_data.py
- api/templates/ e static/
- start_api.py ⭐
- gjb_dev.db ⭐
- requirements.txt
- scripts/ (essenciais)
- README.md

## 📊 RESULTADO ESPERADO
- Redução: ~70% do tamanho
- Foco: MVP funcional limpo
- Segurança: Credenciais removidas