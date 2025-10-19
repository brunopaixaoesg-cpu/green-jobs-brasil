"""
Script para iniciar Green Jobs Brasil com acesso via rede local
Permite acesso do celular no mesmo Wi-Fi
"""
import subprocess
import sys
import socket
import qrcode
from pathlib import Path

def get_local_ip():
    """Obtém o IP local da máquina"""
    try:
        # Cria socket temporário para descobrir IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "Não foi possível obter IP"

def generate_qr_code(url, filename="qr_access_mobile.png"):
    """Gera QR Code para acesso rápido"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="green", back_color="white")
        img.save(filename)
        return True
    except ImportError:
        print("\n⚠️  Pacote 'qrcode' não instalado. Para gerar QR Code:")
        print("   pip install qrcode[pil]")
        return False

def print_instructions(ip, port=8002):
    """Imprime instruções de acesso"""
    dashboard_url = f"http://{ip}:{port}/api/profissionais/dashboard/1"
    perfil_url = f"http://{ip}:{port}/api/profissionais/perfil/1"
    empresa_url = f"http://{ip}:{port}/api/empresas/dashboard/1"
    
    print("\n" + "="*70)
    print("🌿 GREEN JOBS BRASIL - ACESSO MOBILE")
    print("="*70)
    
    print(f"\n📡 IP Local: {ip}")
    print(f"🔌 Porta: {port}")
    
    print("\n📱 COMO ACESSAR NO CELULAR:")
    print("   1. Conecte o celular no MESMO Wi-Fi")
    print("   2. Abra o navegador do celular")
    print("   3. Digite um dos URLs abaixo:\n")
    
    print("   🏠 Dashboard Profissional:")
    print(f"      {dashboard_url}\n")
    
    print("   👤 Perfil Storytelling:")
    print(f"      {perfil_url}\n")
    
    print("   🏢 Dashboard Empresa:")
    print(f"      {empresa_url}\n")
    
    print("   📄 API Docs:")
    print(f"      http://{ip}:{port}/docs\n")
    
    # Tentar gerar QR Code
    if generate_qr_code(dashboard_url):
        print("   📷 QR Code gerado: qr_access_mobile.png")
        print("      Aponte a câmera do celular para acessar!\n")
    
    print("\n⚠️  FIREWALL DO WINDOWS:")
    print("   Se não conseguir acessar, libere a porta no firewall:")
    print("   1. Abra PowerShell como Administrador")
    print("   2. Execute:")
    print(f"      New-NetFirewallRule -DisplayName 'Green Jobs' -Direction Inbound -LocalPort {port} -Protocol TCP -Action Allow")
    
    print("\n" + "="*70)
    print("🚀 Iniciando servidor...")
    print("   Pressione Ctrl+C para parar")
    print("="*70 + "\n")

def main():
    # Obter IP local
    local_ip = get_local_ip()
    
    if local_ip == "Não foi possível obter IP":
        print("❌ Erro: Não foi possível obter o IP local")
        print("   Verifique sua conexão de rede")
        return
    
    # Mostrar instruções
    print_instructions(local_ip)
    
    # Modificar temporariamente o arquivo para aceitar conexões externas
    import os
    os.chdir(r"C:\Users\Bruno\Empresas Verdes")
    
    # Importar e modificar a aplicação
    import sys
    sys.path.insert(0, 'api')
    
    try:
        from api.sqlite_api_clean import app
        import uvicorn
        
        # Rodar com 0.0.0.0 para aceitar conexões externas
        uvicorn.run(
            app,
            host="0.0.0.0",  # Aceita conexões de qualquer IP
            port=8002,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n\n✅ Servidor parado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
