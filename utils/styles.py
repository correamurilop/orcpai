# Estilos CSS - Streamlit
import streamlit as st

def aplicar_estilos():
    """Aplica todos os estilos CSS customizados do sistema"""
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
        /* Reduzir espaçamento entre linhas da tabela */
        .row-widget.stHorizontal {
            gap: 0.5rem !important;
            margin-bottom: 0.3rem !important;
        }
        /* Compactar inputs de número */
        .stNumberInput > div > div > input {
            padding: 0.2rem 0.4rem !important;
            font-size: 0.85rem !important;
            height: 2rem !important;
        }
        /* Compactar botões */
        .stButton > button {
            padding: 0.2rem 0.6rem !important;
            font-size: 0.85rem !important;
            height: 2rem !important;
            min-height: 2rem !important;
        }
        /* Estilizar barra de navegação */
        .nav-container {
            background-color: #f8f9fa;
            padding: 0.5rem 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            border: 1px solid #dee2e6;
        }
        /* Botões de navegação */
        .nav-button {
            background-color: #007bff !important;
            color: white !important;
            border: none !important;
            border-radius: 5px !important;
            font-weight: 500 !important;
        }
        .nav-button:hover {
            background-color: #0056b3 !important;
            transform: translateY(-1px);
        }
    </style>
    """, unsafe_allow_html=True) 