import tkinter as tk
from tkinter import messagebox
import yaml
import os
import subprocess

# Arquivo onde o token será salvo
TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token.txt")
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.yaml")
MAIN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")

class pyInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Configuração do Deploy")

        self.create_widgets()

    def create_widgets(self):
        # Usuário GitHub
        tk.Label(self.root, text="Usuário do GitHub:").grid(row=0, column=0)
        self.entry_usuario = tk.Entry(self.root)
        self.entry_usuario.grid(row=0, column=1)

        # Repositório GitHub
        tk.Label(self.root, text="Repositório:").grid(row=1, column=0)
        self.entry_repositorio = tk.Entry(self.root)
        self.entry_repositorio.grid(row=1, column=1)

        # Diretório do projeto
        tk.Label(self.root, text="Diretório do Projeto:").grid(row=2, column=0)
        self.entry_diretorio = tk.Entry(self.root)
        self.entry_diretorio.grid(row=2, column=1)

        # Token do GitHub
        tk.Label(self.root, text="Token do GitHub:").grid(row=3, column=0)
        self.entry_token = tk.Entry(self.root, show="*")  # O token não aparece
        self.entry_token.grid(row=3, column=1)

        tk.Label(self.root, text="horario de verificação").grid(row=4, column=0)
        self.entry_horario = tk.Entry(self.root)  # O token não aparece
        self.entry_horario.grid(row=4, column=1)

        # Botão para salvar
        self.btn_salvar = tk.Button(self.root, text="Salvar Configurações", command=self.salvar_configuracoes)
        self.btn_salvar.grid(row=5, column=0, columnspan=2)

    def salvar_configuracoes(self):
        usuario = self.entry_usuario.get()
        repositorio = self.entry_repositorio.get()
        diretorio = self.entry_diretorio.get()
        token = self.entry_token.get()
        horario = self.entry_horario.get()

        if not usuario or not repositorio or not diretorio or not token or not horario:
            messagebox.showwarning("Erro", "Todos os campos são obrigatórios!")
            return

        # Salvar configurações básicas
        config = {
            "usuario": usuario,
            "repositorio": repositorio,
            "diretorio": diretorio,
            "horario": horario
        }

        with open(CONFIG_FILE, "w") as f:
            yaml.dump(config, f)

        # Salvar o token no arquivo de texto
        with open(TOKEN_FILE, "w") as f:
            f.write(token)

        messagebox.showinfo("Sucesso", "Configurações salvas!")

        # Executar main.py
        subprocess.Popen(["python", MAIN_FILE])

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    interface = pyInterface()
    interface.run()
