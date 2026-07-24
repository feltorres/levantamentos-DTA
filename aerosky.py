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
# Distância ortodrômica (NM)
# ---------------------------------------------------------

def hav
