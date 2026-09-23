import streamlit as st
import streamlit.components.v1 as components
import os
import json
from datetime import datetime

st.set_page_config(page_title="Balanço ECC Forania", layout="wide")

st.markdown("<style>.main .block-container{padding-top:0.5rem; padding-left:0.2rem; padding-right:0.2rem;}</style>", unsafe_allow_html=True)

# --- SISTEMA DE PERSISTÊNCIA DE DADOS (JSON) ---
ARQUIVO_DADOS = "dados_dashboard.json"

# Valores padrão caso o ficheiro de dados ainda não exista
DADOS_PADRAO = {
    "texto_aconteceu": "Ja realizamos encontros de 1ª etapa nas paroquias Santo Antonio, Sao Pedro e 2ª etapa.\nFaltando as Paroquias Sao Francisco e Santa Clara e Nossa Senhora de Fatima",
    "ano_fichas": 2026,
    "titulo_fichas_base": "📝 FICHAS PREENCHIDAS/ANÁLISE (1ª ETAPA / 2ª ETAPA)",
    "fichas_st": "~15 fichas (abaixo)",
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

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                dados = json.load(f)
                # Garante que novas chaves existam se o ficheiro for antigo
                for k, v in DADOS_PADRAO.items():
                    if k not in dados:
                        dados[k] = v
                return dados
        except Exception:
            return DADOS_PADRAO.copy()
    return DADOS_PADRAO.copy()

def salvar_dados(novos_dados):
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump(novos_dados, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.sidebar.error(f"Erro ao salvar dados automaticamente: {e}")

dados_atuais = carregar_dados()

# --- FUNÇÃO AUXILIAR PARA CÁLCULO DINÂMICO DE VARIAÇÃO ---
def calc_var(atual, anterior):
    dif = atual - anterior
    if anterior == 0:
        if atual == 0:
            pct_str = "-"
            pct_val = 0.0
        else:
            pct_str = "+100%"
            pct_val = 100.0
    else:
        pct = (dif / anterior) * 100
        pct_str = f"{pct:+.2f}%".replace('.', ',')
        pct_val = pct
    
    if dif > 0:
        dif_str = f"+{dif}"
        color_class = "c-blue"
    elif dif < 0:
        dif_str = f"{dif}"
        color_class = "c-red"
    else:
        dif_str = "0"
        color_class = ""
        
    return dif, dif_str, pct_str, color_class, pct_val

# --- CONFIGURAÇÃO SIDEBAR ---
st.sidebar.header("⚙️ Controle de Dados")

# CAMPO EDITÁVEL: O QUE JÁ ACONTECEU EM 2026
texto_aconteceu = st.sidebar.text_area(
    "📅 O que já aconteceu em 2026", 
    value=dados_atuais.get("texto_aconteceu", DADOS_PADRAO["texto_aconteceu"]),
    height=90
)

# === DADOS DE FICHAS EM ANÁLISE POR ANO ===
with st.sidebar.expander("📝 Fichas em Análise", expanded=True):
    anos_opts = [2024, 2025, 2026, 2027]
    idx_ano = anos_opts.index(dados_atuais.get("ano_fichas", 2026)) if dados_atuais.get("ano_fichas", 2026) in anos_opts else 2
    ano_fichas = st.selectbox("Selecione o Ano", anos_opts, index=idx_ano)
    titulo_fichas_base = st.text_input("Título Base do Cartão", value=dados_atuais.get("titulo_fichas_base", DADOS_PADRAO["titulo_fichas_base"]))
    
    st.markdown(f"**Valores por Paróquia / Etapa ({ano_fichas}):**")
    fichas_st = st.text_input("Santo Antônio", value=dados_atuais.get("fichas_st", DADOS_PADRAO["fichas_st"]))
    fichas_sf = st.text_input("São Francisco e S. Clara", value=dados_atuais.get("fichas_sf", DADOS_PADRAO["fichas_sf"]))
    fichas_ns = st.text_input("N. Sra. de Fátima", value=dados_atuais.get("fichas_ns", DADOS_PADRAO["fichas_ns"]))
    fichas_sp = st.text_input("São Pedro Apóstolo", value=dados_atuais.get("fichas_sp", DADOS_PADRAO["fichas_sp"]))
    fichas_e2 = st.text_input("2ª Etapa", value=dados_atuais.get("fichas_e2", DADOS_PADRAO["fichas_e2"]))

titulo_fichas_exibicao = f"{titulo_fichas_base} - ANO {ano_fichas}"

# CAMPO EDITÁVEL: OBSERVAÇÃO DO CARTÃO
obs_card = st.sidebar.text_area(
    "📌 Observação do Cartão", 
    value=dados_atuais.get("obs_card", DADOS_PADRAO["obs_card"]),
    height=90
)

# === DADOS DE CASAIS VIVENCIADOS ===
with st.sidebar.expander("👥 Casais Vivenciados (2024-2027)", expanded=False):
    st.markdown("**Santo Antônio**")
    st_24 = st.number_input("Santo Antônio (2024)", value=dados_atuais.get("st_24", 14), key="st24")
    st_25 = st.number_input("Santo Antônio (2025)", value=dados_atuais.get("st_25", 18), key="st25")
    st_26 = st.number_input("Santo Antônio (2026)", value=dados_atuais.get("st_26", 13), key="st26")
    st_27 = st.number_input("Santo Antônio (2027)", value=dados_atuais.get("st_27", 0), key="st27")

    st.markdown("**S. Francisco e S. Clara**")
    sf_24 = st.number_input("S. Francisco e S. Clara (2024)", value=dados_atuais.get("sf_24", 26), key="sf24")
    sf_25 = st.number_input("S. Francisco e S. Clara (2025)", value=dados_atuais.get("sf_25", 32), key="sf25")
    sf_26 = st.number_input("S. Francisco e S. Clara (2026)", value=dados_atuais.get("sf_26", 22), key="sf26")
    sf_27 = st.number_input("SS. Francisco e S. Clara (2027)", value=dados_atuais.get("sf_27", 0), key="sf27")

    st.markdown("**N. Sra. Fátima**")
    ns_24 = st.number_input("N. Sra. Fátima (2024)", value=dados_atuais.get("ns_24", 22), key="ns24")
    ns_25 = st.number_input("N. Sra. Fátima (2025)", value=dados_atuais.get("ns_25", 15), key="ns25")
    ns_26 = st.number_input("N. Sra. Fátima (2026)", value=dados_atuais.get("ns_26", 15), key="ns26")
    ns_27 = st.number_input("N. Sra. Fátima (2027)", value=dados_atuais.get("ns_27", 0), key="ns27")

    st.markdown("**São Pedro Apóstolo**")
    sp_24 = st.number_input("São Pedro Apóstolo (2024)", value=dados_atuais.get("sp_24", 0), key="sp24")
    sp_25 = st.number_input("São Pedro Apóstolo (2025)", value=dados_atuais.get("sp_25", 0), key="sp25")
    sp_26 = st.number_input("São Pedro Apóstolo (2026)", value=dados_atuais.get("sp_26", 12), key="sp26")
    sp_27 = st.number_input("São Pedro Apóstolo (2027)", value=dados_atuais.get("sp_27", 0), key="sp27")

    st.markdown("**2ª Etapa**")
    e2_24 = st.number_input("2ª Etapa (2024)", value=dados_atuais.get("e2_24", 21), key="e224")
    e2_25 = st.number_input("2ª Etapa (2025)", value=dados_atuais.get("e2_25", 30), key="e225")
    e2_26 = st.number_input("2ª Etapa (2026)", value=dados_atuais.get("e2_26", 25), key="e226")
    e2_27 = st.number_input("2ª Etapa (2027)", value=dados_atuais.get("e2_27", 0), key="e227")

# === DADOS DE CÍRCULOS DE ESTUDO ===
with st.sidebar.expander("📚 Círculos de Estudo (2024-2027)", expanded=False):
    st.markdown("**Santo Antônio**")
    c_st_24 = st.number_input("Círculos St. Antônio (2024)", value=dados_atuais.get("c_st_24", 3), key="c_st24")
    c_st_25 = st.number_input("Círculos St. Antônio (2025)", value=dados_atuais.get("c_st_25", 4), key="c_st25")
    c_st_26 = st.number_input("Círculos St. Antônio (2026)", value=dados_atuais.get("c_st_26", 3), key="c_st26")
    c_st_27 = st.number_input("Círculos St. Antônio (2027)", value=dados_atuais.get("c_st_27", 0), key="c_st27")

    st.markdown("**S. Francisco e S. Clara**")
    c_sf_24 = st.number_input("Círculos S. Francisco e S. Clara (2024)", value=dados_atuais.get("c_sf_24", 5), key="c_sf24")
    c_sf_25 = st.number_input("Círculos S. Francisco e S. Clara (2025)", value=dados_atuais.get("c_sf_25", 5), key="c_sf25")
    c_sf_26 = st.number_input("Círculos S. Francisco e S. Clara (2026)", value=dados_atuais.get("c_sf_26", 4), key="c_sf26")
    c_sf_27 = st.number_input("Círculos S. Francisco e S. Clara (2027)", value=dados_atuais.get("c_sf_27", 0), key="c_sf27")

    st.markdown("**N. Sra. Fátima**")
    c_ns_24 = st.number_input("Círculos N. Sra. Fátima (2024)", value=dados_atuais.get("c_ns_24", 4), key="c_ns24")
    c_ns_25 = st.number_input("Círculos N. Sra. Fátima (2025)", value=dados_atuais.get("c_ns_25", 3), key="c_ns25")
    c_ns_26 = st.number_input("Círculos N. Sra. Fátima (2026)", value=dados_atuais.get("c_ns_26", 4), key="c_ns26")
    c_ns_27 = st.number_input("Círculos N. Sra. Fátima (2027)", value=dados_atuais.get("c_ns_27", 0), key="c_ns27")

    st.markdown("**São Pedro Apóstolo**")
    c_sp_24 = st.number_input("Círculos S. Pedro (2024)", value=dados_atuais.get("c_sp_24", 0), key="c_sp24")
    c_sp_25 = st.number_input("Círculos S. Pedro (2025)", value=dados_atuais.get("c_sp_25", 0), key="c_sp25")
    c_sp_26 = st.number_input("Círculos S. Pedro (2026)", value=dados_atuais.get("c_sp_26", 3), key="c_sp26")
    c_sp_27 = st.number_input("Círculos S. Pedro (2027)", value=dados_atuais.get("c_sp_27", 0), key="c_sp27")

    st.markdown("**2ª Etapa**")
    c_e2_24 = st.number_input("Círculos 2ª Etapa (2024)", value=dados_atuais.get("c_e2_24", 4), key="c_e224")
    c_e2_25 = st.number_input("Círculos 2ª Etapa (2025)", value=dados_atuais.get("c_e2_25", 5), key="c_e225")
    c_e2_26 = st.number_input("Círculos 2ª Etapa (2026)", value=dados_atuais.get("c_e2_26", 5), key="c_e226")
    c_e2_27 = st.number_input("Círculos 2ª Etapa (2027)", value=dados_atuais.get("c_e2_27", 0), key="c_e227")

# === CONTROLE DE SITUAÇÃO ATUAL ===
with st.sidebar.expander("🚦 Status / Situação Atual", expanded=False):
    opcoes_status = ["Concluído", "Em andamento", "Parado"]
    
    def get_idx_status(key_name, default_val):
        val = dados_atuais.get(key_name, default_val)
        return opcoes_status.index(val) if val in opcoes_status else 0

    st_status_e2 = st.selectbox("2ª Etapa", opcoes_status, index=get_idx_status("st_status_e2", "Concluído"))
    st_status_st = st.selectbox("1ª Etapa – St. Antônio", opcoes_status, index=get_idx_status("st_status_st", "Concluído"))
    st_status_ns = st.selectbox("1ª Etapa – N. Sra. Fátima", opcoes_status, index=get_idx_status("st_status_ns", "Concluído"))
    st_status_sp = st.selectbox("1ª Etapa – São Pedro Apóstolo", opcoes_status, index=get_idx_status("st_status_sp", "Concluído"))
    st_status_sf = st.selectbox("1ª Etapa – S. Francisco e S. Clara", opcoes_status, index=get_idx_status("st_status_sf", "Em andamento"))

# PERSISTE TODOS OS DADOS EDITADOS
dados_para_salvar = {
    "texto_aconteceu": texto_aconteceu,
    "ano_fichas": ano_fichas,
    "titulo_fichas_base": titulo_fichas_base,
    "fichas_st": fichas_st, "fichas_sf": fichas_sf, "fichas_ns": fichas_ns, "fichas_sp": fichas_sp, "fichas_e2": fichas_e2,
    "obs_card": obs_card,
    "st_24": st_24, "st_25": st_25, "st_26": st_26, "st_27": st_27,
    "sf_24": sf_24, "sf_25": sf_25, "sf_26": sf_26, "sf_27": sf_27,
    "ns_24": ns_24, "ns_25": ns_25, "ns_26": ns_26, "ns_27": ns_27,
    "sp_24": sp_24, "sp_25": sp_25, "sp_26": sp_26, "sp_27": sp_27,
    "e2_24": e2_24, "e2_25": e2_25, "e2_26": e2_26, "e2_27": e2_27,
    "c_st_24": c_st_24, "c_st_25": c_st_25, "c_st_26": c_st_26, "c_st_27": c_st_27,
    "c_sf_24": c_sf_24, "c_sf_25": c_sf_25, "c_sf_26": c_sf_26, "c_sf_27": c_sf_27,
    "c_ns_24": c_ns_24, "c_ns_25": c_ns_25, "c_ns_26": c_ns_26, "c_ns_27": c_ns_27,
    "c_sp_24": c_sp_24, "c_sp_25": c_sp_25, "c_sp_26": c_sp_26, "c_sp_27": c_sp_27,
    "c_e2_24": c_e2_24, "c_e2_25": c_e2_25, "c_e2_26": c_e2_26, "c_e2_27": c_e2_27,
    "st_status_e2": st_status_e2, "st_status_st": st_status_st, "st_status_ns": st_status_ns,
    "st_status_sp": st_status_sp, "st_status_sf": st_status_sf
}
salvar_dados(dados_para_salvar)

def get_status_badge(status):
    if status == "Concluído":
        return f'<span style="color:#2e7d32; font-weight:bold;">🟢 Concluído</span>'
    elif status == "Em andamento":
        return f'<span style="color:#e65100; font-weight:bold;">🟠 Em andamento</span>'
    else:
        return f'<span style="color:#c62828; font-weight:bold;">🔴 Parado</span>'

# TOTAIS
tot_24 = st_24 + sf_24 + ns_24 + sp_24 + e2_24
tot_25 = st_25 + sf_25 + ns_25 + sp_25 + e2_25
tot_26 = st_26 + sf_26 + ns_26 + sp_26 + e2_26
tot_27 = st_27 + sf_27 + ns_27 + sp_27 + e2_27

tot_c_24 = c_st_24 + c_sf_24 + c_ns_24 + c_sp_24 + c_e2_24
tot_c_25 = c_st_25 + c_sf_25 + c_ns_25 + c_sp_25 + c_e2_25
tot_c_26 = c_st_26 + c_sf_26 + c_ns_26 + c_sp_26 + c_e2_26
tot_c_27 = c_st_27 + c_sf_27 + c_ns_27 + c_sp_27 + c_e2_27

# DADOS PARÓQUIAS
paroquias_dados = [
    ("Santo Antônio", st_24, st_25, st_26, st_27),
    ("S. Francisco e S. Clara", sf_24, sf_25, sf_26, sf_27),
    ("Nossa Senhora de Fátima", ns_24, ns_25, ns_26, ns_27),
    ("São Pedro Apóstolo", sp_24, sp_25, sp_26, sp_27),
    ("2ª Etapa", e2_24, e2_25, e2_26, e2_27),
]

# === CÁLCULO DINÂMICO DE AUMENTOS, QUEDAS E ESTABILIDADE (2025 -> 2026) ===
aumentos_26 = []
quedas_26 = []
estaveis_26 = []

for nome, v24, v25, v26, v27 in paroquias_dados:
    dif, dif_str, pct_str, _, _ = calc_var(v26, v25)
    if dif > 0:
        aumentos_26.append(f"• <b>{nome}:</b> {v25} ➔ {v26} ({dif_str} casais | {pct_str})")
    elif dif < 0:
        quedas_26.append(f"• <b>{nome}:</b> {v25} ➔ {v26} ({dif_str} casais | {pct_str})")
    else:
        estaveis_26.append(f"• <b>{nome}:</b> {v26} casais (sem variação)")

txt_aumento = "<br>".join(aumentos_26) if aumentos_26 else "• Nenhum crescimento individual"
txt_queda = "<br>".join(quedas_26) if quedas_26 else "• Nenhuma queda individual"
txt_estavel = "<br>".join(estaveis_26) if estaveis_26 else ""

def render_row_v(nome, v24, v25, v26, v27):
    _, d25, p25, c25, _ = calc_var(v25, v24)
    _, d26, p26, c26, _ = calc_var(v26, v25)
    _, d27, p27, c27, _ = calc_var(v27, v26) if v27 > 0 else (0, "-", "-", "", 0)
    
    v26_str = v26 if v26 > 0 else "-"
    v27_str = v27 if v27 > 0 else "-"
    
    return f"""
    <tr>
        <td class="td-paroquia">{nome}</td>
        <td>{v24}</td><td>{v25}</td><td>{v26_str}</td><td>{v27_str}</td>
        <td class="{c25}">{d25}</td><td>{p25}</td>
        <td class="{c26}">{d26}</td><td>{p26}</td>
        <td class="{c27}">{d27}</td><td>{p27}</td>
    </tr>
    """

def render_row_c(nome, v24, v25, v26, v27):
    _, d25, p25, c25, _ = calc_var(v25, v24)
    _, d26, p26, c26, _ = calc_var(v26, v25)
    _, d27, p27, c27, _ = calc_var(v27, v26) if v27 > 0 else (0, "-", "-", "", 0)
    
    v26_str = v26 if v26 > 0 else "-"
    v27_str = v27 if v27 > 0 else "-"
    
    return f"""
    <tr>
        <td class="td-paroquia">{nome}</td>
        <td>{v24}</td><td>{v25}</td><td>{v26_str}</td><td>{v27_str}</td>
        <td class="{c25}">{d25}</td><td>{p25}</td>
        <td class="{c26}">{d26}</td><td>{p26}</td>
        <td class="{c27}">{d27}</td><td>{p27}</td>
    </tr>
    """

d_tot_25_num, d_tot_25, p_tot_25, _, _ = calc_var(tot_25, tot_24)
d_tot_26_num, d_tot_26, p_tot_26, _, _ = calc_var(tot_26, tot_25)

def format_fichas_text(texto):
    if "(abaixo)" in texto:
        return texto.replace("(abaixo)", '<span style="color:red; font-weight:bold;">(abaixo)</span>')
    return texto

html_layout = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; }}
    body {{ background: #c8d6e5; padding: 5px; display: flex; flex-direction: column; align-items: center; overflow-x: auto; }}
    
    .btn-export {{
        margin-bottom: 12px;
        background-color: #2e7d32;
        color: white;
        border: none;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        border-radius: 6px;
        cursor: pointer;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }}
    .btn-export:hover {{ background-color: #1b5e20; }}

    .canvas {{
        width: 100%;
        max-width: 1380px;
        min-width: 1200px;
        margin: 0 auto;
        background: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    }}

    .header {{
        background: linear-gradient(90deg, #e65100 0%, #f57c00 100%);
        border-radius: 12px;
        padding: 12px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
        height: 115px;
    }}
    
    .logo-ecc {{
        background: white;
        border-radius: 10px;
        padding: 8px 14px;
        text-align: center;
        color: #002b66;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        min-width: 150px;
    }}
    .logo-ecc .title {{ font-size: 26px; font-weight: 900; letter-spacing: -1px; line-height: 1; }}
    .logo-ecc .sub {{ font-size: 8.5pt; font-weight: 800; margin-top: 3px; line-height: 1.1; }}

    .header-center {{ text-align: center; flex-grow: 1; }}
    .header-center h1 {{ font-size: 30px; font-weight: 900; letter-spacing: 1px; text-shadow: 1px 1px 2px rgba(0,0,0,0.3); margin:0; }}
    .header-center h2 {{ font-size: 17px; font-weight: 700; margin-top: 2px; letter-spacing: 0.5px; }}
    .header-center .sub-tag {{ font-size: 11px; font-weight: bold; background: rgba(0,0,0,0.25); padding: 4px 14px; border-radius: 12px; display: inline-block; margin-top: 5px; }}

    .tables-row {{ display: flex; gap: 10px; margin-top: 12px; width: 100%; }}
    .table-card {{ flex: 1; border: 1.5px solid #b0bec5; border-radius: 8px; overflow: hidden; background: white; }}
    
    .tb-header {{ color: white; padding: 7px 10px; font-size: 14px; font-weight: bold; text-align: center; }}
    .bg-navy {{ background: #002b66; }}
    .bg-darkgreen {{ background: #1b5e20; }}

    table {{ width: 100%; border-collapse: collapse; font-size: 9.5pt; text-align: center; table-layout: auto; }}
    th {{ background: #e8ecef; color: #002b66; border: 1px solid #cfd8dc; padding: 6px 3px; font-size: 8.5pt; font-weight: bold; }}
    td {{ border: 1px solid #e0e0e0; padding: 6px 3px; font-weight: 600; white-space: nowrap; }}
    .td-paroquia {{ text-align: left; padding-left: 8px; color: #222; font-weight: 700; white-space: normal; word-break: break-word; }}
    
    .tr-total {{ background: #d0d9e8; font-weight: bold; font-size: 10pt; }}
    .c-blue {{ color: #002b66; font-weight: bold; }}
    .c-red {{ color: #c62828; font-weight: bold; }}

    .cards-grid-top {{ display: flex; gap: 10px; margin-top: 10px; }}
    .cards-grid-bottom {{ display: flex; gap: 10px; margin-top: 10px; }}

    .card-box {{ border-radius: 8px; padding: 12px; border: 1px solid #b0bec5; font-size: 10pt; position: relative; background: #f8fafc; }}
    .card-title {{ font-weight: bold; font-size: 11pt; color: #002b66; text-align: center; margin-bottom: 8px; }}

    .card-stat {{ flex: 1.1; background: #f0f4f8; text-align: center; }}
    .card-analise {{ flex: 1.4; background: #fffaf5; border-color: #ffcc80; }}
    .card-situacao {{ flex: 1; background: #f0f4f8; }}

    .card-aconteceu {{ flex: 1; background: #fffaf5; border-color: #ffcc80; }}
    .card-fichas {{ flex: 1.2; background: #f0f4f8; }}
    .card-observacao {{ flex: 1; background: #f0f4f8; }}

    .big-number {{ font-size: 16pt; font-weight: 900; color: #002b66; }}
    .status-item {{ display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px dashed #e0e0e0; font-size: 9.5pt; align-items: center; }}

    .footer-phrase {{
        background: linear-gradient(90deg, #001a40 0%, #002b66 50%, #001a40 100%);
        color: white; text-align: center; padding: 10px; border-radius: 6px; font-size: 11pt; font-weight: bold; font-style: italic; margin-top: 10px;
        display: flex; flex-direction: column; align-items: center; gap: 4px;
    }}
    .footer-signature {{
        font-size: 10pt; font-style: normal; font-weight: 600; color: #ffcc80;
    }}
</style>
</head>
<body>

<button class="btn-export" onclick="downloadJPG()">📷 Baixar Dashboard como Imagem (JPG)</button>

<div class="canvas" id="dashboard-area">
    <div class="header">
        <div class="logo-ecc">
            <div class="title">ECC</div>
            <div class="sub">ENCONTRO DE CASAIS<br>COM CRISTO</div>
        </div>
        <div class="header-center">
            <h1>BALANÇO 2024 A 2027</h1>
            <h2>FORANIA SÃO FRANCISCO E SANTA CLARA</h2>
            <div class="sub-tag">✦ ENCONTRO DE CASAIS COM CRISTO – 1ª ETAPA / 2ª ETAPA ✦</div>
        </div>
    </div>

    <div class="tables-row">
        <div class="table-card">
            <div class="tb-header bg-navy">👥 CASAIS VIVENCIADOS</div>
            <table>
                <thead>
                    <tr>
                        <th style="width: 28%;">Paróquia / Etapa</th>
                        <th>2024</th><th>2025</th><th>2026</th><th>2027</th>
                        <th>Dif. 24-25</th><th>% 24-25</th>
                        <th>Dif. 25-26</th><th>% 25-26</th>
                        <th>Dif. 26-27</th><th>% 26-27</th>
                    </tr>
                </thead>
                <tbody>
                    {render_row_v("⛪ Santo Antônio", st_24, st_25, st_26, st_27)}
                    {render_row_v("⛪ S. Francisco e S. Clara", sf_24, sf_25, sf_26, sf_27)}
                    {render_row_v("⛪ Nossa Senhora de Fátima", ns_24, ns_25, ns_26, ns_27)}
                    {render_row_v("⛪ São Pedro Apóstolo", sp_24, sp_25, sp_26, sp_27)}
                    {render_row_v("⛪ 2ª Etapa", e2_24, e2_25, e2_26, e2_27)}
                    {render_row_v("TOTAL", tot_24, tot_25, tot_26, tot_27)}
                </tbody>
            </table>
        </div>

        <div class="table-card">
            <div class="tb-header bg-darkgreen">📚 CÍRCULOS DE ESTUDO</div>
            <table>
                <thead>
                    <tr>
                        <th style="width: 28%;">Paróquia / Etapa</th>
                        <th>2024</th><th>2025</th><th>2026</th><th>2027</th>
                        <th>Dif. 24-25</th><th>% 24-25</th>
                        <th>Dif. 25-26</th><th>% 25-26</th>
                        <th>Dif. 26-27</th><th>% 26-27</th>
                    </tr>
                </thead>
                <tbody>
                    {render_row_c("⛪ Santo Antônio", c_st_24, c_st_25, c_st_26, c_st_27)}
                    {render_row_c("⛪ S. Francisco e S. Clara", c_sf_24, c_sf_25, c_sf_26, c_sf_27)}
                    {render_row_c("⛪ Nossa Senhora de Fátima", c_ns_24, c_ns_25, c_ns_26, c_ns_27)}
                    {render_row_c("⛪ São Pedro Apóstolo", c_sp_24, c_sp_25, c_sp_26, c_sp_27)}
                    {render_row_c("⛪ 2ª Etapa", c_e2_24, c_e2_25, c_e2_26, c_e2_27)}
                    {render_row_c("TOTAL", tot_c_24, tot_c_25, tot_c_26, tot_c_27)}
                </tbody>
            </table>
        </div>
    </div>

    <div class="cards-grid-top">
        <div class="card-box card-stat">
            <div class="card-title">1. TOTAL DE CASAIS VIVENCIADOS</div>
            <div style="display:flex; justify-content:space-around; align-items:center; margin: 8px 0;">
                <div><span style="font-size:9pt; color:#666;">2024</span><br><span class="big-number">{tot_24}</span></div>
                <span style="color:#2e7d32; font-weight:bold; font-size:12pt;">➔</span>
                <div><span style="font-size:9pt; color:#666;">2025</span><br><span class="big-number">{tot_25}</span></div>
                <span style="color:#c62828; font-weight:bold; font-size:12pt;">➔</span>
                <div><span style="font-size:9pt; color:#666;">2026</span><br><span class="big-number">{tot_26}</span></div>
                <span style="color:#002b66; font-weight:bold; font-size:12pt;">➔</span>
                <div><span style="font-size:9pt; color:#666;">2027</span><br><span class="big-number">{tot_27 if tot_27>0 else '-'}</span></div>
            </div>
            <div style="border-top: 1px dashed #ccc; padding-top: 6px; text-align: left; font-size: 9pt;">
                <div class="c-blue">• Variação Global 24➔25: +{d_tot_25_num} casais ({p_tot_25})</div>
                <div class="c-red">• Variação Global 25➔26: {d_tot_26_num} casais ({p_tot_26})</div>
            </div>
        </div>

        <div class="card-box card-analise">
            <div class="card-title" style="color: #e65100;">3. RESUMO DA ANÁLISE DETALHADO (2025 → 2026)</div>
            <div style="line-height: 1.35; font-size: 8.5pt;">
                <div style="color: #1b5e20;"><b>🟢 Crescimento / Aumento:</b><br>{txt_aumento}</div>
                <div style="margin-top: 6px; color: #c62828;"><b>📉 Quedas Registradas:</b><br>{txt_queda}</div>
                {f'<div style="margin-top: 6px; color: #555;"><b>➖ Estabilidade:</b><br>{txt_estavel}</div>' if txt_estavel else ''}
            </div>
        </div>

        <div class="card-box card-situacao">
            <div class="card-title" style="background:#002b66; color:white; margin:-12px -12px 8px -12px; padding:6px; border-radius: 7px 7px 0 0;">
                📋 SITUAÇÃO ATUAL
            </div>
            <div class="status-item"><span><b>2ª Etapa 2026</b></span>{get_status_badge(st_status_e2)}</div>
            <div class="status-item"><span>1ª Etapa – St. Antônio</span>{get_status_badge(st_status_st)}</div>
            <div class="status-item"><span>1ª Etapa – N. Sra. Fátima</span>{get_status_badge(st_status_ns)}</div>
            <div class="status-item"><span>1ª Etapa – São Pedro Apóstolo</span>{get_status_badge(st_status_sp)}</div>
            <div class="status-item"><span>1ª Etapa – S. Francisco e S. Clara</span>{get_status_badge(st_status_sf)}</div>
        </div>
    </div>

    <div class="cards-grid-bottom">
        <div class="card-box card-aconteceu">
            <div class="card-title" style="color: #e65100;">📅 O QUE JÁ ACONTECEU EM 2026</div>
            <p style="text-align: center; font-size: 10pt; line-height: 1.35; white-space: pre-wrap;">{texto_aconteceu}</p>
        </div>

        <div class="card-box card-fichas">
            <div class="card-title">{titulo_fichas_exibicao}</div>
            <div style="font-size: 9.5pt; line-height: 1.45;">
                <div>• <b>Santo Antônio:</b> {format_fichas_text(fichas_st)}</div>
                <div>• <b>São Francisco e S. Clara:</b> {format_fichas_text(fichas_sf)}</div>
                <div>• <b>N. Sra. de Fátima:</b> {format_fichas_text(fichas_ns)}</div>
                <div>• <b>São Pedro Apóstolo:</b> {format_fichas_text(fichas_sp)}</div>
                <div>• <b>2ª Etapa:</b> {format_fichas_text(fichas_e2)}</div>
            </div>
        </div>

        <div class="card-box card-observacao">
            <div class="card-title">📌 OBSERVAÇÕES</div>
            <p style="font-size: 9.5pt; color: #333; white-space: pre-wrap; line-height: 1.35;">{obs_card}</p>
        </div>
    </div>

    <div class="footer-phrase">
        <span>🤍 Cremos na vida, cremos na família e seguimos firmes na missão de evangelizar! 🤍</span>
        <span class="footer-signature">Casal Forâneo: Alexandre e Cíntia</span>
    </div>
</div>

<script>
function downloadJPG() {{
    const element = document.getElementById("dashboard-area");
    html2canvas(element, {{ scale: 2 }}).then(canvas => {{
        let link = document.createElement("a");
        link.download = "Balanco_ECC_Imagem.jpg";
        link.href = canvas.toDataURL("image/jpeg", 0.9);
        link.click();
    }});
}}
</script>

</body>
</html>
"""

# === SEÇÃO DE SALVAR E BAIXAR ARQUIVO ===
st.sidebar.markdown("---")
st.sidebar.subheader("💾 Exportar Dashboard")

timestamp_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
nome_arquivo_novo = f"Balanco_ECC_{timestamp_atual}.html"

caminho_pasta_destino = r"C:\Users\Alexandre\Documents\Eu\DASHBOARD"

if st.sidebar.button("📁 Salvar Direto na Pasta DASHBOARD"):
    try:
        if not os.path.exists(caminho_pasta_destino):
            os.makedirs(caminho_pasta_destino)
            
        caminho_completo = os.path.join(caminho_pasta_destino, nome_arquivo_novo)
        
        with open(caminho_completo, "w", encoding="utf-8") as f:
            f.write(html_layout)
            
        st.sidebar.success(f"✅ Salvo com sucesso!\n\nArquivo: `{nome_arquivo_novo}`")
    except Exception as e:
        st.sidebar.error(f"Erro ao salvar: {e}")

st.sidebar.download_button(
    label="⬇️ Baixar Arquivo (.html)",
    data=html_layout,
    file_name=nome_arquivo_novo,
    mime="text/html"
)

# RENDERIZA O DASHBOARD NA TELA
components.html(html_layout, height=1100, scrolling=True)