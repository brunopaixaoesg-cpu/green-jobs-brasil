# 🚀 Green Jobs Brasil - Próximos Passos

## ✅ Status Atual
- [x] Projeto scaffolded
- [x] API de teste funcionando
- [x] Dependências Python instaladas
- [x] Scripts de automação criados

## 📋 Próximos Passos

### 1. 🗄️ Configurar Banco PostgreSQL
```bash
# Execute este comando no PowerShell:
.\setup_db.bat
```
**O que faz:**
- Cria o banco `gjb_db`
- Aplica o schema completo (tabelas, índices, enums)
- Carrega dados seed dos CNAEs verdes

### 2. 📊 Executar Pipeline ETL
```bash
# Execute este comando:
.\run_etl.bat
```
**O que faz:**
- Cria dados de exemplo de empresas
- Processa e classifica empresas verdes
- Calcula scores baseados em CNAEs
- Salva dados em Parquet e PostgreSQL

### 3. 🚀 Iniciar API Completa
```bash
# Execute este comando:
.\start_api.bat
```
**O que faz:**
- Inicia API completa com acesso ao banco
- Disponibiliza todos os endpoints
- Interface Swagger em `/docs`

## 🎯 Endpoints Disponíveis Após Setup

### 📈 Empresas Verdes
- `GET /empresas` - Listar empresas com filtros
- `GET /empresas/{cnpj}` - Detalhes de empresa específica
- `GET /empresas/stats/por-uf` - Estatísticas por estado

### 🏭 CNAEs Verdes  
- `GET /cnaes` - Listar CNAEs com classificação
- `GET /cnaes/{codigo}` - Detalhes de CNAE específico
- `GET /cnaes/categorias/list` - Categorias disponíveis

### 📊 Estatísticas
- `GET /stats` - Dashboard completo
- `GET /stats/dashboard/kpis` - KPIs principais
- `GET /health` - Status da API

## 🔍 Exemplos de Uso

### Buscar empresas de energia solar em MG:
```bash
curl "http://localhost:8000/empresas?uf=MG&cnae=3511-5/02&limit=10"
```

### Listar CNAEs por categoria:
```bash
curl "http://localhost:8000/cnaes?categoria=Energia%20Renovável"
```

### Ver estatísticas gerais:
```bash
curl "http://localhost:8000/stats"
```

## ⚙️ Configurações

### Arquivo .env
Editado automaticamente com:
- `DATABASE_URL` - Conexão PostgreSQL
- `TARGET_UFS` - Estados para processar (MG,RJ,SP)
- `LOG_LEVEL` - Nível de logs

### Personalizar senha do PostgreSQL
Se sua senha não for 'postgres', edite o arquivo `.env`:
```env
DATABASE_URL=postgresql://postgres:SUA_SENHA@localhost:5432/gjb_db
```

## 🛠️ Troubleshooting

### Erro de conexão com banco:
1. Verifique se PostgreSQL está rodando
2. Confirme senha no arquivo `.env`
3. Execute `.\setup_db.bat` novamente

### API não inicia:
1. Verifique se porta 8000 está livre
2. Confirme instalação das dependências Python
3. Veja logs de erro no terminal

### ETL falha:
1. Verifique conexão com banco
2. Confirme permissões de escrita em `data/`
3. Veja logs detalhados no terminal

## 📈 Próximas Funcionalidades

- [ ] Dashboard Metabase
- [ ] Export CSV/Excel
- [ ] Autenticação
- [ ] Cache Redis
- [ ] Deploy em produção
- [ ] Integração dados RFB reais
- [ ] Testes automatizados

---

**🌱 Green Jobs Brasil** - Sistema completo funcionando!

Para dúvidas, consulte a documentação em `/docs` ou abra uma issue no projeto.