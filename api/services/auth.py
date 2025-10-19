"""
Módulo de Autenticação JWT
Sistema completo de autenticação com JWT, hash de senhas e validação
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
import bcrypt
from pydantic import BaseModel, EmailStr
from fastapi import HTTPException, status

# Configurações de segurança
SECRET_KEY = "greenjobs_brasil_secret_key_2025_change_in_production"  # MUDAR EM PRODUÇÃO!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


# ============================================
# MODELS / SCHEMAS
# ============================================

class Token(BaseModel):
    """Token de acesso JWT"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Dados extraídos do token"""
    user_id: Optional[int] = None
    email: Optional[str] = None
    user_type: Optional[str] = None


class UserBase(BaseModel):
    """Schema base de usuário"""
    email: EmailStr
    full_name: str
    user_type: str  # 'empresa', 'profissional', 'admin'


class UserCreate(UserBase):
    """Schema para criação de usuário"""
    password: str
    empresa_id: Optional[str] = None  # CNPJ se for empresa
    profissional_id: Optional[int] = None  # ID se for profissional


class UserLogin(BaseModel):
    """Schema para login"""
    email: EmailStr
    password: str


class UserInDB(UserBase):
    """Usuário completo do banco"""
    id: int
    hashed_password: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    empresa_id: Optional[str] = None
    profissional_id: Optional[int] = None


class UserResponse(UserBase):
    """Usuário para resposta (sem senha)"""
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    empresa_id: Optional[str] = None
    profissional_id: Optional[int] = None

    class Config:
        from_attributes = True


# ============================================
# FUNÇÕES DE HASH DE SENHA
# ============================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha em texto plano corresponde ao hash
    
    Args:
        plain_password: Senha em texto plano
        hashed_password: Hash da senha armazenada
        
    Returns:
        True se as senhas coincidem, False caso contrário
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """
    Cria hash bcrypt da senha
    
    Args:
        password: Senha em texto plano
        
    Returns:
        Hash da senha
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


# ============================================
# FUNÇÕES DE TOKEN JWT
# ============================================

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um token JWT de acesso
    
    Args:
        data: Dados a serem codificados no token
        expires_delta: Tempo de expiração (opcional)
        
    Returns:
        Token JWT codificado
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Cria um token JWT de refresh (longa duração)
    
    Args:
        data: Dados a serem codificados no token
        
    Returns:
        Refresh token JWT codificado
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> TokenData:
    """
    Decodifica e valida um token JWT
    
    Args:
        token: Token JWT a ser decodificado
        
    Returns:
        TokenData com informações do usuário
        
    Raises:
        HTTPException: Se o token for inválido ou expirado
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_id_str: str = payload.get("sub")
        email: str = payload.get("email")
        user_type: str = payload.get("user_type")
        
        if user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: usuário não encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Converter de volta para int
        user_id = int(user_id_str)
        
        return TokenData(user_id=user_id, email=email, user_type=user_type)
        
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def create_tokens_for_user(user: UserInDB) -> Token:
    """
    Cria access token e refresh token para um usuário
    
    Args:
        user: Usuário do banco de dados
        
    Returns:
        Token com access_token e refresh_token
    """
    token_data = {
        "sub": str(user.id),  # subject deve ser string
        "email": user.email,
        "user_type": user.user_type
    }
    
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token({"sub": str(user.id)})
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


# ============================================
# FUNÇÕES DE VALIDAÇÃO
# ============================================

def validate_user_type(user_type: str) -> bool:
    """
    Valida se o tipo de usuário é válido
    
    Args:
        user_type: Tipo do usuário
        
    Returns:
        True se válido, False caso contrário
    """
    valid_types = ['empresa', 'profissional', 'admin']
    return user_type in valid_types


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Valida a força da senha
    
    Args:
        password: Senha a ser validada
        
    Returns:
        Tupla (é_válida, mensagem_erro)
    """
    if len(password) < 8:
        return False, "Senha deve ter no mínimo 8 caracteres"
    
    if not any(char.isdigit() for char in password):
        return False, "Senha deve conter pelo menos um número"
    
    if not any(char.isupper() for char in password):
        return False, "Senha deve conter pelo menos uma letra maiúscula"
    
    if not any(char.islower() for char in password):
        return False, "Senha deve conter pelo menos uma letra minúscula"
    
    return True, "Senha válida"


# ============================================
# HELPERS
# ============================================

def get_user_display_name(user: UserInDB) -> str:
    """
    Retorna o nome de exibição do usuário
    
    Args:
        user: Usuário do banco
        
    Returns:
        Nome formatado para exibição
    """
    if user.user_type == 'admin':
        return f"{user.full_name} (Admin)"
    elif user.user_type == 'empresa':
        return f"{user.full_name} (Empresa)"
    else:
        return user.full_name


def mask_email(email: str) -> str:
    """
    Mascara um email para exibição segura
    
    Args:
        email: Email a ser mascarado
        
    Returns:
        Email mascarado (ex: j***@example.com)
    """
    if '@' not in email:
        return email
    
    local, domain = email.split('@')
    if len(local) <= 2:
        masked_local = local[0] + '*'
    else:
        masked_local = local[0] + '*' * (len(local) - 2) + local[-1]
    
    return f"{masked_local}@{domain}"
