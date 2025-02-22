import os
import hashlib
import json

def verificar_alteracoes(diretorio):
    print(f"Verificando alterações no diretório: {diretorio}")  # Mensagem de depuração
    arquivos_hash = {}

    # Função para calcular o hash de um arquivo
    def calcular_hash(arquivo):
        hasher = hashlib.sha256()
        with open(arquivo, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    # Verifica os arquivos no diretório
    for raiz, _, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            caminho_arquivo = os.path.join(raiz, arquivo)
            print(f"Lendo arquivo: {caminho_arquivo}")  # Mensagem de depuração
            if os.path.isfile(caminho_arquivo):  # Verifica se é um arquivo
                hash_atual = calcular_hash(caminho_arquivo)  # Calcula o hash atual do arquivo
                arquivos_hash[caminho_arquivo] = hash_atual
                print(f"Hash calculado para {caminho_arquivo}: {hash_atual}")  # Mensagem de depuração
            else:
                print(f"{caminho_arquivo} não é um arquivo.")  # Mensagem de depuração

    # Verificar o estado atual antes de salvar
    print(f"Estado atual dos arquivos: {arquivos_hash}")  # Mensagem de depuração

    # Define o caminho absoluto para o arquivo estado_anterior.json na pasta do projeto
    estado_anterior_path = os.path.join(os.path.dirname(__file__), 'estado_anterior.json')

    # Carrega o estado anterior dos arquivos
    estado_anterior = {}
    if os.path.exists(estado_anterior_path) and os.path.getsize(estado_anterior_path) > 0:
        with open(estado_anterior_path, 'r') as f:
            try:
                estado_anterior = json.load(f)
            except json.JSONDecodeError:
                estado_anterior = {}

    # Se o estado anterior estiver vazio, salva o estado atual e retorna False
    if not estado_anterior:
        with open(estado_anterior_path, 'w') as f:
            json.dump(arquivos_hash, f, indent=4)
        print("Estado anterior vazio. Estado atual salvo.")
        print(f"Estado atual salvo: {arquivos_hash}")
        return False

    # Compara o estado atual com o estado anterior
    alteracoes = False
    for arquivo, hash_atual in arquivos_hash.items():
        hash_anterior = estado_anterior.get(arquivo)
        if hash_anterior != hash_atual:  # Compara o hash atual com o hash anterior
            print(f"Alteração detectada no arquivo: {arquivo}")
            alteracoes = True
            break

    if not alteracoes:
        print("Nenhuma alteração detectada.")

    # Salva o estado atual dos arquivos
    with open(estado_anterior_path, 'w') as f:
        json.dump(arquivos_hash, f, indent=4)

    return alteracoes  # Retorna True se houver alterações, False caso contrário.