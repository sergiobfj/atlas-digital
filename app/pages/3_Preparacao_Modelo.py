import pandas as pd
import streamlit as st

from data_repository import get_pipeline_artifact_status, load_rainfall_dataset
from ui import apply_atlas_style, data_source_notice, header, reading


st.set_page_config(page_title="Preparação e Modelo | Chuvas de Caruaru", page_icon="🌱", layout="wide")
apply_atlas_style()
header(
    "Preparação e modelo",
    "Acompanhamento da base de entrada e dos contratos que o pipeline precisa entregar.",
    "ATLAS CLIMÁTICO · CARUARU/PE",
)
dataset = load_rainfall_dataset()
data = dataset.data
data_source_notice(dataset.source, dataset.notices)

profile, preprocess, model = st.tabs(["Perfil da entrada", "Balanceamento e seleção", "Árvore de Decisão"])

with profile:
    st.subheader("Perfil da variável CHUVA")
    profile_data = data["CHUVA"].value_counts().rename_axis("Classe").reset_index(name="Registros")
    profile_data["Percentual"] = profile_data["Registros"] / profile_data["Registros"].sum() * 100
    st.dataframe(profile_data.style.format({"Percentual": "{:.1f}%"}), hide_index=True, width="stretch")
    st.caption("O perfil acima descreve a base que está sendo exibida; em modo demonstração, não é uma estatística oficial.")
    st.markdown(
        "**Pipeline previsto:** seleção de colunas → tratamento documentado de ausências e outliers → "
        "codificação de `CHUVA` → transformações necessárias → exportação da base preparada."
    )

with preprocess:
    st.subheader("Planejamento do under-sampling")
    before = data["CHUVA"].value_counts()
    target = int(before.min()) if not before.empty else 0
    comparison = pd.DataFrame(
        {
            "Classe": ["SIM", "NAO"],
            "Registros na base de entrada": [before.get("SIM", 0), before.get("NAO", 0)],
            "Meta por classe se aplicado": [target, target],
        }
    )
    st.dataframe(comparison, hide_index=True, width="stretch")
    st.caption("A coluna de meta é apenas uma previsão da interface. O balanceamento real deve ser executado pelo backend no conjunto de treino, preservando o teste.")
    st.subheader("Ganho de informação")
    st.info("Aguardando `data/artifacts/feature_selection.csv`. Os ganhos e pontos de corte só serão mostrados quando forem calculados pelo pipeline.")

with model:
    st.subheader("Treino e avaliação")
    a, b, c = st.columns(3)
    a.metric("Divisão prevista", "80% / 20%")
    b.metric("Estratégia", "Estratificada")
    c.metric("Algoritmo", "Árvore de Decisão")
    st.info("Métricas, matriz de confusão e parâmetros do treino ainda não foram entregues pelo backend.")
    st.subheader("Disponibilidade dos artefatos")
    st.dataframe(get_pipeline_artifact_status(), hide_index=True, width="stretch")

reading("Esta página não simula métricas de modelo. Ela deixa explícitos os pontos de integração para que o backend substitua cada placeholder com segurança.")
