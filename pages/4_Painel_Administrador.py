import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="LC CONTROLE - Painel Admin", layout="wide")

# --- ARQUITETURA DE DESIGN AUTOMOTIVO PREMIUM (MÁXIMO CONTRASTE) ---
st.markdown("""
    <style>
    [data-testid="stHeader"] { background-color: transparent !important; }
    .stApp {
        background-image: linear-gradient(rgba(15, 23, 42, 0.90), rgba(15, 23, 42, 0.97)), 
                         url('https://images.unsplash.com/photo-1616788494707-ec28f08d05a1?q=80&w=1920');
        background-size: cover !important; background-position: center !important; background-attachment: fixed !important; color: #F8FAFC !important;
    }
    [data-testid="stSidebar"] { 
        background-image: linear-gradient(rgba(17, 24, 39, 0.82), rgba(11, 17, 26, 0.92)), 
                         url('https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?q=80&w=600');
        background-size: cover !important;
    }
    [data-testid="stSidebarNav"] [data-testid="stSidebarNavLink"] span {
        color: #FFFFFF !important; font-weight: 700 !important; font-size: 15px !important; text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.9) !important;
    }
    [data-testid="stSidebar"] section[data-testid="stSidebarNav"] li:first-child span { font-size: 0 !important; }
    [data-testid="stSidebar"] section[data-testid="stSidebarNav"] li:first-child span::after {
        content: "Inicio" !important; font-size: 15px !important; font-weight: 700 !important; color: #FFFFFF !important;
    }

    /* FORÇANDO MÁXIMA LEGIBILIDADE NAS MÉTRICAS */
    div[data-testid="stMetricLabel"] p {
        color: #FFFFFF !important; 
        font-weight: 700 !important; 
        font-size: 14px !important;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetricValue"] {
        color: #38BDF8 !important;
        font-weight: 900 !important;
    }

    /* ENTRADAS DE TEXTO, SELETORES E LOGIN */
    div[data-baseweb="input"], div[data-baseweb="select"], input, select { 
        background-color: #1E293B !important; color: #FFFFFF !important; border: 1px solid #475569 !important; border-radius: 6px !important;
    }
    input[type="text"], input[type="password"] { color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; }
    label[data-testid="stWidgetLabel"] p { color: #38BDF8 !important; font-weight: 700 !important; }
    
    .brand-top { color: #38BDF8 !important; font-weight: 900; font-size: 20px; letter-spacing: 1px; margin: 0; text-shadow: 0px 0px 8px rgba(56, 189, 248, 0.4) !important; }
    h2 { color: #FFFFFF !important; font-weight: 800; font-size: 28px; margin-top: 5px; }
    h3 { color: #38BDF8 !important; font-weight: 700; margin-top: 30px; text-transform: uppercase; font-size: 18px; }
    
    .login-container { background-color: rgba(17, 24, 39, 0.85); padding: 35px; border-radius: 8px; border: 1px solid #334155; max-width: 450px; margin: 50px auto; backdrop-filter: blur(10px); }
    
    /* CAIXAS DE CALCULO */
    .calc-box { background-color: rgba(17, 24, 39, 0.8); border: 1px solid #374151; padding: 20px; border-radius: 8px; margin-bottom: 25px; backdrop-filter: blur(8px); }
    .calc-title { color: #38BDF8; font-weight: 700; font-size: 15px; margin-bottom: 15px; text-transform: uppercase; }

    /* ESTILIZAÇÃO DE TABELAS HISTÓRICAS */
    .styled-table { width: 100%; border-collapse: collapse; background-color: rgba(17, 24, 39, 0.85); border-radius: 6px; overflow: hidden; border: 1px solid #374151; margin-bottom: 15px; }
    .styled-table th { background-color: #030712; color: #38BDF8; padding: 12px; font-weight: 700; text-align: left; border-bottom: 2px solid #374151; }
    .styled-table td { padding: 10px 12px; border-bottom: 1px solid #374151; color: #FFFFFF !important; font-size: 14px; font-weight: 500; }
    
    .section-title { color: #FFFFFF !important; font-weight: 700; font-size: 15px; text-transform: uppercase; margin-top: 20px; margin-bottom: 8px; letter-spacing: 0.5px; }
    .stMarkdown p { color: #FFFFFF !important; }
    </style>
""", unsafe_allow_html=True)

DB_FILE = "banco_estetica.db"

def ajustar_tabelas_e_status():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicos_pendentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT, data_hora TEXT, atendente TEXT, veiculo TEXT, servico TEXT, valor REAL, comissao REAL, status TEXT DEFAULT 'PENDENTE'
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vales_solicitados (
            id INTEGER PRIMARY KEY AUTOINCREMENT, data_hora TEXT, atendente TEXT, valor REAL, motivo TEXT, status TEXT DEFAULT 'PENDENTE'
        )
    """)
    conn.commit()
    conn.close()

ajustar_tabelas_e_status()

if "admin_autenticado" not in st.session_state:
    st.session_state["admin_autenticado"] = False

# --- TELA DE LOGIN ---
if not st.session_state["admin_autenticado"]:
    st.markdown("<div class='brand-top' style='text-align:center;'>LC CONTROLE</div>", unsafe_allow_html=True)
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#FFFFFF; text-align:center; margin-top:0;'>🔒 Acesso Restrito</h3>", unsafe_allow_html=True)
    
    usuario = st.text_input("USUÁRIO ADM")
    senha = st.text_input("SENHA DE ACESSO", type="password")
    
    if st.button("ENTRAR NO PAINEL"):
        if usuario == "admin" and senha == "cleber2013":
            st.session_state["admin_autenticado"] = True
            st.rerun()
        else:
            st.error("Credenciais incorretas. Acesso negado.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- CONTEÚDO ADMINISTRATIVO ---
else:
    col_tit, col_logout = st.columns([8, 2])
    with col_tit:
        st.markdown("<div class='brand-top'>LC CONTROLE</div>", unsafe_allow_html=True)
        st.markdown("<h2>PAINEL DE CONTROLE ADMINISTRATIVO</h2>", unsafe_allow_html=True)
    with col_logout:
        if st.button("🔴 LOGOUT / SAIR"):
            st.session_state["admin_autenticado"] = False
            st.rerun()
            
    st.markdown("<hr style='border-color:#334155;'>", unsafe_allow_html=True)
    
    # --- PROCESSAMENTO DE AÇÕES ---
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    if "aprovar_lavagem" in st.query_params:
        cursor.execute("UPDATE servicos_pendentes SET status = 'APROVADO' WHERE id = ?", (st.query_params["aprovar_lavagem"],))
        conn.commit()
        st.query_params.clear()
        st.rerun()
        
    if "recusar_lavagem" in st.query_params:
        cursor.execute("UPDATE servicos_pendentes SET status = 'RECUSADO' WHERE id = ?", (st.query_params["recusar_lavagem"],))
        conn.commit()
        st.query_params.clear()
        st.rerun()

    if "aprovar_vale" in st.query_params:
        cursor.execute("UPDATE vales_solicitados SET status = 'APROVADO' WHERE id = ?", (st.query_params["aprovar_vale"],))
        conn.commit()
        st.query_params.clear()
        st.rerun()
        
    if "recusar_vale" in st.query_params:
        cursor.execute("UPDATE vales_solicitados SET status = 'RECUSADO' WHERE id = ?", (st.query_params["recusar_vale"],))
        conn.commit()
        st.query_params.clear()
        st.rerun()
        
    conn.close()

    # --- CALCULO METRICO GERAL (APROVADOS) ---
    conn = sqlite3.connect(DB_FILE)
    df_servicos_aprovados = pd.read_sql_query("SELECT valor, comissao FROM servicos_pendentes WHERE status = 'APROVADO'", conn)
    df_vales_aprovados = pd.read_sql_query("SELECT valor FROM vales_solicitados WHERE status = 'APROVADO'", conn)
    conn.close()
    
    total_bruto = df_servicos_aprovados['valor'].sum() if not df_servicos_aprovados.empty else 0.0
    total_comissoes = df_servicos_aprovados['comissao'].sum() if not df_servicos_aprovados.empty else 0.0
    total_vales_pagos = df_vales_aprovados['valor'].sum() if not df_vales_aprovados.empty else 0.0
    lucro_liquido = total_bruto - total_comissoes - total_vales_pagos
    
    st.markdown("### 📊 Faturamento Líquido Homologado")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("FATURAMENTO BRUTO (APROVADO)", f"R$ {total_bruto:.2f}")
    with c2:
        st.metric("COMISSÕES DEVIDAS (APROVADO)", f"R$ {total_comissoes:.2f}")
    with c3:
        st.metric("SALDO CAIXA (MENOS COMISSÃO E VALES)", f"R$ {lucro_liquido:.2f}")

    st.markdown("<hr style='border-color:#1E293B;'>", unsafe_allow_html=True)

    # --- SESSÃO DE FILA DE AGUARDO ---
    st.markdown("### 📥 Solicitações Aguardando Resposta")
    
    col_lav, col_val = st.columns(2)
    
    with col_lav:
        st.markdown("<h4>🚗 Lavagens Pendentes</h4>", unsafe_allow_html=True)
        conn = sqlite3.connect(DB_FILE)
        df_lav_p = pd.read_sql_query("SELECT id, data_hora, atendente, veiculo, servico, valor, comissao FROM servicos_pendentes WHERE status = 'PENDENTE' ORDER BY id DESC", conn)
        conn.close()
        
        if df_lav_p.empty:
            st.success("Nenhuma lavagem pendente.")
        else:
            for _, row in df_lav_p.iterrows():
                st.markdown(f"**{row['atendente']}** | {row['veiculo']} | {row['servico']} (R$ {row['valor']:.2f})")
                cb1, cb2 = st.columns(2)
                with cb1:
                    if st.button(f"✅ Aprovar Lavagem #{row['id']}", key=f"al_{row['id']}", use_container_width=True):
                        st.query_params["aprovar_lavagem"] = str(row['id'])
                        st.rerun()
                with cb2:
                    if st.button(f"❌ Recusar Lavagem #{row['id']}", key=f"rl_{row['id']}", use_container_width=True):
                        st.query_params["recusar_lavagem"] = str(row['id'])
                        st.rerun()
                st.markdown("<div style='border-bottom:1px solid #334155; margin:10px 0;'></div>", unsafe_allow_html=True)

    with col_val:
        st.markdown("<h4>📋 Vales Pendentes</h4>", unsafe_allow_html=True)
        conn = sqlite3.connect(DB_FILE)
        df_val_p = pd.read_sql_query("SELECT id, data_hora, atendente, valor, motivo FROM vales_solicitados WHERE status = 'PENDENTE' ORDER BY id DESC", conn)
        conn.close()
        
        if df_val_p.empty:
            st.success("Nenhum pedido de vale pendente.")
        else:
            for _, row in df_val_p.iterrows():
                st.markdown(f"**{row['atendente']}** pediu **R$ {row['valor']:.2f}**<br>Motivo: {row['motivo']}", unsafe_allow_html=True)
                cb1, cb2 = st.columns(2)
                with cb1:
                    if st.button(f"✅ Autorizar Vale #{row['id']}", key=f"av_{row['id']}", use_container_width=True):
                        st.query_params["aprovar_vale"] = str(row['id'])
                        st.rerun()
                with cb2:
                    if st.button(f"❌ Negar Vale #{row['id']}", key=f"rv_{row['id']}", use_container_width=True):
                        st.query_params["recusar_vale"] = str(row['id'])
                        st.rerun()
                st.markdown("<div style='border-bottom:1px solid #334155; margin:10px 0;'></div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1E293B;'>", unsafe_allow_html=True)

    # --- NOVO RECURSO: SOMA E CÁLCULO DE VALES POR FUNCIONÁRIO ---
    st.markdown("### 🧮 Auditoria e Fechamento por Operador")
    
    conn = sqlite3.connect(DB_FILE)
    df_todos_servicos = pd.read_sql_query("SELECT atendente FROM servicos_pendentes WHERE status='APROVADO'", conn)
    df_todos_vales = pd.read_sql_query("SELECT atendente FROM vales_solicitados WHERE status='APROVADO'", conn)
    conn.close()
    
    todos_funcionarios = sorted(list(set(df_todos_servicos['atendente'].unique()).union(set(df_todos_vales['atendente'].unique()))))
    
    if not todos_funcionarios:
        st.info("Nenhum dado aprovado disponível para fechamento.")
    else:
        st.markdown("<div class='calc-box'>", unsafe_allow_html=True)
        col_select, col_m1, col_m2, col_m3 = st.columns([2, 2, 2, 2])
        
        with col_select:
            func_escolhido = st.selectbox("Escolha o Funcionário", todos_funcionarios)
            
        conn = sqlite3.connect(DB_FILE)
        df_f_serv = pd.read_sql_query("SELECT comissao FROM servicos_pendentes WHERE atendente = ? AND status = 'APROVADO'", conn, params=(func_escolhido,))
        df_f_vale = pd.read_sql_query("SELECT valor FROM vales_solicitados WHERE atendente = ? AND status = 'APROVADO'", conn, params=(func_escolhido,))
        conn.close()
        
        soma_comissao = df_f_serv['comissao'].sum() if not df_f_serv.empty else 0.0
        soma_vale = df_f_vale['valor'].sum() if not df_f_vale.empty else 0.0
        saldo_final_funcionario = soma_comissao - soma_vale
        
        with col_m1:
            st.metric("TOTAL COMISSÕES", f"R$ {soma_comissao:.2f}")
        with col_m2:
            st.metric("TOTAL VALES PEGOS", f"R$ {soma_vale:.2f}")
        with col_m3:
            # Mostra em verde se ele tem a receber ou em vermelho se pegou mais vales do que comissão
            label_saldo = "SALDO LÍQUIDO A PAGAR" if saldo_final_funcionario >= 0 else "VALOR DEVIDO À EMPRESA"
            st.metric(label_saldo, f"R$ {abs(saldo_final_funcionario):.2f}")
            
        st.markdown("</div>", unsafe_allow_html=True)

    # --- TABELA HISTÓRICA GERAL DE VALES APROVADOS ---
    st.markdown("### 📜 Histórico de Vales Homologados (Por Período)")
    
    conn = sqlite3.connect(DB_FILE)
    df_historico_vales = pd.read_sql_query("SELECT data_hora, atendente, valor, motivo FROM vales_solicitados WHERE status = 'APROVADO' ORDER BY id DESC", conn)
    conn.close()
    
    if df_historico_vales.empty:
        st.info("Nenhum vale aprovado no histórico recente.")
    else:
        df_historico_vales['data_formatada'] = pd.to_datetime(df_historico_vales['data_hora'], format='%d/%m/%Y %H:%M', errors='coerce')
        df_historico_vales['Ano_Semana'] = df_historico_vales['data_formatada'].dt.strftime('%Y-W%U')
        semanas_vales = sorted(df_historico_vales['Ano_Semana'].dropna().unique(), reverse=True)
        
        for sem in semanas_vales:
            df_sem_v = df_historico_vales[df_historico_vales['Ano_Semana'] == sem]
            d_min = df_sem_v['data_formatada'].min().strftime('%d/%m/%Y')
            d_max = df_sem_v['data_formatada'].max().strftime('%d/%m/%Y')
            
            st.markdown(f"<div class='section-title'>Período de Retiradas: {d_min} até {d_max} (Semana {sem.split('-W')[1]})</div>", unsafe_allow_html=True)
            
            html_vales = "<table class='styled-table'><thead><tr><th>Data/Horário</th><th>Funcionário</th><th>Valor Adiantado</th><th>Justificativa</th></tr></thead><tbody>"
            for _, row in df_sem_v.iterrows():
                html_vales += f"<tr><td>{row['data_hora']}</td><td>{row['atendente']}</td><td>R$ {row['valor']:.2f}</td><td>{row['motivo']}</td></tr>"
            html_vales += "</tbody></table>"
            st.markdown(html_vales, unsafe_allow_html=True)