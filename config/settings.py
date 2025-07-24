"""
Configurações do Sistema ORCPAI
Centraliza todas as configurações da aplicação
"""

# =============================================================================
# CONFIGURAÇÕES DO STREAMLIT
# =============================================================================

STREAMLIT_CONFIG = {
    'page_title': "ORCPAI - Orçamento de Painéis",
    'page_icon': "⚡",
    'layout': "wide",
    'initial_sidebar_state': "collapsed"
}

# =============================================================================
# CONFIGURAÇÕES DO BANCO DE DADOS
# =============================================================================

# Configurações do Supabase (serão carregadas do .env)
SUPABASE_CONFIG = {
    'url': None,  # Será carregado do .env
    'key': None,  # Será carregado do .env
}

# =============================================================================
# CONFIGURAÇÕES DA APLICAÇÃO
# =============================================================================

# Estados iniciais da sessão
INITIAL_SESSION_STATE = {
    'tela_atual': 'inicio',
    'orcamento_atual': None,
    'painel_atual': None,
}

# Configurações de navegação
NAVIGATION_CONFIG = {
    'default_tela': 'inicio',
    'available_telas': ['inicio', 'orcamentos', 'paineis', 'componentes', 'admin']
}

# =============================================================================
# CONFIGURAÇÕES DE ESTILO
# =============================================================================

# Cores do tema
THEME_COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'warning': '#d62728',
    'info': '#9467bd',
    'light': '#8c564b',
    'dark': '#e377c2'
}

# Configurações de CSS
CSS_CONFIG = {
    'card_style': """
        .card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
            border: 1px solid #e0e0e0;
        }
    """,
    'button_style': """
        .stButton > button {
            border-radius: 0.5rem;
            font-weight: 500;
        }
    """
}

# =============================================================================
# CONFIGURAÇÕES DE EXPORTAÇÃO
# =============================================================================

EXPORT_CONFIG = {
    'excel_filename_prefix': 'orcamento_',
    'excel_sheet_name': 'Orçamento',
    'date_format': '%d/%m/%Y',
    'time_format': '%H:%M:%S'
}

# =============================================================================
# CONFIGURAÇÕES DE VALIDAÇÃO
# =============================================================================

VALIDATION_CONFIG = {
    'max_nome_length': 100,
    'max_descricao_length': 500,
    'min_quantidade': 1,
    'max_quantidade': 9999,
    'max_orcamentos_per_user': 100,
    'max_paineis_per_orcamento': 50,
    'max_componentes_per_painel': 200
}

# =============================================================================
# CONFIGURAÇÕES DE MENSAGENS
# =============================================================================

MESSAGES = {
    'success': {
        'componente_criado': "✅ Componente '{nome}' criado!",
        'componente_atualizado': "✅ Componente atualizado!",
        'componente_excluido': "✅ Componente excluído!",
        'orcamento_criado': "✅ Orçamento '{nome}' criado!",
        'orcamento_atualizado': "✅ Orçamento atualizado!",
        'orcamento_excluido': "✅ Orçamento excluído!",
        'painel_criado': "✅ Painel '{nome}' criado!",
        'painel_atualizado': "✅ Painel atualizado!",
        'painel_excluido': "✅ Painel excluído!",
        'componente_adicionado': "✅ {quantidade}x adicionado!",
        'componente_removido': "✅ {quantidade} item(s) removido(s)!",
    },
    'error': {
        'banco_conexao': "❌ Não foi possível conectar ao banco de dados",
        'import_error': "❌ Erro ao importar {modulo}: {erro}",
        'operacao_falhou': "❌ Erro ao {operacao}",
        'validacao_falhou': "❌ Validação falhou: {mensagem}",
    },
    'warning': {
        'quantidade_invalida': "⚠️ Quantidade inválida - botão desabilitado",
        'selecao_dupla': "⚠️ Erro: Seleções em ambas as listas",
        'nome_obrigatorio': "⚠️ Digite um nome para o componente",
    },
    'info': {
        'nenhum_componente': "🔧 Nenhum componente cadastrado ainda.",
        'nenhum_orcamento': "📋 Nenhum orçamento encontrado",
        'nenhum_painel': "⚡ Nenhum painel encontrado",
        'filtro_ativo': "🔍 Filtrando por: **'{filtro}'**",
    }
}

# =============================================================================
# CONFIGURAÇÕES DE DESENVOLVIMENTO
# =============================================================================

DEV_CONFIG = {
    'debug_mode': False,
    'log_level': 'INFO',
    'show_indicators': False,  # Indicadores visuais de modularização
    'auto_reload': True,
}

# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

def get_message(category: str, key: str, **kwargs) -> str:
    """Obtém uma mensagem formatada das configurações"""
    if category in MESSAGES and key in MESSAGES[category]:
        return MESSAGES[category][key].format(**kwargs)
    return f"Mensagem não encontrada: {category}.{key}"

def is_debug_mode() -> bool:
    """Verifica se está em modo debug"""
    return DEV_CONFIG['debug_mode']

def should_show_indicators() -> bool:
    """Verifica se deve mostrar indicadores visuais"""
    return DEV_CONFIG['show_indicators'] 