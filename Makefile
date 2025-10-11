# Green Jobs Brasil Makefile
# Automation commands for the Green Jobs Brasil project

.PHONY: help venv db etl api clean test lint format setup

# Default target
help:
	@echo "Green Jobs Brasil - Available commands:"
	@echo ""
	@echo "Setup and Installation:"
	@echo "  make setup    - Complete project setup (venv + db + deps)"
	@echo "  make venv     - Create virtual environment and install dependencies"
	@echo "  make db       - Setup database schema and seed data"
	@echo ""
	@echo "Data Processing:"
	@echo "  make etl      - Run ETL pipeline to process RFB data"
	@echo ""
	@echo "Application:"
	@echo "  make api      - Start FastAPI development server"
	@echo ""
	@echo "Development:"
	@echo "  make test     - Run tests"
	@echo "  make lint     - Run linting (ruff)"
	@echo "  make format   - Format code (black + ruff)"
	@echo "  make clean    - Clean temporary files and caches"
	@echo ""

# Complete project setup
setup: venv db
	@echo "✅ Project setup completed!"
	@echo "Next steps:"
	@echo "  1. Copy .env.example to .env and configure your settings"
	@echo "  2. Run 'make etl' to process data"
	@echo "  3. Run 'make api' to start the API server"

# Create virtual environment and install dependencies
venv:
	@echo "🐍 Setting up Python virtual environment..."
	python -m venv venv
	@echo "📦 Installing ETL dependencies..."
	venv/Scripts/pip install -r etl/requirements.txt
	@echo "📦 Installing API dependencies..."
	venv/Scripts/pip install -r api/requirements.txt
	@echo "✅ Virtual environment created and dependencies installed"

# Setup database schema and seed data
db:
	@echo "🗄️  Setting up database..."
	@if not exist ".env" ( \
		echo "⚠️  .env file not found. Please copy .env.example to .env and configure it first." && \
		exit 1 \
	)
	@echo "Creating database schema..."
	venv/Scripts/python -c "import psycopg2; from etl.config import config; conn = psycopg2.connect(**config.get_database_params()); cur = conn.cursor(); cur.execute(open('db/schema.sql').read()); conn.commit(); conn.close(); print('✅ Schema created')"
	@echo "Loading CNAE seed data..."
	venv/Scripts/python -c "import psycopg2; from etl.config import config; conn = psycopg2.connect(**config.get_database_params()); cur = conn.cursor(); cur.execute(open('db/seed_cnae.sql').read()); conn.commit(); conn.close(); print('✅ Seed data loaded')"
	@echo "✅ Database setup completed"

# Run ETL pipeline
etl:
	@echo "🔄 Running ETL pipeline..."
	@if not exist ".env" ( \
		echo "⚠️  .env file not found. Please copy .env.example to .env and configure it first." && \
		exit 1 \
	)
	@if not exist "data" mkdir data
	@if not exist "data/raw" mkdir data\raw
	@if not exist "data/processed" mkdir data\processed
	venv/Scripts/python etl/main.py
	@echo "✅ ETL pipeline completed"

# Start FastAPI development server
api:
	@echo "🚀 Starting FastAPI development server..."
	@if not exist ".env" ( \
		echo "⚠️  .env file not found. Please copy .env.example to .env and configure it first." && \
		exit 1 \
	)
	cd api && ../venv/Scripts/uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Run tests
test:
	@echo "🧪 Running tests..."
	venv/Scripts/python -m pytest tests/ -v

# Run linting
lint:
	@echo "🔍 Running linting..."
	venv/Scripts/ruff check etl/ api/
	@echo "✅ Linting completed"

# Format code
format:
	@echo "🎨 Formatting code..."
	venv/Scripts/black etl/ api/
	venv/Scripts/ruff format etl/ api/
	@echo "✅ Code formatting completed"

# Clean temporary files
clean:
	@echo "🧹 Cleaning temporary files..."
	@if exist "__pycache__" rmdir /s /q __pycache__
	@if exist ".pytest_cache" rmdir /s /q .pytest_cache
	@if exist "*.pyc" del /q *.pyc
	@if exist "etl/__pycache__" rmdir /s /q etl\__pycache__
	@if exist "api/__pycache__" rmdir /s /q api\__pycache__
	@for /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
	@echo "✅ Cleanup completed"

# Development helpers
dev-setup: setup
	@echo "🛠️  Setting up development environment..."
	copy .env.example .env
	@echo "✅ Development setup completed"
	@echo "Please edit .env file with your database credentials"

# Quick smoke test
smoke-test:
	@echo "💨 Running smoke tests..."
	@echo "Testing database connection..."
	venv/Scripts/python -c "from api.db import test_connection; print('✅ DB OK' if test_connection() else '❌ DB Failed')"
	@echo "Testing API health..."
	start /b venv/Scripts/python -c "import uvicorn; from api.app import app; uvicorn.run(app, host='127.0.0.1', port=8001, log_level='error')" > nul 2>&1
	timeout /t 3 > nul
	curl -s http://127.0.0.1:8001/health > nul && echo "✅ API OK" || echo "❌ API Failed"
	taskkill /f /im python.exe > nul 2>&1

# Create sample data directories
init-data:
	@echo "📁 Creating data directories..."
	@if not exist "data" mkdir data
	@if not exist "data/raw" mkdir data\raw
	@if not exist "data/processed" mkdir data\processed
	@echo "✅ Data directories created"