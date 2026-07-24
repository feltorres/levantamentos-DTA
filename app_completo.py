import streamlit as st
import urllib.request
import csv
import math

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Planejador de Missões - DTA", page_icon="🚁", layout="wide")

# --- BASE DE DADOS: AEROPORTOS (Plano B / Backup Offline) ---
AEROPORTOS_MG = {
    "SNLI": {"cidade": "Abaeté", "pista": "1200 x 30", "op_noturna": "Não", "dist_planilha": 96.9, "restricao_anac": True},
    "SNFE": {"cidade": "Alfenas", "pista": "1600 x 30", "op_noturna": "Sim", "dist_planilha": 146.3},
    "SNAR": {"cidade": "Almenara", "pista": "1400 x 30", "op_noturna": "Inoperante", "dist_planilha": 289.5},
    "SNUI": {"cidade": "Araçuaí", "pista": "1200 x 30", "op_noturna": "Não", "dist_planilha": 210.3},
    "SNAG": {"cidade": "Araguari", "pista": "1500 x 30", "op_noturna": "Não", "dist_planilha": 250.7, "restricao_anac": True},
    "SBAX": {"cidade": "Araxá", "pista": "1900 x 30", "op_noturna": "Inoperante", "dist_planilha": 171.1},
    "SNBG": {"cidade": "Aymorés", "pista": "1200 x 30", "op_noturna": "Não", "dist_planilha": 165.8, "restricao_anac": True},
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
    "SNKF": {"cidade": "Conselheiro Lafaiete", "pista": "902 x 24", "op_noturna": "Não", "dist_planilha": 53.9, "restricao_anac": True},
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
    "SNJN": {"cidade": "Januária", "pista": "NÃO HOMOLOGADO", "op_noturna": "Não", "dist_planilha": 280, "restricao_anac": True},
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

# --- BASE DE DADOS: FROTA ---
FROTA = {
    "Citation Bravo (PP-LCE)": {"vel_kt": 290, "valor_hora": 18266.14, "pax": "07 Pax"},
    "King Air B350 (PR-XAA)": {"vel_kt": 220, "valor_hora": 12318.67, "pax": "Até 09 Pax C/ bagagem"},
    "King Air B300 (PP-EJO)": {"vel_kt": 220, "valor_hora": 9705.13, "pax": "7 Pax c/ Bagagem\n9 Pax s/ Bagagem"},
    "King Air B200 (PTWGS)": {
        "vel_kt": 200,             
        "vel_kt_t2": 225,          
        "valor_hora": 9705.13, 
        "pax": "7 Pax c/ Bagagem\n9 Pax s/ Bagagem", 
        "regra_tabela_dupla": True 
    },
    "King Air C90 (PR/PT-OSO)": {"vel_kt": 200, "valor_hora": 6323.05, "pax": "06 Pax"},
    "Dauphin N3 (PR-DTG)": {"vel_kt": 110, "valor_hora": 26135.07, "pax": "06 Pax"},
    "Dauphin N2 (PP-EPO)": {"vel_kt": 110, "valor_hora": 26135.07, "pax": "05 Pax"},
    "Esquilo AS350": {"vel_kt": 100, "valor_hora": 9788.57, "pax": "04 Pax"},
}

# --- MOTOR DE CÁLCULO DE DISTÂNCIA GPS ---
def calcular_distancia_nm(lat1, lon1, lat2, lon2):
    R = 3440.065 
    dLat, dLon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2)**2
    return round(R * (2 * math.asin(math.sqrt(a))), 1)

@st.cache_data(ttl=86400, show_spinner=False)
def buscar_coordenadas_e_distancias():
    url = "https://davidmegginson.github.io/ourairports-data/airports.csv"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            linhas = [linha.decode('utf-8') for linha in response.readlines()]
        
        leitor = csv.DictReader(linhas)
        coords = {linha['ident']: {'lat': float(linha['latitude_deg']), 'lon': float(linha['longitude_deg'])} 
                  for linha in leitor if linha['ident'] == 'SBBH' or linha['ident'] in AEROPORTOS_MG}
        
        if 'SBBH' not in coords: return {}
        sbbh = coords['SBBH']
        return {icao: calcular_distancia_nm(sbbh['lat'], sbbh['lon'], c['lat'], c['lon']) for icao, c in coords.items()}
    except Exception:
        return {}

# --- FUNÇÃO AUXILIAR DE TEMPO EM FORMATO HH:MM:SS ---
def decimal_para_hhmmss(tempo_decimal):
    horas = int(tempo_decimal)
    minutos_dec = (tempo_decimal - horas) * 60
    minutos = int(minutos_dec)
    segundos = round((minutos_dec - minutos) * 60)
    
    if segundos == 60:
        segundos = 0
        minutos += 1
    if minutos == 60:
        minutos = 0
        horas += 1
        
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


# --- INTERFACE DE USUÁRIO ---
st.title("🚁 Planejador de Missões Aéreas - DTA")
st.write("Integração Automática: Cálculo Geográfico de Distância + Custos Operacionais de Frota")

# --- SELETOR DE MODO DE CONSULTA ---
modo_consulta = st.radio(
    "Escolha o método de inserção da distância:",
    ("Selecionar Aeroporto na Lista (GPS)", "Digitar Distância Manualmente (NM)"),
    horizontal=True
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Rota")
    
    if modo_consulta == "Selecionar Aeroporto na Lista (GPS)":
        indicativo_selecionado = st.selectbox(
            "Selecione o Destino (Origem: SBBH):", 
            options=list(AEROPORTOS_ORDENADOS.keys()),
            format_func=lambda x: f"{AEROPORTOS_ORDENADOS[x]['cidade']} ({x})"
        )
        distancia_manual = None
    else:
        distancia_manual = st.number_input("Insira a Distância do Trecho em Milhas Náuticas (NM):", min_value=1, value=100, step=1)
        indicativo_selecionado = None

with col2:
    st.subheader("✈️ Aeronave")
    aeronave_selecionada = st.selectbox("Selecione o Equipamento:", options=list(FROTA.keys()))
    dados_aeronave = FROTA[aeronave_selecionada]

if st.button("Calcular Missão Completa", type="primary", use_container_width=True):
    
    # --- DEFINIÇÃO DA DISTÂNCIA BASEADA NO MODO ESCOLHIDO ---
    if modo_consulta == "Selecionar Aeroporto na Lista (GPS)":
        with st.spinner("Buscando coordenadas satelitais..."):
            distancias_gps = buscar_coordenadas_e_distancias()
            
        dados_aeroporto = AEROPORTOS_ORDENADOS[indicativo_selecionado]
        distancia = distancias_gps.get(indicativo_selecionado, dados_aeroporto['dist_planilha'])
        fonte_dist = "Satélite/GPS" if indicativo_selecionado in distancias_gps else "Planilha Histórica"
    else:
        distancia = float(distancia_manual) 
        fonte_dist = "Inserção Manual"

    # --- LÓGICA DE VELOCIDADE & REGRA DE TABELAS ---
    vel_kt = dados_aeronave['vel_kt']
    aviso_tabela = ""

    if dados_aeronave.get("regra_tabela_dupla"):
        tempo_estimado_base = distancia / vel_kt
        if tempo_estimado_base >= 1.0:
            vel_kt = dados_aeronave['vel_kt_t2']
            aviso_tabela = f"*(Tabela 2: ≥ 1h)*"
        else:
            aviso_tabela = f"*(Tabela 1: < 1h)*"

    # --- CÁLCULOS MATEMÁTICOS FINAIS ---
    tempo_decimal_trecho = distancia / vel_kt
    custo_trecho = tempo_decimal_trecho * dados_aeronave['valor_hora']

    tempo_decimal_total = tempo_decimal_trecho * 2
    custo_total = custo_trecho * 2

    # --- EXIBIÇÃO DOS RESULTADOS ---
    st.success("✅ Missão processada com sucesso!")
    
    st.markdown("### 📊 Resumo Operacional")
    info_col1, info_col2, info_col3, info_col4 = st.columns(4)
    
    info_col1.metric("Distância (Trecho)", f"{distancia} NM", f"Fonte: {fonte_dist}", delta_color="off")
    
    if modo_consulta == "Selecionar Aeroporto na Lista (GPS)":
        info_col2.metric("Dimensões da Pista", dados_aeroporto['pista'])
        
        # CHECAGEM DE RESTRIÇÃO DA ANAC
        if dados_aeroporto.get("restricao_anac"):
            info_col3.error("🚨 **AEROPORTO INOPERANTE POR DETERMINAÇÃO DA ANAC**")
        else:
            info_col3.metric("Operação Noturna", "✅ Sim" if "Sim" in dados_aeroporto.get('op_noturna', '') else "⚠️ Não/Inoperante")
            
    else:
        info_col2.metric("Destino", "Não especificado")
        info_col3.metric("Operação Noturna", "Desconhecido")
        
    pax_info = dados_aeronave['pax'].split('\n')
    if len(pax_info) > 1:
        info_col4.metric("Capacidade da Aeronave", pax_info[0], pax_info[1], delta_color="off")
    else:
        info_col4.metric("Capacidade da Aeronave", pax_info[0])
    
    st.divider()

    # --- TRAVA DE SEGURANÇA PARA O JATO (CITATION 550) EM PISTAS < 1200M ---
    restricao_jato_pista_curta = False
    if modo_consulta == "Selecionar Aeroporto na Lista (GPS)" and aeronave_selecionada == "Citation 550 (PP-LCE)":
        pista_info = dados_aeroporto.get('pista', '')
        try:
            # Pega o primeiro valor antes do "x" (ex: pega 960 de "960 x 23")
            comprimento_pista = int(pista_info.split('x')[0].strip())
            if comprimento_pista < 1200:
                restricao_jato_pista_curta = True
        except ValueError:
            # Caso a string seja "NÃO HOMOLOGADO" ou outro formato inesperado
            restricao_jato_pista_curta = True

    # Se a trava do jato for ativada, bloqueia o custo e exibe o alerta. Se não, segue normal.
    if restricao_jato_pista_curta:
        st.error("🚨 **AERONAVE NÃO PODE OPERAR NESTA PISTA**")
    else:
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            titulo_ida = f"🛫 **SOMENTE IDA (SBBH ➔ {indicativo_selecionado})**" if indicativo_selecionado else "🛫 **SOMENTE IDA**"
            st.info(titulo_ida)
            st.write(f"**Velocidade Média Aplicada:** {vel_kt} Kt {aviso_tabela}")
            st.write(f"**Tempo de Voo:** {decimal_para_hhmmss(tempo_decimal_trecho)}")
            st.write(f"**Custo da Hora/Voo:** R$ {custo_trecho:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            
        with res_col2:
            st.success(f"🔄 **MISSÃO COMPLETA (Ida e Volta)**") # Alterado de st.error para st.success (cor verde)
            st.write(f"**Velocidade Média Aplicada:** {vel_kt} Kt {aviso_tabela}")
            st.write(f"**Tempo Total de Voo:** {decimal_para_hhmmss(tempo_decimal_total)}")
            st.write(f"**Custo Total Estimado:** R$ {custo_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
