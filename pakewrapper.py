#!/usr/bin/env python3
import os
import sys
import time
import logging
import signal
import subprocess
from pathlib import Path
from urllib.parse import urlparse, urlunparse
from typing import Optional
import re

# Configuração de cores ANSI
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# Configuração de logging
log_file = os.path.expanduser('~/.pakewrapper.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

def validate_pake_path() -> bool:
    """Valida a existência do binário Pake."""
    pake_path = '/opt/homebrew/bin/pake'
    if not os.path.exists(pake_path):
        logging.error(f"{Colors.RED}Erro: Pake não encontrado em {pake_path}{Colors.RESET}")
        return False
    return True

def validate_url(url: str) -> Optional[str]:
    """Valida e corrige o formato da URL."""
    if not url:
        return None
    
    # Adiciona https:// se não houver protocolo
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            raise ValueError("URL inválida")
        return urlunparse(result)
    except Exception as e:
        logging.error(f"{Colors.RED}Erro: URL inválida - {str(e)}{Colors.RESET}")
        return None

def validate_icon(icon_path: str) -> Optional[str]:
    """Valida e converte o caminho do ícone para absoluto."""
    if not icon_path:
        return None
    
    try:
        icon_path = os.path.expanduser(icon_path)
        icon_path = os.path.abspath(icon_path)
        
        if not os.path.exists(icon_path):
            logging.error(f"{Colors.RED}Erro: Ícone não encontrado em {icon_path}{Colors.RESET}")
            return None
            
        if not icon_path.lower().endswith(('.icns', '.png')):
            logging.error(f"{Colors.RED}Erro: Ícone deve ser .icns ou .png{Colors.RESET}")
            return None
            
        return icon_path
    except Exception as e:
        logging.error(f"{Colors.RED}Erro ao processar ícone: {str(e)}{Colors.RESET}")
        return None

def get_app_name(url: str) -> str:
    """Gera nome do app baseado no domínio."""
    domain = urlparse(url).netloc
    return re.sub(r'[^a-zA-Z0-9]', '', domain).lower()

def build_pake_command(url: str, icon_path: Optional[str] = None) -> str:
    """Constrói o comando Pake com todos os parâmetros."""
    app_name = get_app_name(url)
    cmd = [
        '/opt/homebrew/bin/pake',
        url,
        '--name', app_name,
        '--width', '1280',
        '--height', '800',
        '--multi-arch'
    ]
    
    if icon_path:
        cmd.extend(['--icon', icon_path])
    
    return ' '.join(cmd)

def show_loading():
    """Exibe animação de loading."""
    chars = '⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    for _ in range(20):
        for char in chars:
            sys.stdout.write(f'\r{Colors.CYAN}Compilando... {char}{Colors.RESET}')
            sys.stdout.flush()
            time.sleep(0.1)
    print()

def execute_pake_command(cmd: str) -> bool:
    """Executa o comando Pake com feedback em tempo real."""
    try:
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        print(f"{Colors.CYAN}Processo iniciado. Aguardando saída...{Colors.RESET}")
        
        # Lê a saída em tempo real
        while True:
            if process.poll() is not None:
                break
            try:
                output = process.stdout.readline()
                if output:
                    print(f"{Colors.CYAN}{output.strip()}{Colors.RESET}")
            except:
                continue
        
        # Verifica se houve erros
        if process.returncode != 0:
            error = process.stderr.read()
            if error:
                print(f"{Colors.RED}Erro: {error.strip()}{Colors.RESET}")
            return False
            
        # Verifica se o arquivo .app foi criado
        app_name = get_app_name(cmd.split()[1])
        app_path = f"{app_name}.app"
        if os.path.exists(app_path):
            print(f"{Colors.GREEN}✓ Arquivo {app_path} criado com sucesso!{Colors.RESET}")
            return True
        else:
            print(f"{Colors.RED}✗ Arquivo {app_path} não foi criado.{Colors.RESET}")
            return False
        
    except Exception as e:
        print(f"{Colors.RED}Erro ao executar comando: {str(e)}{Colors.RESET}")
        return False

def handle_sigint(signum, frame):
    """Trata interrupção do usuário."""
    print(f"\n{Colors.YELLOW}Operação interrompida pelo usuário.{Colors.RESET}")
    sys.exit(1)

def main():
    # Registra handler para Ctrl+C
    signal.signal(signal.SIGINT, handle_sigint)
    
    # Verifica permissões
    if os.geteuid() == 0:
        logging.error(f"{Colors.RED}Erro: Não execute como root{Colors.RESET}")
        sys.exit(1)
    
    # Valida Pake
    if not validate_pake_path():
        sys.exit(1)
    
    # Inputs do usuário
    print(f"{Colors.BOLD}=== PakeWrapper - Criador de Apps ==={Colors.RESET}")
    
    url = input("\nDigite a URL do site: ").strip()
    url = validate_url(url)
    if not url:
        sys.exit(1)
    
    icon_path = input("\nDigite o caminho do ícone (opcional): ").strip()
    icon_path = validate_icon(icon_path) if icon_path else None
    
    # Gera e exibe comando
    cmd = build_pake_command(url, icon_path)
    print(f"\n{Colors.CYAN}Comando a ser executado:{Colors.RESET}")
    print(cmd)
    
    # Confirmação
    if input("\nDeseja prosseguir? (s/n): ").lower() != 's':
        print(f"{Colors.YELLOW}Operação cancelada.{Colors.RESET}")
        sys.exit(0)
    
    # Execução
    start_time = time.time()
    print(f"\n{Colors.CYAN}Iniciando compilação...{Colors.RESET}")
    print(f"{Colors.YELLOW}Este processo pode levar alguns minutos...{Colors.RESET}")
    
    if execute_pake_command(cmd):
        end_time = time.time()
        print(f"\n{Colors.GREEN}✓ App criado com sucesso!{Colors.RESET}")
        print(f"Tempo de execução: {end_time - start_time:.2f} segundos")
        
        # Sugestões pós-instalação
        print(f"\n{Colors.BOLD}Sugestões pós-instalação:{Colors.RESET}")
        print("1. O app foi criado na pasta atual")
        print("2. Arraste para a pasta Applications")
        print("3. Execute pela primeira vez para permitir no Security")
    else:
        print(f"\n{Colors.RED}✗ Falha ao criar o app.{Colors.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main() 