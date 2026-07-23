import streamlit as st

# Configuração da página
st.set_page_config(page_title="Distâncias SBBH", page_icon="📍")

# Base de dados extraída da sua planilha "Tempo de Voo APP" (Amostra principal)
# A base já contém a distância em Milhas Náuticas (NM) a partir da Pampulha (SBBH)
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
}

# Ordena os aeroportos por ordem alfabética da cidade para facilitar a busca
AEROPORTOS_ORDENADOS = dict(sorted(AEROPORTOS_MG.items(), key=lambda item: item[1]['cidade']))

st.title("📍 Consulta de Aeroportos - MG")
st.write("Consulte rapidamente a distância em relação à Pampulha (SBBH) e dados da pista.")

with st.container():
    # A caixa de seleção agora permite buscar pelo NOME DA CIDADE e mostra o INDICATIVO
    indicativo_selecionado = st.selectbox(
        "Selecione ou digite o Destino:", 
        options=list(AEROPORTOS_ORDENADOS.keys()),
        format_func=lambda x: f"{AEROPORTOS_ORDENADOS[x]['cidade']} ({x})"
    )

if st.button("Consultar Destino", type="primary"):
    dados = AEROPORTOS_ORDENADOS[indicativo_selecionado]
    
    # Conversão de Milhas Náuticas para Quilômetros (1 NM = 1.852 km)
    dist_km = dados["dist_nm"] * 1.852
    
    # Formatação visual do alerta de operação noturna
    icone_noturno = "✅ " + dados['op_noturna'] if "Sim" in dados['op_noturna'] else "⚠️ " + dados['op_noturna']

    st.success("✅ Consulta realizada com sucesso!")
    
    st.markdown(f"""
    ### 🛫 Origem: Belo Horizonte (SBBH) ➡️ Destino: {dados['cidade']} ({indicativo_selecionado})
    
    | Informação Operacional | Dados |
    | :--- | :--- |
    | **Distância (Milhas Náuticas)** | **{dados['dist_nm']:.1f} NM** |
    | **Distância (Quilômetros)** | {dist_km:.1f} Km |
    | **Dimensões da Pista** | 📏 {dados['pista']} |
    | **Operação Noturna** | 🌙 {icone_noturno} |
    """)
    
    st.info("💡 Dica: Você pode usar o valor em Milhas Náuticas (NM) na Calculadora de Custos para estimar a missão.")
