
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Atlas Digital | Desastres no Brasil",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# Identidade visual
st.markdown(
    """
    <style>
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        background: linear-gradient(120deg, #123D2B, #18794E);
        padding: 2.5rem 2rem;
        border-radius: 18px;
        color: white;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        color: white;
        font-size: clamp(1.8rem, 4vw, 2.8rem);
        margin-bottom: .7rem;
    }

    .hero p {
        color: #E4F3E9;
        font-size: 1.05rem;
        max-width: 760px;
    }

    .hero > p:first-child {
        margin-top: .5rem;
        margin-bottom: 1.5rem;
    }

    .section-title {
        color: #174A32;
        font-weight: 700;
        font-size: 1.35rem;
        margin-top: 1.4rem;
    }

    .info-card {
        background: white;
        border: 1px solid #DCE7DE;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        height: 100%;
    }

    .info-card h4 {
        color: #174A32;
        margin-bottom: .5rem;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #DCE7DE;
        padding: 1rem;
        border-radius: 12px;
    }

    div[data-testid="stVegaLiteChart"] {
        background: white;
        border: 1px solid #DCE7DE;
        border-radius: 12px;
        padding: 12px;
    }

    @media (max-width: 640px) {
        .block-container {
            padding: 1rem;
        }

        .hero {
            padding: 1.5rem 1.1rem;
            margin-top: .75rem;
        }

        .hero > p:first-child {
            margin-top: .5rem;
            margin-bottom: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Cabeçalho
st.markdown(
    """
    <div class="hero">
        <p>ATLAS DIGITAL DE DESASTRES NO BRASIL</p>
        <h1>Falta × Excesso de chuva</h1>
        <p>
            Uma análise de dados para compreender os padrões dos desastres
            relacionados à falta e ao excesso de chuva no Brasil.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">Visão geral da base</div>',
    unsafe_allow_html=True,
)
st.caption(
    "Indicadores da base documentada no projeto. "
    "Os números não representam o desempenho dos modelos."
)

# Indicadores documentados no README
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Registros originais", "76.190")

with col2:
    st.metric("Registros selecionados", "51.921")

with col3:
    st.metric("Classe FALTA", "33.493")
    st.caption("64,5% dos registros selecionados")

with col4:
    st.metric("Classe EXCESSO", "18.428")
    st.caption("35,5% dos registros selecionados")

st.markdown("---")

# Distribuição das classes
left, right = st.columns([1.1, 1])

with left:
    st.subheader("Distribuição das classes")


    distribuicao = pd.DataFrame({
        "Classe": ["FALTA", "EXCESSO"],
        "Descrição": ["Estiagem e seca", "Inundações e alagamentos"],
        "Registros": [33493, 18428],
        "Percentual": [64.5, 35.5],
    })

    grafico = (
        alt.Chart(distribuicao)
        .mark_bar(cornerRadiusEnd=6)
        .encode(
            x=alt.X("Registros:Q", title="Número de registros"),
            y=alt.Y(
                "Classe:N",
                sort=["FALTA", "EXCESSO"],
                title=None,
                axis=alt.Axis(labelFontSize=13),
            ),
            color=alt.Color(
                "Classe:N",
                scale=alt.Scale(
                    domain=["FALTA", "EXCESSO"],
                    range=["#18794E", "#78B995"],
                ),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("Classe:N"),
                alt.Tooltip("Descrição:N"),
                alt.Tooltip("Registros:Q", format=","),
                alt.Tooltip("Percentual:Q", format=".1f", title="Percentual (%)"),
            ],
        )
        .properties(height=150)
    )

    st.altair_chart(grafico, width="stretch")

    st.caption(
        "24.269 registros de outras tipologias ficaram fora "
        "do recorte da classificação."
    )

with right:
    st.subheader("Objetivo do projeto")

    st.markdown(
        """
        O projeto investiga se características de cada ocorrência
        ajudam a distinguir desastres relacionados à falta ou ao
        excesso de chuva.

        **Classe FALTA**
        - Estiagem e seca.
        - Impactos associados à agricultura e ao abastecimento de água.

        **Classe EXCESSO**
        - Inundações, enxurradas e alagamentos.
        - Impactos associados a danos humanos e materiais.
        """
    )

st.markdown("---")
st.subheader("O que analisamos")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="info-card">
            <h4>🌧️ Perfil dos eventos</h4>
            Relação entre as classes, os meses de ocorrência
            e as regiões brasileiras.
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
        <div class="info-card">
            <h4>🏠 Impactos registrados</h4>
            Danos humanos, moradias, prejuízos rurais
            e abastecimento de água.
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
        <div class="info-card">
            <h4>🤖 Classificação supervisionada</h4>
            Preparação dos dados, treinamento de modelos
            e comparação de métricas.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.subheader("Metodologia")

etapas = [
    ("01", "Análise exploratória", "Estrutura, dados ausentes e distribuição."),
    ("02", "Seleção de variáveis", "Definição do alvo e prevenção de vazamento."),
    ("03", "Análise gráfica", "Relação entre os atributos e as classes."),
    ("04", "Pré-processamento", "Tratamento e preparação dos dados."),
    ("05", "Modelagem", "Treinamento e validação dos algoritmos."),
    ("06", "Avaliação", "Comparação de métricas e resultados."),
]

for inicio in range(0, len(etapas), 3):
    cols = st.columns(3)
    for col, etapa in zip(cols, etapas[inicio:inicio + 3]):
        numero, titulo, descricao = etapa
        with col:
            st.markdown(f"**{numero} · {titulo}**")
            st.caption(descricao)

st.markdown("---")
st.caption(
    "Fonte: Atlas Digital de Desastres no Brasil — "
    "base consolidada v1.1, de 06/08/2026. "
    "Projeto acadêmico de análise de dados."
)
