from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable

from .models import PlayerRecord

FIELDS = ("player_id", "name", "club", "position", "age", "nationality", "market_value", "url")


def export_json(records: Iterable[PlayerRecord], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps([record.to_dict() for record in records], indent=2, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )


def export_csv(records: Iterable[PlayerRecord], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(record.to_dict() for record in records)
