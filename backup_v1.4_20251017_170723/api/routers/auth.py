"""
Router de Autenticação
Endpoints para registro, login, logout e gerenciamento de usuários
"""
import sqlite3
import sys
import os
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Adicionar path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.auth import (
    Token, TokenData, UserCreate, UserLogin, UserResponse, UserInDB,
    verify_password, get_password_hash, create_tokens_for_user,
    decode_token, validate_user_type, validate_password_strength
)

router = APIRouter(prefix="/api/auth", tags=["Autenticação"])

# OAuth2 scheme para extração de token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Caminho do banco de dados (relativo ao diretório raiz do projeto)
import os
if os.path.exists("gjb_dev.db"):
    DB_PATH = "gjb_dev.db"
elif os.path.exists("../gjb_dev.db"):
    DB_PATH = "../gjb_dev.db"
else:
    # Tentar caminho absoluto
    DB_PATH = os.path.join(os.path.dirname(__file__), "../../gjb_dev.db")


# ============================================
# FUNÇÕES DE BANCO DE DADOS
# ============================================

def get_db_connection():
    """Cria conexão com o banco SQLite"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_user_by_email(email: str) -> Optional[UserInDB]:
    """Busca usuário por email"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, email, hashed_password, full_name, user_type, 
               is_active, is_verified, created_at, empresa_id, profissional_id
        FROM users
        WHERE email = ?
    """, (email,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return UserInDB(
            id=row['id'],
            email=row['email'],
            hashed_password=row['hashed_password'],
            full_name=row['full_name'],
            user_type=row['user_type'],
            is_active=bool(row['is_active']),
            is_verified=bool(row['is_verified']),
            created_at=datetime.fromisoformat(row['created_at']),
            empresa_id=row['empresa_id'],
            profissional_id=row['profissional_id']
        )
    return None


def get_user_by_id(user_id: int) -> Optional[UserInDB]:
    """Busca usuário por ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, email, hashed_password, full_name, user_type, 
               is_active, is_verified, created_at, empresa_id, profissional_id
        FROM users
        WHERE id = ?
    """, (user_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return UserInDB(
            id=row['id'],
            email=row['email'],
            hashed_password=row['hashed_password'],
            full_name=row['full_name'],
            user_type=row['user_type'],
            is_active=bool(row['is_active']),
            is_verified=bool(row['is_verified']),
            created_at=datetime.fromisoformat(row['created_at']),
            empresa_id=row['empresa_id'],
            profissional_id=row['profissional_id']
        )
    return None


def create_user(user_data: UserCreate) -> UserInDB:
    """Cria novo usuário no banco"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    hashed_password = get_password_hash(user_data.password)
    
    try:
        cursor.execute("""
            INSERT INTO users (email, hashed_password, full_name, user_type, empresa_id, profissional_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_data.email,
            hashed_password,
            user_data.full_name,
            user_data.user_type,
            user_data.empresa_id,
            user_data.profissional_id
        ))
        
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        # Buscar usuário criado
        return get_user_by_id(user_id)
        
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )


def log_auth_action(user_id: int, action: str, ip_address: str = None, user_agent: str = None):
    """Registra ação de autenticação no log"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO auth_logs (user_id, action, ip_address, user_agent)
        VALUES (?, ?, ?, ?)
    """, (user_id, action, ip_address, user_agent))
    
    conn.commit()
    conn.close()


# ============================================
# DEPENDENCY: GET CURRENT USER
# ============================================

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    """
    Dependency para obter usuário atual baseado no token JWT
    Usado em rotas protegidas
    """
    token_data = decode_token(token)
    
    if not token_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = get_user_by_id(token_data.user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )
    
    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    """Dependency para garantir que usuário está ativo"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user


# ============================================
# ENDPOINTS
# ============================================

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Registra novo usuário no sistema
    
    - **email**: Email único do usuário
    - **password**: Senha (mínimo 8 caracteres, 1 maiúscula, 1 número)
    - **full_name**: Nome completo
    - **user_type**: Tipo: 'empresa', 'profissional' ou 'admin'
    - **empresa_id**: CNPJ (opcional, se user_type='empresa')
    - **profissional_id**: ID do profissional (opcional, se user_type='profissional')
    """
    # Validar tipo de usuário
    if not validate_user_type(user_data.user_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de usuário inválido. Use: 'empresa', 'profissional' ou 'admin'"
        )
    
    # Validar força da senha
    is_valid, message = validate_password_strength(user_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    # Verificar se email já existe
    existing_user = get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Criar usuário
    new_user = create_user(user_data)
    
    # Log da ação
    log_auth_action(new_user.id, "register")
    
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        full_name=new_user.full_name,
        user_type=new_user.user_type,
        is_active=new_user.is_active,
        is_verified=new_user.is_verified,
        created_at=new_user.created_at,
        empresa_id=new_user.empresa_id,
        profissional_id=new_user.profissional_id
    )


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login com email e senha
    
    Retorna access_token e refresh_token JWT
    """
    # Buscar usuário
    user = get_user_by_email(form_data.username)  # OAuth2 usa 'username' mas enviamos email
    
    if not user:
        log_auth_action(0, "failed_login")  # user_id=0 para falha sem usuário
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar senha
    if not verify_password(form_data.password, user.hashed_password):
        log_auth_action(user.id, "failed_login")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar se usuário está ativo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )
    
    # Criar tokens
    tokens = create_tokens_for_user(user)
    
    # Log de login bem-sucedido
    log_auth_action(user.id, "login")
    
    return tokens


@router.post("/login-json", response_model=Token)
async def login_json(credentials: UserLogin):
    """
    Login alternativo com JSON (email/password)
    
    Útil para clients que não usam OAuth2PasswordRequestForm
    """
    user = get_user_by_email(credentials.email)
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )
    
    tokens = create_tokens_for_user(user)
    log_auth_action(user.id, "login")
    
    return tokens


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserInDB = Depends(get_current_active_user)):
    """
    Retorna dados do usuário autenticado atual
    
    Requer: Bearer token no header Authorization
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        user_type=current_user.user_type,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at,
        empresa_id=current_user.empresa_id,
        profissional_id=current_user.profissional_id
    )


@router.post("/logout")
async def logout(current_user: UserInDB = Depends(get_current_active_user)):
    """
    Logout do usuário
    
    Em produção, adicionar token à blacklist
    """
    log_auth_action(current_user.id, "logout")
    
    return {
        "message": "Logout realizado com sucesso",
        "user": current_user.email
    }


@router.get("/verify-token")
async def verify_token(current_user: UserInDB = Depends(get_current_active_user)):
    """
    Verifica se o token é válido
    
    Útil para validação no frontend
    """
    return {
        "valid": True,
        "user_id": current_user.id,
        "email": current_user.email,
        "user_type": current_user.user_type
    }
