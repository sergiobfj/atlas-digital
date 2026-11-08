"""Ponto único de acesso aos dados exibidos pelo painel.

O frontend só depende deste módulo. Enquanto o CSV oficial não chega, ele entrega
uma amostra sintética determinística e identificada como demonstração. Assim, a
troca pelo pipeline real não exige alterar as páginas do Streamlit.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REAL_DATA_FILE = PROJECT_ROOT / "data" / "processed" / "caruaru_chuvas.csv"
REQUIRED_COLUMNS = (
    "data_hora",
    "precipitacao_mm",
    "temperatura_c",
    "umidade_pct",
    "CHUVA",
)
PIPELINE_ARTIFACTS = (
    ("Base preparada", PROJECT_ROOT / "data" / "processed" / "caruaru_chuvas_preparada.csv"),
    ("Base balanceada", PROJECT_ROOT / "data" / "processed" / "caruaru_chuvas_balanceada.csv"),
    ("Seleção de atributos", PROJECT_ROOT / "data" / "artifacts" / "feature_selection.csv"),
    ("Avaliação do modelo", PROJECT_ROOT / "data" / "artifacts" / "model_metrics.json"),
)


@dataclass(frozen=True)
class DataLoadResult:
    """Dataset pronto para exibição e contexto para a interface."""

    data: pd.DataFrame
    source: str
    notices: tuple[str, ...] = ()

    @property
    def is_mock(self) -> bool:
        return self.source == "mock"


def load_rainfall_dataset(data_file: Path | None = None) -> DataLoadResult:
    """Lê e valida o CSV real; usa o mock somente como fallback seguro.

    A função é deliberadamente independente de Streamlit para também poder ser
    testada pelo backend e reutilizada por uma futura API.
    """
    source_file = data_file or REAL_DATA_FILE
    if not source_file.exists():
        return DataLoadResult(
            _build_mock_data(),
            "mock",
            ("CSV oficial ainda não encontrado; a demonstração está ativa.",),
        )

    try:
        raw = pd.read_csv(source_file)
        data, notices = _validate_and_normalize(raw)
    except (OSError, UnicodeDecodeError, pd.errors.ParserError, ValueError) as error:
        return DataLoadResult(
            _build_mock_data(),
            "mock",
            (f"Não foi possível usar o CSV oficial ({error}). A demonstração continua ativa.",),
        )

    if data.empty:
        return DataLoadResult(
            _build_mock_data(),
            "mock",
            tuple(notices) + ("O CSV não possui linhas válidas após a validação; a demonstração continua ativa.",),
        )
    return DataLoadResult(data, "csv", tuple(notices))


def load_rainfall_data() -> tuple[pd.DataFrame, bool]:
    """Compatibilidade para consumidores antigos do adaptador."""
    result = load_rainfall_dataset()
    return result.data, result.is_mock


def get_pipeline_artifact_status() -> pd.DataFrame:
    """Expõe apenas a disponibilidade dos artefatos, sem inventar resultados."""
    return pd.DataFrame(
        [
            {
                "Artefato esperado": label,
                "Caminho": path.relative_to(PROJECT_ROOT).as_posix(),
                "Status": "Disponível" if path.exists() else "Aguardando backend",
            }
            for label, path in PIPELINE_ARTIFACTS
        ]
    )


def _validate_and_normalize(raw: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(raw.columns))
    if missing_columns:
        raise ValueError(f"colunas obrigatórias ausentes: {', '.join(missing_columns)}")

    data = raw.loc[:, REQUIRED_COLUMNS].copy()
    data["data_hora"] = pd.to_datetime(data["data_hora"], errors="coerce")
    for column in ("precipitacao_mm", "temperatura_c", "umidade_pct"):
        data[column] = pd.to_numeric(data[column], errors="coerce")
    data["CHUVA"] = data["CHUVA"].astype("string").str.strip().str.upper()

    valid = data.notna().all(axis=1) & data["CHUVA"].isin(("SIM", "NAO"))
    discarded = int((~valid).sum())
    data = data.loc[valid].sort_values("data_hora").reset_index(drop=True)
    notices = []
    if discarded:
        notices.append(f"{discarded} linha(s) inválida(s) do CSV foram ocultadas na visualização.")
    return data, notices


def _build_mock_data() -> pd.DataFrame:
    """Amostra de 2025 com semente fixa: estável para desenvolvimento visual."""
    rng = np.random.default_rng(2025)
    dates = pd.date_range("2025-01-01", "2025-12-31 23:00", freq="h")
    season = np.sin((dates.dayofyear.to_numpy() - 35) * 2 * np.pi / 365)
    rainy = rng.random(len(dates)) < np.clip(0.16 + 0.17 * season, 0.04, 0.38)
    precipitation = np.where(rainy, rng.gamma(shape=1.45, scale=2.1, size=len(dates)), 0)
    temperature = 25.2 + 2.6 * np.sin((dates.dayofyear.to_numpy() - 75) * 2 * np.pi / 365) + rng.normal(0, 1.7, len(dates))
    humidity = np.clip(62 + 13 * season + rainy * 12 + rng.normal(0, 8, len(dates)), 25, 100)
    return pd.DataFrame(
        {
            "data_hora": dates,
            "precipitacao_mm": precipitation.round(2),
            "temperatura_c": temperature.round(1),
            "umidade_pct": humidity.round(1),
            "CHUVA": np.where(rainy, "SIM", "NAO"),
        }
    )
