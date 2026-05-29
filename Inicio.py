import streamlit as st

st.set_page_config(page_title="LC CONTROLE - Início", layout="centered")

# --- ARQUITETURA DE DESIGN AUTOMOTIVO PREMIUM ---
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
    
    /* --- BRANDING LC CONTROLE --- */
    .brand-header { text-align: center; margin-bottom: 30px; }
    .brand-title { color: #38BDF8 !important; font-family: 'Inter', sans-serif; font-weight: 900; font-size: 52px; letter-spacing: 2px; text-shadow: 0px 0px 15px rgba(56, 189, 248, 0.6) !important; margin: 0; }
    .brand-tagline { color: #94A3B8 !important; font-size: 14px; text-transform: uppercase; letter-spacing: 3px; margin-top: 5px; }
    
    .section-title { color: #38BDF8 !important; font-family: 'Inter', sans-serif; font-weight: 700; font-size: 22px; margin-top: 25px; margin-bottom: 15px; }
    hr { border-color: #334155 !important; margin: 20px 0; }
    .regra-box { background-color: rgba(30, 41, 59, 0.75); border-left: 4px solid #EF4444; padding: 18px; border-radius: 6px; margin-bottom: 15px; backdrop-filter: blur(5px); color: #F1F5F9; }
    .protocolo-box { background-color: rgba(30, 41, 59, 0.75); border-left: 4px solid #38BDF8; padding: 18px; border-radius: 6px; margin-bottom: 15px; backdrop-filter: blur(5px); color: #F1F5F9; }
    </style>
""", unsafe_allow_html=True)

# Topo com a marca em destaque absoluto
st.markdown("""
<div class='brand-header'>
    <h1 class='brand-title'>LC CONTROLE</h1>
    <div class='brand-tagline'>Sistema de Gestão Automotiva</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #94A3B8 !important;'>Navegue pelas seções do sistema utilizando o menu de navegação lateral.</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("<div class='section-title'>REGULAMENTO INTERNO DA EMPRESA</div>", unsafe_allow_html=True)
st.markdown("""
<div class='regra-box'>
    <b style='color: #EF4444;'>1. TRANSAÇÕES VIA PIX:</b><br>
    Todos os pagamentos nesta modalidade devem ser direcionados exclusivamente para a chave PIX corporativa da empresa. É terminantemente proibido o recebimento em contas de terceiros ou pessoais.
</div>
<div class='regra-box'>
    <b style='color: #EF4444;'>2. ARRECADAÇÃO EM ESPÉCIE (DINHEIRO):</b><br>
    Os valores recebidos em cédulas devem ser obrigatoriamente reportados e entregues ao profissional responsável pela gestão do caixa no respectivo plantão.
</div>
<div class='regra-box'>
    <b style='color: #EF4444;'>3. POLÍTICA DE COMISSIONAMENTO:</b><br>
    As comissões operacionais seguem a tabela fixa homologada pela administração, sofrendo variações estritamente condicionadas à especificação técnica do serviço prestado.
</div>
<div class='regra-box'>
    <b style='color: #EF4444;'>4. CONDUTA E ÉTICA PROFISSIONAL:</b><br>
    Mantenha postura profissional nas dependências da empresa. São vedadas discussões, linguagem inapropriada ou interações informais excessivas, especialmente no raio de atendimento ao cliente.
</div>
<div class='regra-box'>
    <b style='color: #EF4444;'>5. MANUTENÇÃO E ORGANIZAÇÃO DO AMBIENTE:</b><br>
    É responsabilidade do operador manter insumos e ferramentas acomodados nos devidos suportes. Produtos não devem permanecer ao solo e as flanelas devem ser estendidas em local apropriado para secagem imediata após o uso.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>TABELA RECONHECIDA DE VALORES E COMISSÕES</div>", unsafe_allow_html=True)
st.markdown("""
<div class='protocolo-box'>
    <b>Ducha (Água e Sabão)</b><br>
    • Veículo de Porte Padrão: Valor R$ 10,00 | Comissão Operacional: <span style='color: #38BDF8;'>R$ 2,50</span><br>
    • Veículo de Porte Grande: Valor R$ 20,00 | Comissão Operacional: <span style='color: #38BDF8;'>R$ 5,00</span>
</div>
<div class='protocolo-box'>
    <b>Lavagem Externa</b><br>
    • Valor Único: R$ 20,00 | Comissão Operacional: <span style='color: #38BDF8;'>R$ 5,00</span>
</div>
<div class='protocolo-box'>
    <b>Lavagem Interna</b><br>
    • Valor Único: R$ 20,00 | Comissão Operacional: <span style='color: #38BDF8;'>R$ 5,00</span>
</div>
<div class='protocolo-box'>
    <b>Lavagem Completa</b><br>
    • Veículo de Porte Padrão: Valor R$ 30,00 | Comissão Operacional: <span style='color: #38BDF8;'>R$ 10,00</span><br>
    • Veículo de Porte Grande: Valor sob avaliação entre R$ 40,00 e R$ 60,00
</div>
<div class='protocolo-box' style='border-left-color: #F59E0B;'>
    <b style='color: #F59E0B;'>SERVIÇOS ESPECIAIS (VALORES ACIMA DE R$ 60,00):</b><br>
    Para procedimentos de estética automotiva cujos valores excedam o teto de R$ 60,00, o operador deve obrigatoriamente reportar-se à administração para validação prévia do preço final e margem de comissão.
</div>
""", unsafe_allow_html=True)