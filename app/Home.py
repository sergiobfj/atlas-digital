import altair as alt
import streamlit as st

from data_repository import load_rainfall_dataset
from ui import apply_atlas_style, data_source_notice, header, reading

st.set_page_config(page_title="Chuvas de Caruaru | Atlas", page_icon="🌧️", layout="wide")
apply_atlas_style()
header("Chuvas em Caruaru", "Painel para explorar precipitação, temperatura e umidade. A origem dos dados é sempre indicada abaixo.", "ATLAS CLIMÁTICO · CARUARU/PE")
dataset = load_rainfall_dataset()
data = dataset.data
data_source_notice(dataset.source, dataset.notices)

rainy = data[data["CHUVA"] == "SIM"]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Horas observadas", f"{len(data):,}".replace(",", "."))
c2.metric("Horas com chuva", f"{len(rainy):,}".replace(",", "."))
c3.metric("Precipitação acumulada", f"{data['precipitacao_mm'].sum():.1f} mm")
c4.metric("Temperatura média", f"{data['temperatura_c'].mean():.1f} °C")

months = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
monthly = data.assign(mes=data["data_hora"].dt.month).groupby("mes")["precipitacao_mm"].sum().reset_index()
monthly["Mês"] = monthly["mes"].map(lambda item: months[item - 1])
st.subheader("Precipitação acumulada por mês")
chart = alt.Chart(monthly).mark_bar(color="#18794E", cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
    x=alt.X("Mês:N", sort=months, title=None), y=alt.Y("precipitacao_mm:Q", title="Precipitação (mm)"),
    tooltip=[alt.Tooltip("Mês:N"), alt.Tooltip("precipitacao_mm:Q", title="Precipitação", format=".1f")],
).properties(height=290)
st.altair_chart(chart, width="stretch")
reading("Use o menu lateral para consultar as distribuições, correlações e o roteiro de preparação da base. O adaptador troca automaticamente para o CSV oficial quando ele atende ao contrato.")
