import altair as alt
import pandas as pd
import streamlit as st
from data_repository import load_rainfall_dataset
from ui import apply_atlas_style, data_source_notice, header, reading

st.set_page_config(page_title="Análise Gráfica | Chuvas de Caruaru", page_icon="📊", layout="wide")
apply_atlas_style()
header("Análise gráfica", "Distribuições e relações entre chuva, temperatura e umidade em 2025.", "ATLAS CLIMÁTICO · CARUARU/PE")
dataset = load_rainfall_dataset()
data = dataset.data.copy()
data_source_notice(dataset.source, dataset.notices)
months = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
data["mes"] = data["data_hora"].dt.month
daily = data.assign(dia=data["data_hora"].dt.date).groupby("dia").agg(choveu=("CHUVA", lambda values: values.eq("SIM").any())).reset_index()
daily["mes"] = pd.to_datetime(daily["dia"]).dt.month
by_month = daily.groupby("mes").agg(dias_chuvosos=("choveu", "sum")).reset_index().merge(data.groupby("mes")["temperatura_c"].mean().rename("temperatura_media").reset_index(), on="mes")
by_month["Mês"] = by_month["mes"].map(lambda item: months[item - 1])

t1, t2, t3 = st.tabs(["Chuva e temperatura", "Distribuições", "Correlações"])
with t1:
    c1, c2 = st.columns(2)
    with c1:
        chart = alt.Chart(by_month).mark_bar(color="#18794E").encode(x=alt.X("Mês:N", sort=months, title=None), y=alt.Y("dias_chuvosos:Q", title="Dias chuvosos"), tooltip=["Mês:N", alt.Tooltip("dias_chuvosos:Q", format=".1f")]).properties(title="Dias chuvosos por mês", height=280)
        st.altair_chart(chart, width="stretch")
    with c2:
        chart = alt.Chart(by_month).mark_line(point=True, color="#237A57", strokeWidth=3).encode(x=alt.X("Mês:N", sort=months, title=None), y=alt.Y("temperatura_media:Q", title="Temperatura média (°C)"), tooltip=["Mês:N", alt.Tooltip("temperatura_media:Q", format=".1f")]).properties(title="Temperatura média por mês", height=280)
        st.altair_chart(chart, width="stretch")
with t2:
    c1, c2 = st.columns(2)
    with c1:
        share = data["CHUVA"].value_counts().rename_axis("CHUVA").reset_index(name="horas")
        st.altair_chart(alt.Chart(share).mark_arc(innerRadius=45).encode(theta="horas:Q", color=alt.Color("CHUVA:N", scale=alt.Scale(domain=["SIM", "NAO"], range=["#18794E", "#B8D3C0"])), tooltip=["CHUVA:N", "horas:Q"]).properties(title="Horas com e sem chuva", height=280), width="stretch")
    with c2:
        st.altair_chart(alt.Chart(data).mark_bar(color="#78B995").encode(x=alt.X("temperatura_c:Q", bin=alt.Bin(step=5), title="Temperatura (°C)"), y=alt.Y("count():Q", title="Horas")).properties(title="Histograma de temperatura (faixas de 5 °C)", height=280), width="stretch")
    c3, c4 = st.columns(2)
    with c3:
        daily_share = daily["choveu"].map({True: "Com chuva", False: "Sem chuva"}).value_counts().rename_axis("Dias").reset_index(name="quantidade")
        st.altair_chart(alt.Chart(daily_share).mark_arc(innerRadius=45).encode(theta="quantidade:Q", color=alt.Color("Dias:N", scale=alt.Scale(domain=["Com chuva", "Sem chuva"], range=["#18794E", "#B8D3C0"])), tooltip=["Dias:N", "quantidade:Q"]).properties(title="Dias com e sem chuva", height=280), width="stretch")
    with c4:
        st.altair_chart(alt.Chart(data).mark_bar(color="#237A57").encode(x=alt.X("precipitacao_mm:Q", bin=alt.Bin(step=5), title="Precipitação (mm)"), y=alt.Y("count():Q", title="Horas")).properties(title="Histograma da precipitação (faixas de 5 mm)", height=280), width="stretch")
    st.altair_chart(alt.Chart(data).mark_boxplot(color="#18794E").encode(y=alt.Y("precipitacao_mm:Q", title="Precipitação por hora (mm)")).properties(title="Boxplot da precipitação", height=260), width="stretch")
with t3:
    rain_hours = data[data["CHUVA"] == "SIM"]
    if rain_hours.empty:
        st.info("Não há registros classificados como SIM para exibir as correlações.")
    else:
        c1, c2 = st.columns(2)
        for col, variable, title, axis_title in [(c1, "temperatura_c", "Chuva × temperatura", "Temperatura (°C)"), (c2, "umidade_pct", "Chuva × umidade", "Umidade (%)")]:
            with col:
                st.altair_chart(alt.Chart(rain_hours).mark_circle(size=26, opacity=.42, color="#18794E").encode(x=alt.X(f"{variable}:Q", title=axis_title), y=alt.Y("precipitacao_mm:Q", title="Precipitação (mm)"), tooltip=[variable, alt.Tooltip("precipitacao_mm:Q", format=".2f")]).properties(title=title, height=300), width="stretch")
reading("Os gráficos respondem às tarefas de dias e horas chuvosas, temperatura, histogramas, boxplot e correlações. A leitura final depende da base real.")
