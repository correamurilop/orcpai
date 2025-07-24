import streamlit as st
import json
import os
from datetime import datetime
from core.models import Orcamento, Painel, Componente
from core.componentes_manager import ComponenteInfo

class StreamlitStorage:
    """Adaptador de storage para Streamlit Cloud usando session_state"""
    
    def __init__(self):
        self.inicializar_session_state()
    
    def inicializar_session_state(self):
        """Inicializa os dados na sessão se não existirem"""
        if 'orcamentos_data' not in st.session_state:
            st.session_state.orcamentos_data = {}
        
        if 'componentes_data' not in st.session_state:
            st.session_state.componentes_data = self.criar_componentes_exemplo()
    
    def criar_componentes_exemplo(self):
        """Cria componentes exemplo"""
        componentes = {}
        
        exemplos = [
            ComponenteInfo("Disjuntor 16A", "Disjuntor monopolar 16 ampères"),
            ComponenteInfo("Disjuntor 25A", "Disjuntor monopolar 25 ampères"),
            ComponenteInfo("Disjuntor 32A", "Disjuntor monopolar 32 ampères"),
            ComponenteInfo("Contator 25A", "Contator tripolar 25 ampères"),
            ComponenteInfo("Relé Térmico", "Relé de proteção térmica"),
            ComponenteInfo("Trilho DIN", "Trilho para fixação de componentes"),
            ComponenteInfo("Borne 4mm", "Borne de ligação 4mm²"),
            ComponenteInfo("Parafuso M4", "Parafuso para fixação M4x20"),
        ]
        
        for comp in exemplos:
            componentes[comp.nome] = comp.to_dict()
        
        return componentes
    
    # Métodos para Orçamentos
    def salvar_orcamento(self, orcamento):
        """Salva orçamento na sessão"""
        nome_arquivo = self.gerar_nome_arquivo(orcamento.nome)
        st.session_state.orcamentos_data[nome_arquivo] = orcamento.to_dict()
        return nome_arquivo
    
    def carregar_orcamento(self, nome_arquivo):
        """Carrega orçamento da sessão"""
        if nome_arquivo in st.session_state.orcamentos_data:
            data = st.session_state.orcamentos_data[nome_arquivo]
            return Orcamento.from_dict(data)
        raise FileNotFoundError(f"Orçamento {nome_arquivo} não encontrado")
    
    def listar_orcamentos(self):
        """Lista todos os orçamentos"""
        lista = []
        for nome_arquivo, data in st.session_state.orcamentos_data.items():
            lista.append({
                'nome_arquivo': nome_arquivo,
                'nome_exibicao': data['nome']
            })
        return lista
    
    def excluir_orcamento(self, nome_arquivo):
        """Exclui orçamento da sessão"""
        if nome_arquivo in st.session_state.orcamentos_data:
            del st.session_state.orcamentos_data[nome_arquivo]
    
    # Métodos para Componentes
    def salvar_componente_info(self, comp_info):
        """Salva componente na sessão"""
        st.session_state.componentes_data[comp_info.nome] = comp_info.to_dict()
    
    def carregar_componente_info(self, nome):
        """Carrega componente da sessão"""
        if nome in st.session_state.componentes_data:
            data = st.session_state.componentes_data[nome]
            return ComponenteInfo.from_dict(data)
        raise FileNotFoundError(f"Componente {nome} não encontrado")
    
    def listar_componentes_cadastrados(self):
        """Lista todos os componentes"""
        return list(st.session_state.componentes_data.keys())
    
    def buscar_componentes(self, termo):
        """Busca componentes por nome"""
        termo = termo.lower()
        return [nome for nome in st.session_state.componentes_data.keys() 
                if termo in nome.lower()]
    
    def excluir_componente(self, nome):
        """Exclui componente da sessão"""
        if nome in st.session_state.componentes_data:
            del st.session_state.componentes_data[nome]
    
    # Métodos utilitários
    def gerar_nome_arquivo(self, nome):
        """Gera nome de arquivo único"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_limpo = nome.replace(" ", "_").replace("/", "_")
        return f"{nome_limpo}_{timestamp}"
    
    def exportar_dados_completos(self):
        """Exporta todos os dados para backup"""
        return {
            'orcamentos': st.session_state.orcamentos_data,
            'componentes': st.session_state.componentes_data,
            'timestamp': datetime.now().isoformat()
        }
    
    def importar_dados_completos(self, dados):
        """Importa dados de backup"""
        if 'orcamentos' in dados:
            st.session_state.orcamentos_data.update(dados['orcamentos'])
        if 'componentes' in dados:
            st.session_state.componentes_data.update(dados['componentes'])

# Instância global
storage = StreamlitStorage() 