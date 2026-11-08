import streamlit as st
from content import DATA_CONTRACT, METHODOLOGY_STEPS, PIPELINE_CONTRACTS
from ui import apply_atlas_style, header

st.set_page_config(page_title="Metodologia | Chuvas de Caruaru", page_icon="🧭", layout="wide")
apply_atlas_style()
header("Metodologia", "Fluxo proposto para transformar os registros meteorológicos em uma análise reproduzível.", "ATLAS CLIMÁTICO · CARUARU/PE")
st.info("Roteiro de implementação. Nenhuma métrica de modelo é exibida antes da entrega e validação dos artefatos reais.")
tabs = st.tabs([f"{number}. {title}" for number, title, _ in METHODOLOGY_STEPS])
for tab, (_, title, description) in zip(tabs, METHODOLOGY_STEPS):
    with tab:
        st.subheader(title)
        st.write(description)
st.divider()
st.subheader("Contrato para integração")
path, *columns = DATA_CONTRACT
st.code(f"{path}\nColunas esperadas: {', '.join(columns)}", language=None)
st.caption("Com a base no caminho acima, o frontend deixa de gerar os dados demonstrativos automaticamente.")

st.subheader("Artefatos esperados do backend")
st.caption("Os caminhos abaixo são contratos de integração. A interface não fabrica métricas, ganhos de informação nem resultados de modelo.")
for title, artifact_path, description in PIPELINE_CONTRACTS:
    with st.expander(title):
        st.code(artifact_path, language=None)
        st.write(description)
