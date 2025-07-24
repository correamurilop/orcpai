# Tela de Componentes - Streamlit
import streamlit as st
from utils import navegar_para

def tela_componentes():
    """Tela de gerenciamento de componentes - layout simples e funcional"""
    orcamento = st.session_state.orcamento_atual
    painel = st.session_state.painel_atual
    
    if not orcamento or not painel:
        st.error("❌ Orçamento ou painel não selecionado")
        if st.button("⬅️ Voltar"):
            navegar_para('paineis', orcamento)
        return
    
    st.header(f"🔧 Componentes do Painel: {painel['nome']}")
    st.caption(f"Orçamento: {orcamento['nome']} | Tipo: {painel['tipo']}")
    
    # Botão voltar
    if st.button("⬅️ Voltar aos Painéis"):
        navegar_para('paineis', orcamento)
    
    st.markdown("---")
    
    # BARRA DE BUSCA GLOBAL (para ambas as listas)
    st.subheader("🔍 Buscar Componentes")
    filtro = st.text_input("Filtro", placeholder="Digite para filtrar componentes em ambas as listas simultaneamente...", key="filtro_global", label_visibility="collapsed")
    
    if filtro:
        st.info(f"🔍 Filtrando por: **'{filtro}'** (aplicado em ambas as listas)")
    
    st.markdown("---")
    
    # Inicializar seleções no session_state
    if 'componente_selecionado_esquerda' not in st.session_state:
        st.session_state.componente_selecionado_esquerda = None
    if 'componente_selecionado_direita' not in st.session_state:
        st.session_state.componente_selecionado_direita = None
    if 'quantidade_remover' not in st.session_state:
        st.session_state.quantidade_remover = 1
    if 'radio_reset_counter' not in st.session_state:
        st.session_state.radio_reset_counter = 0
    
    # Garantir consistência - se não há componente selecionado na esquerda, limpar quantidade
    if not st.session_state.componente_selecionado_esquerda and "qty_input_central" in st.session_state:
        del st.session_state["qty_input_central"]
    
    # PROTEÇÃO: Garantir que nunca haja seleções simultâneas
    if st.session_state.componente_selecionado_esquerda and st.session_state.componente_selecionado_direita:
        # Se ambos estão selecionados, limpar o mais antigo (manter o último selecionado)
        # Como não temos histórico, vamos limpar a direita por padrão
        st.session_state.componente_selecionado_direita = None
        st.session_state.quantidade_remover = 1
    
    # Layout: Esquerda | Botões | Direita
    col_esquerda, col_botoes, col_direita = st.columns([5, 2, 5])
    
    # Importar database manager
    from database_manager import db
    
    # COLUNA ESQUERDA - Componentes Disponíveis
    with col_esquerda:
        # Indicador visual se esta lista está ativa
        tem_selecao_esquerda = st.session_state.componente_selecionado_esquerda is not None
        if tem_selecao_esquerda:
            st.subheader("📋 Componentes Disponíveis ✅")
        else:
            st.subheader("📋 Componentes Disponíveis")
        
        # Buscar todos os componentes cadastrados
        todos_componentes = db.listar_componentes_cadastrados()
        
        # Aplicar filtro se houver
        if filtro:
            componentes_filtrados = [
                comp for comp in todos_componentes 
                if filtro.lower() in comp['nome'].lower() or 
                   (comp['descricao'] and filtro.lower() in comp['descricao'].lower())
            ]
        else:
            componentes_filtrados = todos_componentes
        
        if not componentes_filtrados:
            st.info("📋 Nenhum componente encontrado")
        else:
            # Info e botão limpar
            col_info, col_clear = st.columns([3, 1])
            with col_info:
                if filtro:
                    st.caption(f"**{len(componentes_filtrados)} de {len(todos_componentes)} componentes**")
                else:
                    st.caption(f"**{len(componentes_filtrados)} componentes**")
            with col_clear:
                if st.button("☐ Limpar", key="clear_left"):
                    st.session_state.componente_selecionado_esquerda = None
                    st.session_state.componente_selecionado_direita = None
                    st.session_state.quantidade_remover = 1
                    # Incrementar contador para forçar reset do radio
                    st.session_state.radio_reset_counter += 1
                    # Limpar também as quantidades
                    if "qty_input_central" in st.session_state:
                        del st.session_state["qty_input_central"]
                    if "qty_remove_central" in st.session_state:
                        del st.session_state["qty_remove_central"]
                    st.rerun()
            
            # Lista usando radio button (seleção única)
            st.markdown("**Selecione um componente:**")
            
            # Criar lista de opções para o radio
            opcoes_componentes = []
            for comp in componentes_filtrados:
                texto = f"🔧 {comp['nome']}"
                if comp['descricao']:
                    texto += f" - {comp['descricao'][:50]}..."
                opcoes_componentes.append(texto)
            
            # Radio button para seleção única
            if opcoes_componentes:
                # Encontrar índice do componente selecionado atual
                indice_selecionado = None
                if st.session_state.componente_selecionado_esquerda:
                    for i, comp in enumerate(componentes_filtrados):
                        if comp['id'] == st.session_state.componente_selecionado_esquerda:
                            indice_selecionado = i
                            break
                
                selecao = st.radio(
                    "Componentes disponíveis:",
                    options=range(len(opcoes_componentes)),
                    format_func=lambda x: opcoes_componentes[x],
                    index=indice_selecionado,
                    key=f"radio_componentes_esquerda_{st.session_state.radio_reset_counter}",
                    label_visibility="collapsed"
                )
                
                # Atualizar componente selecionado
                if selecao is not None:
                    novo_id = componentes_filtrados[selecao]['id']
                    # Só atualizar se mudou (para evitar loops)
                    if st.session_state.componente_selecionado_esquerda != novo_id:
                        st.session_state.componente_selecionado_esquerda = novo_id
                        # Limpar seleções da direita quando seleciona na esquerda
                        st.session_state.componente_selecionado_direita = None
                        st.session_state.quantidade_remover = 1
                        # Forçar reset do radio da direita
                        st.session_state.radio_reset_counter += 1
                        # Forçar atualização imediata
                        st.rerun()
    
    # COLUNA CENTRAL - Botões de Ação
    with col_botoes:
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Indicador de qual ação está disponível
        tem_selecao_esquerda = st.session_state.componente_selecionado_esquerda is not None
        tem_selecao_direita = st.session_state.componente_selecionado_direita is not None
        
        if tem_selecao_esquerda and tem_selecao_direita:
            st.warning("⚠️ Erro: Seleções em ambas as listas")
        elif tem_selecao_esquerda:
            st.info("➡️ Modo: Adicionar componente")
        elif tem_selecao_direita:
            st.info("⬅️ Modo: Remover componente")
        else:
            st.info("🎯 Selecione em uma das listas")
        
        # Input de quantidade para adicionar (sempre aparece se tiver componente selecionado na esquerda)
        componente_selecionado_esquerda = st.session_state.componente_selecionado_esquerda is not None
        componente_selecionado_direita = st.session_state.componente_selecionado_direita is not None
        
        if componente_selecionado_esquerda:
            # Encontrar o componente selecionado para adicionar
            componente_para_adicionar = None
            if st.session_state.componente_selecionado_esquerda:
                for comp in todos_componentes:
                    if comp['id'] == st.session_state.componente_selecionado_esquerda:
                        componente_para_adicionar = comp
                        break
            
            if componente_para_adicionar:
                st.markdown(f"**{componente_para_adicionar['nome']}**")
                quantidade = st.number_input("Quantidade:", min_value=1, value=1, key="qty_input_central")
        
        # Input de quantidade para remover (sempre aparece se tiver componente selecionado na direita)
        if componente_selecionado_direita:
            # Encontrar o componente selecionado para remover
            componente_para_remover = None
            componentes_painel = db.listar_componentes_do_painel(painel['id'])
            if st.session_state.componente_selecionado_direita:
                for comp in componentes_painel:
                    if comp['id'] == st.session_state.componente_selecionado_direita:
                        componente_para_remover = comp
                        break
            
            if componente_para_remover:
                st.markdown(f"**{componente_para_remover['componentes_cadastrados']['nome']}**")
                quantidade_maxima = componente_para_remover['quantidade']
                st.caption(f"Disponível: {quantidade_maxima} item(s)")
                
                # Garantir que o valor inicial seja válido
                valor_inicial = min(st.session_state.quantidade_remover, quantidade_maxima)
                if valor_inicial < 1:
                    valor_inicial = 1
                
                quantidade_remover = st.number_input(
                    "Qtd remover:", 
                    min_value=1, 
                    max_value=quantidade_maxima, 
                    value=valor_inicial,
                    key="qty_remove_central",
                    help=f"Máximo: {quantidade_maxima} item(s)"
                )
                
                # Validação adicional em tempo real
                if quantidade_remover > quantidade_maxima:
                    st.error(f"⚠️ Quantidade inválida! Máximo permitido: {quantidade_maxima}")
                    st.session_state.quantidade_remover = quantidade_maxima
                elif quantidade_remover < 1:
                    st.error(f"⚠️ Quantidade deve ser pelo menos 1!")
                    st.session_state.quantidade_remover = 1
                else:
                    st.session_state.quantidade_remover = quantidade_remover
        
        # Botão Adicionar (só ativo se tiver seleção na esquerda)
        adicionar_desabilitado = not componente_selecionado_esquerda or componente_selecionado_direita
        
        if st.button("➡️ Adicionar", disabled=adicionar_desabilitado, use_container_width=True, type="primary"):
            if componente_selecionado_esquerda:
                quantidade = st.session_state.get("qty_input_central", 1)
                if db.adicionar_componente_ao_painel(painel['id'], st.session_state.componente_selecionado_esquerda, quantidade):
                    # Limpar todas as seleções
                    st.session_state.componente_selecionado_esquerda = None
                    st.session_state.componente_selecionado_direita = None
                    st.session_state.quantidade_remover = 1
                    # Incrementar contador para forçar reset do radio
                    st.session_state.radio_reset_counter += 1
                    # Limpar também a quantidade
                    if "qty_input_central" in st.session_state:
                        del st.session_state["qty_input_central"]
                    st.success(f"✅ {quantidade}x adicionado!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao adicionar")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botão Remover (só ativo se tiver seleção na direita e quantidade válida)
        qtd_remover = st.session_state.quantidade_remover if componente_selecionado_direita else 0
        
        # Verificar se a quantidade é válida
        quantidade_valida = True
        if componente_selecionado_direita:
            componentes_painel = db.listar_componentes_do_painel(painel['id'])
            comp_atual = next((c for c in componentes_painel if c['id'] == st.session_state.componente_selecionado_direita), None)
            if comp_atual:
                quantidade_valida = 1 <= qtd_remover <= comp_atual['quantidade']
        
        remover_desabilitado = not componente_selecionado_direita or componente_selecionado_esquerda or not quantidade_valida
        
        # Mostrar aviso se quantidade é inválida
        if componente_selecionado_direita and not quantidade_valida:
            st.warning("⚠️ Quantidade inválida - botão desabilitado")
        
        if st.button(f"⬅️ Remover ({qtd_remover} itens)", disabled=remover_desabilitado, use_container_width=True):
            if componente_selecionado_direita:
                comp_painel_id = st.session_state.componente_selecionado_direita
                qtd_remover = st.session_state.quantidade_remover
                
                # Buscar quantidade atual do componente
                componentes_painel = db.listar_componentes_do_painel(painel['id'])
                comp_atual = next((c for c in componentes_painel if c['id'] == comp_painel_id), None)
                
                if comp_atual:
                    quantidade_disponivel = comp_atual['quantidade']
                    
                    # VALIDAÇÃO: Verificar se a quantidade a remover é válida
                    if qtd_remover > quantidade_disponivel:
                        st.error(f"❌ Erro: Tentando remover {qtd_remover} itens, mas só há {quantidade_disponivel} disponível(s)!")
                        return
                    
                    if qtd_remover <= 0:
                        st.error(f"❌ Erro: Quantidade deve ser maior que zero!")
                        return
                    
                    # Executar remoção apenas se validação passou
                    nova_quantidade = quantidade_disponivel - qtd_remover
                    if nova_quantidade <= 0:
                        # Remover completamente
                        db.remover_componente_do_painel(comp_painel_id)
                        st.success(f"✅ Componente removido completamente ({qtd_remover} item(s))!")
                    else:
                        # Atualizar quantidade
                        db.atualizar_quantidade_componente(comp_painel_id, nova_quantidade)
                        st.success(f"✅ {qtd_remover} item(s) removido(s)! Restam {nova_quantidade}.")
                    
                    # Limpar todas as seleções apenas se a operação foi bem-sucedida
                    st.session_state.componente_selecionado_direita = None
                    st.session_state.componente_selecionado_esquerda = None
                    st.session_state.quantidade_remover = 1
                    # Incrementar contador para forçar reset do radio
                    st.session_state.radio_reset_counter += 1
                    # Limpar também a quantidade
                    if "qty_input_central" in st.session_state:
                        del st.session_state["qty_input_central"]
                    if "qty_remove_central" in st.session_state:
                        del st.session_state["qty_remove_central"]
                    st.rerun()
                else:
                    st.error("❌ Erro: Componente não encontrado!")
    
    # COLUNA DIREITA - Componentes do Painel
    with col_direita:
        # Indicador visual se esta lista está ativa
        tem_selecao_direita = st.session_state.componente_selecionado_direita is not None
        if tem_selecao_direita:
            st.subheader("✅ Componentes do Painel ✅")
        else:
            st.subheader("✅ Componentes do Painel")
        
        componentes_painel = db.listar_componentes_do_painel(painel['id'])
        
        # Aplicar o mesmo filtro na lista da direita
        if filtro and componentes_painel:
            componentes_painel_filtrados = []
            for comp in componentes_painel:
                nome_comp = comp['componentes_cadastrados']['nome'].lower()
                desc_comp = comp['componentes_cadastrados']['descricao']
                desc_comp = desc_comp.lower() if desc_comp else ""
                
                if filtro.lower() in nome_comp or filtro.lower() in desc_comp:
                    componentes_painel_filtrados.append(comp)
        else:
            componentes_painel_filtrados = componentes_painel
        
        if not componentes_painel_filtrados:
            if not componentes_painel:
                st.info("📋 Nenhum componente adicionado")
            else:
                st.info("🔍 Nenhum componente do painel encontrado com esse filtro")
        else:
            # Info e botão limpar
            col_info, col_clear = st.columns([3, 1])
            with col_info:
                if filtro:
                    st.caption(f"**{len(componentes_painel_filtrados)} de {len(componentes_painel)} componentes**")
                else:
                    st.caption(f"**{len(componentes_painel_filtrados)} componentes**")
            with col_clear:
                if st.button("☐ Limpar", key="clear_right"):
                    st.session_state.componente_selecionado_direita = None
                    st.session_state.componente_selecionado_esquerda = None
                    st.session_state.quantidade_remover = 1
                    # Incrementar contador para forçar reset do radio
                    st.session_state.radio_reset_counter += 1
                    # Limpar também as quantidades
                    if "qty_input_central" in st.session_state:
                        del st.session_state["qty_input_central"]
                    if "qty_remove_central" in st.session_state:
                        del st.session_state["qty_remove_central"]
                    st.rerun()
            
            # Lista usando radio button (seleção única)
            st.markdown("**Selecione um componente:**")
            
            # Criar lista de opções para o radio
            opcoes_componentes = []
            for comp in componentes_painel_filtrados:
                nome_comp = comp['componentes_cadastrados']['nome']
                desc_comp = comp['componentes_cadastrados']['descricao']
                qtd_atual = comp['quantidade']
                
                texto = f"🔧 {nome_comp} (Qtd: {qtd_atual})"
                if desc_comp:
                    texto += f" - {desc_comp[:40]}..."
                opcoes_componentes.append(texto)
            
            # Radio button para seleção única
            if opcoes_componentes:
                # Encontrar índice do componente selecionado atual
                indice_selecionado = None
                if st.session_state.componente_selecionado_direita:
                    for i, comp in enumerate(componentes_painel_filtrados):
                        if comp['id'] == st.session_state.componente_selecionado_direita:
                            indice_selecionado = i
                            break
                
                selecao = st.radio(
                    "Componentes no painel:",
                    options=range(len(opcoes_componentes)),
                    format_func=lambda x: opcoes_componentes[x],
                    index=indice_selecionado,
                    key=f"radio_componentes_direita_{st.session_state.radio_reset_counter}",
                    label_visibility="collapsed"
                )
                
                # Atualizar componente selecionado
                if selecao is not None:
                    novo_id = componentes_painel_filtrados[selecao]['id']
                    # Só atualizar se mudou (para evitar loops)
                    if st.session_state.componente_selecionado_direita != novo_id:
                        st.session_state.componente_selecionado_direita = novo_id
                        # Limpar seleção da esquerda quando seleciona na direita
                        st.session_state.componente_selecionado_esquerda = None
                        st.session_state.quantidade_remover = 1
                        # Forçar reset do radio da esquerda
                        st.session_state.radio_reset_counter += 1
                        # Forçar atualização imediata
                        st.rerun()
                
                # Botão de edição para o componente selecionado
                if st.session_state.componente_selecionado_direita:
                    comp_selecionado = next((c for c in componentes_painel_filtrados if c['id'] == st.session_state.componente_selecionado_direita), None)
                    if comp_selecionado and st.button("✏️ Editar quantidade total", key=f"edit_{comp_selecionado['id']}", use_container_width=True):
                        st.session_state[f'edit_modal_{comp_selecionado["id"]}'] = True
    

    
    # MODAIS DE EDIÇÃO
    for comp in componentes_painel:
        if st.session_state.get(f'edit_modal_{comp["id"]}', False):
            with st.form(f"form_edit_{comp['id']}"):
                st.markdown("### ✏️ Editar Quantidade")
                st.write(f"**Componente:** {comp['componentes_cadastrados']['nome']}")
                st.write(f"**Quantidade atual:** {comp['quantidade']}")
                
                nova_quantidade = st.number_input("Nova quantidade:", min_value=1, value=comp['quantidade'])
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("✅ Salvar", type="primary"):
                        if db.atualizar_quantidade_componente(comp['id'], nova_quantidade):
                            st.session_state[f'edit_modal_{comp["id"]}'] = False
                            st.success("✅ Quantidade atualizada!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao atualizar")
                
                with col2:
                    if st.form_submit_button("❌ Cancelar"):
                        st.session_state[f'edit_modal_{comp["id"]}'] = False
                        st.rerun() 