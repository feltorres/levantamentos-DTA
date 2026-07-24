import requests
from bs4 import BeautifulSoup
import math
import json
import time

# ---------------------------------------------------------
# Função: Buscar coordenadas no SkyVector
# ---------------------------------------------------------

def get_coords_from_skyvector(icao):
    url = f"https://skyvector.com/airport/{icao}"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    coords_tag = soup.find("span", {"id": "coords"})
    if not coords_tag:
        raise ValueError(f"Coordenadas não encontradas para {icao}")

    coords_text = coords_tag.text.strip()

    lat_str = coords_text.split("Lat:")[1].split(",")[0].strip()
    lon_str = coords_text.split("Lon:")[1].strip()

    return float(lat_str), float(lon_str)


# ---------------------------------------------------------
# Função: Distância ortodrômica (NM)
# ---------------------------------------------------------

def haversine_nm(lat1, lon1, lat2, lon2):
    R_km = 6371.0
    R_nm = R_km / 1.852

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    return R_nm * c


# ---------------------------------------------------------
# Coordenadas da origem SBBH
# ---------------------------------------------------------

print("Buscando coordenadas de SBBH...")
SBBH_LAT, SBBH_LON = get_coords_from_skyvector("SBBH")
print(f"SBBH → LAT {SBBH_LAT}, LON {SBBH_LON}\n")


# ---------------------------------------------------------
# Lista de ICAOs (Ipatinga → Viçosa)
# ---------------------------------------------------------

ICAOS = [
    "SBIP","SNZK","SNYB","SNYU","SNLG","SNMK","SNAP","SNCK","SNJI","SNJQ","SNJP",
    "SBJF","SNLY","SBLS","SSOL","SNJM","SWWM","SSYF","SBMK","SNBM","SNNU","SNTD",
    "SSYD","SNRZ","SNOF","SNPA","SNZR","SWZT","SNOS","SNPD","SNPJ","SNPX","SNUH",
    "SBPC","SNCZ","SNZA","SNSS","SIEX","SNJV","SNJR","SNLO","SNPY","SDJR","SNTO",
    "SNVI","SNAS","SNFI","SNUB","SBUR","SBUL","SBVG","SSAT","SNVC"
]


# ---------------------------------------------------------
# Cálculo das distâncias
# ---------------------------------------------------------

distancias = {}

for icao in ICAOS:
    try:
        print(f"Buscando coordenadas de {icao}...")
        lat, lon = get_coords_from_skyvector(icao)
        dist_nm = round(haversine_nm(SBBH_LAT, SBBH_LON, lat, lon), 1)
        distancias[icao] = dist_nm
        print(f"{icao}: {dist_nm} NM\n")
        time.sleep(1)  # evita bloqueio do SkyVector
    except Exception as e:
        print(f"Erro ao processar {icao}: {e}")


# ---------------------------------------------------------
# Salvar JSON
# ---------------------------------------------------------

with open("distancias.json", "w") as f:
    json.dump(distancias, f, indent=4)

print("\nArquivo distancias.json criado com sucesso!")


# ---------------------------------------------------------
# Gerar arquivo pronto para o Streamlit
# ---------------------------------------------------------

with open("aeroportos_atualizados.py", "w") as f:
    f.write("DIST_ATUALIZADAS = {\n")
    for icao, dist in distancias.items():
        f.write(f'    "{icao}": {dist},\n')
    f.write("}\n")

print("Arquivo aeroportos_atualizados.py criado com sucesso!")
