from datetime import datetime
from typing import List, Dict, Any

class Componente:
    """Representa um componente de painel com nome e quantidade"""
    
    def __init__(self, nome: str, quantidade: int):
        self.nome = nome
        self.quantidade = quantidade
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o componente para dicionário"""
        return {
            'nome': self.nome,
            'quantidade': self.quantidade
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Componente':
        """Cria um componente a partir de um dicionário"""
        return cls(
            nome=data['nome'],
            quantidade=data['quantidade']
        )
    
    def __repr__(self):
        return f"Componente(nome='{self.nome}', quantidade={self.quantidade})"

class Painel:
    """Representa um painel elétrico com seus componentes"""
    
    def __init__(self, nome: str, tipo: str = "QDF"):
        self.nome = nome
        self.tipo = tipo
        self.componentes: List[Componente] = []
    
    def adicionar_componente(self, componente: Componente):
        """Adiciona um componente ao painel"""
        self.componentes.append(componente)
    
    def remover_componente(self, nome_componente: str):
        """Remove um componente pelo nome"""
        self.componentes = [c for c in self.componentes if c.nome != nome_componente]
    
    def obter_componente(self, nome: str) -> Componente:
        """Busca um componente pelo nome"""
        for componente in self.componentes:
            if componente.nome == nome:
                return componente
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o painel para dicionário"""
        return {
            'nome': self.nome,
            'tipo': self.tipo,
            'componentes': [c.to_dict() for c in self.componentes]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Painel':
        """Cria um painel a partir de um dicionário"""
        painel = cls(
            nome=data['nome'],
            tipo=data.get('tipo', 'QDF')
        )
        for comp_data in data.get('componentes', []):
            painel.adicionar_componente(Componente.from_dict(comp_data))
        return painel
    
    def __repr__(self):
        return f"Painel(nome='{self.nome}', tipo='{self.tipo}', componentes={len(self.componentes)})"

class Orcamento:
    """Representa um orçamento completo com múltiplos painéis"""
    
    def __init__(self, nome: str, data: str = None):
        self.nome = nome
        self.data = data or datetime.now().strftime('%Y-%m-%d')
        self.paineis: List[Painel] = []
    
    def adicionar_painel(self, painel: Painel):
        """Adiciona um painel ao orçamento"""
        self.paineis.append(painel)
    
    def remover_painel(self, nome_painel: str):
        """Remove um painel pelo nome"""
        self.paineis = [p for p in self.paineis if p.nome != nome_painel]
    
    def obter_painel(self, nome: str) -> Painel:
        """Busca um painel pelo nome"""
        for painel in self.paineis:
            if painel.nome == nome:
                return painel
        return None
    
    def obter_todos_componentes(self) -> List[tuple]:
        """Retorna todos os componentes de todos os painéis como lista de tuplas (painel_nome, componente)"""
        componentes = []
        for painel in self.paineis:
            for componente in painel.componentes:
                componentes.append((painel.nome, componente))
        return componentes
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o orçamento para dicionário"""
        return {
            'nome': self.nome,
            'data': self.data,
            'paineis': [p.to_dict() for p in self.paineis]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Orcamento':
        """Cria um orçamento a partir de um dicionário"""
        orcamento = cls(
            nome=data['nome'],
            data=data.get('data', datetime.now().strftime('%Y-%m-%d'))
        )
        for painel_data in data.get('paineis', []):
            orcamento.adicionar_painel(Painel.from_dict(painel_data))
        return orcamento
    
    def __repr__(self):
        return f"Orcamento(nome='{self.nome}', data='{self.data}', paineis={len(self.paineis)})" 