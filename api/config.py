"""
Configuração centralizada do Green Jobs Brasil
Gerencia variáveis de ambiente com validação e defaults
"""
import os
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    """Configuração centralizada da aplicação"""
    
    # ============================================
    # PATHS
    # ============================================
    BASE_DIR = Path(__file__).parent.parent
    API_DIR = BASE_DIR / "api"
    
    # ============================================
    # SERVIDOR
    # ============================================
    PORT: int = int(os.getenv("PORT", "8002"))
    HOST: str = os.getenv("HOST", "127.0.0.1")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    RELOAD: bool = os.getenv("RELOAD", "true").lower() == "true"
    
    # ============================================
    # BANCO DE DADOS
    # ============================================
    DB_PATH: str = os.getenv("DB_PATH", "api/gjb_dev.db")
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    
    @classmethod
    def get_db_path(cls) -> Path:
        """Retorna o caminho completo do banco de dados"""
        return cls.BASE_DIR / cls.DB_PATH
    
    # ============================================
    # SEGURANÇA
    # ============================================
    SECRET_KEY: str = os.getenv("SECRET_KEY", "INSECURE_DEFAULT_KEY_CHANGE_IN_PRODUCTION")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_MINUTES: int = int(os.getenv("JWT_EXPIRATION_MINUTES", "1440"))
    BCRYPT_ROUNDS: int = int(os.getenv("BCRYPT_ROUNDS", "12"))
    
    # ============================================
    # CORS
    # ============================================
    @classmethod
    def get_cors_origins(cls) -> List[str]:
        """Parse CORS_ORIGINS como lista"""
        origins = os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://localhost:8002,http://127.0.0.1:8002"
        )
        return [origin.strip() for origin in origins.split(",")]
    
    CORS_ALLOW_CREDENTIALS: bool = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
    CORS_ALLOW_METHODS: str = os.getenv("CORS_ALLOW_METHODS", "GET,POST,PUT,DELETE,PATCH,OPTIONS")
    CORS_ALLOW_HEADERS: str = os.getenv("CORS_ALLOW_HEADERS", "*")
    
    # ============================================
    # RATE LIMITING
    # ============================================
    RATE_LIMIT_PER_SECOND: int = int(os.getenv("RATE_LIMIT_PER_SECOND", "10"))
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "100"))
    RATE_LIMIT_PER_HOUR: int = int(os.getenv("RATE_LIMIT_PER_HOUR", "1000"))
    
    # ============================================
    # LOGGING
    # ============================================
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "text")  # text ou json
    LOG_DIR: str = os.getenv("LOG_DIR", "logs")
    LOG_FILE: str = os.getenv("LOG_FILE", "greenjobs.log")
    LOG_MAX_SIZE_MB: int = int(os.getenv("LOG_MAX_SIZE_MB", "10"))
    LOG_BACKUP_COUNT: int = int(os.getenv("LOG_BACKUP_COUNT", "5"))
    
    @classmethod
    def get_log_path(cls) -> Path:
        """Retorna o caminho completo do arquivo de log"""
        log_dir = cls.BASE_DIR / cls.LOG_DIR
        log_dir.mkdir(exist_ok=True)
        return log_dir / cls.LOG_FILE
    
    # ============================================
    # STORAGE
    # ============================================
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "api/static/uploads")
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "5"))
    
    @classmethod
    def get_allowed_extensions(cls) -> List[str]:
        """Parse ALLOWED_EXTENSIONS como lista"""
        extensions = os.getenv("ALLOWED_EXTENSIONS", "jpg,jpeg,png,pdf,doc,docx")
        return [ext.strip() for ext in extensions.split(",")]
    
    @classmethod
    def get_upload_path(cls) -> Path:
        """Retorna o caminho completo do diretório de uploads"""
        upload_dir = cls.BASE_DIR / cls.UPLOAD_DIR
        upload_dir.mkdir(parents=True, exist_ok=True)
        return upload_dir
    
    # ============================================
    # APIs EXTERNAS
    # ============================================
    RECEITA_API_URL: str = os.getenv("RECEITA_API_URL", "https://www.receitaws.com.br/v1")
    EXTERNAL_API_TIMEOUT: int = int(os.getenv("EXTERNAL_API_TIMEOUT", "30"))
    EXTERNAL_API_MAX_RETRIES: int = int(os.getenv("EXTERNAL_API_MAX_RETRIES", "3"))
    
    # ============================================
    # FEATURES FLAGS
    # ============================================
    ENABLE_REGISTRATION: bool = os.getenv("ENABLE_REGISTRATION", "true").lower() == "true"
    ENABLE_ML_MATCHING: bool = os.getenv("ENABLE_ML_MATCHING", "true").lower() == "true"
    ENABLE_AUTO_IMPORT: bool = os.getenv("ENABLE_AUTO_IMPORT", "false").lower() == "true"
    MAINTENANCE_MODE: bool = os.getenv("MAINTENANCE_MODE", "false").lower() == "true"
    
    # ============================================
    # AMBIENTE
    # ============================================
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    APP_NAME: str = os.getenv("APP_NAME", "Green Jobs Brasil")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.6.0")
    BASE_URL: str = os.getenv("BASE_URL", f"http://127.0.0.1:{PORT}")
    
    @classmethod
    def is_production(cls) -> bool:
        """Verifica se está em ambiente de produção"""
        return cls.ENVIRONMENT.lower() == "production"
    
    @classmethod
    def is_development(cls) -> bool:
        """Verifica se está em ambiente de desenvolvimento"""
        return cls.ENVIRONMENT.lower() == "development"
    
    # ============================================
    # VALIDAÇÃO
    # ============================================
    @classmethod
    def validate(cls) -> List[str]:
        """
        Valida configurações obrigatórias
        Retorna lista de erros encontrados
        """
        errors = []
        
        # Validar SECRET_KEY em produção
        if cls.is_production() and cls.SECRET_KEY == "INSECURE_DEFAULT_KEY_CHANGE_IN_PRODUCTION":
            errors.append("SECRET_KEY deve ser alterado em produção!")
        
        # Validar SECRET_KEY não é o padrão inseguro
        if "CHANGE_ME" in cls.SECRET_KEY or len(cls.SECRET_KEY) < 32:
            errors.append(f"SECRET_KEY inseguro (tamanho: {len(cls.SECRET_KEY)}, mínimo: 32)")
        
        # Validar banco de dados
        if cls.is_production() and not cls.DATABASE_URL:
            errors.append("DATABASE_URL obrigatório em produção (use PostgreSQL)")
        
        # Validar porta
        if not 1024 <= cls.PORT <= 65535:
            errors.append(f"PORT inválido: {cls.PORT} (deve estar entre 1024-65535)")
        
        # Validar CORS em produção
        if cls.is_production():
            origins = cls.get_cors_origins()
            if any("localhost" in origin or "127.0.0.1" in origin for origin in origins):
                errors.append("CORS_ORIGINS contém localhost/127.0.0.1 em produção!")
        
        # Validar paths existem
        if not cls.get_db_path().parent.exists():
            errors.append(f"Diretório do banco de dados não existe: {cls.get_db_path().parent}")
        
        return errors
    
    @classmethod
    def print_config(cls):
        """Imprime configuração atual (sem valores sensíveis)"""
        print("=" * 60)
        print(f"🌿 {cls.APP_NAME} v{cls.APP_VERSION}")
        print("=" * 60)
        print(f"Ambiente:    {cls.ENVIRONMENT}")
        print(f"Host:        {cls.HOST}:{cls.PORT}")
        print(f"Debug:       {cls.DEBUG}")
        print(f"Reload:      {cls.RELOAD}")
        print(f"Banco:       {cls.DB_PATH}")
        print(f"CORS:        {len(cls.get_cors_origins())} origens")
        print(f"Logs:        {cls.LOG_LEVEL} ({cls.LOG_FORMAT})")
        print(f"Rate Limit:  {cls.RATE_LIMIT_PER_SECOND}/s")
        print(f"SECRET_KEY:  {'✓ configurado' if cls.SECRET_KEY != 'INSECURE_DEFAULT_KEY_CHANGE_IN_PRODUCTION' else '⚠ usar default'}")
        print("=" * 60)
        
        # Validar e mostrar erros
        errors = cls.validate()
        if errors:
            print("\n⚠️  AVISOS DE CONFIGURAÇÃO:")
            for error in errors:
                print(f"   • {error}")
            print()


# Instância global de configuração
config = Config()


# Validar no import (apenas warnings, não bloquear)
if __name__ != "__main__":
    errors = config.validate()
    if errors and config.DEBUG:
        print("\n⚠️  Avisos de configuração:")
        for error in errors:
            print(f"   • {error}")


if __name__ == "__main__":
    # Script de teste da configuração
    config.print_config()
    
    # Validar
    errors = config.validate()
    if errors:
        print("\n❌ ERROS DE VALIDAÇÃO:")
        for error in errors:
            print(f"   • {error}")
        exit(1)
    else:
        print("\n✅ Configuração válida!")
