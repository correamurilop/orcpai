"""
ORCPAI - Sistema de Orçamento de Painéis
Aplicação Streamlit principal - Versão Modularizada
"""

import streamlit as st

# =============================================================================
# IMPORTS E CONFIGURAÇÕES
# =============================================================================

# Database Manager
try:
    from database_manager import db
except ImportError as e:
    st.error(f"Erro ao importar database manager: {e}")
    st.stop()

# Utilitários
from utils import criar_barra_navegacao, navegar_para, aplicar_estilos

# Telas do sistema
from screens import (
    tela_inicio,
    tela_orcamentos, 
    tela_paineis,
    tela_componentes,
    tela_admin
)

# =============================================================================
# VERIFICAÇÕES INICIAIS
# =============================================================================

# Verificar conexão com banco
if not db.is_connected():
    st.error("❌ Não foi possível conectar ao banco de dados")
    st.stop()

# =============================================================================
# CONFIGURAÇÃO DA PÁGINA
# =============================================================================

# Importar configurações
from config import STREAMLIT_CONFIG

st.set_page_config(
    page_title=STREAMLIT_CONFIG['page_title'],
    page_icon=STREAMLIT_CONFIG['page_icon'],
    layout=STREAMLIT_CONFIG['layout'],
    initial_sidebar_state=STREAMLIT_CONFIG['initial_sidebar_state']
)

# Aplicar estilos CSS
aplicar_estilos()

# =============================================================================
# INICIALIZAÇÃO DO ESTADO
# =============================================================================

# Importar configurações de estado
from config import INITIAL_SESSION_STATE

# Inicializar estado da sessão
for key, value in INITIAL_SESSION_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =============================================================================
# INTERFACE PRINCIPAL
# =============================================================================

# Criar barra de navegação superior
criar_barra_navegacao()

# =============================================================================
# ROTEAMENTO PRINCIPAL
# =============================================================================

if st.session_state.tela_atual == 'inicio':
    tela_inicio()
elif st.session_state.tela_atual == 'orcamentos':
    tela_orcamentos()
elif st.session_state.tela_atual == 'paineis':
    tela_paineis()
elif st.session_state.tela_atual == 'componentes':
    tela_componentes()
elif st.session_state.tela_atual == 'admin':
    tela_admin()
else:
    tela_inicio() 