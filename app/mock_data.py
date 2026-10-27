"""Adaptadores temporários de resultados para a interface Streamlit.

O backend deve gravar os arquivos sem o sufixo ``_mock`` em
``reports/metrics``. Enquanto eles não existem, os dados desta camada deixam
claro que a interface está em modo demonstração.
"""
from __future__ import annotations

from pathlib import Path
import json

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
METRICS_DIR = ROOT / "reports" / "metrics"


def _read_or_mock(filename: str, mock_filename: str) -> tuple[pd.DataFrame, bool]:
    """Prioriza a saída do backend; retorna ``is_mock`` quando usa o fallback."""
    production_path = METRICS_DIR / filename
    if production_path.exists():
        return pd.read_csv(production_path), False
    return pd.read_csv(METRICS_DIR / mock_filename), True


def load_comparison() -> tuple[pd.DataFrame, bool]:
    return _read_or_mock("comparacao.csv", "comparacao_mock.csv")


def load_confusion_matrices() -> tuple[dict[str, list[list[int]]], bool]:
    """Contrato futuro: ``matrizes_confusao.json`` com modelo -> matriz 2x2."""
    path = METRICS_DIR / "matrizes_confusao.json"
    if path.exists():
        with path.open(encoding="utf-8") as file:
            return json.load(file), False
    return {
        "Regressão logística": [[5700, 998], [848, 2840]],
        "Random forest": [[6020, 678], [670, 3018]],
        "XGBoost": [[6105, 593], [632, 3056]],
    }, True


def load_roc_curves() -> tuple[dict[str, pd.DataFrame], bool]:
    """Contrato futuro: ``curvas_roc.csv`` com modelo, fpr e tpr."""
    path = METRICS_DIR / "curvas_roc.csv"
    if path.exists():
        data = pd.read_csv(path)
        return {name: group for name, group in data.groupby("modelo")}, False

    curves = {}
    for model, exponent in {
        "Regressão logística": 2.15,
        "Random forest": 3.45,
        "XGBoost": 4.15,
    }.items():
        fpr = [round(value / 20, 3) for value in range(21)]
        curves[model] = pd.DataFrame({"fpr": fpr, "tpr": [round(1 - (1 - x) ** exponent, 3) for x in fpr]})
    return curves, True


def best_model(comparison: pd.DataFrame) -> pd.Series:
    return comparison.loc[comparison["AUROC"].idxmax()]
