import subprocess
import yaml
import os

class Deploy:
    def __init__(self):
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yaml')
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

        self.repositorio = config['repositorio']
        self.usuario = config['usuario']
        self.diretorio_projeto = config['diretorio']  # Caminho do projeto

        # Ler o token do arquivo e definir como variável de ambiente
        token_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'token.txt')
        with open(token_file, 'r') as f:
            self.token = f.read().strip()
        os.environ['GITHUB_TOKEN'] = self.token

    def realizar_deploy(self):
        # Muda para o diretório do projeto
        os.chdir(self.diretorio_projeto)

        # Verifica se a pasta já é um repositório Git
        if not os.path.exists(os.path.join(self.diretorio_projeto, ".git")):
            print("🛠️ Inicializando repositório Git...")
            subprocess.run(["git", "init"])
            subprocess.run(["git", "branch", "-M", "main"])  # Define a branch principal como "main"
            url_repositorio = f"https://{self.token}@github.com/{self.usuario}/{self.repositorio}.git"
            subprocess.run(["git", "remote", "add", "origin", url_repositorio])

        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "Deploy automático"])

        # Corrigir o problema do "fetch first"
        subprocess.run(["git", "pull", "--rebase", "origin", "main"])

        url_repositorio = f"https://{self.token}@github.com/{self.usuario}/{self.repositorio}.git"
        result = subprocess.run(
            ["git", "push", "-u", "origin", "main"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✅ Deploy realizado com sucesso!")
        else:
            print("❌ Erro ao realizar deploy:", result.stderr)

if __name__ == "__main__":
    deploy = Deploy()
    deploy.realizar_deploy()
