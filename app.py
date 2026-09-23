import streamlit as st
import json
import os

# 1. Configuração da página com o ícone 📜 escolhido
st.set_page_config(
    page_title="Balanço ECC - Forania",
    page_icon="📜",
    layout="wide"
)

# 2. Caminho do arquivo JSON de dados
DATA_FILE = "dados_dashboard.json"

# Valores padrão de segurança (caso o arquivo JSON não exista)
DEFAULT_DATA = {
    "texto_aconteceu": "Realizamos os encontros nas paróquias das Foranias São Francisco e Santa Clara, e retomamos na...",
    "ano_fichas": 2026,
    "titulo_fichas_base": "📝 FICHAS PREENCHIDAS/ANÁLISE",
    "fichas_st": "~15 fichas",
    "fichas_sf": "~32 fichas",
    "fichas_ns": "~30 fichas",
    "fichas_sp": "~35 fichas",
    "fichas_e2": "~25 fichas",
    "obs_card": "Simulação de Dados..",
    "st_24": 14, "st_25": 18, "st_26": 13, "st_27": 0,
    "sf_24": 26, "sf_25": 32, "sf_26": 22, "sf_27": 0,
    "ns_24": 22, "ns_25": 15, "ns_26": 15, "ns_27": 0,
    "sp_24": 0, "sp_25": 0, "sp_26": 12, "sp_27": 0,
    "e2_24": 21, "e2_25": 30, "e2_26": 25, "e2_27": 0,
    "c_st_24": 3, "c_st_25": 4, "c_st_26": 3, "c_st_27": 0,
    "c_sf_24": 5, "c_sf_25": 5, "c_sf_26": 4, "c_sf_27": 0,
    "c_ns_24": 4, "c_ns_25": 3, "c_ns_26": 4, "c_ns_27": 0,
    "c_sp_24": 0, "c_sp_25": 0, "c_sp_26": 3, "c_sp_27": 0,
    "c_e2_24": 4, "c_e2_25": 5, "c_e2_26": 5, "c_e2_27": 0,
    "st_status_e2": "Concluído",
    "st_status_st": "Concluído",
    "st_status_ns": "Concluído",
    "st_status_sp": "Concluído",
    "st_status_sf": "Em andamento"
}

# Funções para carregar e salvar os dados
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_DATA.copy()
    return DEFAULT_DATA.copy()

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Carrega os dados salvos
data = load_data()

# ---------------------------------------------------------
# BARRA LATERAL (Painel de Controle)
# ---------------------------------------------------------
st.sidebar.title("⚙️ Controle de Dados")

# O que já aconteceu
st.sidebar.subheader("🗓️ O que já aconteceu")
texto_aconteceu = st.sidebar.text_area(
    "Texto do Card 'O que já aconteceu':",
    value=data.get("texto_aconteceu", ""),
    height=100
)

# Fichas em Análise
st.sidebar.subheader("📄 Fichas em Análise")
ano_fichas = st.sidebar.selectbox(
    "Selecione o Ano",
    options=[2024, 2025, 2026, 2027],
    index=[2024, 2025, 2026, 2027].index(data.get("ano_fichas", 2026))
)
titulo_fichas_base = st.sidebar.text_input("Título Base do Cartão", value=data.get("titulo_fichas_base", "📝 FICHAS PREENCHIDAS/ANÁLISE"))

fichas_st = st.sidebar.text_input("Santo Antônio (Fichas)", value=data.get("fichas_st", ""))
fichas_sf = st.sidebar.text_input("São Francisco e Santa Clara (Fichas)", value=data.get("fichas_sf", ""))
fichas_ns = st.sidebar.text_input("Nossa Senhora de Fátima (Fichas)", value=data.get("fichas_ns", ""))
fichas_sp = st.sidebar.text_input("São Pedro Apóstolo (Fichas)", value=data.get("fichas_sp", ""))
fichas_e2 = st.sidebar.text_input("2ª Etapa (Fichas)", value=data.get("fichas_e2", ""))

obs_card = st.sidebar.text_input("Observação do Rodapé das Fichas", value=data.get("obs_card", ""))

# Botão para salvar alterações na sessão atual
if st.sidebar.button("💾 Salvar Alterações no App"):
    data["texto_aconteceu"] = texto_aconteceu
    data["ano_fichas"] = ano_fichas
    data["titulo_fichas_base"] = titulo_fichas_base
    data["fichas_st"] = fichas_st
    data["fichas_sf"] = fichas_sf
    data["fichas_ns"] = fichas_ns
    data["fichas_sp"] = fichas_sp
    data["fichas_e2"] = fichas_e2
    data["obs_card"] = obs_card
    save_data(data)
    st.sidebar.success("Dados salvos com sucesso!")

# ---------------------------------------------------------
# CORPO PRINCIPAL DO DASHBOARD
# ---------------------------------------------------------

# Botão superior de download fictício/estético
st.button("📸 Baixar Dashboard como Imagem (JPG)", use_container_width=True)

# Banner Principal
st.markdown(f"""
    <div style="background-color: #E65100; padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 20px;">
        <h1 style="margin:0;">BALANÇO 2024 A 2027</h1>
        <h3 style="margin:0;">FORANIA SÃO FRANCISCO E SANTA CLARA</h3>
        <p style="margin:0; font-size: 14px;">✦ ENCONTRO DE CASAIS COM CRISTO – 1ª ETAPA / 2ª ETAPA ✦</p>
    </div>
""", unsafe_allow_html=True)

# Layout em colunas para os cartões e tabelas
col1, col2 = st.columns(2)

with col1:
    st.subheader("👥 CASAIS VIVENCIADOS")
    st.markdown(f"""
    | Paróquia / Etapa | 2024 | 2025 | 2026 | 2027 |
    | :--- | :---: | :---: | :---: | :---: |
    | ⛪ Santo Antônio | {data.get('st_24', 0)} | {data.get('st_25', 0)} | {data.get('st_26', 0)} | {data.get('st_27', 0)} |
    | ⛪ S. Francisco e S. Clara | {data.get('sf_24', 0)} | {data.get('sf_25', 0)} | {data.get('sf_26', 0)} | {data.get('sf_27', 0)} |
    | ⛪ Nossa Senhora de Fátima | {data.get('ns_24', 0)} | {data.get('ns_25', 0)} | {data.get('ns_26', 0)} | {data.get('ns_27', 0)} |
    | ⛪ São Pedro Apóstolo | {data.get('sp_24', 0)} | {data.get('sp_25', 0)} | {data.get('sp_26', 0)} | {data.get('sp_27', 0)} |
    | ⛪ 2ª Etapa | {data.get('e2_24', 0)} | {data.get('e2_25', 0)} | {data.get('e2_26', 0)} | {data.get('e2_27', 0)} |
    """)

with col2:
    st.subheader("⭕ CÍRCULOS DE ESTUDO")
    st.markdown(f"""
    | Paróquia / Etapa | 2024 | 2025 | 2026 | 2027 |
    | :--- | :---: | :---: | :---: | :---: |
    | ⛪ Santo Antônio | {data.get('c_st_24', 0)} | {data.get('c_st_25', 0)} | {data.get('c_st_26', 0)} | {data.get('c_st_27', 0)} |
    | ⛪ S. Francisco e S. Clara | {data.get('c_sf_24', 0)} | {data.get('c_sf_25', 0)} | {data.get('c_sf_26', 0)} | {data.get('c_sf_27', 0)} |
    | ⛪ Nossa Senhora de Fátima | {data.get('c_ns_24', 0)} | {data.get('c_ns_25', 0)} | {data.get('c_ns_26', 0)} | {data.get('c_ns_27', 0)} |
    | ⛪ São Pedro Apóstolo | {data.get('c_sp_24', 0)} | {data.get('c_sp_25', 0)} | {data.get('c_sp_26', 0)} | {data.get('c_sp_27', 0)} |
    | ⛪ 2ª Etapa | {data.get('c_e2_24', 0)} | {data.get('c_e2_25', 0)} | {data.get('c_e2_26', 0)} | {data.get('c_e2_27', 0)} |
    """)

# Seção inferior com o resumo das fichas e o texto informativo
st.divider()

c_info1, c_info2 = st.columns(2)

with c_info1:
    st.info(f"**{titulo_fichas_base} ({ano_fichas})**\n\n"
            f"* Santo Antônio: {fichas_st}\n"
            f"* São Francisco e Santa Clara: {fichas_sf}\n"
            f"* Nossa Senhora de Fátima: {fichas_ns}\n"
            f"* São Pedro Apóstolo: {fichas_sp}\n"
            f"* 2ª Etapa: {fichas_e2}\n\n"
            f"_{obs_card}_")

with c_info2:
    st.success(f"**🗓️ O que já aconteceu em {ano_fichas}:**\n\n{texto_aconteceu}")
