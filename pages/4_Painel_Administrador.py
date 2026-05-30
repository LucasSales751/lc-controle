import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="LC CONTROLE - Painel Admin", layout="wide")

# --- DESIGN AUTOMOTIVO PREMIUM (MÁXIMO CONTRASTE) ---
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
    
    /* CORES E FONTES */
    .stMetric label p { color: #FFFFFF !important; font-weight: 700 !important; }
    div[data-testid="stMetricValue"] { color: #38BDF8 !important; font-weight: 900 !important; }
    
    h2, h3, h4 { color: #FFFFFF !important; font-weight: 800; }
    .brand-top { color: #38BDF8 !important; font-weight: 900; font-size: 20px; letter-spacing: 1px; text-shadow: 0px 0px 8px rgba(56, 189, 248, 0.4); }
    
    /* TABELAS */
    .styled-table { width: 100%; border-collapse: collapse; background-color: rgba(17, 24, 39, 0.85); border-radius: 6px; overflow: hidden; border: 1px solid #374151; margin-bottom: 20px; }
    .styled-table th { background-color: #030712; color: #38BDF8; padding: 12px; text-align: left; font-size: 14px; border-bottom: 2px solid #374151; }
    .styled-table td { padding: 12px; border-bottom: 1px solid #374151; color: #FFFFFF !important; font-size: 14px; font-weight: 500; }
    
    .login-container { background-color: rgba(17, 24, 39, 0.85); padding: 35px; border-radius: 8px; border: 1px solid #334155; max-width: 450px; margin: 50px auto; }
    </style>
""", unsafe_allow_html=True)

DB_FILE = "banco_estetica.db"

if "admin_autenticado" not in st.session_state:
    st.session_state["admin_autenticado"] = False

# --- LOGIN ---
if not st.session_state["admin_autenticado"]:
    st.markdown("<div class='brand-top' style='text-align:center;'>LC CONTROLE</div>", unsafe_allow_html=True)
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; margin-top:0;'>🔒 ACESSO ADM</h3>", unsafe_allow_html=True)
    u = st.text_input("USUÁRIO")
    s = st.text_input("SENHA", type="password")
    if st.button("ENTRAR"):
        if u == "admin" and s == "lc123":
            st.session_state["admin_autenticado"] = True
            st.rerun()
        else: st.error("Acesso Negado")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- HEADER ---
    c_tit, c_log = st.columns([8, 2])
    with c_tit:
        st.markdown("<div class='brand-top'>LC CONTROLE</div>", unsafe_allow_html=True)
        st.markdown("<h2>GERENCIAMENTO ADMINISTRATIVO</h2>", unsafe_allow_html=True)
    with c_log:
        if st.button("🔴 SAIR"):
            st.session_state["admin_autenticado"] = False
            st.rerun()

    st.markdown("---")

    # --- FUNÇÕES DE BANCO DE DADOS ---
    def executar_query(query, params=()):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    # --- PROCESSAMENTO DE EXCLUSÃO E APROVAÇÃO ---
    qp = st.query_params
    if "del_lav" in qp:
        executar_query("DELETE FROM servicos_pendentes WHERE id = ?", (qp["del_lav"],))
        st.query_params.clear(); st.rerun()
    if "del_val" in qp:
        executar_query("DELETE FROM vales_solicitados WHERE id = ?", (qp["del_val"],))
        st.query_params.clear(); st.rerun()
    if "ap_lav" in qp:
        executar_query("UPDATE servicos_pendentes SET status = 'APROVADO' WHERE id = ?", (qp["ap_lav"],))
        st.query_params.clear(); st.rerun()
    if "ap_val" in qp:
        executar_query("UPDATE vales_solicitados SET status = 'APROVADO' WHERE id = ?", (qp["ap_val"],))
        st.query_params.clear(); st.rerun()

    # --- MÉTRICAS GERAIS ---
    conn = sqlite3.connect(DB_FILE)
    df_s = pd.read_sql_query("SELECT atendente, valor, comissao FROM servicos_pendentes WHERE status='APROVADO'", conn)
    df_v = pd.read_sql_query("SELECT atendente, valor FROM vales_solicitados WHERE status='APROVADO'", conn)
    conn.close()

    bruto = df_s['valor'].sum() if not df_s.empty else 0.0
    comis = df_s['comissao'].sum() if not df_s.empty else 0.0
    vales = df_v['valor'].sum() if not df_v.empty else 0.0
    
    st.markdown("### 📊 Resumo de Caixa Geral")
    m1, m2, m3 = st.columns(3)
    m1.metric("FATURAMENTO BRUTO", f"R$ {bruto:.2f}")
    m2.metric("TOTAL COMISSÕES", f"R$ {comis:.2f}")
    m3.metric("LUCRO LÍQUIDO", f"R$ {bruto - comis - vales:.2f}")

    # --- INDIVIDUAL (SOMA VALES E COMISSÕES POR PESSOA) ---
    st.markdown("---")
    st.markdown("### 👥 Fechamento por Funcionário (Cálculo Automático)")
    
    if not df_s.empty:
        df_s['atendente'] = df_s['atendente'].str.upper().str.strip()
        df_comis_agrup = df_s.groupby('atendente')['comissao'].sum().reset_index()
    else:
        df_comis_agrup = pd.DataFrame(columns=['atendente', 'comissao'])
        
    if not df_v.empty:
        df_v['atendente'] = df_v['atendente'].str.upper().str.strip()
        df_vales_agrup = df_v.groupby('atendente')['valor'].sum().reset_index().rename(columns={'valor': 'total_vale'})
    else:
        df_vales_agrup = pd.DataFrame(columns=['atendente', 'total_vale'])
    
    df_fechamento = pd.merge(df_comis_agrup, df_vales_agrup, on='atendente', how='outer').fillna(0)
    df_fechamento['liquido'] = df_fechamento['comissao'] - df_fechamento['total_vale']

    if df_fechamento.empty:
        st.info("Nenhum registro aprovado para calcular o fechamento dos funcionários ainda.")
    else:
        html_tabela = """
        <table class='styled-table'>
            <thead>
                <tr>
                    <th>FUNCIONÁRIO</th>
                    <th>(+) TOTAL COMISSÕES</th>
                    <th>(-) TOTAL VALES PEGO</th>
                    <th>(=) SALDO LÍQUIDO A PAGAR</th>
                </tr>
            </thead>
            <tbody>
        """
        for _, linha in df_fechamento.iterrows():
            cor_saldo = "#34D399" if linha['liquido'] >= 0 else "#F87171"
            html_tabela += f"""
                <tr>
                    <td><b>{linha['atendente']}</b></td>
                    <td style='color: #34D399;'>R$ {linha['comissao']:.2f}</td>
                    <td style='color: #F87171;'>R$ {linha['total_vale']:.2f}</td>
                    <td style='color: {cor_saldo}; font-weight: 700;'>R$ {linha['liquido']:.2f}</td>
                </tr>
            """
        html_tabela += """
            </tbody>
        </table>
        """
        st.markdown(html_tabela, unsafe_allow_html=True)

    # --- FILA DE PENDENTES ---
    st.markdown("---")
    col_l, col_v = st.columns(2)

    with col_l:
        st.markdown("### 🚗 Lavagens Pendentes")
        conn = sqlite3.connect(DB_FILE)
        df_lp = pd.read_sql_query("SELECT * FROM servicos_pendentes WHERE status='PENDENTE'", conn)
        conn.close()
        for _, r in df_lp.iterrows():
            st.write(f"**{r['atendente']}** | {r['veiculo']} | R$ {r['valor']:.2f}")
            b1, b2 = st.columns(2)
            if b1.button(f"✅ Aprovar", key=f"ap_l_{r['id']}"):
                st.query_params["ap_lav"] = str(r['id']); st.rerun()
            if b2.button(f"🗑️ Excluir", key=f"del_l_{r['id']}"):
                st.query_params["del_lav"] = str(r['id']); st.rerun()

    with col_v:
        st.markdown("### 📋 Vales Pendentes")
        conn = sqlite3.connect(DB_FILE)
        df_vp = pd.read_sql_query("SELECT * FROM vales_solicitados WHERE status='PENDENTE'", conn)
        conn.close()
        for _, r in df_vp.iterrows():
            st.write(f"**{r['atendente']}** pediu R$ {r['valor']:.2f}")
            b1, b2 = st.columns(2)
            if b1.button(f"✅ Autorizar", key=f"ap_v_{r['id']}"):
                st.query_params["ap_val"] = str(r['id']); st.rerun()
            if b2.button(f"🗑️ Excluir", key=f"del_v_{r['id']}"):
                st.query_params["del_val"] = str(r['id']); st.rerun()

    # --- HISTÓRICO E EXCLUSÃO DE REGISTROS ANTIGOS ---
    st.markdown("---")
    st.markdown("### 📜 Histórico de Registros Aprovados")
    tab_lav, tab_val = st.tabs(["Serviços Lavados", "Vales Pagos"])

    with tab_lav:
        conn = sqlite3.connect(DB_FILE)
        df_h_l = pd.read_sql_query("SELECT id, data_hora, atendente, veiculo, valor FROM servicos_pendentes WHERE status='APROVADO' ORDER BY id DESC", conn)
        conn.close()
        if df_h_l.empty: st.info("Sem histórico")
        else:
            for _, r in df_h_l.iterrows():
                c1, c2 = st.columns([8, 2])
                c1.markdown(f"**{r['data_hora']}** - {r['atendente']} - {r['veiculo']} - R$ {r['valor']:.2f}")
                if c2.button("🗑️ Apagar", key=f"hist_l_{r['id']}"):
                    st.query_params["del_lav"] = str(r['id']); st.rerun()

    with tab_val:
        conn = sqlite3.connect(DB_FILE)
        df_h_v = pd.read_sql_query("SELECT id, data_hora, atendente, valor, motivo FROM vales_solicitados WHERE status='APROVADO' ORDER BY id DESC", conn)
        conn.close()
        if df_h_v.empty: st.info("Sem histórico")
        else:
            for _, r in df_h_v.iterrows():
                c1, c2 = st.columns([8, 2])
                c1.markdown(f"**{r['data_hora']}** - {r['atendente']} - R$ {r['valor']:.2f} - {r['motivo']}")
                if c2.button("🗑️ Apagar", key=f"hist_v_{r['id']}"):
                    st.query_params["del_val"] = str(r['id']); st.rerun()
