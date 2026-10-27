from pathlib import Path

import streamlit as st

from content import GRAPH_ANALYSES
from ui import apply_atlas_style, header, reading

# CONFIGURAÇÃO E CAMINHO DOS GRÁFICOS EXPORTADOS PELOS NOTEBOOKS
st.set_page_config(page_title="Análise Gráfica | Atlas Digital", page_icon="📊", layout="wide")
apply_atlas_style()

FIGURES_DIR = Path(__file__).resolve().parents[2] / "reports" / "figures"

# CABEÇALHO
header("Análise gráfica", "Quatro recortes para entender como os impactos, o calendário e o território diferenciam FALTA e EXCESSO de chuva.")

# GRÁFICOS — nomes dos PNGs e leituras ficam em app/content.py.
tabs = st.tabs([chart["title"] for chart in GRAPH_ANALYSES])
for tab, chart in zip(tabs, GRAPH_ANALYSES):
    with tab:
        image_path = FIGURES_DIR / chart["figure"]
        st.image(str(image_path), caption=chart["title"], width="stretch")
        reading(chart["insight"])

st.caption("Gráficos produzidos a partir da análise exploratória do projeto. Não são métricas de desempenho dos modelos.")
