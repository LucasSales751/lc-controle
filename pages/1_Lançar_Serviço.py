import streamlit as st
import sqlite3
import datetime

st.set_page_config(page_title="LC CONTROLE - Lançamento de Serviços", layout="centered")

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

    div[data-baseweb="input"], div[data-baseweb="select"], input, select, textarea { 
        background-color: #1E293B !important; color: #FFFFFF !important; border: 1px solid #475569 !important; border-radius: 6px !important;
    }
    input[type="text"] { color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; }
    label[data-testid="stWidgetLabel"] p { color: #38BDF8 !important; font-weight: 700 !important; letter-spacing: 0.5px; }
    
    /* BRANDING */
    .brand-top { color: #38BDF8 !important; font-weight: 900; font-size: 20px; letter-spacing: 1px; margin: 0; opacity: 0.8; text-shadow: 0px 0px 8px rgba(56, 189, 248, 0.4) !important; }
    h2 { color: #FFFFFF !important; font-weight: 800; font-size: 28px; margin-top: 5px; margin-bottom: 20px; }
    .resumo-card { background-color: rgba(30, 41, 59, 0.8); padding: 20px; border-radius: 6px; backdrop-filter: blur(5px); border: 1px solid #334155; margin-top: 15px; }
    .stButton>button { background: #0284C7 !important; color: white !important; font-weight: 700; width: 100%; height: 45px; border-radius: 4px; border: none !important; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

DB_FILE = "banco_estetica.db"

st.markdown("<div class='brand-top'>LC CONTROLE</div>", unsafe_allow_html=True)
st.markdown("<h2>REGISTRO OPERACIONAL DE ATIVIDADES</h2>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    atendente = st.text_input("IDENTIFICAÇÃO DO OPERADOR", placeholder="Digite seu nome...")
with c2:
    veiculo = st.text_input("ESPECIFICAÇÃO DO VEÍCULO", placeholder="Ex: CIVIC PRATA")

servico_selecionado = st.selectbox("CATEGORIA DO SERVIÇO", ["Ducha (Água e Sabão)", "Lavagem Externa", "Lavagem Interna", "Lavagem Completa"])

valores_padrao = {
    "Ducha (Água e Sabão)": (10.0, 2.50),
    "Lavagem Externa": (30.0, 7.50),
    "Lavagem Interna": (30.0, 7.50),
    "Lavagem Completa": (50.0, 12.50)
}
valor_cliente, comissao = valores_padrao.get(servico_selecionado, (0.0, 0.0))

st.markdown(f"""
<div class='resumo-card'>
    <b>Serviço Escolhido:</b> {servico_selecionado}<br>
    <b>Valor cobrado:</b> R$ {valor_cliente:.2f}<br>
    <span style='color: #38BDF8;'><b>Sua comissão fixa: R$ {comissao:.2f}</b></span>
</div>
""", unsafe_allow_html=True)

if st.button("CONCLUIR REGISTRO"):
    if atendente and veiculo:
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS servicos_pendentes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, data_hora TEXT, atendente TEXT, veiculo TEXT, servico TEXT, valor REAL, comissao REAL
                )
            """)
            data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            cursor.execute("""
                INSERT INTO servicos_pendentes (data_hora, atendente, veiculo, servico, valor, comissao)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (data_atual, atendente, veiculo.upper(), servico_selecionado, valor_cliente, comissao))
            conn.commit()
            conn.close()
            st.success(f"Serviço registrado com sucesso para o veículo {veiculo.upper()}!")
        except Exception as e:
            st.error(f"Erro ao salvar no banco de dados: {e}")
    else:
        st.warning("Por favor, preencha todos os campos obrigatórios.")