import streamlit as st

# Configuração da página
st.set_page_config(page_title="Distâncias SBBH", page_icon="📍")

# Base de dados completa (A-Z) extraída da planilha "Tempo de Voo APP"
AEROPORTOS_MG = {
    "SNLI": {"cidade": "Abaeté - MG", "pista": "1200 x 30", "op_noturna": "Não", "dist_nm": 96.9},
    "SNFE": {"cidade": "Alfenas - MG", "pista": "1600 x 30", "op_noturna": "Sim", "dist_nm": 146.3},
    "SNAR": {"cidade": "Almenara - MG", "pista": "1400 x 30", "op_noturna": "Inoperante", "dist_nm": 289.5},
    "SNUI": {"cidade": "Araçuaí - MG", "pista": "1200 x 30", "op_noturna": "Não", "dist_nm": 210.3},
    "SNAG": {"cidade": "Araguari - MG", "pista": "1500 x 30", "op_noturna": "Não", "dist_nm": 250.7},
    "SBAX": {"cidade": "Araxá - MG", "pista": "1900 x 30", "op_noturna": "Inoperante", "dist_nm": 171.1},
    "SNBG": {"cidade": "Aymorés - MG", "pista": "1200 x 30", "op_noturna": "Não", "dist_nm": 165.8},
    "SBBQ (MIL)": {"cidade": "Barbacena - MG", "pista": "1760 x 30", "op_noturna": "Sim", "dist_nm": 85.7},
    "SNGQ": {"cidade": "Bom Despacho - MG", "pista": "1000 x 18", "op_noturna": "Sim", "dist_nm": 75.2},
    "SNCA": {"cidade": "Campo Belo - MG", "pista": "1420 x 30", "op_noturna": "Não", "dist_nm": 99.9},
    "SICK": {"cidade": "Capelinha - MG", "pista": "1229 x 30", "op_noturna": "Sim. Só decola.", "dist_nm": 153.4},
    "SNCT": {"cidade": "Caratinga - MG", "pista": "1080 x 23", "op_noturna": "Não", "dist_nm": 104.2},
    "SNEW": {"cidade": "Carneirinho - MG", "pista": "1250 x 29", "op_noturna": "Não", "dist_nm": 395.8},
    "SNXB": {"cidade": "Caxambú - MG", "pista": "1500 x 30", "op_noturna": "Sim", "dist_nm": 136.6},
    "SDNA (PRIV)": {"cidade": "Comendador Gomes - MG", "pista": "1300 x 23", "op_noturna": "Não", "dist_nm": 285.3},
    "SNKD": {"cidade": "Conceição do Mato Dentro - MG", "pista": "960 x 23", "op_noturna": "Não", "dist_nm": 57.9},
    "SBCF": {"cidade": "Confins - MG", "pista": "3600 x 45", "op_noturna": "Sim", "dist_nm": 13.7},
    "SNKF": {"cidade": "Conselheiro Lafaiete - MG", "pista": "902 x 24", "op_noturna": "Não", "dist_nm": 53.9},
    "SIWH": {"cidade": "Coromandel - MG", "pista": "1300 x 20", "op_noturna": "Sim", "dist_nm": 203.3},
    "SNQV": {"cidade": "Curvelo - MG", "pista": "1200 x 23", "op_noturna": "Não", "dist_nm": 72.2},
    "SNDT": {"cidade": "Diamantina - MG", "pista": "1700 x 30", "op_noturna": "Sim", "dist_nm": 98.8},
    "SNDV": {"cidade": "Divinópolis - MG", "pista": "1520 x 30", "op_noturna": "Sim", "dist_nm": 55.5},
    "SNXV (PRIV)": {"cidade": "Felixlândia - MG", "pista": "1500 x 30", "op_noturna": "Não", "dist_nm": 92.9},
    "SNFU": {"cidade": "Frutal - MG", "pista": "1320 x 30", "op_noturna": "Sim", "dist_nm": 282.9},
    "SBZM": {"cidade": "Goianá - MG", "pista": "2525 x 45", "op_noturna": "Sim", "dist_nm": 108.9},
    "SBGV": {"cidade": "Governador Valadares - MG", "pista": "1701 x 30", "op_noturna": "Sim", "dist_nm": 125.4},
    "SSVG (PRIV)": {"cidade": "Guapé - MG", "pista": "1200 x 30", "op_noturna": "Não", "dist_nm": 127.0},
    "SNSR (PRIV)": {"cidade": "Guarda-Mor - MG", "pista": "1100 x 25", "op_noturna": "Não", "dist_nm": 220.9},
    "SNGX": {"cidade": "Guaxupé - MG", "pista": "1500 x 30", "op_noturna": "Sim", "dist_nm": 179.6},
    "SSDK (PRIV)": {"cidade": "Igaratinga - MG", "pista": "1300 x 30", "op_noturna": "Sim", "dist_nm": 45.9},
    "SBIP": {"cidade": "Ipatinga - MG", "pista": "2004 x 45", "op_noturna": "Sim", "dist_nm": 85.8},
    "SNZK (PRIV)": {"cidade": "Itacarambi - MG", "pista": "1560 x 24", "op_noturna": "Não", "dist_nm": 315},
    "SNYB": {"cidade": "Ituiutaba - MG (Pista Ruim)", "pista": "1782 x 30", "op_noturna": "Não", "dist_nm": 295},
    "SNYU": {"cidade": "Iturama - MG", "pista": "1550 x 30", "op_noturna": "Sim", "dist_nm": 365},
    "SNLG (PRIV)": {"cidade": "Jaboticatubas - MG", "pista": "1260 x 20", "op_noturna": "Não", "dist_nm": 28.5},
    "SNMK": {"cidade": "Jaíba - MG", "pista": "1531 x 30", "op_noturna": "Não", "dist_nm": 285},
    "SNAP": {"cidade": "Janaúba - MG", "pista": "1500 x 30", "op_noturna": "Não", "dist_nm": 270},
    "SNJN": {"cidade": "Januária - MG", "pista": "NÃO HOMOLOGADO", "op_noturna": "Não", "dist_nm": 280},
    "SNJI (PRIV)": {"cidade": "Jequitaí - MG", "pista": "1080 x 18", "op_noturna": "Não", "dist_nm": 190},
    "SNJQ": {"cidade": "Jequitinhonha - MG", "pista": "1130 x 23", "op_noturna": "Não", "dist_nm": 245},
    "SNJP": {"cidade": "João Pinheiro - MG", "pista": "1300 x 23", "op_noturna": "Não", "dist_nm": 210},
    "SBJF": {"cidade": "Juiz de Fora - MG", "pista": "1535 x 30", "op_noturna": "Sim", "dist_nm": 102.5},
    "SNLY (PRIV)": {"cidade": "Lagoa da Prata - MG", "pista": "1000 x 20", "op_noturna": "Não", "dist_nm": 92},
    "SBLS (MIL)": {"cidade": "Lagoa Santa - MG", "pista": "1840 x 30", "op_noturna": "Sim", "dist_nm": 11.5},
    "SSOL": {"cidade": "Lavras - MG", "pista": "1500 x 30", "op_noturna": "Sim", "dist_nm": 118},
    "SNJM": {"cidade": "Manhuaçu - MG", "pista": "1170 x 30", "op_noturna": "Não", "dist_nm": 128},
    "SWWM (PRIV)": {"cidade": "Mantena - MG", "pista": "1050 x 18", "op_noturna": "Não", "dist_nm": 160},
    "SSYF (PRIV)": {"cidade": "Monte Alegre de Minas - ", "pista": "1200 x 24", "op_noturna": "Não", "dist_nm": 290},
    "SBMK": {"cidade": "Montes Claros - MG", "pista": "2100 x 45", "op_noturna": "Sim", "dist_nm": 212},
    "SNBM": {"cidade": "Muriaé - MG", "pista": "1140 x 23", "op_noturna": "Não", "dist_nm": 138},
    "SNNU": {"cidade": "Nanuque - MG", "pista": "1220 x 23", "op_noturna": "Sim", "dist_nm": 258},
    "SNTD (PRIV)": {"cidade": "Natalândia - MG", "pista": "1350 x 23", "op_noturna": "Não", "dist_nm": 230},
    "SSYD (PRIV)": {"cidade": "Nova Ponte - MG", "pista": "1500 x 45", "op_noturna": "Não", "dist_nm": 218},
    "SNRZ": {"cidade": "Oliveira - MG", "pista": "1180 x 18", "op_noturna": "Não", "dist_nm": 71.5},
    "SNOF": {"cidade": "Ouro Fino - MG", "pista": "1050 x 23", "op_noturna": "Não", "dist_nm": 152},
    "SNPA": {"cidade": "Pará de Minas - MG", "pista": "1260 x 23", "op_noturna": "Não", "dist_nm": 38},
    "SNZR": {"cidade": "Paracatu - MG", "pista": "1500 x 30", "op_noturna": "Sim", "dist_nm": 270},
    "SWZT (PRIV)": {"cidade": "Paraopeba - MG", "pista": "1240 x 23", "op_noturna": "Não", "dist_nm": 52},
    "SNOS": {"cidade": "Passos - MG", "pista": "1500 x 30", "op_noturna": "Sim", "dist_nm": 148},
    "SNPD": {"cidade": "Patos de Minas - MG", "pista": "1700 x 30", "op_noturna": "Sim", "dist_nm": 190},
    "SNPJ": {"cidade": "Patrocínio - MG", "pista": "1200 x 30", "op_noturna": "Não", "dist_nm": 180},
    "SNPX": {"cidade": "Pirapora - MG", "pista": "1480 x 30", "op_noturna": "Sim", "dist_nm": 152},
    "SNUH": {"cidade": "Piumhi - MG", "pista": "1148 x 30", "op_noturna": "Não", "dist_nm": 110},
    "SBPC": {"cidade": "Poços de Caldas - MG", "pista": "1515 x 30", "op_noturna": "Sim", "dist_nm": 182},
    "SNCZ": {"cidade": "Ponte Nova - MG", "pista": "1060 x 30", "op_noturna": "Não", "dist_nm": 82},
    "SNZA": {"cidade": "Pouso Alegre - MG", "pista": "1280 x 30", "op_noturna": "Sim", "dist_nm": 160},
    "SNSS": {"cidade": "Salinas - MG", "pista": "1480 x 30", "op_noturna": "Sim", "dist_nm": 248},
    "SIEX (PRIV)": {"cidade": "Santa Vitória - MG", "pista": "1106 x 18", "op_noturna": "Não", "dist_nm": 360},
    "SNJV (PRIV)": {"cidade": "São João da Ponte - MG", "pista": "1600 x 18", "op_noturna": "Não", "dist_nm": 240},
    "SNJR": {"cidade": "São João Del Rei - MG", "pista": "1400 x 30", "op_noturna": "Sim", "dist_nm": 98},
    "SNLO": {"cidade": "São Lourenço - MG", "pista": "1300 x 30", "op_noturna": "Não", "dist_nm": 148},
    "SNPY": {"cidade": "São Sebastião do Paraíso", "pista": "1600 x 30", "op_noturna": "Sim", "dist_nm": 188},
    "SDJR": {"cidade": "Sete Lagoas - MG", "pista": "1500 x 23", "op_noturna": "Sim", "dist_nm": 28},
    "SNTO": {"cidade": "Teófilo Otoni - MG", "pista": "1190 x 23", "op_noturna": "Sim", "dist_nm": 188},
    "SNVI": {"cidade": "Três Corações - MG", "pista": "1300 x 23", "op_noturna": "Sim", "dist_nm": 121},
    "SNAS": {"cidade": "Três Marias - MG", "pista": "1500 x 45", "op_noturna": "Não", "dist_nm": 115},
    "SNFI (PRIV)": {"cidade": "Tupaciguara - MG", "pista": "1500 x 26", "op_noturna": "Não", "dist_nm": 280},
    "SNUB": {"cidade": "Ubá - MG", "pista": "1402 x 30", "op_noturna": "Sim", "dist_nm": 102},
    "SBUR": {"cidade": "Uberaba", "pista": "1759 x 45", "op_noturna": "Sim", "dist_nm": 228},
    "SBUL": {"cidade": "Uberlândia - MG", "pista": "2100 x 45", "op_noturna": "Sim", "dist_nm": 248},
    "SBVG": {"cidade": "Varginha - MG", "pista": "2100 x 30", "op_noturna": "Sim", "dist_nm": 130},
    "SSAT (PRIV)": {"cidade": "Vazante - MG", "pista": "1500 x 22", "op_noturna": "Sim", "dist_nm": 232},
    "SNVC": {"cidade": "Viçosa - MG", "pista": "1105 x 30", "op_noturna": "Sim", "dist_nm": 86.5},
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

    st.success("✅ Consulta realizada com sucesso!")
    
    st.markdown(f"""
    ### 🛫 Origem: Belo Horizonte (SBBH) ➡️ Destino: {dados['cidade']} ({indicativo_selecionado})
    
    | Informação Operacional | Dados |
    | :--- | :--- |
    | **Distância** | **{dados['dist_nm']} NM** |
    | **Dimensões da Pista** | 📏 {dados['pista']} |
    | **Operação Noturna** | 🌙 {icone_noturno} |
    """)
