import streamlit as st
import os
import sys
import json
from datetime import datetime
import pandas as pd
from io import BytesIO

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Garantir que os diretórios necessários existam
os.makedirs('orcamentos', exist_ok=True)
os.makedirs('data/componentes', exist_ok=True)

# Importar módulos existentes
try:
    from core.models import Orcamento, Painel, Componente
    from core.file_manager import salvar_orcamento, carregar_orcamento, listar_orcamentos, excluir_orcamento
    from core.componentes_manager import listar_componentes_cadastrados, carregar_componente_info, buscar_componentes, inicializar_componentes
    from core.exportador_excel import exportar_orcamento_para_excel
    
    # Inicializar componentes exemplo se não existirem
    if not listar_componentes_cadastrados():
        inicializar_componentes()
        
except ImportError as e:
    st.error(f"Erro ao importar módulos: {e}")
    st.stop()

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
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar estado da sessão
if 'tela_atual' not in st.session_state:
    st.session_state.tela_atual = 'inicio'
if 'orcamento_atual' not in st.session_state:
    st.session_state.orcamento_atual = None
if 'painel_atual' not in st.session_state:
    st.session_state.painel_atual = None

def navegar_para(tela, orcamento=None, painel=None):
    """Função para navegação entre telas"""
    st.session_state.tela_atual = tela
    if orcamento:
        st.session_state.orcamento_atual = orcamento
    if painel:
        st.session_state.painel_atual = painel

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
        
        try:
            orcamentos = listar_orcamentos()
            componentes = listar_componentes_cadastrados()
            
            col_stats1, col_stats2 = st.columns(2)
            with col_stats1:
                st.metric("Orçamentos", len(orcamentos))
            with col_stats2:
                st.metric("Componentes Cadastrados", len(componentes))
                
        except Exception as e:
            st.warning(f"Erro ao carregar estatísticas: {str(e)}")

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
                try:
                    novo_orcamento = Orcamento(nome_novo.strip())
                    salvar_orcamento(novo_orcamento)
                    st.success(f"✅ Orçamento '{nome_novo}' criado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao criar orçamento: {str(e)}")
            else:
                st.warning("⚠️ Digite um nome para o orçamento")
    
    st.markdown("---")
    
    # Lista de orçamentos
    st.subheader("📄 Orçamentos Existentes")
    
    try:
        orcamentos = listar_orcamentos()
        
        if not orcamentos:
            st.info("📝 Nenhum orçamento encontrado. Crie seu primeiro orçamento acima!")
        else:
            # Busca
            busca = st.text_input("🔍 Buscar orçamento", placeholder="Digite para filtrar...")
            
            # Filtrar orçamentos
            if busca:
                orcamentos_filtrados = [orc for orc in orcamentos if busca.lower() in orc['nome_exibicao'].lower()]
            else:
                orcamentos_filtrados = orcamentos
            
            if not orcamentos_filtrados:
                st.warning("🔍 Nenhum orçamento encontrado com esse filtro")
            else:
                # Exibir orçamentos
                for orc in orcamentos_filtrados:
                    with st.container():
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        
                        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                        
                        with col1:
                            st.write(f"**📋 {orc['nome_exibicao']}**")
                            st.caption(f"Arquivo: {orc['nome_arquivo']}")
                        
                        with col2:
                            if st.button("📂 Abrir", key=f"abrir_{orc['nome_arquivo']}"):
                                try:
                                    orcamento = carregar_orcamento(orc['nome_arquivo'])
                                    navegar_para('paineis', orcamento)
                                except Exception as e:
                                    st.error(f"Erro ao abrir: {str(e)}")
                        
                        with col3:
                            if st.button("📤 Exportar", key=f"export_{orc['nome_arquivo']}"):
                                try:
                                    orcamento = carregar_orcamento(orc['nome_arquivo'])
                                    buffer = BytesIO()
                                    exportar_orcamento_para_excel(orcamento, buffer)
                                    buffer.seek(0)
                                    
                                    st.download_button(
                                        label="⬇️ Download Excel",
                                        data=buffer.getvalue(),
                                        file_name=f"{orcamento.nome}.xlsx",
                                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                        key=f"download_{orc['nome_arquivo']}"
                                    )
                                except Exception as e:
                                    st.error(f"Erro na exportação: {str(e)}")
                        
                        with col4:
                            if st.button("🗑️ Excluir", key=f"excluir_{orc['nome_arquivo']}"):
                                try:
                                    excluir_orcamento(orc['nome_arquivo'])
                                    st.success("✅ Orçamento excluído!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Erro ao excluir: {str(e)}")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        
    except Exception as e:
        st.error(f"❌ Erro ao carregar orçamentos: {str(e)}")

def tela_paineis():
    """Tela de gerenciamento de painéis"""
    orcamento = st.session_state.orcamento_atual
    
    if not orcamento:
        st.error("❌ Nenhum orçamento selecionado")
        if st.button("⬅️ Voltar aos Orçamentos"):
            navegar_para('orcamentos')
        return
    
    st.header(f"⚡ Painéis do Orçamento: {orcamento.nome}")
    
    # Botão voltar
    if st.button("⬅️ Voltar aos Orçamentos"):
        navegar_para('orcamentos')
    
    st.markdown("---")
    
    # Seção de criação de painel
    st.subheader("➕ Novo Painel")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        nome_painel = st.text_input("Nome do Painel", placeholder="Digite o nome do painel...")
    
    with col2:
        tipo_painel = st.selectbox("Tipo de Painel", ["QDF/QDL"])
        if tipo_painel == "QDF/QDL":
            subtipo = st.selectbox("Subtipo", ["Espinha Completa", "Meia Espinha", "Cabeado"], index=0)
            tipo_completo = f"{tipo_painel} - {subtipo}"
        else:
            tipo_completo = tipo_painel
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Criar Painel", use_container_width=True, type="primary"):
            if nome_painel.strip():
                try:
                    novo_painel = Painel(nome_painel.strip(), tipo_completo)
                    orcamento.adicionar_painel(novo_painel)
                    salvar_orcamento(orcamento)
                    st.success(f"✅ Painel '{nome_painel}' criado!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao criar painel: {str(e)}")
            else:
                st.warning("⚠️ Digite um nome para o painel")
    
    st.markdown("---")
    
    # Lista de painéis
    st.subheader("🔧 Painéis Existentes")
    
    if not orcamento.paineis:
        st.info("🔧 Nenhum painel encontrado. Crie seu primeiro painel acima!")
    else:
        # Busca
        busca_painel = st.text_input("🔍 Buscar painel", placeholder="Digite para filtrar...")
        
        # Filtrar painéis
        if busca_painel:
            paineis_filtrados = [p for p in orcamento.paineis if busca_painel.lower() in p.nome.lower()]
        else:
            paineis_filtrados = orcamento.paineis
        
        if not paineis_filtrados:
            st.warning("🔍 Nenhum painel encontrado com esse filtro")
        else:
            for painel in paineis_filtrados:
                with st.container():
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"**⚡ {painel.nome}**")
                        st.caption(f"Tipo: {painel.tipo} | Componentes: {len(painel.componentes)}")
                    
                    with col2:
                        if st.button("📂 Abrir", key=f"abrir_painel_{painel.nome}"):
                            navegar_para('componentes', orcamento, painel)
                    
                    with col3:
                        if st.button("🗑️ Excluir", key=f"excluir_painel_{painel.nome}"):
                            try:
                                orcamento.remover_painel(painel.nome)
                                salvar_orcamento(orcamento)
                                st.success("✅ Painel excluído!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao excluir: {str(e)}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)

def tela_componentes():
    """Tela de gerenciamento de componentes do painel"""
    orcamento = st.session_state.orcamento_atual
    painel = st.session_state.painel_atual
    
    if not orcamento or not painel:
        st.error("❌ Orçamento ou painel não selecionado")
        if st.button("⬅️ Voltar"):
            navegar_para('paineis', orcamento)
        return
    
    st.header(f"🔧 Componentes do Painel: {painel.nome}")
    st.caption(f"Orçamento: {orcamento.nome} | Tipo: {painel.tipo}")
    
    # Botão voltar
    if st.button("⬅️ Voltar aos Painéis"):
        navegar_para('paineis', orcamento)
    
    st.markdown("---")
    
    # Seção de adição de componentes
    st.subheader("➕ Adicionar Componentes")
    
    try:
        componentes_cadastrados = listar_componentes_cadastrados()
        
        if not componentes_cadastrados:
            st.warning("⚠️ Nenhum componente cadastrado. Vá para Administração para cadastrar componentes.")
        else:
            # Busca de componentes
            busca_comp = st.text_input("🔍 Buscar componente", placeholder="Digite para filtrar componentes...")
            
            if busca_comp:
                componentes_filtrados = buscar_componentes(busca_comp)
            else:
                componentes_filtrados = componentes_cadastrados
            
            if componentes_filtrados:
                st.write("**Componentes Disponíveis:**")
                
                for comp_nome in componentes_filtrados:
                    try:
                        comp_info = carregar_componente_info(comp_nome)
                        
                        with st.container():
                            st.markdown('<div class="card">', unsafe_allow_html=True)
                            
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                st.write(f"**🔧 {comp_info.nome}**")
                                if comp_info.descricao:
                                    st.caption(comp_info.descricao)
                            
                            with col2:
                                if st.button("➕ Adicionar", key=f"add_{comp_nome}"):
                                    # Modal para quantidade
                                    st.session_state[f'show_qty_{comp_nome}'] = True
                            
                            # Modal de quantidade
                            if st.session_state.get(f'show_qty_{comp_nome}', False):
                                with st.form(f"form_{comp_nome}"):
                                    quantidade = st.number_input("Quantidade", min_value=1, value=1)
                                    
                                    col_form1, col_form2 = st.columns(2)
                                    with col_form1:
                                        if st.form_submit_button("✅ Confirmar", type="primary"):
                                            try:
                                                componente = Componente(comp_info.nome, quantidade)
                                                painel.adicionar_componente(componente)
                                                salvar_orcamento(orcamento)
                                                st.success(f"✅ {quantidade}x {comp_info.nome} adicionado!")
                                                st.session_state[f'show_qty_{comp_nome}'] = False
                                                st.rerun()
                                            except Exception as e:
                                                st.error(f"Erro: {str(e)}")
                                    
                                    with col_form2:
                                        if st.form_submit_button("❌ Cancelar"):
                                            st.session_state[f'show_qty_{comp_nome}'] = False
                                            st.rerun()
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    except Exception as e:
                        st.error(f"Erro ao carregar componente {comp_nome}: {str(e)}")
            else:
                st.info("🔍 Nenhum componente encontrado com esse filtro")
                
    except Exception as e:
        st.error(f"❌ Erro ao carregar componentes: {str(e)}")
    
    st.markdown("---")
    
    # Lista de componentes do painel
    st.subheader("📋 Componentes no Painel")
    
    if not painel.componentes:
        st.info("📋 Nenhum componente adicionado ao painel ainda.")
    else:
        for i, comp in enumerate(painel.componentes):
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**🔧 {comp.nome}**")
                    st.caption(f"Quantidade: {comp.quantidade}")
                
                with col2:
                    if st.button("🗑️ Remover", key=f"remove_{i}"):
                        try:
                            painel.remover_componente(i)
                            salvar_orcamento(orcamento)
                            st.success("✅ Componente removido!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro: {str(e)}")
                
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
                try:
                    from core.componentes_manager import salvar_componente_info, ComponenteInfo
                    
                    comp_info = ComponenteInfo(nome_comp.strip(), desc_comp.strip())
                    salvar_componente_info(comp_info)
                    st.success(f"✅ Componente '{nome_comp}' criado!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao criar componente: {str(e)}")
            else:
                st.warning("⚠️ Digite um nome para o componente")
    
    st.markdown("---")
    
    # Lista de componentes
    st.subheader("🔧 Componentes Cadastrados")
    
    try:
        componentes = listar_componentes_cadastrados()
        
        if not componentes:
            st.info("🔧 Nenhum componente cadastrado ainda.")
        else:
            # Busca
            busca_admin = st.text_input("🔍 Buscar componente", placeholder="Digite para filtrar...")
            
            if busca_admin:
                componentes_filtrados = buscar_componentes(busca_admin)
            else:
                componentes_filtrados = componentes
            
            if not componentes_filtrados:
                st.warning("🔍 Nenhum componente encontrado")
            else:
                for comp_nome in componentes_filtrados:
                    try:
                        comp_info = carregar_componente_info(comp_nome)
                        
                        with st.container():
                            st.markdown('<div class="card">', unsafe_allow_html=True)
                            
                            col1, col2, col3 = st.columns([3, 1, 1])
                            
                            with col1:
                                st.write(f"**🔧 {comp_info.nome}**")
                                if comp_info.descricao:
                                    st.caption(comp_info.descricao)
                                st.caption(f"Regras derivadas: {len(comp_info.regras_derivadas)}")
                            
                            with col2:
                                if st.button("✏️ Editar", key=f"edit_{comp_nome}"):
                                    st.session_state[f'edit_mode_{comp_nome}'] = True
                            
                            with col3:
                                if st.button("🗑️ Excluir", key=f"del_{comp_nome}"):
                                    try:
                                        from core.componentes_manager import excluir_componente
                                        excluir_componente(comp_nome)
                                        st.success("✅ Componente excluído!")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Erro: {str(e)}")
                            
                            # Modal de edição
                            if st.session_state.get(f'edit_mode_{comp_nome}', False):
                                with st.form(f"edit_form_{comp_nome}"):
                                    st.write("**Editando Componente:**")
                                    
                                    novo_nome = st.text_input("Nome", value=comp_info.nome)
                                    nova_desc = st.text_area("Descrição", value=comp_info.descricao)
                                    
                                    col_edit1, col_edit2 = st.columns(2)
                                    with col_edit1:
                                        if st.form_submit_button("✅ Salvar", type="primary"):
                                            try:
                                                from core.componentes_manager import salvar_componente_info, excluir_componente, ComponenteInfo
                                                
                                                # Se nome mudou, excluir o antigo
                                                if novo_nome != comp_info.nome:
                                                    excluir_componente(comp_nome)
                                                
                                                # Salvar com novos dados
                                                comp_atualizado = ComponenteInfo(novo_nome, nova_desc, comp_info.regras_derivadas)
                                                salvar_componente_info(comp_atualizado)
                                                
                                                st.success("✅ Componente atualizado!")
                                                st.session_state[f'edit_mode_{comp_nome}'] = False
                                                st.rerun()
                                            except Exception as e:
                                                st.error(f"Erro: {str(e)}")
                                    
                                    with col_edit2:
                                        if st.form_submit_button("❌ Cancelar"):
                                            st.session_state[f'edit_mode_{comp_nome}'] = False
                                            st.rerun()
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                    except Exception as e:
                        st.error(f"Erro ao carregar {comp_nome}: {str(e)}")
                        
    except Exception as e:
        st.error(f"❌ Erro ao carregar componentes: {str(e)}")

# Sidebar de navegação
with st.sidebar:
    st.title("🧭 Navegação")
    
    # Breadcrumb
    if st.session_state.tela_atual != 'inicio':
        st.markdown("**📍 Você está em:**")
        
        if st.session_state.tela_atual == 'orcamentos':
            st.write("📋 Orçamentos")
        elif st.session_state.tela_atual == 'paineis' and st.session_state.orcamento_atual:
            if st.button("📋 " + st.session_state.orcamento_atual.nome, key="breadcrumb_orc"):
                navegar_para('paineis', st.session_state.orcamento_atual)
            st.write("⚡ Painéis")
        elif st.session_state.tela_atual == 'componentes':
            if st.session_state.orcamento_atual and st.button("📋 " + st.session_state.orcamento_atual.nome, key="breadcrumb_orc2"):
                navegar_para('paineis', st.session_state.orcamento_atual)
            if st.session_state.painel_atual:
                st.write("⚡ " + st.session_state.painel_atual.nome)
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

# Roteamento principal
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