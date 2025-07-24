import json
import os
from typing import List
from core.models import Componente

REGRAS_CAMINHO = "data/regras.json"

def carregar_regras() -> List[dict]:
    """Carrega as regras do arquivo JSON"""
    try:
        if not os.path.exists(REGRAS_CAMINHO):
            # Criar arquivo padrão se não existir
            regras_padrao = [
                {
                    "entrada": {"nome": "Disjuntor Trifásico 32A"},
                    "saida": [
                        {"nome": "Parafuso Tipo X", "quantidade": 2},
                        {"nome": "Trilho DIN 12cm", "quantidade": 1}
                    ]
                }
            ]
            salvar_regras(regras_padrao)
            return regras_padrao
        
        with open(REGRAS_CAMINHO, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def salvar_regras(regras: List[dict]):
    """Salva as regras no arquivo JSON"""
    # Garantir que o diretório existe
    diretorio = os.path.dirname(REGRAS_CAMINHO)
    if diretorio and not os.path.exists(diretorio):
        os.makedirs(diretorio)
    
    with open(REGRAS_CAMINHO, 'w', encoding='utf-8') as f:
        json.dump(regras, f, ensure_ascii=False, indent=2)

def aplicar_regras(componente: Componente) -> List[Componente]:
    """
    Aplica as regras a um componente e retorna lista de componentes derivados
    """
    regras = carregar_regras()
    derivados = []
    
    for regra in regras:
        entrada = regra.get('entrada', {})
        nome_regra = entrada.get('nome', '').lower()
        nome_componente = componente.nome.lower()
        
        # Verificar se a regra se aplica (busca por substring)
        if nome_regra in nome_componente or nome_componente in nome_regra:
            for item in regra.get('saida', []):
                nome_derivado = item.get('nome', '')
                quantidade_base = item.get('quantidade', 0)
                
                if nome_derivado and quantidade_base > 0:
                    quantidade_total = quantidade_base * componente.quantidade
                    derivados.append(Componente(
                        nome=nome_derivado, 
                        quantidade=quantidade_total
                    ))
    
    return derivados

def aplicar_regras_painel(painel) -> List[Componente]:
    """
    Aplica regras a todos os componentes de um painel
    Retorna lista consolidada de componentes derivados
    """
    todos_derivados = []
    
    for componente in painel.componentes:
        derivados = aplicar_regras(componente)
        todos_derivados.extend(derivados)
    
    # Consolidar componentes iguais
    componentes_consolidados = {}
    for derivado in todos_derivados:
        if derivado.nome in componentes_consolidados:
            componentes_consolidados[derivado.nome].quantidade += derivado.quantidade
        else:
            componentes_consolidados[derivado.nome] = derivado
    
    return list(componentes_consolidados.values())

def aplicar_regras_orcamento(orcamento) -> List[tuple]:
    """
    Aplica regras a todos os painéis de um orçamento
    Retorna lista de tuplas (nome_painel, componente_derivado)
    """
    resultado = []
    
    for painel in orcamento.paineis:
        derivados = aplicar_regras_painel(painel)
        for derivado in derivados:
            resultado.append((painel.nome, derivado))
    
    return resultado

def validar_regras(texto_json: str) -> tuple:
    """
    Valida se o texto JSON das regras está correto
    Retorna (é_válido, mensagem_erro)
    """
    try:
        regras = json.loads(texto_json)
        
        if not isinstance(regras, list):
            return False, "O arquivo deve conter uma lista de regras."
        
        for i, regra in enumerate(regras):
            if not isinstance(regra, dict):
                return False, f"Regra {i+1} deve ser um objeto."
            
            if 'entrada' not in regra:
                return False, f"Regra {i+1} deve ter campo 'entrada'."
            
            if 'saida' not in regra:
                return False, f"Regra {i+1} deve ter campo 'saida'."
            
            entrada = regra['entrada']
            if not isinstance(entrada, dict) or 'nome' not in entrada:
                return False, f"Regra {i+1}: 'entrada' deve ter campo 'nome'."
            
            saida = regra['saida']
            if not isinstance(saida, list):
                return False, f"Regra {i+1}: 'saida' deve ser uma lista."
            
            for j, item in enumerate(saida):
                if not isinstance(item, dict):
                    return False, f"Regra {i+1}, item {j+1}: deve ser um objeto."
                
                if 'nome' not in item or 'quantidade' not in item:
                    return False, f"Regra {i+1}, item {j+1}: deve ter 'nome' e 'quantidade'."
                
                if not isinstance(item['quantidade'], int) or item['quantidade'] <= 0:
                    return False, f"Regra {i+1}, item {j+1}: 'quantidade' deve ser um número inteiro positivo."
        
        return True, "Regras válidas!"
        
    except json.JSONDecodeError as e:
        return False, f"Erro de JSON: {str(e)}"
    except Exception as e:
        return False, f"Erro: {str(e)}" 