from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal


@dataclass(frozen=True, slots=True)
class PlayerRecord:
    player_id: str | None
    name: str
    club: str | None
    position: str | None
    age: int | None
    nationality: str | None
    market_value: str | None
    url: str | None

    def to_dict(self) -> dict[str, str | int | None]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class AccessResult:
    status: Literal[
        "ok", "verification_required", "rate_limited", "access_denied", "http_error"
    ]
    checkpoint: str | None = None
    retryable: bool = False
    manual_action_required: bool = False
    http_status: int | None = None
    retry_after: str | None = None

    def to_dict(self) -> dict[str, str | int | bool | None]:
        return asdict(self)
