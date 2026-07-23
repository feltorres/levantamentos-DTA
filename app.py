import streamlit as st

# Configuração da página Streamlit (Ícone e Título na aba do navegador)
st.set_page_config(page_title="Calculadora DTA", page_icon="✈️")

# Banco de dados com nomes comerciais elegantes e prefixos padronizados
BASE_DADOS = {
    "PT-WGS": {"modelo": "King Air B200", "vel_t1": 200, "vel_t2": 225, "val_hora": 9705.13},
    "PP-LCE": {"modelo": "Citation Bravo C550", "vel_t1": 290, "vel_t2": 300, "val_hora": 18266.14},
    "Esquilo": {"modelo": "Helibras AS350", "vel_t1": 100, "vel_t2": 100, "val_hora": 9788.57},
    "PP-EJO": {"modelo": "King Air B300", "vel_t1": 220, "val_hora": 9705.13},
    "PR-XAA": {"modelo": "King Air B350", "vel_t1": 220, "val_hora": 12318.67},
    "PR-OSO": {"modelo": "King Air C90", "vel_t1": 200, "val_hora": 6323.05},
    "PT-OSO": {"modelo": "King Air C90", "vel_t1": 200, "val_hora": 6323.05},
    "PP-EPO": {"modelo": "Dauphin N2", "vel_t1": 110, "val_hora": 26135.07},
    "PR-DTG": {"modelo": "Dauphin N3", "vel_t1": 110, "val_hora": 26135.07},
}

def formatar_tempo(horas_decimais: float) -> str:
    """Converte horas em formato decimal para o formato de string HH:MM:SS."""
    total_segundos = int(round(horas_decimais * 3600))
    h = total_segundos // 3600
    m = (total_segundos % 3600) // 60
    s = total_segundos % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def formatar_moeda(valor: float) -> str:
    """Formata um valor numérico para o padrão de moeda do Brasil (R$)."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- Interface Gráfica ---

st.title("✈️ Calculadora de Custos - DTA")
st.write("Selecione a aeronave e informe a distância para calcular o custo e o tempo de voo.")

# Agrupando os inputs para organização
with st.container():
    prefixo = st.selectbox("Selecione a Aeronave:", list(BASE_DADOS.keys()))
    # format="%g" remove a exibição obrigatória de casas decimais
    distancia_nm = st.number_input("Insira a Distância (NM):", min_value=0.0, value=100.0, step=1.0, format="%g")

# Botão destacado (type primary)
if st.button("Calcular Missão", type="primary"):
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

    # Processamento final
    tempo_str = formatar_tempo(tempo_decimal)
    custo_total = tempo_decimal * val_hora
    custo_fmt = formatar_moeda(custo_total)

    # Exibição do resultado em um formato de Tabela limpa
    st.success("✅ Cálculo realizado com sucesso!")
    
    st.markdown(f"""
    | Parâmetro | Resultado |
    | :--- | :--- |
    | **Aeronave** | **{prefixo} - {anv['modelo']}** |
    | **Distância** | {distancia_nm} NM |
    | **Tempo de Voo** | ⏱️ {tempo_str} |
    | **Regra Aplicada** | {regra} |
    | **Custo Total Estimado** | **{custo_fmt}** |
    """)
