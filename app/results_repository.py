"""Fonte única de resultados para a página Resultados.

INTEGRAÇÃO COM O BACKEND
-------------------------
Não altere as páginas Streamlit para desmockar. Gere os arquivos reais em
``reports/metrics`` com os formatos de ``reports/metrics/README.md``. Este
módulo os prioriza automaticamente; os valores abaixo só são fallback local.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
METRICS_DIR = PROJECT_ROOT / "reports" / "metrics"

# BACKEND: estes são os únicos nomes de arquivo que precisam ser gerados.
COMPARISON_FILE = "comparacao.csv"
CONFUSION_MATRICES_FILE = "matrizes_confusao.json"
ROC_CURVES_FILE = "curvas_roc.csv"

# FRONTEND: não remova os mocks. Eles permitem rodar a interface enquanto o
# backend não terminou e deixam de ser usados assim que os arquivos reais chegam.
COMPARISON_MOCK_FILE = "comparacao_mock.csv"
MOCK_CONFUSION_MATRICES = {
    "Regressão logística": [[5700, 998], [848, 2840]],
    "Random forest": [[6020, 678], [670, 3018]],
    "XGBoost": [[6105, 593], [632, 3056]],
}
MOCK_ROC_EXPONENTS = {
    "Regressão logística": 2.15,
    "Random forest": 3.45,
    "XGBoost": 4.15,
}


def _load_csv_or_mock(real_filename: str, mock_filename: str) -> tuple[pd.DataFrame, bool]:
    """Prioriza a saída real e retorna ``is_mock=True`` apenas no fallback."""
    real_path = METRICS_DIR / real_filename
    if real_path.exists():
        return pd.read_csv(real_path), False
    return pd.read_csv(METRICS_DIR / mock_filename), True


def load_comparison() -> tuple[pd.DataFrame, bool]:
    """Carrega a tabela comparativa dos modelos."""
    return _load_csv_or_mock(COMPARISON_FILE, COMPARISON_MOCK_FILE)


def load_confusion_matrices() -> tuple[dict[str, list[list[int]]], bool]:
    """Carrega matrizes 2x2: linhas reais e colunas previstas (FALTA, EXCESSO)."""
    real_path = METRICS_DIR / CONFUSION_MATRICES_FILE
    if real_path.exists():
        with real_path.open(encoding="utf-8") as file:
            return json.load(file), False
    return MOCK_CONFUSION_MATRICES, True


def load_roc_curves() -> tuple[dict[str, pd.DataFrame], bool]:
    """Carrega os pontos das curvas ROC, agrupados pelo nome do modelo."""
    real_path = METRICS_DIR / ROC_CURVES_FILE
    if real_path.exists():
        data = pd.read_csv(real_path)
        return {model: group for model, group in data.groupby("modelo")}, False
    return _build_mock_roc_curves(), True


def _build_mock_roc_curves() -> dict[str, pd.DataFrame]:
    """Gera curvas apenas para a demonstração visual enquanto não há backend."""
    curves = {}
    for model, exponent in MOCK_ROC_EXPONENTS.items():
        false_positive_rate = [round(value / 20, 3) for value in range(21)]
        curves[model] = pd.DataFrame(
            {
                "fpr": false_positive_rate,
                "tpr": [round(1 - (1 - value) ** exponent, 3) for value in false_positive_rate],
            }
        )
    return curves


def best_model(comparison: pd.DataFrame) -> pd.Series:
    """Define o destaque da interface pelo maior AUROC.

    Se a equipe decidir usar outro critério, altere somente esta função.
    """
    return comparison.loc[comparison["AUROC"].idxmax()]
