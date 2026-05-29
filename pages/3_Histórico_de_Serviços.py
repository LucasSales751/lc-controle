import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="LC CONTROLE - Histórico de Serviços", layout="wide")

st.markdown("""
    <style>
    [data-testid="stHeader"] { background-color: transparent !important; background: transparent !important; }
    .stApp {
        background-image: linear-gradient(rgba(15, 23, 42, 0.88), rgba(15, 23, 42, 0.96)), 
                         url('https://images.unsplash.com/photo-1616788494707-ec28f08d05a1?q=80&w=1920');
        background-size: cover !important; background-position: center !important; background-attachment: fixed !important; color: #F8FAFC !important;
    }
    [data-testid="stSidebar"] { 
        background-image: linear-gradient(rgba(17, 24, 39, 0.82), rgba(11, 17, 26, 0.92)), 
                         url('https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?q=80&w=600');
        background-size: cover !important; background-position: center !important; border-right: 1px solid #1E293B !important;
    }
    [data-testid="stSidebar"] section[data-testid="stSidebarNav"] li:first-child span { font-size: 0 !important; }
    [data-testid="stSidebar"] section[data-testid="stSidebarNav"] li:first-child span::after {
        content: "Inicio" !important; font-size: 15px !important; font-weight: 700 !important; color: #FFFFFF !important;
    }
    [data-testid="stSidebarNav"] [data-testid="stSidebarNavLink"] span {
        color: #FFFFFF !important; font-weight: 700 !important; font-size: 15px !important; opacity: 1 !important; text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.9) !important;
    }
    
    /* BRANDING */
    .brand-top { color: #38BDF8 !important; font-weight: 900; font-size: 20px; letter-spacing: 1px; margin: 0; opacity: 0.8; text-shadow: 0px 0px 8px rgba(56, 189, 248, 0.4) !important; }
    .main-title { color: #FFFFFF !important; font-family: 'Inter', sans-serif; font-weight: 800; font-size: 32px; margin-top: 5px; margin-bottom: 5px; }
    .section-title { color: #94A3B8 !important; font-weight: 600; font-size: 15px; text-transform: uppercase; margin-top: 25px; letter-spacing: 0.5px; }
    
    div[data-baseweb="select"], .stSelectbox { background-color: #1F2937 !important; border: 1px solid #4B5563 !important; border-radius: 6px !important; }
    .stMetric label { color: #94A3B8 !important; font-weight: 500; }
    .stMetric div[data-testid="stMetricValue"] { color: #38BDF8 !important; font-weight: 800; }
    
    .styled-table { width: 100%; border-collapse: collapse; background-color: rgba(17, 24, 39, 0.85); border-radius: 6px; overflow: hidden; margin-top: 15px; border: 1px solid #374151; }
    .styled-table th { background-color: #030712; color: #38BDF8; padding: 14px; font-weight: 700; text-align: left; border-bottom: 2px solid #374151; }
    .styled-table td { padding: 12px 14px; border-bottom: 1px solid #374151; color: #F1F5F9; font-size: 14px; }
    
    .calc-box { background-color: rgba(17, 24, 39, 0.8); border: 1px solid #374151; padding: 22px; border-radius: 8px; margin-bottom: 25px; backdrop-filter: blur(8px); }
    .calc-title { color: #38BDF8; font-weight: 700; font-size: 15px; margin-bottom: 15px; text-transform: uppercase; }
    </style>
""", unsafe_allow_html=True)

DB_FILE = "banco_estetica.db"

def carregar_dados():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicos_pendentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT, data_hora TEXT, atendente TEXT, veiculo TEXT, servico TEXT, valor REAL, comissao REAL
        )
    """)
    conn.commit()
    df = pd.read_sql_query("SELECT data_hora, atendente, veiculo, servico, valor, comissao FROM servicos_pendentes ORDER BY id DESC", conn)
    conn.close()
    return df

st.markdown("<div class='brand-top'>LC CONTROLE</div>", unsafe_allow_html=True)
st.markdown("<div class='main-title'>AUDITORIA E HISTÓRICO DE SERVIÇOS</div>", unsafe_allow_html=True)

try:
    df_servicos = carregar_dados()
except Exception as e:
    st.error("Erro ao ler o banco de dados.")
    st.stop()

if df_servicos.empty:
    st.info("Nenhum registro localizado.")
else:
    st.markdown("<div class='calc-box'>", unsafe_allow_html=True)
    st.markdown("<div class='calc-title'>Soma Acumulada por Funcionário</div>", unsafe_allow_html=True)
    
    funcionarios_disponiveis = sorted(df_servicos['atendente'].unique())
    col_sel, col_res1, col_res2 = st.columns([2, 2, 2])
    
    with col_sel:
        func_selecionado = st.selectbox("Selecione o operador", funcionarios_disponiveis)
        
    df_filtrado = df_servicos[df_servicos['atendente'] == func_selecionado]
    total_lavagens = len(df_filtrado)
    total_comissao = df_filtrado['comissao'].sum()
    
    with col_res1:
        st.metric(label="LAVAGENS REALIZADAS", value=f"{total_lavagens} serv.")
    with col_res2:
        st.metric(label="COMISSÃO TOTAL ACUMULADA", value=f"R$ {total_comissao:.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    df_servicos['data_formatada'] = pd.to_datetime(df_servicos['data_hora'], format='%d/%m/%Y %H:%M', errors='coerce')
    df_servicos['Ano_Semana'] = df_servicos['data_formatada'].dt.strftime('%Y-W%U')
    semanas_unicas = sorted(df_servicos['Ano_Semana'].dropna().unique(), reverse=True)
    
    for semana in semanas_unicas:
        df_semana = df_servicos[df_servicos['Ano_Semana'] == semana]
        data_min = df_semana['data_formatada'].min().strftime('%d/%m/%Y')
        data_max = df_semana['data_formatada'].max().strftime('%d/%m/%Y')
        
        st.markdown(f"<div class='section-title'>Período: {data_min} até {data_max} (Semana {semana.split('-W')[1]})</div>", unsafe_allow_html=True)
        
        html_table = "<table class='styled-table'><thead><tr><th>Data/Horário</th><th>Operador</th><th>Veículo</th><th>Serviço</th><th>Valor (R$)</th><th>Comissão (R$)</th></tr></thead><tbody>"
        for _, row in df_semana.iterrows():
            html_table += f"<tr><td>{row['data_hora']}</td><td>{row['atendente']}</td><td>{row['veiculo']}</td><td>{row['servico']}</td><td>{row['valor']:.2f}</td><td>{row['comissao']:.2f}</td></tr>"
        html_table += "</tbody></table>"
        st.markdown(html_table, unsafe_allow_html=True)