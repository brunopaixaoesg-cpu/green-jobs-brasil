"""
Teste rápido de hash de senha usando bcrypt diretamente
"""
import bcrypt

# Gerar hash da senha admin123
password = "admin123"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

print("Senha original:", password)
print("Hash gerado:", hashed.decode('utf-8'))
print()

# Testar hash do banco
hash_banco = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU.6YrDqKleu"
print("Hash do banco:", hash_banco)
print("Verificação:", bcrypt.checkpw(password.encode('utf-8'), hash_banco.encode('utf-8')))
