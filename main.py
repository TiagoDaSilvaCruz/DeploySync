import time
import schedule
from interface import Interface
from verificacao import verificar_alteracoes
import os
import subprocess
from deploy import Deploy
import yaml
from datetime import datetime
import os  # Importar o módulo os para configurar variáveis de ambiente

# Nome do arquivo onde o token está salvo
TOKEN_FILE = "token.txt"

with open('config.yaml', 'r') as f:
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
schedule.every().day.at("12:00").do(verificar_e_deploy)
schedule.every().day.at("00:00").do(verificar_e_deploy)

def main():
    print("Monitoramento de alterações iniciado...")
    while False:
        now = datetime.now().strftime("%H:%M")
        if now == "12:00" or now == "00:00":
            time.sleep(60)  # Evita múltiplas execuções no mesmo minuto
            verificar_e_deploy()
        
        schedule.run_pending()
        time.sleep(30)  # Verifica as tarefas a cada 30 segundos

if __name__ == "__main__":
    main()
