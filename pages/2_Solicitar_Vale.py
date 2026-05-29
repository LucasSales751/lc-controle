import streamlit as st
import sqlite3
import datetime

st.set_page_config(page_title="LC CONTROLE - Solicitação de Vales", layout="centered")

st.markdown("""
    <style>
    [data-testid="stHeader"] { background-color: transparent !important; }
    .stApp {
        background-image: linear-gradient(rgba(15, 23, 42, 0.88), rgba(15, 23, 42, 0.96)), 
                         url('https://images.unsplash.com/photo-1616788494707-ec28f08d05a1?q=80&w=1920');
        background-size: cover !important; background-position: center !important; background-attachment: fixed !important; color: #F8FAFC !important;
    }
    [data-testid="stSidebar"] { 
        background-image: linear-gradient(rgba(17, 24, 39, 0.82), rgba(11, 17, 26, 0.92)), 
                         url('https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?q=80&w=600');
        background-size: cover !important; background-position: center !important;
    }
    [data-testid="stSidebarNav"] [data-testid="stSidebarNavLink"] span {
        color: #FFFFFF !important; font-weight: 700 !important; font-size: 15px !important; opacity: 1 !important; text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.9) !important;
    }
    [data-testid="stSidebar"] section[data-testid="stSidebarNav"] li:first-child span { font-size: 0 !important; }
    [data-testid="stSidebar"] section[data-testid="stSidebarNav"] li:first-child span::after {
        content: "Inicio" !important; font-size: 15px !important; font-weight: 700 !important; color: #FFFFFF !important;
    }

    div[data-baseweb="input"], div[data-baseweb="number-input"], input { 
        background-color: #1E293B !important; color: #FFFFFF !important; border: 1px solid #475569 !important; border-radius: 6px !important;
    }
    input[type="text"], input[type="number"] { color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; }
    label[data-testid="stWidgetLabel"] p { color: #38BDF8 !important; font-weight: 700 !important; letter-spacing: 0.5px; }
    
    /* BRANDING */
    .brand-top { color: #38BDF8 !important; font-weight: 900; font-size: 20px; letter-spacing: 1px; margin: 0; opacity: 0.8; text-shadow: 0px 0px 8px rgba(56, 189, 248, 0.4) !important; }
    h2 { color: #FFFFFF !important; font-weight: 800; font-size: 28px; margin-top: 5px; margin-bottom: 20px; }
    .stButton>button { background: #DC2626 !important; color: white !important; font-weight: 700; width: 100%; height: 45px; border-radius: 4px; border: none !important; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

DB_FILE = "banco_estetica.db"

st.markdown("<div class='brand-top'>LC CONTROLE</div>", unsafe_allow_html=True)
st.markdown("<h2>REQUERIMENTO DE VALE EMERGENCIAL</h2>", unsafe_allow_html=True)

c1, c2 = st.columns([3, 2])
with c1:
    atendente = st.text_input("NOME DO SOLICITANTE", placeholder="Digite seu nome completo...")
with c2:
    valor = st.number_input("VALOR COMPLEMENTAR (R$)", min_value=0.0, step=5.0, value=0.0)

motivo = st.text_input("JUSTIFICATIVA / MOTIVO DO VALE", placeholder="Ex: Adiantamento para transporte")

if st.button("SUBMETER REQUERIMENTO"):
    if atendente and valor > 0 and motivo:
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vales_solicitados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, data_hora TEXT, atendente TEXT, valor REAL, motivo TEXT
                )
            """)
            data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            cursor.execute("INSERT INTO vales_solicitados (data_hora, atendente, valor, motivo) VALUES (?, ?, ?, ?)", (data_atual, atendente, valor, motivo))
            conn.commit()
            conn.close()
            st.success(f"Requisição de R$ {valor:.2f} registrada com sucesso!")
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")
    else:
        st.warning("Preencha todos os campos.")