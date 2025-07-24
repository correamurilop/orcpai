import os
from supabase import create_client, Client
from datetime import datetime
from typing import List, Dict, Optional
import streamlit as st

class DatabaseManager:
    """Gerenciador de banco de dados usando Supabase"""
    
    def __init__(self):
        # Credenciais do Supabase
        self.url = "https://muzojaemprdtpkfresdt.supabase.co"
        self.key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im11em9qYWVtcHJkdHBrZnJlc2R0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTMzNzk3NDAsImV4cCI6MjA2ODk1NTc0MH0.HVMdJSq8AKLC8tHpPv9yk8ETacLxvZ-pPBHNeYxyL74"
        
        try:
            self.supabase: Client = create_client(self.url, self.key)
        except Exception as e:
            st.error(f"Erro ao conectar com banco de dados: {e}")
            self.supabase = None
    
    def is_connected(self) -> bool:
        """Verifica se está conectado ao banco"""
        return self.supabase is not None
    
    # ========================
    # MÉTODOS PARA ORÇAMENTOS
    # ========================
    
    def criar_orcamento(self, nome: str) -> Optional[Dict]:
        """Cria um novo orçamento"""
        try:
            result = self.supabase.table('orcamentos').insert({
                'nome': nome
            }).execute()
            
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            st.error(f"Erro ao criar orçamento: {e}")
            return None
    
    def listar_orcamentos(self) -> List[Dict]:
        """Lista todos os orçamentos"""
        try:
            result = self.supabase.table('orcamentos').select('*').order('criado_em', desc=True).execute()
            return result.data if result.data else []
        except Exception as e:
            st.error(f"Erro ao listar orçamentos: {e}")
            return []
    
    def buscar_orcamento(self, orcamento_id: str) -> Optional[Dict]:
        """Busca um orçamento por ID"""
        try:
            result = self.supabase.table('orcamentos').select('*').eq('id', orcamento_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            st.error(f"Erro ao buscar orçamento: {e}")
            return None
    
    def atualizar_orcamento(self, orcamento_id: str, nome: str) -> bool:
        """Atualiza nome do orçamento"""
        try:
            result = self.supabase.table('orcamentos').update({
                'nome': nome,
                'atualizado_em': datetime.now().isoformat()
            }).eq('id', orcamento_id).execute()
            return len(result.data) > 0
        except Exception as e:
            st.error(f"Erro ao atualizar orçamento: {e}")
            return False
    
    def excluir_orcamento(self, orcamento_id: str) -> bool:
        """Exclui um orçamento"""
        try:
            result = self.supabase.table('orcamentos').delete().eq('id', orcamento_id).execute()
            return len(result.data) > 0
        except Exception as e:
            st.error(f"Erro ao excluir orçamento: {e}")
            return False
    
    # ====================
    # MÉTODOS PARA PAINÉIS
    # ====================
    
    def criar_painel(self, orcamento_id: str, nome: str, tipo: str) -> Optional[Dict]:
        """Cria um novo painel"""
        try:
            result = self.supabase.table('paineis').insert({
                'orcamento_id': orcamento_id,
                'nome': nome,
                'tipo': tipo
            }).execute()
            
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            st.error(f"Erro ao criar painel: {e}")
            return None
    
    def listar_paineis(self, orcamento_id: str) -> List[Dict]:
        """Lista painéis de um orçamento"""
        try:
            result = self.supabase.table('paineis').select('*').eq('orcamento_id', orcamento_id).order('criado_em').execute()
            return result.data if result.data else []
        except Exception as e:
            st.error(f"Erro ao listar painéis: {e}")
            return []
    
    def buscar_painel(self, painel_id: str) -> Optional[Dict]:
        """Busca um painel por ID"""
        try:
            result = self.supabase.table('paineis').select('*').eq('id', painel_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            st.error(f"Erro ao buscar painel: {e}")
            return None
    
    def atualizar_painel(self, painel_id: str, nome: str) -> bool:
        """Atualiza nome do painel"""
        try:
            result = self.supabase.table('paineis').update({
                'nome': nome
            }).eq('id', painel_id).execute()
            return len(result.data) > 0
        except Exception as e:
            st.error(f"Erro ao atualizar painel: {e}")
            return False
    
    def excluir_painel(self, painel_id: str) -> bool:
        """Exclui um painel"""
        try:
            result = self.supabase.table('paineis').delete().eq('id', painel_id).execute()
            return len(result.data) > 0
        except Exception as e:
            st.error(f"Erro ao excluir painel: {e}")
            return False
    
    # ===============================
    # MÉTODOS PARA COMPONENTES CADASTRADOS
    # ===============================
    
    def criar_componente_cadastrado(self, nome: str, descricao: str = '') -> Optional[Dict]:
        """Cria um novo componente cadastrado"""
        try:
            result = self.supabase.table('componentes_cadastrados').insert({
                'nome': nome,
                'descricao': descricao
            }).execute()
            
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            st.error(f"Erro ao criar componente: {e}")
            return None
    
    def listar_componentes_cadastrados(self) -> List[Dict]:
        """Lista todos os componentes cadastrados"""
        try:
            result = self.supabase.table('componentes_cadastrados').select('*').order('nome').execute()
            return result.data if result.data else []
        except Exception as e:
            st.error(f"Erro ao listar componentes: {e}")
            return []
    
    def buscar_componentes_cadastrados(self, termo: str) -> List[Dict]:
        """Busca componentes por nome"""
        try:
            result = self.supabase.table('componentes_cadastrados').select('*').ilike('nome', f'%{termo}%').order('nome').execute()
            return result.data if result.data else []
        except Exception as e:
            st.error(f"Erro ao buscar componentes: {e}")
            return []
    
    def atualizar_componente_cadastrado(self, componente_id: str, nome: str, descricao: str) -> bool:
        """Atualiza um componente cadastrado"""
        try:
            result = self.supabase.table('componentes_cadastrados').update({
                'nome': nome,
                'descricao': descricao
            }).eq('id', componente_id).execute()
            return len(result.data) > 0
        except Exception as e:
            st.error(f"Erro ao atualizar componente: {e}")
            return False
    
    def excluir_componente_cadastrado(self, componente_id: str) -> bool:
        """Exclui um componente cadastrado"""
        try:
            result = self.supabase.table('componentes_cadastrados').delete().eq('id', componente_id).execute()
            return len(result.data) > 0
        except Exception as e:
            st.error(f"Erro ao excluir componente: {e}")
            return False
    
    # ===============================
    # MÉTODOS PARA COMPONENTES DO PAINEL
    # ===============================
    
    def adicionar_componente_ao_painel(self, painel_id: str, componente_id: str, quantidade: int) -> Optional[Dict]:
        """Adiciona um componente ao painel"""
        try:
            result = self.supabase.table('componentes_painel').insert({
                'painel_id': painel_id,
                'componente_id': componente_id,
                'quantidade': quantidade
            }).execute()
            
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            st.error(f"Erro ao adicionar componente ao painel: {e}")
            return None
    
    def listar_componentes_do_painel(self, painel_id: str) -> List[Dict]:
        """Lista componentes de um painel com detalhes"""
        try:
            result = self.supabase.table('componentes_painel').select('''
                *,
                componentes_cadastrados (
                    nome,
                    descricao
                )
            ''').eq('painel_id', painel_id).order('criado_em').execute()
            return result.data if result.data else []
        except Exception as e:
            st.error(f"Erro ao listar componentes do painel: {e}")
            return []
    
    def atualizar_quantidade_componente(self, componente_painel_id: str, quantidade: int) -> bool:
        """Atualiza quantidade de um componente no painel"""
        try:
            result = self.supabase.table('componentes_painel').update({
                'quantidade': quantidade
            }).eq('id', componente_painel_id).execute()
            return len(result.data) > 0
        except Exception as e:
            st.error(f"Erro ao atualizar quantidade: {e}")
            return False
    
    def remover_componente_do_painel(self, componente_painel_id: str) -> bool:
        """Remove um componente do painel"""
        try:
            result = self.supabase.table('componentes_painel').delete().eq('id', componente_painel_id).execute()
            return len(result.data) > 0
        except Exception as e:
            st.error(f"Erro ao remover componente: {e}")
            return False

# Instância global
db = DatabaseManager() 