import time
import schedule
from verificacao import verificar_alteracoes
import os
from deploy import Deploy
import yaml
from datetime import datetime

# Nome do arquivo onde o token está salvo
TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token.txt")
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.yaml")

with open(CONFIG_FILE, 'r') as f:
    config = yaml.safe_load(f)

def recuperar_token():
    try:
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Arquivo de token não encontrado! Certifique-se de salvar as configurações corretamente.")
        return None

def verificar_e_deploy():
    diretorio = config['diretorio']  # Use barras duplas
    
    if verificar_alteracoes(diretorio):
        token = recuperar_token()
        if not token:
            print("Erro: Token não encontrado! Configure o programa corretamente.")
            return
        
        # Definir o token como variável de ambiente
        os.environ['GITHUB_TOKEN'] = token

        deploy = Deploy()  # Instancia a classe Deploy
        deploy.realizar_deploy()
    else:
        print("Sem alterações para realizar o deploy!")

# Agendar a verificação nos horários específicos
schedule.every().day.at(config['horario']).do(verificar_e_deploy)

def main():
    print("Monitoramento de alterações iniciado...")

    while True:
        now = datetime.now().strftime("%H:%M")
        if now == config['horario'] or now == "00:00":
            print("Verificando alterações...")
            time.sleep(60) 
            verificar_e_deploy()
        
        schedule.run_pending()
        time.sleep(30)  # Verifica as tarefas a cada 30 segundos

if __name__ == "__main__":
    main()
