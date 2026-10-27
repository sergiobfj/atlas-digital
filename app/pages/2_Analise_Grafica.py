from pathlib import Path
import streamlit as st
from ui import apply_atlas_style, header, reading

st.set_page_config(page_title="Análise Gráfica | Atlas Digital", page_icon="📊", layout="wide")
apply_atlas_style()

ROOT = Path(__file__).resolve().parents[2]
FIGURES = ROOT / "reports" / "figures"

header("Análise gráfica", "Quatro recortes para entender como os impactos, o calendário e o território diferenciam FALTA e EXCESSO de chuva.")

charts = [
    ("Danos humanos e moradias", "Ocorrências de EXCESSO apresentam percentuais muito maiores de desalojados, desabrigados e danos a moradias. Isso evidencia impactos súbitos e concentrados."),
    ("Prejuízos econômicos", "Em FALTA, agricultura, pecuária e abastecimento de água aparecem com mais frequência, mostrando um impacto prolongado sobre atividades rurais e serviços."),
    ("Registros por mês", "A sazonalidade ajuda a contextualizar os eventos: o excesso de chuva se concentra em períodos chuvosos, enquanto a falta tem uma distribuição própria no ano."),
    ("Classe por região", "A composição muda entre as regiões brasileiras. Essa diferença regional é um sinal útil, mas não substitui os indicadores de impacto no modelo."),
]

tabs = st.tabs([title for title, _ in charts])
for index, (tab, (title, interpretation)) in enumerate(zip(tabs, charts), start=1):
    with tab:
        image = FIGURES / f"grafico{index}_{['danos_humanos_moradias', 'prejuizos_economicos', 'registros_por_mes', 'classe_por_regiao'][index - 1]}.png"
        st.image(str(image), caption=title, width="stretch")
        reading(interpretation)

st.caption("Gráficos produzidos a partir da análise exploratória do projeto. Não são métricas de desempenho dos modelos.")
