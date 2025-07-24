# Tela de Painéis - Streamlit
import streamlit as st
from utils import navegar_para

def tela_paineis():
    """Tela de gerenciamento de painéis"""
    orcamento = st.session_state.orcamento_atual
    
    if not orcamento:
        st.error("❌ Nenhum orçamento selecionado")
        if st.button("⬅️ Voltar aos Orçamentos"):
            navegar_para('orcamentos')
        return
    
    st.header(f"⚡ Painéis do Orçamento: {orcamento['nome']}")
    
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
                # Importar database manager
                from database_manager import db
                
                resultado = db.criar_painel(orcamento['id'], nome_painel.strip(), tipo_completo)
                if resultado:
                    st.success(f"✅ Painel '{nome_painel}' criado!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao criar painel")
            else:
                st.warning("⚠️ Digite um nome para o painel")
    
    st.markdown("---")
    
    # Lista de painéis
    st.subheader("🔧 Painéis Existentes")
    
    # Importar database manager
    from database_manager import db
    
    paineis = db.listar_paineis(orcamento['id'])
    
    if not paineis:
        st.info("🔧 Nenhum painel encontrado. Crie seu primeiro painel acima!")
    else:
        # Busca
        busca_painel = st.text_input("🔍 Buscar painel", placeholder="Digite para filtrar...")
        
        # Filtrar painéis
        if busca_painel:
            paineis_filtrados = [p for p in paineis if busca_painel.lower() in p['nome'].lower()]
        else:
            paineis_filtrados = paineis
        
        if not paineis_filtrados:
            st.warning("🔍 Nenhum painel encontrado com esse filtro")
        else:
            for painel in paineis_filtrados:
                with st.container():
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**⚡ {painel['nome']}**")
                        st.caption(f"Tipo: {painel['tipo']} | Criado em: {painel['criado_em'][:10]}")
                    
                    with col2:
                        if st.button("📂 Abrir", key=f"abrir_painel_{painel['id']}"):
                            navegar_para('componentes', orcamento, painel)
                    
                    with col3:
                        if st.button("✏️ Renomear", key=f"renomear_painel_{painel['id']}"):
                            st.session_state[f'renomear_painel_modal_{painel["id"]}'] = True
                    
                    with col4:
                        if st.button("🗑️ Excluir", key=f"excluir_painel_{painel['id']}"):
                            st.session_state[f'confirmar_exclusao_painel_{painel["id"]}'] = True
                    
                    # Modal de renomeação de painel
                    if st.session_state.get(f'renomear_painel_modal_{painel["id"]}', False):
                        with st.form(f"form_renomear_painel_{painel['id']}"):
                            st.write("**✏️ Renomear Painel**")
                            novo_nome = st.text_input("Novo nome:", value=painel['nome'])
                            
                            col_form1, col_form2 = st.columns(2)
                            with col_form1:
                                if st.form_submit_button("✅ Salvar", type="primary"):
                                    if novo_nome.strip() and novo_nome.strip() != painel['nome']:
                                        if db.atualizar_painel(painel['id'], novo_nome.strip()):
                                            st.success("✅ Painel renomeado!")
                                            st.session_state[f'renomear_painel_modal_{painel["id"]}'] = False
                                            st.rerun()
                                        else:
                                            st.error("❌ Erro ao renomear painel")
                                    elif not novo_nome.strip():
                                        st.warning("⚠️ Digite um nome válido")
                                    else:
                                        st.info("ℹ️ Nome não foi alterado")
                            
                            with col_form2:
                                if st.form_submit_button("❌ Cancelar"):
                                    st.session_state[f'renomear_painel_modal_{painel["id"]}'] = False
                                    st.rerun()
                    
                    # Modal de confirmação de exclusão de painel
                    if st.session_state.get(f'confirmar_exclusao_painel_{painel["id"]}', False):
                        with st.form(f"form_excluir_painel_{painel['id']}"):
                            st.write("**⚠️ Confirmar Exclusão**")
                            st.warning(f"Tem certeza que deseja excluir o painel **'{painel['nome']}'**?")
                            st.caption("⚠️ Esta ação não pode ser desfeita!")
                            
                            col_form1, col_form2 = st.columns(2)
                            with col_form1:
                                if st.form_submit_button("🗑️ Sim, Excluir", type="primary"):
                                    if db.excluir_painel(painel['id']):
                                        st.success("✅ Painel excluído!")
                                        st.session_state[f'confirmar_exclusao_painel_{painel["id"]}'] = False
                                        st.rerun()
                                    else:
                                        st.error("❌ Erro ao excluir painel")
                            
                            with col_form2:
                                if st.form_submit_button("❌ Cancelar"):
                                    st.session_state[f'confirmar_exclusao_painel_{painel["id"]}'] = False
                                    st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True) 