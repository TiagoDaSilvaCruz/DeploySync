import subprocess
import yaml
import os

class Deploy:
    def __init__(self):
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)

        self.repositorio = config['repositorio']
        self.usuario = config['usuario']
        self.diretorio_projeto = config['diretorio']  # Caminho do projeto

        # Ler o token do arquivo e definir como variável de ambiente
        with open('token.txt', 'r') as f:
            self.token = f.read().strip()
        os.environ['GITHUB_TOKEN'] = self.token

    def realizar_deploy(self):
        # Muda para o diretório do projeto
        os.chdir(self.diretorio_projeto)

        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "Deploy automático"])

        # Corrigir o problema do "fetch first"
        subprocess.run(["git", "pull", "--rebase", "origin", "main"])

        url_repositorio = f"https://{self.token}@github.com/{self.usuario}/{self.repositorio}.git"
        result = subprocess.run(
            ["git", "push", url_repositorio],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✅ Deploy realizado com sucesso!")
        else:
            print("❌ Erro ao realizar deploy:", result.stderr)