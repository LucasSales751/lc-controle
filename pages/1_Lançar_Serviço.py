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
                         url('https://images.unsplash.com/photo-1520340356584-f9917d1eea6f?q=80&w=1920');
        background-size: cover !important; 
        background-position: center !important; 
        background-attachment: fixed !important;
        color: #F8FAFC !important;
    }
    .brand-top { color: #38BDF8 !important; font-weight: 900; font-size: 20px; letter-spacing: 1px; text-shadow: 0px 0px 8px rgba(56, 189, 248, 0.4); }
    h2 { color: #FFFFFF !important; font-weight: 800; margin-top: 5px; }
    
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
st.markdown("Preencha os dados abaixo para enviar o serviço.")

DB_FILE = "banco_estetica.db"

# --- FORMULÁRIO DE LANÇAMENTO ---
with st.form("form_servico", clear_on_submit=True):
    
    # Seleção de quantas pessoas trabalharam no veículo
    qtd_trabalhadores = st.selectbox("👥 QUANTAS PESSOAS LAVARAM?", [1, 2, 3, 4], index=0)
    
    # Campos dinâmicos para os nomes baseados na quantidade selecionada
    atendentes = []
    if qtd_trabalhadores == 1:
        atendentes.append(st.text_input("👤 SEU NOME (FUNCIONÁRIO)", placeholder="Digite seu nome").strip())
    else:
        for i in range(qtd_trabalhadores):
            atendentes.append(st.text_input(f"👤 NOME DO {i+1}º FUNCIONÁRIO", placeholder=f"Nome do lavador {i+1}").strip())
            
    veiculo = st.text_input("🚘 PLACA OU MODELO DO VEÍCULO", placeholder="Ex: Civic Preto, Titan 160, etc.").upper()
    
    tipo_servico = st.selectbox("🛠️ TIPO DE SERVIÇO", [
        "Ducha", 
        "Lavagem Externa",
        "Lavagem Completa", 
        "Higienização Interna",
        "Lavagem de Moto"
    ])
    
    tamanho_veiculo = st.selectbox("📏 PORTE DO VEÍCULO (Apenas p/ Carros)", ["Pequeno", "Médio", "Grande (SUV / Camionete)"])

    # Campo dinâmico para preço da moto (só aparece se selecionar Lavagem de Moto)
    preco_moto_escolhido = 20.00
    if tipo_servico == "Lavagem de Moto":
        preco_moto_escolhido = st.selectbox("🏍️ VALOR DA MOTO (Flexível)", [20.00, 25.00], help="Escolha R$ 25 ou R$ 20 caso dê desconto.")

    # --- LÓGICA DE PREÇOS E COMISSÕES AJUSTADA ---
    valor_final = 0.0
    comissao_total_servico = 0.0

    # 1. Ducha
    if tipo_servico == "Ducha":
        if tamanho_veiculo == "Grande (SUV / Camionete)":
            valor_final = 20.00
            comissao_total_servico = 5.00
        else:
            valor_final = 10.00
            comissao_total_servico = 2.50

    # 2. Lavagem Externa
    elif tipo_servico == "Lavagem Externa":
        valor_final = 20.00
        comissao_total_servico = 5.00

    # 3. Higienização Interna
    elif tipo_servico == "Higienização Interna":
        valor_final = 20.00
        comissao_total_servico = 5.00

    # 4. Lavagem Completa
    elif tipo_servico == "Lavagem Completa":
        if tamanho_veiculo == "Grande (SUV / Camionete)":
            valor_final = 50.00
            comissao_total_servico = 10.00 # Fixo em R$ 10
        else:
            valor_final = 30.00
            comissao_total_servico = 10.00 # Fixo em R$ 10

    # 5. Lavagem de Moto (Comissão Fixa corrigida para R$ 10.00)
    elif tipo_servico == "Lavagem de Moto":
        valor_final = preco_moto_escolhido
        comissao_total_servico = 10.00

    # Divisão matemática exata da comissão por cabeça
    comissao_por_pessoa = comissao_total_servico / qtd_trabalhadores

    # Mostra o resumo na tela antes de enviar
    texto_nomes = ", ".join([n for n in atendentes if n])
    st.markdown(f"""
    <div class="resumo-box">
        <p style="margin:0; color:#94A3B8;">Resumo do Lançamento:</p>
        <b style="color:#FFFFFF;">Valor Total do Serviço:</b> <span style="color:#38BDF8; font-weight:700;">R$ {valor_final:.2f}</span><br>
        <b style="color:#FFFFFF;">Comissão Total:</b> <span style="color:#34D399; font-weight:700;">R$ {comissao_total_servico:.2f}</span><br>
        <b style="color:#38BDF8;">Cada um vai receber:</b> <span style="color:#34D399; font-weight:700;">R$ {comissao_por_pessoa:.2f}</span>
    </div>
    """, unsafe_allow_html=True)

    botao_enviar = st.form_submit_button("🔥 ENVIAR PARA APROVAÇÃO DO ADM")

# --- GRAVAÇÃO NO BANCO DE DADOS ---
if botao_enviar:
    nomes_vazios = any(not nome for nome in atendentes)
    
    if nomes_vazios or not veiculo:
        st.error("❌ Por favor, preencha todos os nomes dos lavadores e os dados do veículo!")
    else:
        try:
            data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
            
            if tipo_servico == "Lavagem de Moto":
                veiculo_detalhado = f"{veiculo} (MOTO)"
            else:
                veiculo_detalhado = f"{veiculo} ({tamanho_veiculo})"
                
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            
            # Loop para cadastrar a comissão dividida de forma justa para cada ajudante
            for lavador in atendentes:
                cursor.execute("""
                    INSERT INTO servicos_pendentes (data_hora, atendente, veiculo, servico, valor, comissao, status)
                    VALUES (?, ?, ?, ?, ?, ?, 'PENDENTE')
                """, (data_atual, lavador, veiculo_detalhado, tipo_servico, valor_final, comissao_por_pessoa))
            
            conn.commit()
            conn.close()
            
            st.success(f"✅ Sucesso! Serviço lançado para {texto_nomes}. Cada comissão ficou em R$ {comissao_por_pessoa:.2f}")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao salvar no banco de dados: {e}")
