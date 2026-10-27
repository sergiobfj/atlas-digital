import streamlit as st
from ui import apply_atlas_style, header

st.set_page_config(page_title="Metodologia | Atlas Digital", page_icon="🧭", layout="wide")
apply_atlas_style()

header("Metodologia", "Do dado bruto à avaliação dos modelos: um percurso explicável, com escolhas feitas para evitar conclusões enganosas.")

st.info("Esta página descreve o processo planejado. Resultados de desempenho aparecem como dados mockados na página Resultados até a integração com o backend.")

etapas = [
    ("1", "Recorte do problema", "Selecionamos registros ligados à estiagem/seca (FALTA) e a inundações, enxurradas e alagamentos (EXCESSO)."),
    ("2", "Seleção de variáveis", "Mantemos indicadores de impactos humanos, materiais, rurais, mês e região; removemos identificadores e campos que revelariam a resposta."),
    ("3", "Preparação", "Tratamos ausências, codificamos categorias e separamos treino e teste de forma estratificada para preservar a proporção entre as classes."),
    ("4", "Modelagem", "Comparamos regressão logística, random forest e XGBoost, com validação cruzada e ajuste de hiperparâmetros."),
    ("5", "Avaliação", "Avaliamos AUROC, F1, sensibilidade, especificidade, matrizes de confusão e curvas ROC."),
]

tabs = st.tabs([f"{number}. {title}" for number, title, _ in etapas])
for tab, (number, title, text) in zip(tabs, etapas):
    with tab:
        st.subheader(title)
        st.write(text)
        if number == "2":
            st.markdown("**Proteção contra vazamento:** tipologia, códigos de desastre e identificadores não entram como preditores, pois poderiam entregar a classe ao modelo.")
        elif number == "3":
            st.markdown("**Por que separar treino e teste?** Para testar o modelo em casos que ele ainda não viu, simulando o uso em novos registros.")
        elif number == "5":
            st.markdown("**Como ler:** valores mais altos indicam melhor capacidade de separar FALTA e EXCESSO, sempre considerando o equilíbrio entre os erros possíveis.")

st.divider()
st.subheader("O que cada classe representa")
left, right = st.columns(2)
with left:
    st.markdown("**FALTA**\n\nEstiagem e seca, geralmente associadas a prejuízos na agricultura, pecuária e abastecimento de água.")
with right:
    st.markdown("**EXCESSO**\n\nInundações, enxurradas e alagamentos, associados a danos humanos, moradias e infraestrutura.")
