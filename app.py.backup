import streamlit as st

# Banco de dados completo com todas as aeronaves e parâmetros de T1 e T2
BASE_DADOS = {
    "PTWGS": {
        "modelo": "B200 - BE20",
        "vel_t1": 200,
        "vel_t2": 225,
        "val_hora": 9705.13,
    },
    "PP-LCE": {
        "modelo": "C550",
        "vel_t1": 290,
        "vel_t2": 300,
        "val_hora": 18266.14,
    },
    "ESQUILO": {
        "modelo": "AS350 - AS50",
        "vel_t1": 100,
        "vel_t2": 100,
        "val_hora": 9788.57,
    },
    # Aeronaves que operam com tabela padrão única
    "PP-EJO": {"modelo": "B300 - BE20", "vel_t1": 220, "val_hora": 9705.13},
    "PR-XAA": {"modelo": "B350 - BE30", "vel_t1": 220, "val_hora": 12318.67},
    "PR-OSO": {"modelo": "C90 - BE9L", "vel_t1": 200, "val_hora": 6323.05},
    "PT-OSO": {"modelo": "C90 - BE9L", "vel_t1": 200, "val_hora": 6323.05},
    "PP-EPO": {"modelo": "N2 - AS65", "vel_t1": 110, "val_hora": 26135.07},
    "PR-DTG": {"modelo": "N3 - AS65", "vel_t1": 110, "val_hora": 26135.07},
}


def formatar_tempo(horas_decimais):
  total_segundos = int(horas_decimais * 3600)
  h = total_segundos // 3600
  m = (total_segundos % 3600) // 60
  s = total_segundos % 60
  return f"{h:02d}:{m:02d}:{s:02d}"


st.title("Calculadora de Custos - DTA")
st.write(
    "Selecione a aeronave e informe a distância para calcular o custo e o"
    " tempo de voo."
)

# Seleção da Aeronave e Distância
prefixo = st.selectbox("Selecione a Aeronave:", list(BASE_DADOS.keys()))
distancia_nm = st.number_input(
    "Insira a Distância (NM):", min_value=0.0, value=100.0, step=1.0
)

if st.button("Calcular Missão"):
  anv = BASE_DADOS[prefixo]
  vel_t1 = anv["vel_t1"]
  val_hora = anv["val_hora"]

  # 1. Calcula o tempo preliminar com base na Tabela 1
  tempo_decimal_t1 = distancia_nm / vel_t1

  # 2. Regra de Transição: Se atingir/superar 1 hora e houver Tabela 2 cadastrada
  if tempo_decimal_t1 >= 1.0 and "vel_t2" in anv:
    vel_t2 = anv["vel_t2"]
    tempo_decimal = distancia_nm / vel_t2
    regra = "Tabela 2 (>= 1h)"
  else:
    tempo_decimal = tempo_decimal_t1
    regra = "Tabela 1 (< 1h)" if "vel_t2" in anv else "Cálculo Padrão"

  # Formatação do tempo e cálculo proporcional do custo total
  tempo_str = formatar_tempo(tempo_decimal)
  custo_total = tempo_decimal * val_hora

  custo_fmt = (
      f"R$ {custo_total:,.2f}"
      .replace(",", "X")
      .replace(".", ",")
      .replace("X", ".")
  )

  st.success("Cálculo realizado com sucesso!")
  st.markdown(f"""
    * **Aeronave:** {prefixo} ({anv['modelo']})
    * **Distância:** {distancia_nm} NM
    * **Tempo de Voo:** {tempo_str}
    * **Custo Total Estimado:** **{custo_fmt}**
    * **Regra Aplicada:** {regra}
    """)
