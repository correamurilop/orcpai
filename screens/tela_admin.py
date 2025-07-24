# Tela de Administração - Streamlit
import streamlit as st
from utils import navegar_para

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
        from core.componentes_manager import listar_componentes_cadastrados, carregar_componente_info, buscar_componentes
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