import requests
from bs4 import BeautifulSoup
import math
import json
import time

# ---------------------------------------------------------
# Converter DMS para decimal
# ---------------------------------------------------------

def dms_to_decimal(dms):
    dms = dms.replace("°", " ").replace("'", " ").replace('"', " ")
    parts = dms.split()

    deg = float(parts[0])
    min_ = float(parts[1])
    sec = float(parts[2])
    hemi = parts[3]

    decimal = deg + min_/60 + sec/3600

    if hemi in ["S", "W"]:
        decimal = -decimal

    return decimal


# ---------------------------------------------------------
# Buscar coordenadas no SkyVector (novo HTML)
# ---------------------------------------------------------

def get_coords_from_skyvector(icao):
    url = f"https://skyvector.com/airport/{icao}"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    table = soup.find("table", {"class": "aptHeaderTable"})
    if not table:
        raise ValueError(f"Não encontrei tabela de coordenadas para {icao}")

    tds = table.find_all("td")

    lat_dms = None
    lon_dms = None

    for i in range(len(tds)):
        if "Latitude" in tds[i].text:
            lat_dms = tds[i+1].text.strip()
        if "Longitude" in tds[i].text:
            lon_dms = tds[i+1].text.strip()

    if not lat_dms or not lon_dms:
        raise ValueError(f"Coordenadas não encontradas para {icao}")

    lat = dms_to_decimal(lat_dms)
    lon = dms_to_decimal(lon_dms)

    return lat, lon


# ---------------------------------------------------------
# Coordenadas da origem SBBH (fixas, oficiais)
# ---------------------------------------------------------

SBBH_LAT = -19.8511
SBBH_LON = -43.9506

print(f"SBBH LAT={SBBH_LAT}, LON={SBBH_LON}\n")


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
        time.sleep(1)
    except Exception as e:
        print(f"Erro ao processar {icao}: {e}")


# ---------------------------------------------------------
# Salvar JSON
# ---------------------------------------------------------

with open("distancias.json", "w") as f:
    json.dump(distancias, f, indent=4)

print("\nArquivo distancias.json criado com sucesso!")
