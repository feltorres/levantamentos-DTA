import streamlit as st

# Configuração da página
st.set_page_config(page_title="Distâncias SBBH", page_icon="📍")

# Base de dados completa (A-Z) extraída da planilha "Tempo de Voo APP"
AEROPORTOS_MG = {
    "SNLI": {"cidade": "Abaeté", "pista": "1200 x 30", "op_noturna": "Não", "dist_nm": 96.9},
    "SNFE": {"cidade": "Alfenas", "pista": "1600 x 30", "op_noturna": "Sim", "dist_nm": 146.3},
    "SNAR": {"cidade": "Almenara", "pista": "1400 x 30", "op_noturna": "Inoperante", "dist_nm": 289.5},
    "SNUI": {"cidade": "Araçuaí", "pista": "1200 x 30", "op_noturna": "Não", "dist_nm": 210.3},
    "SNAG": {"cidade": "Araguari", "pista": "1500 x 30", "op_noturna": "Não", "dist_nm": 250.7},
    "SBAX": {"cidade": "Araxá", "pista": "1900 x 30", "op_noturna": "Inoperante", "dist_nm": 171.1},
    "SNBG": {"cidade": "Aymorés", "pista": "1200 x 30", "op_noturna": "Não", "dist_nm": 165.8},
    "SBBQ": {"cidade": "Barbacena (MIL)", "pista": "1760 x 30", "op_noturna": "Sim", "dist_nm": 85.7},
    "SNGQ": {"cidade": "Bom Despacho", "pista": "1000 x 18", "op_noturna": "Sim", "dist_nm": 75.2},
    "SNCA": {"cidade": "Campo Belo", "pista": "1420 x 30", "op_noturna": "Não", "dist_nm": 99.9},
    "SICK": {"cidade": "Capelinha", "pista": "1229 x 30", "op_noturna": "Sim. Só decola.", "dist_nm": 153.4},
    "SNCT": {"cidade": "Caratinga", "pista": "1080 x 23", "op_noturna": "Não", "dist_nm": 104.2},
    "SNEW": {"cidade": "Carneirinho", "pista": "1250 x 29", "op_noturna": "Não", "dist_nm": 395.8},
    "SNXB": {"cidade": "Caxambú", "pista": "1500 x 30", "op_noturna": "Sim", "dist_nm": 136.6},
    "SDNA": {"cidade": "Comendador Gomes (PRIV)", "pista": "1300 x 23", "op_noturna": "Não", "dist_nm": 285.3},
    "SNKD": {"cidade": "Conceição do Mato Dentro", "pista": "960 x 23", "op_noturna": "Não", "dist_nm": 57.9},
    "SBCF": {"cidade": "Confins", "pista": "3600 x 45", "op_noturna": "Sim", "dist_nm": 13.7},
    "SNKF": {"cidade": "Conselheiro Lafaiete", "pista": "902 x 24", "op_noturna": "Não", "dist_nm": 53.9},
    "SIWH": {"cidade": "Coromandel", "pista": "1300 x 20", "op_noturna": "Sim", "dist_nm": 203.3},
    "SNQV": {"cidade": "Curvelo", "pista": "1200 x 23", "op_noturna": "Não", "dist_nm": 72.2},
    "SNDT": {"cidade": "Diamantina", "pista": "1700 x 30", "op_noturna": "Sim", "dist_nm": 98.8},
    "SNDV": {"cidade": "Divinópolis", "pista": "1520 x 30", "op_noturna": "Sim", "dist_nm": 55.5},
    "SNXV": {"cidade": "Felixlândia (PRIV)", "pista": "1500 x 30", "op_noturna": "Não", "dist_nm": 92.9},
    "SNFU": {"cidade": "Frutal", "pista": "1320 x 30", "op_noturna": "Sim", "dist_nm": 282.9},
    "SBZM": {"cidade": "Goianá", "pista": "2525 x 45", "op_noturna": "Sim", "dist_nm": 108.9},
    "SBGV": {"cidade": "Governador Valadares", "pista": "1701 x 30", "op_noturna": "Sim", "dist_nm": 125.4},
    "SSVG": {"cidade": "Guapé (PRIV)", "pista": "1200 x 30", "op_noturna": "Não", "dist_nm": 127.0},
    "SNSR": {"cidade": "Guarda-Mor (PRIV)", "pista": "1100 x 25", "op_noturna": "Não", "dist_nm": 220.9},
    "SNGX": {"cidade": "Guaxupé", "pista": "1500 x 30", "op_noturna": "Sim", "dist_nm": 179.6},
    "SSDK": {"cidade": "Igaratinga (PRIV)", "pista": "1300 x 30", "op_noturna": "Sim", "dist_nm": 45.9},
    "SBIP": {"cidade": "Ipatinga", "pista": "2004 x 45", "op_noturna": "Sim", "dist_nm": 85.8},
    
    # --- AEROPORTOS PENDENTES DE CADASTRO DE DISTÂNCIA NA PLANILHA (VALOR ZERO) ---
    "SNZK": {"cidade": "Itacarambi (PRIV)", "pista": "1560 x 24", "op_noturna": "Não", "dist_nm": 0.0},
    "SNYB": {"cidade": "Ituiutaba", "pista": "1782 x 30", "op_noturna": "Não", "dist_nm": 0.0},
    "SNYU": {"cidade": "Iturama", "pista": "1550 x 30", "op_noturna": "Sim", "dist_nm": 0.0},
    "SNLG": {"cidade": "Jaboticatubas (PRIV)", "pista": "1260 x 20", "op_noturna": "Não", "dist_nm": 0.0},
    "SNMK": {"cidade": "Jaíba", "pista": "1531 x 30", "op_noturna": "Não", "dist_nm": 0.0},
    "SNAP": {"cidade": "Janaúba", "pista": "1500 x 30", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNCK": {"cidade": "Januária", "pista": "1000 x 20", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNJI": {"cidade": "Jequitaí (PRIV)", "pista": "1080 x 18", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNJQ": {"cidade": "Jequitinhonha", "pista": "1130 x 23", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNJP": {"cidade": "João Pinheiro", "pista": "1300 x 23", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SBJF": {"cidade": "Juiz de Fora", "pista": "1535 x 30", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNLY": {"cidade": "Lagoa da Prata (PRIV)", "pista": "1000 x 20", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SBLS": {"cidade": "Lagoa Santa (MIL)", "pista": "1840 x 30", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SSOL": {"cidade": "Lavras", "pista": "1500 x 30", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNJM": {"cidade": "Manhuaçu", "pista": "1170 x 30", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SWWM": {"cidade": "Mantena (PRIV)", "pista": "1050 x 18", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SSYF": {"cidade": "Monte Alegre de Minas (PRIV)", "pista": "1200 x 24", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SBMK": {"cidade": "Montes Claros", "pista": "2100 x 45", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNBM": {"cidade": "Muriaé", "pista": "1140 x 23", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNNU": {"cidade": "Nanuque", "pista": "1220 x 23", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNTD": {"cidade": "Natalândia (PRIV)", "pista": "1350 x 23", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SSYD": {"cidade": "Nova Ponte (PRIV)", "pista": "1500 x 45", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNRZ": {"cidade": "Oliveira", "pista": "1180 x 18", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNOF": {"cidade": "Ouro Fino", "pista": "1050 x 23", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNPA": {"cidade": "Pará de Minas", "pista": "1260 x 23", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNZR": {"cidade": "Paracatu", "pista": "1500 x 30", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SWZT": {"cidade": "Paraopeba (PRIV)", "pista": "1240 x 23", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNOS": {"cidade": "Passos", "pista": "1500 x 30", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNPD": {"cidade": "Patos de Minas", "pista": "1700 x 30", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNPJ": {"cidade": "Patrocínio", "pista": "1200 x 30", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNPX": {"cidade": "Pirapora", "pista": "1480 x 30", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNUH": {"cidade": "Piumhi", "pista": "1148 x 30", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SBPC": {"cidade": "Poços de Caldas", "pista": "1515 x 30", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNCZ": {"cidade": "Ponte Nova", "pista": "1060 x 30", "op_noturna": "Não", "dist_nm": 0.0},
    "SNZA": {"cidade": "Pouso Alegre", "pista": "1280 x 30", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNSS": {"cidade": "Salinas", "pista": "1480 x 30", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SIEX": {"cidade": "Santa Vitória (PRIV)", "pista": "1106 x 18", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNJV": {"cidade": "São João da Ponte (PRIV)", "pista": "1600 x 18", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNJR": {"cidade": "São João Del Rei", "pista": "1400 x 30", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNLO": {"cidade": "São Lourenço", "pista": "1300 x 30", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNPY": {"cidade": "São Sebastião do Paraíso", "pista": "1600 x 30", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SDJR": {"cidade": "Sete Lagoas", "pista": "1500 x 23", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNTO": {"cidade": "Teófilo Otoni", "pista": "1190 x 23", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNVI": {"cidade": "Três Corações", "pista": "1300 x 23", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNAS": {"cidade": "Três Marias", "pista": "1500 x 45", "op_noturna": "Não", "dist_nm": 0.0},
    "SNFI": {"cidade": "Tupaciguara (PRIV)", "pista": "1500 x 26", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNUB": {"cidade": "Ubá", "pista": "1402 x 30", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SBUR": {"cidade": "Uberaba", "pista": "1759 x 45", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SBUL": {"cidade": "Uberlândia", "pista": "2100 x 45", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SBVG": {"cidade": "Varginha", "pista": "2100 x 30", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SSAT": {"cidade": "Vazante (PRIV)", "pista": "1500 x 22", "op_noturna": "Verificar", "dist_nm": 0.0},
    "SNVC": {"cidade": "Viçosa", "pista": "1105 x 30", "op_noturna": "Verificar", "dist_nm": 0.0},
}

# Ordena os aeroportos por ordem alfabética da cidade para facilitar a busca no menu
AEROPORTOS_ORDENADOS = dict(sorted(AEROPORTOS_MG.items(), key=lambda item: item[1]['cidade']))

st.title("📍 Consulta de Aeroportos - MG")
st.write("Consulte rapidamente a distância em milhas náuticas (NM) a partir da Pampulha (SBBH).")

with st.container():
    # Caixa de seleção com busca pelo Nome da Cidade e Indicativo
    indicativo_selecionado = st.selectbox(
        "Selecione ou digite o Destino:", 
        options=list(AEROPORTOS_ORDENADOS.keys()),
        format_func=lambda x: f"{AEROPORTOS_ORDENADOS[x]['cidade']} ({x})"
    )

if st.button("Consultar Destino", type="primary"):
    dados = AEROPORTOS_ORDENADOS[indicativo_selecionado]
    
    # Tratamento visual da Operação Noturna
    op_noturna = dados.get('op_noturna', 'Verificar')
    if "Sim" in op_noturna:
        icone_noturno = f"✅ {op_noturna}"
    elif "Não" in op_noturna or "Inoperante" in op_noturna:
        icone_noturno = f"⚠️ {op_noturna}"
    else:
        icone_noturno = f"❓ {op_noturna}"
        
    # Tratamento visual da Distância (Para avisar se ainda for 0.0)
    if dados["dist_nm"] > 0:
        dist_display = f"**{dados['dist_nm']} NM**"
    else:
        dist_display = "⚠️ *Pendente de cadastro (Preencher no código)*"

    st.success("✅ Consulta realizada com sucesso!")
    
    st.markdown(f"""
    ### 🛫 Origem: Belo Horizonte (SBBH) ➡️ Destino: {dados['cidade']} ({indicativo_selecionado})
    
    | Informação Operacional | Dados |
    | :--- | :--- |
    | **Distância** | {dist_display} |
    | **Dimensões da Pista** | 📏 {dados['pista']} |
    | **Operação Noturna** | 🌙 {icone_noturno} |
    """)
