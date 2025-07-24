import streamlit as st
import json
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="ORCPAI - Orçamento de Painéis",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar estado da sessão
if 'tela_atual' not in st.session_state:
    st.session_state.tela_atual = 'inicio'
if 'orcamentos_demo' not in st.session_state:
    st.session_state.orcamentos_demo = [
        {'nome': 'Orçamento Exemplo 1', 'data': '2025-01-20'},
        {'nome': 'Orçamento Exemplo 2', 'data': '2025-01-19'}
    ]
if 'componentes_demo' not in st.session_state:
    st.session_state.componentes_demo = [
        'Disjuntor 16A',
        'Disjuntor 25A', 
        'Disjuntor 32A',
        'Contator 25A',
        'Relé Térmico'
    ]

def navegar_para(tela):
    """Função para navegação entre telas"""
    st.session_state.tela_atual = tela

def tela_inicio():
    """Tela inicial do sistema"""
    st.markdown('<h1 class="main-header">⚡ ORCPAI</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #6c757d;">Sistema de Orçamento de Painéis Elétricos</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("---")
        
        if st.button("📋 Gerenciar Orçamentos", use_container_width=True, type="primary"):
            navegar_para('orcamentos')
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("⚙️ Administração de Componentes", use_container_width=True):
            navegar_para('admin')
        
        st.markdown("---")
        
        # Estatísticas rápidas
        st.subheader("📊 Resumo do Sistema")
        
        col_stats1, col_stats2 = st.columns(2)
        with col_stats1:
            st.metric("Orçamentos", len(st.session_state.orcamentos_demo))
        with col_stats2:
            st.metric("Componentes Cadastrados", len(st.session_state.componentes_demo))

def tela_orcamentos():
    """Tela de gerenciamento de orçamentos"""
    st.header("📋 Gerenciamento de Orçamentos")
    
    # Botão voltar
    if st.button("⬅️ Voltar ao Início"):
        navegar_para('inicio')
    
    st.markdown("---")
    
    # Seção de criação
    st.subheader("➕ Novo Orçamento")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        nome_novo = st.text_input("Nome do Orçamento", placeholder="Digite o nome do novo orçamento...")
    
    with col2:
        if st.button("Criar", use_container_width=True, type="primary"):
            if nome_novo.strip():
                novo_orc = {
                    'nome': nome_novo.strip(),
                    'data': datetime.now().strftime("%Y-%m-%d")
                }
                st.session_state.orcamentos_demo.append(novo_orc)
                st.success(f"✅ Orçamento '{nome_novo}' criado com sucesso!")
                st.rerun()
            else:
                st.warning("⚠️ Digite um nome para o orçamento")
    
    st.markdown("---")
    
    # Lista de orçamentos
    st.subheader("📄 Orçamentos Existentes")
    
    if not st.session_state.orcamentos_demo:
        st.info("📝 Nenhum orçamento encontrado. Crie seu primeiro orçamento acima!")
    else:
        # Busca
        busca = st.text_input("🔍 Buscar orçamento", placeholder="Digite para filtrar...")
        
        # Filtrar orçamentos
        if busca:
            orcamentos_filtrados = [orc for orc in st.session_state.orcamentos_demo 
                                  if busca.lower() in orc['nome'].lower()]
        else:
            orcamentos_filtrados = st.session_state.orcamentos_demo
        
        if not orcamentos_filtrados:
            st.warning("🔍 Nenhum orçamento encontrado com esse filtro")
        else:
            # Exibir orçamentos
            for i, orc in enumerate(orcamentos_filtrados):
                with st.container():
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**📋 {orc['nome']}**")
                        st.caption(f"Criado em: {orc['data']}")
                    
                    with col2:
                        if st.button("📂 Abrir", key=f"abrir_{i}"):
                            st.info("🚧 Em desenvolvimento - Painéis em breve!")
                    
                    with col3:
                        if st.button("📤 Exportar", key=f"export_{i}"):
                            st.info("🚧 Em desenvolvimento - Exportação em breve!")
                    
                    with col4:
                        if st.button("🗑️ Excluir", key=f"excluir_{i}"):
                            st.session_state.orcamentos_demo.remove(orc)
                            st.success("✅ Orçamento excluído!")
                            st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)

def tela_admin():
    """Tela de administração de componentes"""
    st.header("⚙️ Administração de Componentes")
    
    # Botão voltar
    if st.button("⬅️ Voltar ao Início"):
        navegar_para('inicio')
    
    st.markdown("---")
    
    # Seção de criação
    st.subheader("➕ Novo Componente")
    
    with st.form("novo_componente"):
        col1, col2 = st.columns([2, 2])
        
        with col1:
            nome_comp = st.text_input("Nome do Componente", placeholder="Ex: Disjuntor 32A")
        
        with col2:
            desc_comp = st.text_area("Descrição", placeholder="Descrição opcional do componente")
        
        if st.form_submit_button("Criar Componente", type="primary"):
            if nome_comp.strip():
                st.session_state.componentes_demo.append(nome_comp.strip())
                st.success(f"✅ Componente '{nome_comp}' criado!")
                st.rerun()
            else:
                st.warning("⚠️ Digite um nome para o componente")
    
    st.markdown("---")
    
    # Lista de componentes
    st.subheader("🔧 Componentes Cadastrados")
    
    if not st.session_state.componentes_demo:
        st.info("🔧 Nenhum componente cadastrado ainda.")
    else:
        # Busca
        busca_admin = st.text_input("🔍 Buscar componente", placeholder="Digite para filtrar...")
        
        if busca_admin:
            componentes_filtrados = [comp for comp in st.session_state.componentes_demo 
                                   if busca_admin.lower() in comp.lower()]
        else:
            componentes_filtrados = st.session_state.componentes_demo
        
        if not componentes_filtrados:
            st.warning("🔍 Nenhum componente encontrado")
        else:
            for i, comp_nome in enumerate(componentes_filtrados):
                with st.container():
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"**🔧 {comp_nome}**")
                        st.caption("Componente de exemplo")
                    
                    with col2:
                        if st.button("✏️ Editar", key=f"edit_{i}"):
                            st.info("🚧 Em desenvolvimento - Edição em breve!")
                    
                    with col3:
                        if st.button("🗑️ Excluir", key=f"del_{i}"):
                            st.session_state.componentes_demo.remove(comp_nome)
                            st.success("✅ Componente excluído!")
                            st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar de navegação
with st.sidebar:
    st.title("🧭 Navegação")
    
    # Breadcrumb
    if st.session_state.tela_atual != 'inicio':
        st.markdown("**📍 Você está em:**")
        
        if st.session_state.tela_atual == 'orcamentos':
            st.write("📋 Orçamentos")
        elif st.session_state.tela_atual == 'admin':
            st.write("⚙️ Administração")
        
        st.markdown("---")
    
    # Menu principal
    st.markdown("**🏠 Menu Principal:**")
    
    if st.button("🏠 Início", use_container_width=True):
        navegar_para('inicio')
    
    if st.button("📋 Orçamentos", use_container_width=True):
        navegar_para('orcamentos')
    
    if st.button("⚙️ Administração", use_container_width=True):
        navegar_para('admin')
    
    st.markdown("---")
    st.markdown("**ℹ️ Sobre:**")
    st.caption("ORCPAI v1.0")
    st.caption("Sistema de Orçamento de Painéis Elétricos")
    st.caption("🚧 Versão de Desenvolvimento")

# Roteamento principal
if st.session_state.tela_atual == 'inicio':
    tela_inicio()
elif st.session_state.tela_atual == 'orcamentos':
    tela_orcamentos()
elif st.session_state.tela_atual == 'admin':
    tela_admin()
else:
    tela_inicio() 