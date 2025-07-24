# ORCPAI - Sistema de Orçamento de Painéis

Sistema completo para gerenciamento e orçamento de painéis elétricos, desenvolvido em Python com Streamlit e Supabase.

## 🚀 Características

- **Interface Web Moderna** - Desenvolvida com Streamlit
- **Banco de Dados em Nuvem** - Supabase (PostgreSQL)
- **Arquitetura Modular** - Código organizado e escalável
- **CRUD Completo** - Orçamentos, painéis e componentes
- **Exportação Excel** - Relatórios em formato .xlsx
- **Busca e Filtros** - Interface intuitiva de pesquisa
- **Validações** - Sistema robusto de validação de dados

## 📁 Estrutura do Projeto

```
orcpai/
├── app_streamlit.py              # Aplicação principal (Streamlit)
├── database_manager.py           # Gerenciador de banco de dados
├── requirements.txt              # Dependências Python
├── .env                         # Variáveis de ambiente (não versionado)
│
├── config/                      # Configurações do sistema
│   ├── __init__.py
│   └── settings.py              # Configurações centralizadas
│
├── screens/                     # Telas da aplicação
│   ├── __init__.py
│   ├── tela_inicio.py           # Tela inicial
│   ├── tela_orcamentos.py       # Gerenciamento de orçamentos
│   ├── tela_paineis.py          # Gerenciamento de painéis
│   ├── tela_componentes.py      # Gerenciamento de componentes
│   └── tela_admin.py            # Administração do sistema
│
├── utils/                       # Utilitários e funções auxiliares
│   ├── __init__.py
│   ├── navigation.py            # Navegação entre telas
│   └── styles.py                # Estilos CSS customizados
│
├── core/                        # Lógica de negócio
│   ├── __init__.py
│   ├── models.py                # Modelos de dados
│   ├── componentes_manager.py   # Gerenciamento de componentes
│   └── exportador_excel.py      # Exportação para Excel
│
├── data/                        # Dados e arquivos
│   ├── __init__.py
│   └── storage_adapter.py       # Adaptador de armazenamento
│
└── manual_de_desenvolvimento/   # Documentação de desenvolvimento
    ├── Plano_Modularizacao.txt  # Plano de modularização
    └── Capitulo_*.txt           # Capítulos do manual
```

## 🛠️ Instalação

### Pré-requisitos

- Python 3.8+
- Conta no Supabase
- Git

### Passos

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd orcpai
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure as variáveis de ambiente**
   ```bash
   # Crie um arquivo .env na raiz do projeto
   SUPABASE_URL=sua_url_do_supabase
   SUPABASE_KEY=sua_chave_do_supabase
   ```

4. **Execute a aplicação**
   ```bash
   streamlit run app_streamlit.py
   ```

## 🎯 Funcionalidades

### 📋 Orçamentos
- Criar, editar e excluir orçamentos
- Listagem com busca e filtros
- Exportação para Excel

### ⚡ Painéis
- Gerenciamento de painéis por orçamento
- Diferentes tipos de painéis
- Organização hierárquica

### 🔧 Componentes
- Catálogo de componentes cadastrados
- Adição/remoção de componentes em painéis
- Controle de quantidades
- Busca global em tempo real

### ⚙️ Administração
- CRUD de componentes do sistema
- Gerenciamento de regras derivadas
- Interface administrativa

## 🏗️ Arquitetura

### Modularização
O sistema foi completamente modularizado para facilitar manutenção e escalabilidade:

- **`screens/`** - Cada tela em arquivo separado
- **`utils/`** - Funções auxiliares reutilizáveis
- **`config/`** - Configurações centralizadas
- **`core/`** - Lógica de negócio isolada

### Banco de Dados
- **Supabase** como backend
- **PostgreSQL** como banco de dados
- **Autenticação** integrada
- **Backup automático**

### Interface
- **Streamlit** para interface web
- **CSS customizado** para estilização
- **Responsivo** e intuitivo
- **Navegação fluida** entre telas

## 🔧 Configuração

### Variáveis de Ambiente
```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_chave_anon_public
```

### Configurações do Sistema
As configurações estão centralizadas em `config/settings.py`:
- Configurações do Streamlit
- Mensagens do sistema
- Validações
- Estilos CSS
- Configurações de desenvolvimento

## 📊 Tecnologias Utilizadas

- **Frontend**: Streamlit
- **Backend**: Python
- **Banco de Dados**: Supabase (PostgreSQL)
- **Exportação**: openpyxl
- **Estilização**: CSS customizado

## 🚀 Deploy

### Streamlit Cloud
1. Conecte seu repositório ao Streamlit Cloud
2. Configure as variáveis de ambiente
3. Deploy automático

### Local
```bash
streamlit run app_streamlit.py --server.port 8501
```

## 📝 Desenvolvimento

### Estrutura de Desenvolvimento
- **Modularização completa** - Cada funcionalidade em módulo separado
- **Configurações centralizadas** - Fácil manutenção
- **Documentação atualizada** - Manual de desenvolvimento
- **Testes incrementais** - Validação a cada fase

### Adicionando Novas Funcionalidades
1. Crie a tela em `screens/`
2. Adicione a navegação em `utils/navigation.py`
3. Configure em `config/settings.py`
4. Teste localmente
5. Documente as mudanças

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte e dúvidas:
- Abra uma issue no GitHub
- Consulte o manual de desenvolvimento
- Verifique a documentação do código

---

**ORCPAI** - Sistema de Orçamento de Painéis ⚡ 