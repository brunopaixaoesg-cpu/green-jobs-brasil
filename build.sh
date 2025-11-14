#!/usr/bin/env bash
# ============================================
# RENDER.COM - Build Script
# Green Jobs Brasil API
# ============================================

set -o errexit  # Exit on error

echo "🚀 Starting Green Jobs Brasil build..."

# ============================================
# 1. UPGRADE PIP
# ============================================
echo "📦 Upgrading pip..."
pip install --upgrade pip

# ============================================
# 2. INSTALL DEPENDENCIES
# ============================================
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# ============================================
# 3. CREATE DIRECTORIES
# ============================================
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p uploads
mkdir -p api/static/uploads

# Set permissions for uploads
chmod 755 uploads
chmod 755 api/static/uploads

# ============================================
# 4. DATABASE MIGRATIONS (if needed)
# ============================================
echo "🗄️ Checking database..."

# O Render já fornece DATABASE_URL
if [ -n "$DATABASE_URL" ]; then
    echo "✅ DATABASE_URL found"
    
    # Criar tabelas se não existirem
    # (Por enquanto usando init_database() na inicialização da API)
    echo "ℹ️ Database will be initialized on first API startup"
else
    echo "⚠️ DATABASE_URL not found - using SQLite for testing"
fi

# ============================================
# 5. COLLECT STATIC FILES (if needed)
# ============================================
echo "📦 Static files ready"

# ============================================
# 6. SMOKE TEST
# ============================================
echo "🧪 Running smoke test..."
python -c "
import sys
try:
    from api.settings import settings
    print(f'✅ Settings loaded: {settings.app_name}')
    print(f'✅ Environment: {settings.environment}')
    print(f'✅ TSB Enabled: {settings.enable_tsb}')
except Exception as e:
    print(f'❌ Error loading settings: {e}')
    sys.exit(1)
"

# ============================================
# 7. BUILD COMPLETE
# ============================================
echo "✅ Build completed successfully!"
echo "🎯 Application: Green Jobs Brasil API"
echo "🌍 Environment: $ENVIRONMENT"
echo "🔧 Ready to start with: uvicorn api.main:app"
