import csv
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from transfermarkt_values.exporter import export_csv, export_json
from transfermarkt_values.models import PlayerRecord


class ExporterTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            PlayerRecord(
                "DEMO-PLAYER-TEST",
                "Test player",
                "Demo FC",
                "Goalkeeper",
                26,
                "Germany",
                "€2.00m",
                "https://example.test",
            )
        ]

    def test_json_export(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "players.json"
            export_json(self.records, path)
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data[0]["name"], "Test player")

    def test_csv_export(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "players.csv"
            export_csv(self.records, path)
            with path.open(encoding="utf-8") as handle:
                data = list(csv.DictReader(handle))
            self.assertEqual(data[0]["player_id"], "DEMO-PLAYER-TEST")


if __name__ == "__main__":
    unittest.main()
