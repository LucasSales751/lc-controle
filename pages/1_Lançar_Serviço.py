import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="LC CONTROLE - Lançar Serviço", layout="centered")

# --- DESIGN AUTOMOTIVO PREMIUM ---
st.markdown("""
    <style>
    [data-testid="stHeader"] { background-color: transparent !important; }
    .stApp {
        background-image: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.95)), 
                         url('https://images.unsplash.com/photo-1607860108855-64acf2078ed9?q=80&w=1200');
        background-size: cover !important; background-position: center !important; color: #F8FAFC !important;
    }
    .brand-top { color: #38BDF8 !important; font-weight: 900; font-size: 20px; letter-spacing: 1px; text-shadow: 0px 0px 8px rgba(56, 189, 248, 0.4); }
    h2 { color: #FFFFFF !important; font-weight: 800; margin-top: 5px; }
    
    /* CAIXA DE PREVISÃO DE VALORES */
    .resumo-box {
        background-color: rgba(30, 41, 59, 0.7);
        border: 1px solid #38BDF8;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='brand-top'>LC CONTROLE</div>", unsafe_allow_html=True)
st.markdown("<h2>🚀 LANÇAR NOVO SERVIÇO</h2>", unsafe_allow_html=True)
st.markdown("Preencha os dados do veículo e o serviço realizado abaixo.")

DB_FILE = "banco_estetica.db"

# --- FORMULÁRIO DE LANÇAMENTO ---
with st.form("form_servico", clear_on_submit=True):
    atendente = st.selectbox("👤 QUEM FEZ O SERVIÇO?", ["Selecione...", "Carlos", "Eduardo", "Marcos", "Lucas"])
    
    veiculo = st.text_input("🚘 PLACA OU MODELO DO CARRO", placeholder="Ex: Civic Preto ou BRA2E19").upper()
    
    tipo_servico = st.selectbox("🛠️ TIPO DE SERVIÇO", ["Ducha", "Lavagem Completa"])
    
    tamanho_veiculo = st.selectbox("📏 PORTE DO VEÍCULO", ["Pequeno", "Médio", "Grande (SUV / Camionete)"])

    # --- LÓGICA AUTOMÁTICA DE PREÇOS E COMISSÕES ---
    valor_final = 0.0
    comissao_final = 0.0

    if tipo_servico == "Ducha":
        if tamanho_veiculo == "Pequeno" or tamanho_veiculo == "Médio":
            valor_final = 10.00
            comissao_final = 2.50
        else:  # Grande
            valor_final = 20.
