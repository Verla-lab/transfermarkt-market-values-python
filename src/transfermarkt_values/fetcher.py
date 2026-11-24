from __future__ import annotations

import time
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .models import AccessResult
from .parser import classify_access


@dataclass(frozen=True, slots=True)
class FetchResponse:
    access: AccessResult
    html: str | None = None


def validate_limits(delay: float, max_pages: int) -> None:
    if delay < 2:
        raise ValueError("delay must be at least 2 seconds")
    if not 1 <= max_pages <= 5:
        raise ValueError("max_pages must be between 1 and 5")


def fetch_page(url: str, *, delay: float = 3, timeout: float = 20) -> FetchResponse:
    if delay < 2:
        raise ValueError("delay must be at least 2 seconds")

    time.sleep(delay)
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (compatible; VerlaLabPublicDataExample/0.1; "
                "+https://github.com/Verla-lab)"
            )
        },
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            html = response.read().decode("utf-8", errors="replace")
            return FetchResponse(access=classify_access(html), html=html)
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        classified = classify_access(body)
        if classified.status != "ok":
            return FetchResponse(access=classified, html=body)
        if exc.code == 429:
            return FetchResponse(
                access=AccessResult(
                    status="rate_limited",
                    retryable=False,
                    http_status=429,
                    retry_after=exc.headers.get("Retry-After"),
                )
            )
        if exc.code in (401, 403):
            return FetchResponse(
                access=AccessResult(status="access_denied", http_status=exc.code)
            )
        return FetchResponse(
            access=AccessResult(status="http_error", http_status=exc.code)
        )
    except URLError:
        return FetchResponse(access=AccessResult(status="http_error"))
