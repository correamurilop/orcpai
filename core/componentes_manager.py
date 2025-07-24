import json
import os
from typing import List, Dict, Any
from core.models import Componente

COMPONENTES_DIR = "data/componentes/"

class ComponenteInfo:
    """Classe para representar informações de um componente pré-cadastrado"""
    
    def __init__(self, nome: str, descricao: str = "", regras_derivadas: List[Dict] = None):
        self.nome = nome
        self.descricao = descricao
        self.regras_derivadas = regras_derivadas or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            'nome': self.nome,
            'descricao': self.descricao,
            'regras_derivadas': self.regras_derivadas
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ComponenteInfo':
        """Cria a partir de dicionário"""
        return cls(
            nome=data['nome'],
            descricao=data.get('descricao', ''),
            regras_derivadas=data.get('regras_derivadas', [])
        )

def garantir_diretorio_componentes():
    """Garante que o diretório de componentes existe"""
    if not os.path.exists(COMPONENTES_DIR):
        os.makedirs(COMPONENTES_DIR)

def salvar_componente_info(componente_info: ComponenteInfo):
    """Salva informações de um componente em arquivo .componente"""
    garantir_diretorio_componentes()
    
    # Nome do arquivo baseado no nome do componente (sanitizado)
    nome_arquivo = sanitizar_nome_arquivo(componente_info.nome)
    caminho = os.path.join(COMPONENTES_DIR, f"{nome_arquivo}.componente")
    
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(componente_info.to_dict(), f, ensure_ascii=False, indent=2)

def carregar_componente_info(nome_componente: str) -> ComponenteInfo:
    """Carrega informações de um componente"""
    nome_arquivo = sanitizar_nome_arquivo(nome_componente)
    caminho = os.path.join(COMPONENTES_DIR, f"{nome_arquivo}.componente")
    
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Componente não encontrado: {nome_componente}")
    
    with open(caminho, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return ComponenteInfo.from_dict(data)

def listar_componentes_cadastrados() -> List[ComponenteInfo]:
    """Lista todos os componentes cadastrados"""
    garantir_diretorio_componentes()
    
    componentes = []
    for arquivo in os.listdir(COMPONENTES_DIR):
        if arquivo.endswith('.componente'):
            try:
                nome_componente = arquivo[:-11]  # Remove .componente
                nome_real = desanitizar_nome_arquivo(nome_componente)
                componente_info = carregar_componente_info(nome_real)
                componentes.append(componente_info)
            except Exception:
                continue
    
    return sorted(componentes, key=lambda x: x.nome)

def buscar_componentes(termo: str = "") -> List[ComponenteInfo]:
    """Busca componentes por termo"""
    todos_componentes = listar_componentes_cadastrados()
    
    if not termo:
        return todos_componentes
    
    resultado = []
    for comp in todos_componentes:
        if termo.lower() in comp.nome.lower():
            resultado.append(comp)
    
    return resultado

def excluir_componente(nome_componente: str) -> bool:
    """Exclui um componente cadastrado"""
    try:
        nome_arquivo = sanitizar_nome_arquivo(nome_componente)
        caminho = os.path.join(COMPONENTES_DIR, f"{nome_arquivo}.componente")
        
        if os.path.exists(caminho):
            os.remove(caminho)
            return True
        return False
    except Exception:
        return False

def sanitizar_nome_arquivo(nome: str) -> str:
    """Sanitiza nome para usar como nome de arquivo"""
    # Remove caracteres especiais e substitui espaços por underscore
    import re
    nome_limpo = re.sub(r'[<>:"/\\|?*]', '', nome)
    nome_limpo = nome_limpo.replace(' ', '_')
    return nome_limpo

def desanitizar_nome_arquivo(nome_arquivo: str) -> str:
    """Converte nome de arquivo de volta para nome original"""
    return nome_arquivo.replace('_', ' ')

def criar_componentes_exemplo():
    """Cria alguns componentes de exemplo para teste"""
    componentes_exemplo = [
        ComponenteInfo(
            nome="Disjuntor Trifásico 32A",
            descricao="Disjuntor tripolar 32A para proteção de circuitos trifásicos",
            regras_derivadas=[
                {"nome": "Parafuso M4x20", "quantidade": 2},
                {"nome": "Trilho DIN 35mm", "quantidade": 1}
            ]
        ),
        ComponenteInfo(
            nome="Disjuntor Monofásico 16A",
            descricao="Disjuntor unipolar 16A para proteção de circuitos monofásicos",
            regras_derivadas=[
                {"nome": "Parafuso M4x16", "quantidade": 1},
                {"nome": "Trilho DIN 35mm", "quantidade": 1}
            ]
        ),
        ComponenteInfo(
            nome="Contator 25A",
            descricao="Contator tripolar 25A para comando de motores",
            regras_derivadas=[
                {"nome": "Parafuso M5x25", "quantidade": 4},
                {"nome": "Trilho DIN 35mm", "quantidade": 2}
            ]
        ),
        ComponenteInfo(
            nome="Relé Térmico 16-25A",
            descricao="Relé térmico ajustável para proteção de sobrecarga",
            regras_derivadas=[
                {"nome": "Parafuso M4x20", "quantidade": 2}
            ]
        )
    ]
    
    for comp in componentes_exemplo:
        salvar_componente_info(comp)

# Inicializar com componentes exemplo se não existir nenhum
def inicializar_componentes():
    """Inicializa o sistema com componentes exemplo se necessário"""
    if not listar_componentes_cadastrados():
        criar_componentes_exemplo() 