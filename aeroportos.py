import streamlit as st
import urllib.request
import csv
import math

# Configuração da página
st.set_page_config(page_title="Distâncias SBBH", page_icon="📍")

# Base de dados original (Distâncias da planilha mantidas como "Plano B" caso a pista falhe na busca online)
AEROPORTOS_MG = {
    "SNLI": {"cidade": "Abaeté", "pista": "1200 x 30", "op_noturna": "Não", "dist_planilha": 96.9},
    "SNFE": {"cidade": "Alfenas", "pista": "1600 x 30", "op_noturna": "Sim", "dist_planilha": 146.3},
    "SNAR": {"cidade": "Almenara", "pista": "1400 x 30", "op_noturna": "Inoperante", "dist_planilha": 289.5},
    "SNUI": {"cidade": "Araçuaí", "pista": "1200 x 30", "op_noturna": "Não", "dist_planilha": 210.3},
    "SNAG": {"cidade": "Araguari", "pista": "1500 x 30", "op_noturna": "Não", "dist_planilha": 250.7},
    "SBAX": {"cidade": "Araxá", "pista": "1900 x 30", "op_noturna": "Inoperante", "dist_planilha": 171.1},
    "SNBG": {"cidade": "Aymorés", "pista": "1200 x 30", "op_noturna": "Não", "dist_planilha": 165.8},
    "SBBQ": {"cidade": "Barbacena (MIL)", "pista": "1760 x 30", "op_noturna": "Sim", "dist_planilha": 85.7},
    "SNGQ": {"cidade": "Bom Despacho", "pista": "1000 x 18", "op_noturna": "Sim", "dist_planilha": 75.2},
    "SNCA": {"cidade": "Campo Belo", "pista": "1420 x 30", "op_noturna": "Não", "dist_planilha": 99.9},
    "SICK": {"cidade": "Capelinha", "pista": "1229 x 30", "op_noturna": "Sim. Só decola.", "dist_planilha": 153.4},
    "SNCT": {"cidade": "Caratinga", "pista": "1080 x 23", "op_noturna": "Não", "dist_planilha": 104.2},
    "SNEW": {"cidade": "Carneirinho", "pista": "1250 x 29", "op_noturna": "Não", "dist_planilha": 395.8},
    "SNXB": {"cidade": "Caxambú", "pista": "1500 x 30", "op_noturna": "Sim", "dist_planilha": 136.6},
    "SDNA": {"cidade": "Comendador Gomes (PRIV)", "pista": "1300 x 23", "op_noturna": "Não", "dist_planilha": 285.3},
    "SNKD": {"cidade": "Conceição do Mato Dentro", "pista": "960 x 23", "op_noturna": "Não", "dist_planilha": 57.9},
    "SBCF": {"cidade": "Confins", "pista": "3600 x 45", "op_noturna": "Sim", "dist_planilha": 13.7},
    "SNKF": {"cidade": "Conselheiro Lafaiete", "pista": "902 x 24", "op_noturna": "Não", "dist_planilha": 53.9},
    "SIWH": {"cidade": "Coromandel", "pista": "1300 x 20", "op_noturna": "Sim", "dist_planilha": 203.3},
    "SNQV": {"cidade": "Curvelo", "pista": "1200 x 23", "op_noturna": "Não", "dist_planilha": 72.2},
    "SNDT": {"cidade": "Diamantina", "pista": "1700 x 30", "op_noturna": "Sim", "dist_planilha": 98.8},
    "SNDV": {"cidade": "Divinópolis", "pista": "1520 x 30", "op_noturna": "Sim", "dist_planilha": 55.5},
    "SNXV": {"cidade": "Felixlândia (PRIV)", "pista": "1500 x 30", "op_noturna": "Não", "dist_planilha": 92.9},
    "SNFU": {"cidade": "Frutal", "pista": "1320 x 30", "op_noturna": "Sim", "dist_planilha": 282.9},
    "SBZM": {"cidade": "Goianá", "pista": "2525 x 45", "op_noturna": "Sim", "dist_planilha": 108.9},
    "SBGV": {"cidade": "Governador Valadares", "pista": "1701 x 30", "op_noturna": "Sim", "dist_planilha": 125.4},
    "SSVG": {"cidade": "Guapé (PRIV)", "pista": "1200 x 30", "op_noturna": "Não", "dist_planilha": 127.0},
    "SNSR": {"cidade": "Guarda-Mor (PRIV)", "pista": "1100 x 25", "op_noturna": "Não", "dist_planilha": 220.9},
    "SNGX": {"cidade": "Guaxupé", "pista": "1500 x 30", "op_noturna": "Sim", "dist_planilha": 179.6},
    "SSDK": {"cidade": "Igaratinga (PRIV)", "pista": "1300 x 30", "op_noturna": "Sim", "dist_planilha": 45.9},
    "SBIP": {"cidade": "Ipatinga", "pista": "2004 x 45", "op_noturna": "Sim", "dist_planilha": 85.8},
    "SNZK": {"cidade": "Itacarambi", "pista": "1560 x 24", "op_noturna": "Não", "dist_planilha": 315},
    "SNYB": {"cidade": "Ituiutaba", "pista": "1782 x 30", "op_noturna": "Não", "dist_planilha": 295},
    "SNYU": {"cidade": "Iturama", "pista": "1550 x 30", "op_noturna": "Sim", "dist_planilha": 365},
    "SNLG": {"cidade": "Jaboticatubas (PRIV)", "pista": "1260 x 20", "op_noturna": "Não", "dist_planilha": 28.5},
    "SNMK": {"cidade": "Jaíba", "pista": "1531 x 30", "op_noturna": "Não", "dist_planilha": 285},
    "SNAP": {"cidade": "Janaúba", "pista": "1500 x 30", "op_noturna": "Não", "dist_planilha": 270},
    "SNJN": {"cidade": "Januária", "pista": "NÃO HOMOLOGADO", "op_noturna": "Não", "dist_planilha": 280},
    "SNJI": {"cidade": "Jequitaí (PRIV)", "pista": "1080 x 18", "op_noturna": "Não", "dist_planilha": 190},
    "SNJQ": {"cidade": "Jequitinhonha", "pista": "1130 x 23", "op_noturna": "Não", "dist_planilha": 245},
    "SNJP": {"cidade": "João Pinheiro", "pista": "1300 x 23", "op_noturna": "Não", "dist_planilha": 210},
    "SBJF": {"cidade": "Juiz de Fora", "pista": "1535 x 30", "op_noturna": "Sim", "dist_planilha": 102.5},
    "SNLY": {"cidade": "Lagoa da Prata (PRIV)", "pista": "1000 x 20", "op_noturna": "Não", "dist_planilha": 92},
    "SBLS": {"cidade": "Lagoa Santa (MIL)", "pista": "1840 x 30", "op_noturna": "Sim", "dist_planilha": 11.5},
    "SSOL": {"cidade": "Lavras", "pista": "1500 x 30", "op_noturna": "Sim", "dist_planilha": 118},
    "SNJM": {"cidade": "Manhuaçu", "pista": "1170 x 30", "op_noturna": "Não", "dist_planilha": 128},
    "SWWM": {"cidade": "Mantena (PRIV)", "pista": "1050 x 18", "op_noturna": "Não", "dist_planilha": 160},
    "SSYF": {"cidade": "Monte Alegre de Minas (PRIV)", "pista": "1200 x 24", "op_noturna": "Não", "dist_planilha": 290},
    "SBMK": {"cidade": "Montes Claros", "pista": "2100 x 45", "op_noturna": "Sim", "dist_planilha": 212},
    "SNBM": {"cidade": "Muriaé", "pista": "1140 x 23", "op_noturna": "Não", "dist_planilha": 138},
    "SNNU": {"cidade": "Nanuque", "pista": "1220 x 23", "op_noturna": "Sim", "dist_planilha": 258},
    "SNTD": {"cidade": "Natalândia (PRIV)", "pista": "1350 x 23", "op_noturna": "Não", "dist_planilha": 230},
    "SSYD": {"cidade": "Nova Ponte (PRIV)", "pista": "1500 x 45", "op_noturna": "Não", "dist_planilha": 218},
    "SNRZ": {"cidade": "Oliveira", "pista": "1180 x 18", "op_noturna": "Não", "dist_planilha": 71.5},
    "SNOF": {"cidade": "Ouro Fino", "pista": "1050 x 23", "op_noturna": "Não", "dist_planilha": 152},
    "SNPA": {"cidade": "Pará de Minas", "pista": "1260 x 23", "op_noturna": "Não", "dist_planilha": 38},
    "SNZR": {"cidade": "Paracatu", "pista": "1500 x 30", "op_noturna": "Sim", "dist_planilha": 270},
    "SWZT": {"cidade": "Paraopeba (PRIV)", "pista": "1240 x 23", "op_noturna": "Não", "dist_planilha": 52},
    "SNOS": {"cidade": "Passos", "pista": "1500 x 30", "op_noturna": "Sim", "dist_planilha": 148},
    "SNPD": {"cidade": "Patos de Minas", "pista": "1700 x 30", "op_noturna": "Sim", "dist_planilha": 190},
    "SNPJ": {"cidade": "Patrocínio", "pista": "1200 x 30", "op_noturna": "Não", "dist_planilha": 180},
    "SNPX": {"cidade": "Pirapora", "pista": "1480 x 30", "op_noturna": "Sim", "dist_planilha": 152},
    "SNUH": {"cidade": "Piumhi", "pista": "1148 x 30", "op_noturna": "Não", "dist_planilha": 110},
    "SBPC": {"cidade": "Poços de Caldas", "pista": "1515 x 30", "op_noturna": "Sim", "dist_planilha": 182},
    "SNCZ": {"cidade": "Ponte Nova", "pista": "1060 x 30", "op_noturna": "Não", "dist_planilha": 82},
    "SNZA": {"cidade": "Pouso Alegre", "pista": "1280 x 30", "op_noturna": "Sim", "dist_planilha": 160},
    "SNSS": {"cidade": "Salinas", "pista": "1480 x 30", "op_noturna": "Sim", "dist_planilha": 248},
    "SIEX": {"cidade": "Santa Vitória (PRIV)", "pista": "1106 x 18", "op_noturna": "Não", "dist_planilha": 360},
    "SNJV": {"cidade": "São João da Ponte (PRIV)", "pista": "1600 x 18", "op_noturna": "Não", "dist_planilha": 240},
    "SNJR": {"cidade": "São João Del Rei", "pista": "1400 x 30", "op_noturna": "Sim", "dist_planilha": 98},
    "SNLO": {"cidade": "São Lourenço", "pista": "1300 x 30", "op_noturna": "Não", "dist_planilha": 148},
    "SNPY": {"cidade": "São Sebastião do Paraíso", "pista": "1600 x 30", "op_noturna": "Sim", "dist_planilha": 188},
    "SDJR": {"cidade": "Sete Lagoas", "pista": "1500 x 23", "op_noturna": "Sim", "dist_planilha": 28},
    "SNTO": {"cidade": "Teófilo Otoni", "pista": "1190 x 23", "op_noturna": "Sim", "dist_planilha": 188},
    "SNVI": {"cidade": "Três Corações", "pista": "1300 x 23", "op_noturna": "Sim", "dist_planilha": 121},
    "SNAS": {"cidade": "Três Marias", "pista": "1500 x 45", "op_noturna": "Não", "dist_planilha": 115},
    "SNFI": {"cidade": "Tupaciguara (PRIV)", "pista": "1500 x 26", "op_noturna": "Não", "dist_planilha": 280},
    "SNUB": {"cidade": "Ubá", "pista": "1402 x 30", "op_noturna": "Sim", "dist_planilha": 102},
    "SBUR": {"cidade": "Uberaba", "pista": "1759 x 45", "op_noturna": "Sim", "dist_planilha": 228},
    "SBUL": {"cidade": "Uberlândia", "pista": "2100 x 45", "op_noturna": "Sim", "dist_planilha": 248},
    "SBVG": {"cidade": "Varginha", "pista": "2100 x 30", "op_noturna": "Sim", "dist_planilha": 130},
    "SSAT": {"cidade": "Vazante (PRIV)", "pista": "1500 x 22", "op_noturna": "Sim", "dist_planilha": 232},
    "SNVC": {"cidade": "Viçosa", "pista": "1105 x 30", "op_noturna": "Sim", "dist_planilha": 86.5},
}

AEROPORTOS_ORDENADOS = dict(sorted(AEROPORTOS_MG.items(), key=lambda item: item[1]['cidade']))

# --- MOTOR DE CÁLCULO VIA COORDENADAS ---

def calcular_distancia_nm(lat1, lon1, lat2, lon2):
    R = 3440.065  # Raio da Terra em Milhas Náuticas
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return round(R * c, 1)

# O @st.cache_data garante que o download só ocorra 1 vez a cada 24 horas (86400 segundos)
@st.cache_data(ttl=86400, show_spinner=False)
def baixar_e_calcular_distancias():
    url = "https://davidmegginson.github.io/ourairports-data/airports.csv"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            linhas = [linha.decode('utf-8') for linha in response.readlines()]
        
        leitor = csv.DictReader(linhas)
        coords = {}
        
        # Filtra apenas SBBH e as pistas da nossa lista para economizar processamento
        for linha in leitor:
            ident = linha['ident']
            if ident == 'SBBH' or ident in AEROPORTOS_MG.keys():
                coords[ident] = {
                    'lat': float(linha['latitude_deg']),
                    'lon': float(linha['longitude_deg'])
                }
        
        sbbh = coords.get('SBBH')
        if not sbbh: return {}

        # Calcula a distância matemática
        distancias = {}
        for icao in AEROPORTOS_MG.keys():
            destino = coords.get(icao)
            if destino:
                distancias[icao] = calcular_distancia_nm(sbbh['lat'], sbbh['lon'], destino['lat'], destino['lon'])
        return distancias
        
    except Exception:
        return {} # Retorna vazio caso falhe a internet

# --- INTERFACE DE USUÁRIO ---

st.title("📍 Consulta de Aeroportos - MG")
st.write("Consulte rapidamente a distância em milhas náuticas (NM) a partir da Pampulha (SBBH).")

with st.container():
    indicativo_selecionado = st.selectbox(
        "Selecione ou digite o Destino:", 
        options=list(AEROPORTOS_ORDENADOS.keys()),
        format_func=lambda x: f"{AEROPORTOS_ORDENADOS[x]['cidade']} ({x})"
    )

if st.button("Consultar Destino", type="primary"):
    # O spinner aparece rapidinho se for a primeira vez no dia baixando o arquivo
    with st.spinner("Mapeando coordenadas e calculando rota direta..."):
        distancias_calculadas = baixar_e_calcular_distancias()
        
    dados = AEROPORTOS_ORDENADOS[indicativo_selecionado]
    
    # Tratamento Visual: Operação Noturna
    op_noturna = dados.get('op_noturna', 'Verificar')
    if "Sim" in op_noturna:
        icone_noturno = f"✅ {op_noturna}"
    elif "Não" in op_noturna or "Inoperante" in op_noturna:
        icone_noturno = f"⚠️ {op_noturna}"
    else:
        icone_noturno = f"❓ {op_noturna}"

    # Tratamento Visual: Exibição da Distância (GPS vs Planilha)
    dist_gps = distancias_calculadas.get(indicativo_selecionado)
    
    if dist_gps:
        dist_display = f"**{dist_gps} NM** 🛰️ *(Cálculo exato via Coordenadas)*"
    else:
        dist_display = f"**{dados['dist_planilha']} NM** 📋 *(Estimativa da Planilha)*"

    st.success("✅ Rota estabelecida!")
    
    st.markdown(f"""
    ### 🛫 Origem: Pampulha (SBBH) ➡️ Destino: {dados['cidade']} ({indicativo_selecionado})
    
    | Informação Operacional | Dados |
    | :--- | :--- |
    | **Distância em Linha Reta** | {dist_display} |
    | **Dimensões da Pista** | 📏 {dados['pista']} |
    | **Operação Noturna** | 🌙 {icone_noturno} |
    """)
