import streamlit as st

# Banco de dados oficial limpo e padronizado para toda a frota (excluindo PTMGS)
BASE_DADOS = {
    "PTWGS": {"modelo": "B200 - BE20", "vel_kt": 200, "val_hora": 9705.13},
    "PP-LCE": {"modelo": "C550", "vel_kt": 290, "val_hora": 18266.14},
    "ESQUILO": {"modelo": "AS350 - AS50", "vel_kt": 100, "val_hora": 9788.57},
    "PP-EJO": {"modelo": "B300 - BE20", "vel_kt": 220, "val_hora": 9705.13},
    "PR-XAA": {"modelo": "B350 - BE30", "vel_kt": 220, "val_hora": 12318.67},
    "PR-OSO": {"modelo": "C90 - BE9L", "vel_kt": 200, "val_hora": 6323.05},
    "PT-OSO": {"modelo": "C90 - BE9L", "vel_kt": 200, "val_hora": 6323.05},
    "PP-EPO": {"modelo": "N2 - AS65", "vel_kt": 110, "val_hora": 26135.07},
    "PR-DTG": {"modelo": "N3 - AS65", "vel_kt": 110, "val_hora": 26135.07},
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

# Seleção da Aeronave
prefixo = st.selectbox("Selecione a Aeronave:", list(BASE_DADOS.keys()))
distancia_nm = st.number_input(
    "Insira a Distância (NM):", min_value=0.0, value=100.0, step=1.0
)

if st.button("Calcular Missão"):
  anv = BASE_DADOS[prefixo]

  # Cálculo exato do tempo de voo decimal
  tempo_decimal = distancia_nm / anv["vel_kt"]
  tempo_str = formatar_tempo(tempo_decimal)

  # Custo total exato: Tempo de Voo Decimal × Valor da Hora de Voo
  custo_total = tempo_decimal * anv["val_hora"]

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
    """)
