# Funções de Navegação - Streamlit
import streamlit as st

def navegar_para(tela, orcamento=None, painel=None):
    """Função para navegação entre telas"""
    st.session_state.tela_atual = tela
    if orcamento:
        st.session_state.orcamento_atual = orcamento
    if painel:
        st.session_state.painel_atual = painel

def criar_barra_navegacao():
    """Cria a barra de navegação superior"""
    # Container para a barra de navegação
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    
    # Linha principal com logo e navegação
    col_logo, col_nav, col_breadcrumb = st.columns([2, 4, 3])
    
    with col_logo:
        st.markdown("### ⚡ ORCPAI")
    
    with col_nav:
        # Menu principal horizontal
        nav_col1, nav_col2, nav_col3 = st.columns(3)
        
        with nav_col1:
            if st.button("🏠 Início", use_container_width=True, key="nav_inicio", type="primary"):
                navegar_para('inicio')
        
        with nav_col2:
            if st.button("📋 Orçamentos", use_container_width=True, key="nav_orcamentos", type="primary"):
                navegar_para('orcamentos')
        
        with nav_col3:
            if st.button("⚙️ Administração", use_container_width=True, key="nav_admin", type="primary"):
                navegar_para('admin')
    
    with col_breadcrumb:
        # Breadcrumb dinâmico
        if st.session_state.tela_atual != 'inicio':
            breadcrumb_items = []
            
            if st.session_state.tela_atual == 'orcamentos':
                breadcrumb_items = ["📋 Orçamentos"]
            
            elif st.session_state.tela_atual == 'paineis' and st.session_state.orcamento_atual:
                breadcrumb_items = [
                    f"📋 {st.session_state.orcamento_atual['nome'][:20]}",
                    "⚡ Painéis"
                ]
            
            elif st.session_state.tela_atual == 'componentes':
                if st.session_state.orcamento_atual and st.session_state.painel_atual:
                    breadcrumb_items = [
                        f"📋 {st.session_state.orcamento_atual['nome'][:15]}",
                        f"⚡ {st.session_state.painel_atual['nome'][:15]}"
                    ]
            
            elif st.session_state.tela_atual == 'admin':
                breadcrumb_items = ["⚙️ Administração"]
            
            # Mostrar breadcrumb
            if breadcrumb_items:
                breadcrumb_text = " → ".join(breadcrumb_items)
                st.markdown(f"**📍 {breadcrumb_text}**")
        else:
            st.markdown("**Sistema de Orçamento de Painéis Elétricos**")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("")  # Espaçamento 