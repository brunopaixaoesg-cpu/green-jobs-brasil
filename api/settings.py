"""
Configuração centralizada da aplicação usando Pydantic Settings.
Carrega variáveis de ambiente do arquivo .env
"""
import os
from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Configurações da aplicação Green Jobs Brasil"""
    
    # Servidor
    port: int = Field(default=8002, env="PORT")
    host: str = Field(default="127.0.0.1", env="HOST")
    debug: bool = Field(default=False, env="DEBUG")
    reload: bool = Field(default=False, env="RELOAD")
    
    # Database
    db_path: str = Field(default="api/gjb_dev.db", env="DB_PATH")
    database_url: str | None = Field(default=None, env="DATABASE_URL")
    
    # Segurança
    secret_key: str = Field(default="dev-secret-key-CHANGE-IN-PRODUCTION", env="SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_expiration_minutes: int = Field(default=1440, env="JWT_EXPIRATION_MINUTES")
    bcrypt_rounds: int = Field(default=12, env="BCRYPT_ROUNDS")
    
    # CORS
    cors_origins: Union[str, List[str]] = Field(
        default="http://localhost:3000,http://localhost:8002,http://127.0.0.1:8002",
        env="CORS_ORIGINS"
    )
    cors_allow_credentials: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")
    cors_allow_methods: Union[str, List[str]] = Field(
        default="GET,POST,PUT,DELETE,PATCH,OPTIONS",
        env="CORS_ALLOW_METHODS"
    )
    cors_allow_headers: str = Field(default="*", env="CORS_ALLOW_HEADERS")
    
    # Rate Limiting
    rate_limit_per_second: int = Field(default=10, env="RATE_LIMIT_PER_SECOND")
    rate_limit_per_minute: int = Field(default=100, env="RATE_LIMIT_PER_MINUTE")
    rate_limit_per_hour: int = Field(default=1000, env="RATE_LIMIT_PER_HOUR")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="text", env="LOG_FORMAT")
    log_dir: str = Field(default="logs", env="LOG_DIR")
    log_file: str = Field(default="greenjobs.log", env="LOG_FILE")
    log_max_size_mb: int = Field(default=10, env="LOG_MAX_SIZE_MB")
    log_backup_count: int = Field(default=5, env="LOG_BACKUP_COUNT")
    
    # Storage
    upload_dir: str = Field(default="api/static/uploads", env="UPLOAD_DIR")
    max_upload_size_mb: int = Field(default=5, env="MAX_UPLOAD_SIZE_MB")
    allowed_extensions: Union[str, List[str]] = Field(
        default="jpg,jpeg,png,pdf,doc,docx",
        env="ALLOWED_EXTENSIONS"
    )
    
    # APIs Externas
    receita_api_url: str = Field(default="https://www.receitaws.com.br/v1", env="RECEITA_API_URL")
    external_api_timeout: int = Field(default=30, env="EXTERNAL_API_TIMEOUT")
    external_api_max_retries: int = Field(default=3, env="EXTERNAL_API_MAX_RETRIES")
    
    # Features Flags
    enable_registration: bool = Field(default=True, env="ENABLE_REGISTRATION")
    enable_ml_matching: bool = Field(default=True, env="ENABLE_ML_MATCHING")
    enable_auto_import: bool = Field(default=False, env="ENABLE_AUTO_IMPORT")
    enable_tsb: bool = Field(default=True, env="ENABLE_TSB")
    enable_storytelling: bool = Field(default=True, env="ENABLE_STORYTELLING")
    maintenance_mode: bool = Field(default=False, env="MAINTENANCE_MODE")
    
    # Ambiente
    environment: str = Field(default="development", env="ENVIRONMENT")
    app_name: str = Field(default="Green Jobs Brasil", env="APP_NAME")
    app_version: str = Field(default="2.0.0", env="APP_VERSION")
    base_url: str = Field(default="http://127.0.0.1:8002", env="BASE_URL")
    
    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Converte string CSV ou lista em lista"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @field_validator("allowed_extensions", mode="before")
    @classmethod
    def parse_allowed_extensions(cls, v):
        """Converte string CSV ou lista em lista"""
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(",")]
        return v
    
    @field_validator("cors_allow_methods", mode="before")
    @classmethod
    def parse_cors_methods(cls, v):
        """Converte string CSV ou lista em lista"""
        if isinstance(v, str):
            return [method.strip() for method in v.split(",")]
        return v
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Garante que cors_origins sempre retorna lista"""
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return self.cors_origins
    
    @property
    def cors_methods_list(self) -> List[str]:
        """Garante que cors_allow_methods sempre retorna lista"""
        if isinstance(self.cors_allow_methods, str):
            return [method.strip() for method in self.cors_allow_methods.split(",")]
        return self.cors_allow_methods
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Garante que allowed_extensions sempre retorna lista"""
        if isinstance(self.allowed_extensions, str):
            return [ext.strip() for ext in self.allowed_extensions.split(",")]
        return self.allowed_extensions
    
    @property
    def is_production(self) -> bool:
        """Verifica se está em produção"""
        return self.environment.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Verifica se está em desenvolvimento"""
        return self.environment.lower() == "development"
    
    @property
    def database_connection_string(self) -> str:
        """Retorna string de conexão do banco"""
        if self.database_url:
            # Render usa postgres://, mas SQLAlchemy 1.4+ requer postgresql://
            url = self.database_url
            if url.startswith("postgres://"):
                url = url.replace("postgres://", "postgresql://", 1)
            return url
        return f"sqlite:///{self.db_path}"
    
    @property
    def is_render(self) -> bool:
        """Detecta se está rodando no Render.com"""
        return os.getenv("RENDER") == "true"
    
    @property
    def is_sqlite(self) -> bool:
        """Verifica se está usando SQLite"""
        return "sqlite" in self.database_connection_string.lower()
    
    @property
    def is_postgresql(self) -> bool:
        """Verifica se está usando PostgreSQL"""
        return "postgresql" in self.database_connection_string.lower()
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


# Instância global de configurações
settings = Settings()


# Validação de configurações críticas em produção
def validate_production_settings():
    """Valida configurações obrigatórias em produção"""
    if not settings.is_production:
        return
    
    errors = []
    
    # Secret key não pode ser default
    if "CHANGE" in settings.secret_key or settings.secret_key == "dev-secret-key-CHANGE-IN-PRODUCTION":
        errors.append("SECRET_KEY não pode ser o valor default em produção!")
    
    # Deve usar PostgreSQL em produção
    if not settings.database_url or "sqlite" in settings.database_url.lower():
        errors.append("DATABASE_URL deve usar PostgreSQL em produção!")
    
    # Debug deve estar desligado
    if settings.debug:
        errors.append("DEBUG deve ser False em produção!")
    
    if errors:
        raise ValueError(f"Configuração inválida para produção:\n" + "\n".join(f"- {e}" for e in errors))


# Executar validação ao importar
if __name__ != "__main__":
    validate_production_settings()
