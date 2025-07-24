# Módulo screens - Todas as telas do sistema Streamlit
# Facilita imports das telas

from .tela_inicio import tela_inicio
from .tela_orcamentos import tela_orcamentos
from .tela_paineis import tela_paineis
from .tela_componentes import tela_componentes
from .tela_admin import tela_admin

# Todas as telas foram implementadas!
__all__ = [
    'tela_inicio',
    'tela_orcamentos',
    'tela_paineis',
    'tela_componentes',
    'tela_admin'
] 