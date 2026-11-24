from __future__ import annotations

from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .models import AccessResult, PlayerRecord

BASE_URL = "https://www.transfermarkt.com"
VERIFICATION_MARKERS = (
    "security measure",
    "verify yourself",
    "verification challenge",
)
LOGIN_MARKERS = ("sign in to continue", "login required")


def classify_access(html: str) -> AccessResult:
    lowered = html.lower()
    if any(marker in lowered for marker in VERIFICATION_MARKERS):
        return AccessResult(
            status="verification_required",
            checkpoint="interactive_verification",
            retryable=False,
            manual_action_required=True,
        )
    if any(marker in lowered for marker in LOGIN_MARKERS):
        return AccessResult(
            status="verification_required",
            checkpoint="login_required",
            retryable=False,
            manual_action_required=True,
        )
    return AccessResult(status="ok")


def _text(element) -> str | None:
    if element is None:
        return None
    value = element.get_text(" ", strip=True)
    return value or None


def _integer(value: str | None) -> int | None:
    if not value:
        return None
    digits = "".join(character for character in value if character.isdigit())
    return int(digits) if digits else None


def parse_players(html: str, base_url: str = BASE_URL) -> list[PlayerRecord]:
    access = classify_access(html)
    if access.status != "ok":
        return []

    soup = BeautifulSoup(html, "html.parser")
    players: list[PlayerRecord] = []

    for row in soup.select("table.items > tbody > tr[data-player-id], tr[data-player-id]"):
        player_id = (row.get("data-player-id") or "").strip() or None
        name = _text(row.select_one(".player-name, [data-field='name']"))
        if not name:
            continue

        link = row.select_one("a.player-link[href], a[data-field='url'][href]")
        href = link.get("href") if link else None
        url = urljoin(base_url, href) if href else None

        club = _text(row.select_one(".club-name, [data-field='club']"))
        position = _text(row.select_one(".position, [data-field='position']"))
        age = _integer(_text(row.select_one(".age, [data-field='age']")))
        nationality = _text(row.select_one(".nationality, [data-field='nationality']"))
        market_value = _text(row.select_one(".market-value, [data-field='market-value']"))

        players.append(
            PlayerRecord(
                player_id=player_id,
                name=name,
                club=club,
                position=position,
                age=age,
                nationality=nationality,
                market_value=market_value,
                url=url,
            )
        )

    return players
