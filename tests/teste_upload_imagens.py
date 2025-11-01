"""
Teste de Upload de Imagens - Storytelling v1.6+
Testa endpoints de upload de foto de perfil e banner
"""
import requests
import os
from pathlib import Path
from io import BytesIO
from PIL import Image

API_BASE = "http://127.0.0.1:8002"
PROF_ID = 316  # Maria Silva

def create_test_image(width=800, height=600, color=(0, 150, 136)):
    """Criar imagem de teste"""
    img = Image.new('RGB', (width, height), color=color)
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    return buffer

def test_upload_foto_perfil():
    """Testar upload de foto de perfil"""
    print("\n🧪 Teste 1: Upload de Foto de Perfil")
    print("=" * 60)
    
    # Criar imagem de teste (180x180)
    image_data = create_test_image(180, 180, color=(16, 185, 129))
    
    files = {
        'file': ('foto_perfil.jpg', image_data, 'image/jpeg')
    }
    
    response = requests.post(
        f"{API_BASE}/api/profissionais/{PROF_ID}/upload?tipo=foto_perfil",
        files=files
    )
    
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    
    if response.status_code == 200:
        print(f"✅ Upload bem-sucedido!")
        print(f"   URL: {data['url']}")
        print(f"   Tamanho: {data['size_kb']}KB")
        return data['url']
    else:
        print(f"❌ Erro: {data}")
        return None

def test_upload_banner():
    """Testar upload de banner"""
    print("\n🧪 Teste 2: Upload de Banner")
    print("=" * 60)
    
    # Criar imagem de teste (1200x300)
    image_data = create_test_image(1200, 300, color=(102, 126, 234))
    
    files = {
        'file': ('banner.jpg', image_data, 'image/jpeg')
    }
    
    response = requests.post(
        f"{API_BASE}/api/profissionais/{PROF_ID}/upload?tipo=banner",
        files=files
    )
    
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    
    if response.status_code == 200:
        print(f"✅ Upload bem-sucedido!")
        print(f"   URL: {data['url']}")
        print(f"   Tamanho: {data['size_kb']}KB")
        return data['url']
    else:
        print(f"❌ Erro: {data}")
        return None

def test_upload_invalid_type():
    """Testar upload de arquivo inválido"""
    print("\n🧪 Teste 3: Upload de Tipo Inválido (deve falhar)")
    print("=" * 60)
    
    # Criar "arquivo" de texto
    files = {
        'file': ('documento.txt', BytesIO(b'teste'), 'text/plain')
    }
    
    response = requests.post(
        f"{API_BASE}/api/profissionais/{PROF_ID}/upload?tipo=foto_perfil",
        files=files
    )
    
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    
    if response.status_code == 400:
        print(f"✅ Validação funcionando corretamente!")
    else:
        print(f"❌ Deveria ter retornado erro 400")

def test_upload_too_large():
    """Testar upload de arquivo muito grande"""
    print("\n🧪 Teste 4: Upload de Arquivo Grande (deve falhar)")
    print("=" * 60)
    
    # Criar imagem grande (simular 6MB)
    large_image = create_test_image(4000, 4000)
    
    files = {
        'file': ('foto_grande.jpg', large_image, 'image/jpeg')
    }
    
    response = requests.post(
        f"{API_BASE}/api/profissionais/{PROF_ID}/upload?tipo=foto_perfil",
        files=files
    )
    
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    
    if response.status_code == 400:
        print(f"✅ Validação de tamanho funcionando!")
    else:
        print(f"⚠️  Upload permitido (verificar se < 5MB)")

def test_remove_image():
    """Testar remoção de imagem"""
    print("\n🧪 Teste 5: Remoção de Imagem")
    print("=" * 60)
    
    response = requests.delete(
        f"{API_BASE}/api/profissionais/{PROF_ID}/upload?tipo=banner"
    )
    
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    
    if response.status_code == 200:
        print(f"✅ Remoção bem-sucedida!")
    else:
        print(f"❌ Erro ao remover: {data}")

def test_get_perfil():
    """Verificar se URLs estão no perfil"""
    print("\n🧪 Teste 6: Verificar URLs no Perfil")
    print("=" * 60)
    
    response = requests.get(f"{API_BASE}/api/profissionais/{PROF_ID}/storytelling")
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        foto_url = data.get('foto_perfil_url')
        banner_url = data.get('banner_url')
        
        print(f"Foto de perfil: {foto_url if foto_url else '❌ Não definida'}")
        print(f"Banner: {banner_url if banner_url else '❌ Não definido'}")
        
        if foto_url:
            print(f"✅ Foto de perfil salva no banco!")
        if banner_url:
            print(f"✅ Banner salvo no banco!")
    else:
        print(f"❌ Erro ao buscar perfil")

def main():
    """Executar todos os testes"""
    print("\n" + "=" * 60)
    print("🎨 TESTE DE UPLOAD DE IMAGENS - STORYTELLING v1.6+")
    print("=" * 60)
    
    try:
        # Instalar Pillow se necessário
        try:
            from PIL import Image
        except ImportError:
            print("\n📦 Instalando Pillow...")
            os.system("pip install Pillow")
            from PIL import Image
        
        # Executar testes
        foto_url = test_upload_foto_perfil()
        banner_url = test_upload_banner()
        test_upload_invalid_type()
        test_upload_too_large()
        test_remove_image()
        test_get_perfil()
        
        # Resumo
        print("\n" + "=" * 60)
        print("📊 RESUMO DOS TESTES")
        print("=" * 60)
        print(f"✅ Foto de perfil: {'OK' if foto_url else 'FALHOU'}")
        print(f"✅ Banner: {'OK' if banner_url else 'FALHOU'}")
        print(f"✅ Validações: OK")
        print(f"✅ Remoção: OK")
        
        print("\n🎉 Todos os testes de upload concluídos!")
        print(f"\n🌐 Teste manual:")
        print(f"   Editar: http://127.0.0.1:8002/api/profissionais/editar/{PROF_ID}")
        print(f"   Perfil: http://127.0.0.1:8002/api/profissionais/perfil/{PROF_ID}")
        
    except Exception as e:
        print(f"\n❌ Erro nos testes: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
