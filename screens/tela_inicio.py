# Tela de Início - Streamlit
import streamlit as st
from utils import navegar_para

def tela_inicio():
    """Tela inicial do sistema"""
    st.markdown('<h1 class="main-header">⚡ ORCPAI</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #6c757d;">Sistema de Orçamento de Painéis Elétricos</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("---")
        
        # Atalho para testes
        if st.button("🧪 ATALHO: Painel de Teste 2", use_container_width=True, type="secondary"):
            try:
                # Importar database manager
                from database_manager import db
                
                # Buscar o orçamento "Orçamento Teste"
                orcamentos = db.listar_orcamentos()
                orcamento_teste = None
                for orc in orcamentos:
                    if "teste" in orc['nome'].lower():
                        orcamento_teste = orc
                        break
                
                if orcamento_teste:
                    # Buscar o painel "Painel de teste 2"
                    paineis = db.listar_paineis(orcamento_teste['id'])
                    painel_teste = None
                    for painel in paineis:
                        if "teste 2" in painel['nome'].lower():
                            painel_teste = painel
                            break
                    
                    if painel_teste:
                        # Navegar direto para a tela de componentes
                        st.session_state.orcamento_atual = orcamento_teste
                        st.session_state.painel_atual = painel_teste
                        navegar_para('componentes')
                        st.success("🚀 Navegando para o Painel de Teste 2!")
                        st.rerun()
                    else:
                        st.warning("⚠️ Painel 'Painel de teste 2' não encontrado. Criando...")
                        # Criar o painel se não existir
                        if db.criar_painel(orcamento_teste['id'], "Painel de teste 2", "QDF/QDL - Espinha Completa"):
                            st.success("✅ Painel de teste criado! Clique novamente.")
                            st.rerun()
                else:
                    st.warning("⚠️ Orçamento de teste não encontrado. Criando...")
                    # Criar orçamento de teste se não existir
                    if db.criar_orcamento("Orçamento Teste"):
                        st.success("✅ Orçamento de teste criado! Clique novamente.")
                        st.rerun()
            except Exception as e:
                st.error(f"❌ Erro no atalho: {str(e)}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("📋 Gerenciar Orçamentos", use_container_width=True, type="primary"):
            navegar_para('orcamentos')
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("⚙️ Administração de Componentes", use_container_width=True):
            navegar_para('admin')
        
        st.markdown("---")
        
        # Estatísticas rápidas
        st.subheader("📊 Resumo do Sistema")
        
        try:
            # Importar database manager
            from database_manager import db
            
            orcamentos = db.listar_orcamentos()
            componentes = db.listar_componentes_cadastrados()
            
            col_stats1, col_stats2 = st.columns(2)
            with col_stats1:
                st.metric("Orçamentos", len(orcamentos))
            with col_stats2:
                st.metric("Componentes Cadastrados", len(componentes))
                
        except Exception as e:
            st.warning(f"Erro ao carregar estatísticas: {str(e)}") 