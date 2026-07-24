import streamlit as st
import urllib.request
import csv
import math

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Planejador de Missões - DTA", page_icon="🚁", layout="wide")

# --- BASE DE DADOS: AEROPORTOS ---
AEROPORTOS = {
    "SBBH": {"cidade": "Belo Horizonte", "pista": "2364 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SBCF": {"cidade": "Confins", "pista": "3600 x 45", "op_noturna": "Sim", "uf": "MG"},
    "SNLI": {"cidade": "Abaeté", "pista": "1200 x 30", "op_noturna": "Não", "uf": "MG", "restricao_anac": True},
    "SNFE": {"cidade": "Alfenas", "pista": "1600 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNAR": {"cidade": "Almenara", "pista": "1400 x 30", "op_noturna": "Inoperante", "uf": "MG"},
    "SNUI": {"cidade": "Araçuaí", "pista": "1200 x 30", "op_noturna": "Não", "uf": "MG"},
    "SNAG": {"cidade": "Araguari", "pista": "1500 x 30", "op_noturna": "Não", "uf": "MG", "restricao_anac": True},
    "SBAX": {"cidade": "Araxá", "pista": "1900 x 30", "op_noturna": "Inoperante", "uf": "MG"},
    "SNBG": {"cidade": "Aymorés", "pista": "1200 x 30", "op_noturna": "Não", "uf": "MG", "restricao_anac": True},
    "SBBQ": {"cidade": "Barbacena", "pista": "1760 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNGQ": {"cidade": "Bom Despacho", "pista": "1000 x 18", "op_noturna": "Sim", "uf": "MG"},
    "SNCA": {"cidade": "Campo Belo", "pista": "1420 x 30", "op_noturna": "Não", "uf": "MG"},
    "SICK": {"cidade": "Capelinha", "pista": "1229 x 30", "op_noturna": "Sim. Só decola.", "uf": "MG"},
    "SNCT": {"cidade": "Caratinga", "pista": "1080 x 23", "op_noturna": "Não", "uf": "MG"},
    "SNEW": {"cidade": "Carneirinho", "pista": "1250 x 29", "op_noturna": "Não", "uf": "MG"},
    "SNXB": {"cidade": "Caxambú", "pista": "1500 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SDNA": {"cidade": "Comendador Gomes", "pista": "1300 x 23", "op_noturna": "Não", "uf": "MG"},
    "SNKD": {"cidade": "Conceição do Mato Dentro", "pista": "960 x 23", "op_noturna": "Não", "uf": "MG"},
    "SNKF": {"cidade": "Conselheiro Lafaiete", "pista": "902 x 24", "op_noturna": "Não", "uf": "MG", "restricao_anac": True},
    "SIWH": {"cidade": "Coromandel", "pista": "1300 x 20", "op_noturna": "Sim", "uf": "MG"},
    "SNQV": {"cidade": "Curvelo", "pista": "1200 x 23", "op_noturna": "Não", "uf": "MG"},
    "SNDT": {"cidade": "Diamantina", "pista": "1700 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNDV": {"cidade": "Divinópolis", "pista": "1520 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNXV": {"cidade": "Felixlândia", "pista": "1500 x 30", "op_noturna": "Não", "uf": "MG"},
    "SNFU": {"cidade": "Frutal", "pista": "1320 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SBZM": {"cidade": "Goianá", "pista": "2525 x 45", "op_noturna": "Sim", "uf": "MG"},
    "SBGV": {"cidade": "Governador Valadares", "pista": "1701 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SSVG": {"cidade": "Guapé", "pista": "1200 x 30", "op_noturna": "Não", "uf": "MG"},
    "SNSR": {"cidade": "Guarda-Mor", "pista": "1100 x 25", "op_noturna": "Não", "uf": "MG"},
    "SNGX": {"cidade": "Guaxupé", "pista": "1500 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SSDK": {"cidade": "Igaratinga", "pista": "1300 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SBIP": {"cidade": "Ipatinga", "pista": "2004 x 45", "op_noturna": "Sim", "uf": "MG"},
    "SNZK": {"cidade": "Itacarambi", "pista": "1560 x 24", "op_noturna": "Não", "uf": "MG"},
    "SNYB": {"cidade": "Ituiutaba", "pista": "1782 x 30", "op_noturna": "Não", "uf": "MG"},
    "SNYU": {"cidade": "Iturama", "pista": "1550 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNLG": {"cidade": "Jaboticatubas", "pista": "1260 x 20", "op_noturna": "Não", "uf": "MG"},
    "SNMK": {"cidade": "Jaíba", "pista": "1531 x 30", "op_noturna": "Não", "uf": "MG"},
    "SNAP": {"cidade": "Janaúba", "pista": "1500 x 30", "op_noturna": "Não", "uf": "MG"},
    "SNJN": {"cidade": "Januária", "pista": "NÃO HOMOLOGADO", "op_noturna": "Não", "uf": "MG", "restricao_anac": True},
    "SNJI": {"cidade": "Jequitaí", "pista": "1080 x 18", "op_noturna": "Não", "uf": "MG"},
    "SNJQ": {"cidade": "Jequitinhonha", "pista": "1130 x 23", "op_noturna": "Não", "uf": "MG"},
    "SNJP": {"cidade": "João Pinheiro", "pista": "1300 x 23", "op_noturna": "Não", "uf": "MG"},
    "SBJF": {"cidade": "Juiz de Fora", "pista": "1535 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNLY": {"cidade": "Lagoa da Prata", "pista": "1000 x 20", "op_noturna": "Não", "uf": "MG"},
    "SBLS": {"cidade": "Lagoa Santa", "pista": "1840 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SSOL": {"cidade": "Lavras", "pista": "1500 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNJM": {"cidade": "Manhuaçu", "pista": "1170 x 30", "op_noturna": "Não", "uf": "MG"},
    "SWWM": {"cidade": "Mantena", "pista": "1050 x 18", "op_noturna": "Não", "uf": "MG"},
    "SSYF": {"cidade": "Monte Alegre de Minas", "pista": "1200 x 24", "op_noturna": "Não", "uf": "MG"},
    "SBMK": {"cidade": "Montes Claros", "pista": "2100 x 45", "op_noturna": "Sim", "uf": "MG"},
    "SNBM": {"cidade": "Muriaé", "pista": "1140 x 23", "op_noturna": "Não", "uf": "MG"},
    "SNNU": {"cidade": "Nanuque", "pista": "1220 x 23", "op_noturna": "Sim", "uf": "MG"},
    "SNTD": {"cidade": "Natalândia", "pista": "1350 x 23", "op_noturna": "Não", "uf": "MG"},
    "SSYD": {"cidade": "Nova Ponte", "pista": "1500 x 45", "op_noturna": "Não", "uf": "MG"},
    "SNRZ": {"cidade": "Oliveira", "pista": "1180 x 18", "op_noturna": "Não", "uf": "MG"},
    "SNOF": {"cidade": "Ouro Fino", "pista": "1050 x 23", "op_noturna": "Não", "uf": "MG"},
    "SNPA": {"cidade": "Pará de Minas", "pista": "1260 x 23", "op_noturna": "Não", "uf": "MG"},
    "SNZR": {"cidade": "Paracatu", "pista": "1500 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SWZT": {"cidade": "Paraopeba", "pista": "1240 x 23", "op_noturna": "Não", "uf": "MG"},
    "SNOS": {"cidade": "Passos", "pista": "1500 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNPD": {"cidade": "Patos de Minas", "pista": "1700 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNPJ": {"cidade": "Patrocínio", "pista": "1200 x 30", "op_noturna": "Não", "uf": "MG"},
    "SNPX": {"cidade": "Pirapora", "pista": "1480 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNUH": {"cidade": "Piumhi", "pista": "1148 x 30", "op_noturna": "Não", "uf": "MG"},
    "SBPC": {"cidade": "Poços de Caldas", "pista": "1515 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNCZ": {"cidade": "Ponte Nova", "pista": "1060 x 30", "op_noturna": "Não", "uf": "MG"},
    "SNZA": {"cidade": "Pouso Alegre", "pista": "1280 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNSS": {"cidade": "Salinas", "pista": "1480 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SIEX": {"cidade": "Santa Vitória", "pista": "1106 x 18", "op_noturna": "Não", "uf": "MG"},
    "SNJV": {"cidade": "São João da Ponte", "pista": "1600 x 18", "op_noturna": "Não", "uf": "MG"},
    "SNJR": {"cidade": "São João Del Rei", "pista": "1400 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNLO": {"cidade": "São Lourenço", "pista": "1300 x 30", "op_noturna": "Não", "uf": "MG"},
    "SNPY": {"cidade": "São Sebastião do Paraíso", "pista": "1600 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SDJR": {"cidade": "Sete Lagoas", "pista": "1500 x 23", "op_noturna": "Sim", "uf": "MG"},
    "SNTO": {"cidade": "Teófilo Otoni", "pista": "1190 x 23", "op_noturna": "Sim", "uf": "MG"},
    "SNVI": {"cidade": "Três Corações", "pista": "1300 x 23", "op_noturna": "Sim", "uf": "MG"},
    "SNAS": {"cidade": "Três Marias", "pista": "1500 x 45", "op_noturna": "Não", "uf": "MG"},
    "SNFI": {"cidade": "Tupaciguara", "pista": "1500 x 26", "op_noturna": "Não", "uf": "MG"},
    "SNUB": {"cidade": "Ubá", "pista": "1402 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SBUR": {"cidade": "Uberaba", "pista": "1759 x 45", "op_noturna": "Sim", "uf": "MG"},
    "SBUL": {"cidade": "Uberlândia", "pista": "2100 x 45", "op_noturna": "Sim", "uf": "MG"},
    "SBVG": {"cidade": "Varginha", "pista": "2100 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SSAT": {"cidade": "Vazante", "pista": "1500 x 22", "op_noturna": "Sim", "uf": "MG"},
    "SNVC": {"cidade": "Viçosa", "pista": "1105 x 30", "op_noturna": "Sim", "uf": "MG"},
}
AEROPORTOS_ORDENADOS = dict(sorted(AEROPORTOS.items(), key=lambda item: item[1]['cidade']))

# --- BASE DE DADOS: FROTA ---
FROTA = {
    "Citation Bravo": {"vel_kt": 290, "valor_hora": 18266.14, "pax": "07 Pax", "requer_pista_1200": True, "tipo_sigla": "JATO"},
    "King Air B350 (PR-XAA)": {"vel_kt": 220, "valor_hora": 12318.67, "pax": "Até 09 Pax C/ bagagem", "tipo_sigla": "KING"},
    "King Air B300 (PP-EJO)": {"vel_kt": 220, "valor_hora": 9705.13, "pax": "7 Pax c/ Bagagem\n9 Pax s/ Bagagem", "tipo_sigla": "KING"},
    "King Air B200 (PTWGS)": {
        "vel_kt": 200,             
        "vel_kt_t2": 225,          
        "valor_hora": 9705.13, 
        "pax": "7 Pax c/ Bagagem\n9 Pax s/ Bagagem", 
        "regra_tabela_dupla": True,
        "tipo_sigla": "KING"
    },
    "King Air C90 (PR/PT-OSO)": {"vel_kt": 200, "valor_hora": 6323.05, "pax": "06 Pax", "tipo_sigla": "KING"},
    "Dauphin N3 (PR-DTG)": {"vel_kt": 110, "valor_hora": 26135.07, "pax": "06 Pax", "tipo_sigla": "DAUPHIN"},
    "Dauphin N2 (PP-EPO)": {"vel_kt": 110, "valor_hora": 26135.07, "pax": "05 Pax", "tipo_sigla": "DAUPHIN"},
    "Esquilo AS350": {"vel_kt": 100, "valor_hora": 9788.57, "pax": "04 Pax", "tipo_sigla": "ESQUILO"},
}

# --- MOTOR DE CÁLCULO GPS ---
def calcular_distancia_nm(lat1, lon1, lat2, lon2):
    R = 3440.065 
    dLat, dLon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2)**2
    return round(R * (2 * math.asin(math.sqrt(a))), 1)

@st.cache_data(ttl=86400, show_spinner=False)
def buscar_coordenadas():
    # Fallback offline para pistas que não constam no banco de dados global (OurAirports)
    coords_backup = {
        "SNGQ": {'lat': -19.7411, 'lon': -45.2447}, # Bom Despacho
        "SIWH": {'lat': -18.4752, 'lon': -47.1916}, # Coromandel
        "SDNA": {'lat': -19.7616, 'lon': -49.0763}, # Comendador Gomes
        "SNXV": {'lat': -18.7613, 'lon': -44.8988}, # Felixlândia
        "SSVG": {'lat': -20.7672, 'lon': -45.9186}, # Guapé
        "SNSR": {'lat': -17.7802, 'lon': -47.0988}, # Guarda-Mor
        "SSDK": {'lat': -19.9547, 'lon': -44.6069}, # Igaratinga
        "SNLY": {'lat': -20.0219, 'lon': -45.5458}, # Lagoa da Prata
        "SWWM": {'lat': -18.0647, 'lon': -40.9788}, # Mantena
        "SSYF": {'lat': -18.8711, 'lon': -48.8805}, # Monte Alegre de Minas
        "SNTD": {'lat': -16.4858, 'lon': -46.5413}, # Natalândia
        "SSYD": {'lat': -19.1416, 'lon': -47.6780}, # Nova Ponte
        "SWZT": {'lat': -19.2736, 'lon': -44.4041}, # Paraopeba
        "SIEX": {'lat': -18.8419, 'lon': -50.1219}, # Santa Vitória
        "SNJV": {'lat': -15.9344, 'lon': -44.0105}, # São João da Ponte
        "SNFI": {'lat': -18.5908, 'lon': -48.7052}, # Tupaciguara
        "SSAT": {'lat': -17.9869, 'lon': -46.9058}, # Vazante
        "SNJN": {'lat': -15.4677, 'lon': -44.3644}, # Januária
        "SNBG": {'lat': -19.4672, 'lon': -41.0119}, # Aymorés
        "SNAR": {'lat': -16.1683, 'lon': -40.6694}, # Almenara
        "SNKD": {'lat': -19.0436, 'lon': -43.4350}, # Conceição do Mato Dentro
        "SNJI": {'lat': -17.2288, 'lon': -44.4372}, # Jequitaí
        "SICK": {'lat': -17.6694, 'lon': -42.5488}, # Capelinha
        "SNLG": {'lat': -19.5161, 'lon': -43.7436}, # Jaboticatubas
        "SNEW": {'lat': -19.6894, 'lon': -50.6866}, # Carneirinho
    }
    
    url = "https://davidmegginson.github.io/ourairports-data/airports.csv"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            linhas = [linha.decode('utf-8') for linha in response.readlines()]
        leitor = csv.DictReader(linhas)
        for linha in leitor:
            if linha['ident'] in AEROPORTOS:
                # Atualiza o dicionário de backup com as coordenadas oficiais, se existirem
                coords_backup[linha['ident']] = {'lat': float(linha['latitude_deg']), 'lon': float(linha['longitude_deg'])}
        return coords_backup
    except Exception:
        # Em caso de falha de conexão, retorna o fallback como proteção
        return coords_backup

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

def verifica_restricao_pista(icao, aeronave_nome):
    if icao not in AEROPORTOS: return False, ""
    dados = AEROPORTOS[icao]
    
    if dados.get("restricao_anac"):
        return True, f"AEROPORTO INOPERANTE POR DETERMINAÇÃO DA ANAC ({icao})"
        
    aero_dados = FROTA[aeronave_nome]
    if aero_dados.get("requer_pista_1200"):
        pista_str = dados.get('pista', '')
        try:
            comprimento = int(pista_str.split('x')[0].strip())
            if comprimento < 1200:
                return True, f"AERONAVE ({aeronave_nome}) NÃO PODE OPERAR NESTA PISTA ({icao} - {comprimento}m)"
        except ValueError:
            return True, f"AERONAVE ({aeronave_nome}) NÃO PODE OPERAR NESTA PISTA ({icao} - Não Homologada)"
            
    return False, ""

# --- CONTROLE DE ESTADO (MÚLTIPLAS PERNAS) ---
if 'trechos' not in st.session_state:
    st.session_state.trechos = [{"origem": "SBBH", "destino": "SBCF", "aeronave": list(FROTA.keys())[0]}]

def adicionar_trecho():
    ultimo_trecho = st.session_state.trechos[-1]
    st.session_state.trechos.append({
        "origem": ultimo_trecho["destino"], 
        "destino": "SBBH", 
        "aeronave": ultimo_trecho["aeronave"]
    })

def remover_trecho():
    if len(st.session_state.trechos) > 1:
        st.session_state.trechos.pop()

# --- INTERFACE ---
st.title("🚁 Planejador de Missões Aéreas - DTA")
st.write("Roteirizador Dinâmico Point-to-Point com Especificação de Aeronave por Perna")

st.divider()
st.subheader("📍 Rota da Missão")

opcoes_aeroportos = list(AEROPORTOS_ORDENADOS.keys())
formatador = lambda x: f"{AEROPORTOS_ORDENADOS[x]['cidade']} ({x})"

# Interface de Seleção Compactada (sem textos extras ou traços)
for i in range(len(st.session_state.trechos)):
    col1, col2, col3 = st.columns([3, 3, 4])
    with col1:
        st.session_state.trechos[i]["origem"] = st.selectbox(
            f"{i+1}. Origem", 
            options=opcoes_aeroportos, 
            index=opcoes_aeroportos.index(st.session_state.trechos[i]["origem"]),
            format_func=formatador,
            key=f"origem_{i}"
        )
    with col2:
        st.session_state.trechos[i]["destino"] = st.selectbox(
            f"{i+1}. Destino", 
            options=opcoes_aeroportos, 
            index=opcoes_aeroportos.index(st.session_state.trechos[i]["destino"]),
            format_func=formatador,
            key=f"destino_{i}"
        )
    with col3:
        st.session_state.trechos[i]["aeronave"] = st.selectbox(
            f"{i+1}. Aeronave (Equipamento)", 
            options=list(FROTA.keys()), 
            index=list(FROTA.keys()).index(st.session_state.trechos[i]["aeronave"]),
            key=f"aeronave_{i}"
        )

# Botões de Adicionar/Remover
st.write("") # Pequeno respiro visual
col_add, col_rem, _ = st.columns([2, 2, 8])
col_add.button("➕ Adicionar Trecho", on_click=adicionar_trecho)
if len(st.session_state.trechos) > 1:
    col_rem.button("➖ Remover Trecho", on_click=remover_trecho)

st.divider()

if st.button("Calcular Missão Completa", type="primary", use_container_width=True):
    coords = buscar_coordenadas()
    
    linhas_tabela = []
    custo_total_missao = 0
    erros_restricao = []
    
    for i, trecho in enumerate(st.session_state.trechos):
        origem = trecho["origem"]
        destino = trecho["destino"]
        aeronave_escolhida = trecho["aeronave"]
        dados_aero = FROTA[aeronave_escolhida]
        
        # 1. Validação de Restrições
        restricao_origem, erro_origem = verifica_restricao_pista(origem, aeronave_escolhida)
        restricao_destino, erro_destino = verifica_restricao_pista(destino, aeronave_escolhida)
        
        if restricao_origem: erros_restricao.append(f"Trecho {i+1}: {erro_origem}")
        if restricao_destino: erros_restricao.append(f"Trecho {i+1}: {erro_destino}")
        
        # 2. Cálculo da Distância Ortodrômica
        if origem in coords and destino in coords:
            dist_nm = calcular_distancia_nm(coords[origem]['lat'], coords[origem]['lon'], coords[destino]['lat'], coords[destino]['lon'])
        else:
            dist_nm = 0 
            erros_restricao.append(f"Trecho {i+1}: Falha ao localizar coordenadas no banco global ({origem} ou {destino}).")
            
        # 3. Regra de Tabelas
        vel_kt = dados_aero['vel_kt']
        if dados_aero.get("regra_tabela_dupla"):
            tempo_base = dist_nm / vel_kt if vel_kt > 0 else 0
            if tempo_base >= 1.0:
                vel_kt = dados_aero['vel_kt_t2']

        # 4. Custos e Tempo
        tempo_decimal = dist_nm / vel_kt if vel_kt > 0 else 0
        custo_perna = tempo_decimal * dados_aero['valor_hora']
        custo_total_missao += custo_perna
        
        # Estrutura para o HTML
        linhas_tabela.append({
            "mun_orig": AEROPORTOS[origem]['cidade'],
            "uf_orig": AEROPORTOS[origem]['uf'],
            "ind_orig": origem,
            "mun_dest": AEROPORTOS[destino]['cidade'],
            "uf_dest": AEROPORTOS[destino]['uf'],
            "ind_dest": destino,
            "anv": dados_aero['tipo_sigla'],
            "tempo": decimal_para_hhmmss(tempo_decimal),
            "custo": custo_perna,
            "pax": dados_aero['pax']
        })

    # Renderização
    if erros_restricao:
        for erro in erros_restricao:
            st.error(f"🚨 {erro}")
    else:
        # GERADOR HTML SEGURO (Compacto numa só variável para não quebrar no Streamlit)
        html_linhas = ""
        for linha in linhas_tabela:
            custo_formatado = f"R$ {linha['custo']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            pax_formatado = str(linha['pax']).replace('\n', '<br>')
            html_linhas += (
                "<tr style='background-color: #ffffff; color: #000000; text-align: center;'>"
                f"<td style='padding: 8px; border: 1px solid #000000;'>{linha['mun_orig']}</td>"
                f"<td style='padding: 8px; border: 1px solid #000000;'>{linha['uf_orig']}</td>"
                f"<td style='padding: 8px; border: 1px solid #000000;'>{linha['ind_orig']}</td>"
                f"<td style='padding: 8px; border: 1px solid #000000;'>{linha['mun_dest']}</td>"
                f"<td style='padding: 8px; border: 1px solid #000000;'>{linha['uf_dest']}</td>"
                f"<td style='padding: 8px; border: 1px solid #000000;'>{linha['ind_dest']}</td>"
                f"<td style='padding: 8px; border: 1px solid #000000; font-weight: bold; background-color: #f9f9f9;'>{linha['anv']}</td>"
                f"<td style='padding: 8px; border: 1px solid #000000;'>{linha['tempo']}</td>"
                f"<td style='padding: 8px; border: 1px solid #000000;'>{custo_formatado}</td>"
                f"<td style='padding: 8px; border: 1px solid #000000;'>{pax_formatado}</td>"
                "</tr>"
            )
            
        custo_final_formatado = f"R$ {custo_total_missao:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        # ESTRUTURA COMPLETA DA TABELA
        tabela_html = (
            "<div id='tabela-missao-container' style='overflow-x: auto;'>"
            "<table id='tabela-missao' style='width:100%; text-align:center; border-collapse: collapse; font-family: sans-serif; border: 2px solid #000000;'>"
            "<thead>"
            "<tr style='background-color: #9bc2e6; color: #000000; border: 1px solid #000000;'>"
            "<th colspan='3' style='padding: 8px; border: 1px solid #000000;'>ORIGEM</th>"
            "<th colspan='3' style='padding: 8px; border: 1px solid #000000;'>DESTINO</th>"
            "<th colspan='4' style='padding: 8px; border: 1px solid #000000;'>AERONAVE / FROTA MULTIPERNA</th>"
            "</tr>"
            "<tr style='background-color: #ddebf7; color: #000000; font-size: 13px;'>"
            "<th style='padding: 8px; border: 1px solid #000000;'>MUNICÍPIO - DECOLAGEM</th>"
            "<th style='padding: 8px; border: 1px solid #000000;'>UF</th>"
            "<th style='padding: 8px; border: 1px solid #000000;'>ICAO</th>"
            "<th style='padding: 8px; border: 1px solid #000000;'>MUNICÍPIO - POUSO</th>"
            "<th style='padding: 8px; border: 1px solid #000000;'>UF</th>"
            "<th style='padding: 8px; border: 1px solid #000000;'>ICAO</th>"
            "<th style='padding: 8px; border: 1px solid #000000;'>ANV</th>"
            "<th style='padding: 8px; border: 1px solid #000000;'>TEMPO DE<br>DESLOCAMENTO</th>"
            "<th style='padding: 8px; border: 1px solid #000000;'>CUSTO TOTAL<br>ESTIMADO DA MISSÃO</th>"
            "<th style='padding: 8px; border: 1px solid #000000;'>CAPACIDADE</th>"
            "</tr>"
            "</thead>"
            "<tbody>"
            f"{html_linhas}"
            "<tr style='background-color: #f2f2f2; color: #000000; font-weight: bold;'>"
            "<td colspan='8' style='padding: 10px; text-align: right; border: 1px solid #000000;'>TOTAL</td>"
            f"<td colspan='2' style='padding: 10px; text-align: left; border: 1px solid #000000;'>{custo_final_formatado}</td>"
            "</tr>"
            "</tbody>"
            "</table>"
            "</div>"
        )
        
        st.success("✅ Rotas calculadas e validadas com sucesso.")
        
        # BOTÃO ÍCONE DE CÓPIA DIRETA COM JAVASCRIPT
        botao_copia_html = """
        <div style="text-align: right; margin-bottom: 5px;">
            <button onclick="
                var range = document.createRange();
                range.selectNode(document.getElementById('tabela-missao'));
                window.getSelection().removeAllRanges();
                window.getSelection().addRange(range);
                document.execCommand('copy');
                window.getSelection().removeAllRanges();
                alert('Tabela copiada com sucesso! Pronta para colar no Excel.');
            " title="Copiar Tabela" style="background: transparent; border: none; font-size: 32px; cursor: pointer;">
                📋
            </button>
        </div>
        """
        
        st.markdown(botao_copia_html, unsafe_allow_html=True)
        st.markdown(tabela_html, unsafe_allow_html=True)
