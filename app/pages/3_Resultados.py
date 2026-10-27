import altair as alt
import pandas as pd
import streamlit as st

# DADOS — não leia CSV/JSON diretamente nesta página. Toda a integração com o
# backend e o fallback mock ficam em app/results_repository.py.
from results_repository import best_model, load_comparison, load_confusion_matrices, load_roc_curves
from ui import apply_atlas_style, header, reading

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Resultados | Atlas Digital", page_icon="🏁", layout="wide")
apply_atlas_style()


def render_status(is_mock: bool) -> None:
    """Mostra de onde os resultados vieram."""
    if is_mock:
        st.warning(
            "MODO DEMONSTRAÇÃO — os números abaixo são dados mockados, usados "
            "somente para validar a interface. Serão substituídos automaticamente "
            "quando o backend gravar os arquivos de métricas."
        )
    else:
        st.success("Resultados carregados a partir das saídas do backend.")


def render_comparison(comparison: pd.DataFrame) -> pd.Series:
    """Exibe o destaque e a tabela que comparam os modelos."""
    winner = best_model(comparison)
    metrics = st.columns(3)
    metrics[0].metric("Melhor modelo", winner["Modelo"])
    metrics[1].metric("AUROC", f"{winner['AUROC']:.3f}")
    metrics[2].metric("F1", f"{winner['F1']:.3f}")

    st.subheader("Comparação dos modelos")
    metric_columns = ["AUROC", "F1", "Sensibilidade", "Especificidade"]
    formatted_comparison = comparison.style.format(
        {column: "{:.3f}" for column in metric_columns}
    )
    st.dataframe(formatted_comparison, width="stretch", hide_index=True)
    st.caption(
        "AUROC mede a capacidade de separar as duas classes; F1 equilibra "
        "acertos de FALTA e EXCESSO. Quanto maior, melhor."
    )
    return winner


def render_confusion_matrices(matrices: dict[str, list[list[int]]]) -> None:
    """Exibe uma aba por modelo com sua matriz de confusão."""
    st.subheader("Matrizes de confusão")
    matrix_tabs = st.tabs(list(matrices))
    for tab, matrix in zip(matrix_tabs, matrices.values()):
        with tab:
            table = pd.DataFrame(
                matrix,
                index=["Real: FALTA", "Real: EXCESSO"],
                columns=["Previsto: FALTA", "Previsto: EXCESSO"],
            )
            st.dataframe(table, width="stretch")
            st.caption("A diagonal reúne os acertos; os demais campos representam classificações trocadas.")


def render_roc_curves(curves: dict[str, pd.DataFrame]) -> None:
    """Exibe em um só gráfico as curvas ROC de todos os modelos."""
    st.subheader("Curvas ROC")
    roc_data = pd.concat(
        [frame.assign(Modelo=model) for model, frame in curves.items()],
        ignore_index=True,
    )
    roc_chart = alt.Chart(roc_data).mark_line(strokeWidth=3).encode(
        x=alt.X("fpr:Q", title="Taxa de falsos positivos", scale=alt.Scale(domain=[0, 1])),
        y=alt.Y("tpr:Q", title="Taxa de verdadeiros positivos", scale=alt.Scale(domain=[0, 1])),
        color=alt.Color("Modelo:N", title="Modelo"),
        tooltip=["Modelo:N", alt.Tooltip("fpr:Q", format=".2f"), alt.Tooltip("tpr:Q", format=".2f")],
    ).properties(height=360)
    baseline = alt.Chart(pd.DataFrame({"x": [0, 1], "y": [0, 1]})).mark_line(strokeDash=[6, 6], color="#777").encode(x="x:Q", y="y:Q")
    st.altair_chart(baseline + roc_chart, width="stretch")
    st.caption(
        "Quanto mais a curva se aproxima do canto superior esquerdo, melhor a "
        "separação entre as classes. A diagonal representa um classificador ao acaso."
    )


# MONTAGEM DA TELA — os dados chegam sempre pelo repositório acima.
header("Resultados", "Comparação transparente entre os modelos. Os números abaixo são uma demonstração até a conclusão da etapa de avaliação.")
comparison, comparison_is_mock = load_comparison()
matrices, matrices_is_mock = load_confusion_matrices()
curves, curves_is_mock = load_roc_curves()
is_mock = comparison_is_mock or matrices_is_mock or curves_is_mock

render_status(is_mock)
winner = render_comparison(comparison)
render_confusion_matrices(matrices)
render_roc_curves(curves)

if is_mock:
    reading(
        f"Nos dados mockados, <strong>{winner['Modelo']}</strong> tem o melhor "
        f"AUROC ({winner['AUROC']:.3f}). Esta conclusão só será válida após a "
        "avaliação real."
    )
else:
    reading(
        f"Com os dados atuais, <strong>{winner['Modelo']}</strong> tem o melhor "
        f"AUROC ({winner['AUROC']:.3f})."
    )
