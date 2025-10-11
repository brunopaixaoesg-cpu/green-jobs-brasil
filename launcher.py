"""
Green Jobs Brasil - Launcher para executável
Interface gráfica simples para iniciar o sistema
"""
import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import threading
import webbrowser
import os
import sys
from datetime import datetime

class GreenJobsLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Green Jobs Brasil 🌱")
        self.root.geometry("600x500")
        self.root.configure(bg='#2d5a27')
        
        # Variáveis
        self.api_process = None
        self.api_running = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # Título
        title_frame = tk.Frame(self.root, bg='#2d5a27')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame, 
            text="🌱 GREEN JOBS BRASIL 🌱", 
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#2d5a27'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Sistema de Identificação de Empresas Verdes",
            font=('Arial', 12),
            fg='#a8d8a8',
            bg='#2d5a27'
        )
        subtitle_label.pack()
        
        # Status
        self.status_label = tk.Label(
            self.root,
            text="🔴 API Parada",
            font=('Arial', 14, 'bold'),
            fg='#ff6b6b',
            bg='#2d5a27'
        )
        self.status_label.pack(pady=10)
        
        # Botões
        button_frame = tk.Frame(self.root, bg='#2d5a27')
        button_frame.pack(pady=20)
        
        self.start_button = tk.Button(
            button_frame,
            text="🚀 Iniciar Sistema",
            command=self.start_api,
            font=('Arial', 12, 'bold'),
            bg='#4a9d4a',
            fg='white',
            padx=20,
            pady=10,
            width=15
        )
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = tk.Button(
            button_frame,
            text="🛑 Parar Sistema",
            command=self.stop_api,
            font=('Arial', 12, 'bold'),
            bg='#d9534f',
            fg='white',
            padx=20,
            pady=10,
            width=15,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        # Links rápidos
        links_frame = tk.Frame(self.root, bg='#2d5a27')
        links_frame.pack(pady=20)
        
        tk.Label(
            links_frame,
            text="🔗 Acesso Rápido:",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#2d5a27'
        ).pack()
        
        links_buttons = tk.Frame(links_frame, bg='#2d5a27')
        links_buttons.pack(pady=10)
        
        tk.Button(
            links_buttons,
            text="📚 Documentação",
            command=lambda: self.open_url('http://127.0.0.1:8000/docs'),
            bg='#5bc0de',
            fg='white',
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            links_buttons,
            text="🏢 Empresas",
            command=lambda: self.open_url('http://127.0.0.1:8000/empresas'),
            bg='#5bc0de',
            fg='white',
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            links_buttons,
            text="📊 Estatísticas",
            command=lambda: self.open_url('http://127.0.0.1:8000/stats'),
            bg='#5bc0de',
            fg='white',
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        # Log
        log_frame = tk.Frame(self.root, bg='#2d5a27')
        log_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(
            log_frame,
            text="📋 Log do Sistema:",
            font=('Arial', 10, 'bold'),
            fg='white',
            bg='#2d5a27'
        ).pack(anchor=tk.W)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=8,
            bg='#1a1a1a',
            fg='#00ff00',
            font=('Courier', 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Log inicial
        self.log(f"🌱 Green Jobs Brasil iniciado - {datetime.now().strftime('%H:%M:%S')}")
        self.log("📍 Sistema pronto para uso!")
        
    def log(self, message):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
    def start_api(self):
        """Inicia a API"""
        try:
            self.log("🚀 Iniciando API...")
            
            # Caminho para o script da API
            api_script = os.path.join(os.path.dirname(__file__), 'api', 'sqlite_api.py')
            python_exe = sys.executable
            
            # Iniciar processo da API
            self.api_process = subprocess.Popen(
                [python_exe, api_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.api_running = True
            self.status_label.config(text="🟢 API Rodando", fg='#5cb85c')
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            
            self.log("✅ API iniciada com sucesso!")
            self.log("📍 Acesse: http://127.0.0.1:8000")
            self.log("📚 Docs: http://127.0.0.1:8000/docs")
            
            # Monitorar processo em thread separada
            threading.Thread(target=self.monitor_api, daemon=True).start()
            
        except Exception as e:
            self.log(f"❌ Erro ao iniciar API: {str(e)}")
            messagebox.showerror("Erro", f"Falha ao iniciar API:\n{str(e)}")
            
    def stop_api(self):
        """Para a API"""
        try:
            if self.api_process:
                self.log("🛑 Parando API...")
                self.api_process.terminate()
                self.api_process.wait(timeout=5)
                
            self.api_running = False
            self.status_label.config(text="🔴 API Parada", fg='#ff6b6b')
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            
            self.log("✅ API parada com sucesso!")
            
        except Exception as e:
            self.log(f"❌ Erro ao parar API: {str(e)}")
            
    def monitor_api(self):
        """Monitora o processo da API"""
        if self.api_process:
            self.api_process.wait()
            if self.api_running:
                self.log("⚠️ API encerrada inesperadamente")
                self.stop_api()
                
    def open_url(self, url):
        """Abre URL no navegador"""
        if self.api_running:
            self.log(f"🌐 Abrindo: {url}")
            webbrowser.open(url)
        else:
            messagebox.showwarning("Aviso", "Inicie a API primeiro!")
            
    def on_closing(self):
        """Callback para fechamento da janela"""
        if self.api_running:
            if messagebox.askokcancel("Fechar", "Deseja parar a API e fechar?"):
                self.stop_api()
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    root = tk.Tk()
    app = GreenJobsLauncher(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()