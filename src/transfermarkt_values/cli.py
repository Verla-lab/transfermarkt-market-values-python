from __future__ import annotations

import argparse
import json
from pathlib import Path

from .exporter import export_csv, export_json
from .fetcher import fetch_page, validate_limits
from .parser import classify_access, parse_players


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export public player-search fields")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--fixture", type=Path, help="Local HTML fixture")
    source.add_argument("--url", help="Public search-result URL")
    parser.add_argument("--live", action="store_true", help="Explicitly enable a live request")
    parser.add_argument("--delay", type=float, default=3)
    parser.add_argument("--max-pages", type=int, default=1)
    parser.add_argument("--format", choices=("json", "csv"), default="json")
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    validate_limits(args.delay, args.max_pages)

    if args.url:
        if not args.live:
            raise SystemExit("Live URLs require --live")
        response = fetch_page(args.url, delay=args.delay)
        if response.access.status != "ok":
            print(json.dumps(response.access.to_dict(), indent=2))
            return 2
        html = response.html or ""
    else:
        html = args.fixture.read_text(encoding="utf-8")
        access = classify_access(html)
        if access.status != "ok":
            print(json.dumps(access.to_dict(), indent=2))
            return 2

    records = parse_players(html)
    if args.format == "csv":
        export_csv(records, args.output)
    else:
        export_json(records, args.output)
    print(f"Exported {len(records)} players to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
