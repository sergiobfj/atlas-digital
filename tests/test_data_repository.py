import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

APP_DIR = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP_DIR))
from data_repository import REQUIRED_COLUMNS, load_rainfall_dataset  # noqa: E402


class DataRepositoryTests(unittest.TestCase):
    def test_missing_file_returns_deterministic_mock(self):
        result = load_rainfall_dataset(Path("this-file-does-not-exist.csv"))
        self.assertTrue(result.is_mock)
        self.assertEqual(set(result.data.columns), set(REQUIRED_COLUMNS))
        self.assertEqual(len(result.data), 8760)

    def test_valid_csv_is_normalized(self):
        raw = pd.DataFrame({"data_hora": ["2025-02-02 03:00", "2025-02-01 03:00"], "precipitacao_mm": [1.2, 0], "temperatura_c": [25.0, 24.5], "umidade_pct": [80, 70], "CHUVA": [" sim ", "nao"]})
        with patch("data_repository.Path.exists", return_value=True), patch("data_repository.pd.read_csv", return_value=raw):
            result = load_rainfall_dataset(Path("rain.csv"))
        self.assertFalse(result.is_mock)
        self.assertEqual(result.data["CHUVA"].tolist(), ["NAO", "SIM"])
        self.assertTrue(result.data["data_hora"].is_monotonic_increasing)

    def test_invalid_contract_falls_back_to_mock(self):
        raw = pd.DataFrame({"data_hora": ["2025-01-01"]})
        with patch("data_repository.Path.exists", return_value=True), patch("data_repository.pd.read_csv", return_value=raw):
            result = load_rainfall_dataset(Path("rain.csv"))
        self.assertTrue(result.is_mock)
        self.assertIn("colunas obrigatórias ausentes", result.notices[0])


if __name__ == "__main__":
    unittest.main()
