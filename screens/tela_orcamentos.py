# Tela de Orçamentos - Streamlit
import streamlit as st
from utils import navegar_para

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
                # Importar database manager
                from database_manager import db
                
                resultado = db.criar_orcamento(nome_novo.strip())
                if resultado:
                    st.success(f"✅ Orçamento '{nome_novo}' criado com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao criar orçamento")
            else:
                st.warning("⚠️ Digite um nome para o orçamento")
    
    st.markdown("---")
    
    # Lista de orçamentos
    st.subheader("📄 Orçamentos Existentes")
    
    # Importar database manager
    from database_manager import db
    
    orcamentos = db.listar_orcamentos()
    
    if not orcamentos:
        st.info("📝 Nenhum orçamento encontrado. Crie seu primeiro orçamento acima!")
    else:
        # Busca
        busca = st.text_input("🔍 Buscar orçamento", placeholder="Digite para filtrar...")
        
        # Filtrar orçamentos
        if busca:
            orcamentos_filtrados = [orc for orc in orcamentos if busca.lower() in orc['nome'].lower()]
        else:
            orcamentos_filtrados = orcamentos
        
        if not orcamentos_filtrados:
            st.warning("🔍 Nenhum orçamento encontrado com esse filtro")
        else:
            # Exibir orçamentos
            for orc in orcamentos_filtrados:
                with st.container():
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    
                    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**📋 {orc['nome']}**")
                        st.caption(f"Criado em: {orc['criado_em'][:10]}")
                    
                    with col2:
                        if st.button("📂 Abrir", key=f"abrir_{orc['id']}"):
                            navegar_para('paineis', orc)
                    
                    with col3:
                        if st.button("✏️ Renomear", key=f"renomear_{orc['id']}"):
                            st.session_state[f'renomear_modal_{orc["id"]}'] = True
                    
                    with col4:
                        if st.button("📤 Exportar", key=f"export_{orc['id']}"):
                            st.info("🚧 Em desenvolvimento - Exportação em breve!")
                    
                    with col5:
                        if st.button("🗑️ Excluir", key=f"excluir_{orc['id']}"):
                            st.session_state[f'confirmar_exclusao_{orc["id"]}'] = True
                    
                    # Modal de renomeação
                    if st.session_state.get(f'renomear_modal_{orc["id"]}', False):
                        with st.form(f"form_renomear_{orc['id']}"):
                            st.write("**✏️ Renomear Orçamento**")
                            novo_nome = st.text_input("Novo nome:", value=orc['nome'])
                            
                            col_form1, col_form2 = st.columns(2)
                            with col_form1:
                                if st.form_submit_button("✅ Salvar", type="primary"):
                                    if novo_nome.strip() and novo_nome.strip() != orc['nome']:
                                        if db.atualizar_orcamento(orc['id'], novo_nome.strip()):
                                            st.success("✅ Orçamento renomeado!")
                                            st.session_state[f'renomear_modal_{orc["id"]}'] = False
                                            st.rerun()
                                        else:
                                            st.error("❌ Erro ao renomear orçamento")
                                    elif not novo_nome.strip():
                                        st.warning("⚠️ Digite um nome válido")
                                    else:
                                        st.info("ℹ️ Nome não foi alterado")
                            
                            with col_form2:
                                if st.form_submit_button("❌ Cancelar"):
                                    st.session_state[f'renomear_modal_{orc["id"]}'] = False
                                    st.rerun()
                    
                    # Modal de confirmação de exclusão
                    if st.session_state.get(f'confirmar_exclusao_{orc["id"]}', False):
                        with st.form(f"form_excluir_{orc['id']}"):
                            st.write("**⚠️ Confirmar Exclusão**")
                            st.warning(f"Tem certeza que deseja excluir o orçamento **'{orc['nome']}'**?")
                            st.caption("⚠️ Esta ação não pode ser desfeita!")
                            
                            col_form1, col_form2 = st.columns(2)
                            with col_form1:
                                if st.form_submit_button("🗑️ Sim, Excluir", type="primary"):
                                    if db.excluir_orcamento(orc['id']):
                                        st.success("✅ Orçamento excluído!")
                                        st.session_state[f'confirmar_exclusao_{orc["id"]}'] = False
                                        st.rerun()
                                    else:
                                        st.error("❌ Erro ao excluir orçamento")
                            
                            with col_form2:
                                if st.form_submit_button("❌ Cancelar"):
                                    st.session_state[f'confirmar_exclusao_{orc["id"]}'] = False
                                    st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True) 