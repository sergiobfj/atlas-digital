"""Ponto único de integração entre o backend e as páginas de resultados.

COMO DESMOCKAR (não é preciso alterar as páginas Streamlit):
1. Grave os três arquivos reais em ``reports/metrics`` com os nomes e colunas
   documentados em ``reports/metrics/README.md``.
2. Ao encontrar um arquivo real, cada função abaixo o prioriza e retorna
   ``False`` como segundo valor. A interface então remove o aviso de demonstração.
3. Os arquivos ``*_mock`` continuam apenas como fallback para desenvolvimento.

Se o contrato do backend mudar, ajuste somente esta camada adaptadora. Não
espalhe leitura de CSV/JSON pelas páginas da interface.
"""
from __future__ import annotations

from pathlib import Path
import json

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
METRICS_DIR = ROOT / "reports" / "metrics"


def _read_or_mock(filename: str, mock_filename: str) -> tuple[pd.DataFrame, bool]:
    """Lê o arquivo do backend; sem ele, usa o fallback visual temporário."""
    production_path = METRICS_DIR / filename
    if production_path.exists():
        return pd.read_csv(production_path), False
    return pd.read_csv(METRICS_DIR / mock_filename), True


def load_comparison() -> tuple[pd.DataFrame, bool]:
    # BACKEND: crie reports/metrics/comparacao.csv com as colunas do README.
    # Quando esse arquivo existir, comparacao_mock.csv deixa de ser utilizado.
    return _read_or_mock("comparacao.csv", "comparacao_mock.csv")


def load_confusion_matrices() -> tuple[dict[str, list[list[int]]], bool]:
    """Retorna ``modelo -> [[real FALTA], [real EXCESSO]]`` em matriz 2x2."""
    # BACKEND: crie reports/metrics/matrizes_confusao.json conforme o README.
    # A ordem aceita pela interface é: linhas reais FALTA/EXCESSO e colunas
    # previstas FALTA/EXCESSO.
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
    """Retorna pontos ROC agrupados por modelo."""
    # BACKEND: crie reports/metrics/curvas_roc.csv com modelo, fpr e tpr.
    # Um modelo pode ter quantos pontos forem necessários; não há limite fixo.
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
    # Regra visível e fácil de alterar caso o critério mude no projeto.
    return comparison.loc[comparison["AUROC"].idxmax()]
