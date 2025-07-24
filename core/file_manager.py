import json
import os
from typing import List
from core.models import Orcamento

def salvar_orcamento(orcamento: Orcamento, caminho: str):
    """Salva o objeto Orcamento em um arquivo .orcpai no caminho especificado"""
    # Garantir que o diretório existe
    diretorio = os.path.dirname(caminho)
    if diretorio and not os.path.exists(diretorio):
        os.makedirs(diretorio)
    
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(orcamento.to_dict(), f, ensure_ascii=False, indent=4)

def carregar_orcamento(caminho: str) -> Orcamento:
    """Carrega um arquivo .orcpai e retorna um objeto Orcamento"""
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return Orcamento.from_dict(data)
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
    except json.JSONDecodeError:
        raise ValueError(f"Arquivo corrompido ou formato inválido: {caminho}")

def listar_arquivos_orcamentos(diretorio: str = 'orcamentos/') -> List[str]:
    """Retorna uma lista com os caminhos dos arquivos .orcpai na pasta informada"""
    # Garantir que o diretório existe
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
        return []
    
    arquivos = []
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.orcpai'):
            arquivos.append(os.path.join(diretorio, arquivo))
    
    return sorted(arquivos)

def excluir_orcamento(caminho: str) -> bool:
    """Exclui um arquivo de orçamento. Retorna True se bem-sucedido"""
    try:
        if os.path.exists(caminho):
            os.remove(caminho)
            return True
        return False
    except OSError:
        return False

def obter_nome_arquivo_sem_extensao(caminho: str) -> str:
    """Retorna o nome do arquivo sem extensão e sem o caminho"""
    nome_completo = os.path.basename(caminho)
    return os.path.splitext(nome_completo)[0] 