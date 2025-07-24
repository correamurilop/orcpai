# ORCPAI – Sistema de Orçamento de Painéis

Este é um sistema interno para criação e organização de orçamentos de painéis elétricos. Utiliza arquivos `.orcpai` como base de dados e gera planilhas Excel com os componentes necessários.

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o sistema:
```bash
python main.py
```

## Funcionalidades

- Gerenciamento de múltiplos orçamentos
- Cada orçamento pode conter múltiplos painéis
- Sistema de regras para componentes automáticos
- Exportação para Excel
- Interface administrativa para configuração de regras

## Estrutura do Projeto

- `ui/` - Interfaces gráficas
- `core/` - Lógica de negócio
- `data/` - Arquivos de configuração e regras
- `orcamentos/` - Arquivos .orcpai salvos
- `assets/` - Recursos visuais 