import altair as alt
import pandas as pd
import streamlit as st

# Não leia CSV/JSON diretamente nesta página. O adaptador abaixo concentra a
# troca entre mock e backend; veja app/mock_data.py e reports/metrics/README.md.
from mock_data import best_model, load_comparison, load_confusion_matrices, load_roc_curves
from ui import apply_atlas_style, header, reading

st.set_page_config(page_title="Resultados | Atlas Digital", page_icon="🏁", layout="wide")
apply_atlas_style()

header("Resultados", "Comparação transparente entre os modelos. Os números abaixo são uma demonstração até a conclusão da etapa de avaliação.")
comparison, comparison_is_mock = load_comparison()
matrices, matrices_is_mock = load_confusion_matrices()
curves, curves_is_mock = load_roc_curves()
is_mock = comparison_is_mock or matrices_is_mock or curves_is_mock

if is_mock:
    st.warning("MODO DEMONSTRAÇÃO — os números abaixo são dados mockados, usados somente para validar a interface. Serão substituídos automaticamente quando o backend gravar os arquivos de métricas.")
else:
    st.success("Resultados carregados a partir das saídas do backend.")

winner = best_model(comparison)
metrics = st.columns(3)
metrics[0].metric("Melhor modelo", winner["Modelo"])
metrics[1].metric("AUROC", f"{winner['AUROC']:.3f}")
metrics[2].metric("F1", f"{winner['F1']:.3f}")

st.subheader("Comparação dos modelos")
st.dataframe(comparison.style.format({column: "{:.3f}" for column in ["AUROC", "F1", "Sensibilidade", "Especificidade"]}), width="stretch", hide_index=True)
st.caption("AUROC mede a capacidade de separar as duas classes; F1 equilibra acertos de FALTA e EXCESSO. Quanto maior, melhor.")

st.subheader("Matrizes de confusão")
matrix_tabs = st.tabs(list(matrices))
for tab, (model, matrix) in zip(matrix_tabs, matrices.items()):
    with tab:
        table = pd.DataFrame(matrix, index=["Real: FALTA", "Real: EXCESSO"], columns=["Previsto: FALTA", "Previsto: EXCESSO"])
        st.dataframe(table, width="stretch")
        st.caption("A diagonal reúne os acertos; os demais campos representam classificações trocadas.")

st.subheader("Curvas ROC")
roc_data = pd.concat([frame.assign(Modelo=model) for model, frame in curves.items()], ignore_index=True)
roc_chart = alt.Chart(roc_data).mark_line(strokeWidth=3).encode(
    x=alt.X("fpr:Q", title="Taxa de falsos positivos", scale=alt.Scale(domain=[0, 1])),
    y=alt.Y("tpr:Q", title="Taxa de verdadeiros positivos", scale=alt.Scale(domain=[0, 1])),
    color=alt.Color("Modelo:N", title="Modelo"),
    tooltip=["Modelo:N", alt.Tooltip("fpr:Q", format=".2f"), alt.Tooltip("tpr:Q", format=".2f")],
).properties(height=360)
baseline = alt.Chart(pd.DataFrame({"x": [0, 1], "y": [0, 1]})).mark_line(strokeDash=[6, 6], color="#777").encode(x="x:Q", y="y:Q")
st.altair_chart(baseline + roc_chart, width="stretch")
st.caption("Quanto mais a curva se aproxima do canto superior esquerdo, melhor a separação entre as classes. A diagonal representa um classificador ao acaso.")

reading(f"Nos dados mockados, <strong>{winner['Modelo']}</strong> tem o melhor AUROC ({winner['AUROC']:.3f}). Esta conclusão só será válida após a avaliação real.")
