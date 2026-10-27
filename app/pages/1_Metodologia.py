import streamlit as st
from content import CLASS_DESCRIPTIONS, METHODOLOGY_STEPS
from ui import apply_atlas_style, header

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Metodologia | Atlas Digital", page_icon="🧭", layout="wide")
apply_atlas_style()

# CABEÇALHO
header("Metodologia", "Do dado bruto à avaliação dos modelos: um percurso explicável, com escolhas feitas para evitar conclusões enganosas.")

st.info("Esta página descreve o processo planejado. Resultados de desempenho aparecem como dados mockados na página Resultados até a integração com o backend.")

# ETAPAS — o conteúdo fica em app/content.py para facilitar revisão textual.
tabs = st.tabs([f"{step['number']}. {step['title']}" for step in METHODOLOGY_STEPS])
for tab, step in zip(tabs, METHODOLOGY_STEPS):
    with tab:
        st.subheader(step["title"])
        st.write(step["description"])
        if detail := step.get("detail"):
            st.markdown(detail)

# CLASSES — também editáveis em app/content.py.
st.divider()
st.subheader("O que cada classe representa")
for column, (name, description) in zip(st.columns(2), CLASS_DESCRIPTIONS):
    with column:
        st.markdown(f"**{name}**\n\n{description}")
