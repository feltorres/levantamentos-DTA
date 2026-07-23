import streamlit as st

# Banco de dados interno
BASE_DADOS = {
    "PP-LCE": {
        "modelo": "C550",
        "t1": {
            "vel_kt": 290,
            "val_hora": 18266.14,
            "custo_op_base": 3149.33,
            "val_consumo": 117.24,
            "dist_ref": 50,
        },
        "t2": {"vel_kt": 300, "val_hora": 18266.14, "custo_total": 15221.78},
    },
    "PTWGS": {
        "modelo": "B200 - BE20",
        "t1": {
            "vel_kt": 200,
            "val_hora": 9705.13,
            "custo_op_base": 8734.62,
            "val_consumo": 409.50,
            "dist_ref": 180,
        },
        "t2": {"vel_kt": 225, "val_hora": 9705.13, "custo_total": 10783.48},
    },
    "ESQUILO": {
        "modelo": "AS350 - AS50",
        "t1": {
            "vel_kt": 100,
            "val_hora": 9788.57,
            "custo_op_base": 9788.57,
            "val_consumo": 425.00,
            "dist_ref": 125,
        },
        "t2": {"vel_kt": 100, "val_hora": 9788.57, "custo_total": 12235.71},
    },
}

def formatar_tempo(horas_decimais):
    total_segundos = int(horas_decimais * 3600)
    h = total_segundos // 3600
    m = (total_segundos % 3600) // 60
    s = total_segundos % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

st.title("Calculadora de Custos - DTA")
st.write("Selecione a aeronave e informe a distância para calcular o custo e o tempo de voo.")

prefixo = st.selectbox("Selecione a Aeronave:", list(BASE_DADOS.keys()))
distancia_nm = st.number_input("Insira a Distância (NM):", min_value=0.0, value=100.0, step=1.0)

if st.button("Calcular Missão"):
    anv = BASE_DADOS[prefixo]
    t1 = anv["t1"]
    tempo_decimal_t1 = distancia_nm / t1["vel_kt"]

    if tempo_decimal_t1 >= 1.0:
        t2 = anv["t2"]
        tempo_decimal_t2 = distancia_nm / t2["vel_kt"]
        tempo_str = formatar_tempo(tempo_decimal_t2)
        custo_total = t2["custo_total"] * (distancia_nm / 250) if "custo_total" in t2 else (tempo_decimal_t2 * t2["val_hora"])
        regra = "Tabela 2 (>= 1h)"
    else:
        tempo_str = formatar_tempo(tempo_decimal_t1)
        custo_total = (tempo_decimal_t1 * t1["val_hora"]) + ((distancia_nm / t1["dist_ref"]) * t1["val_consumo"])
        regra = "Tabela 1 (< 1h)"

    custo_fmt = f"R$ {custo_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    st.success("Cálculo realizado com sucesso!")
    st.markdown(f"""
    * **Aeronave:** {prefixo} ({anv['modelo']})
    * **Distância:** {distancia_nm} NM
    * **Tempo de Voo:** {tempo_str}
    * **Custo Total Estimado:** **{custo_fmt}**
    * **Regra Aplicada:** {regra}
    """)
