# How to Collect Transfermarkt Player Market Values with Python

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/tests-offline-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

A fixture-first Python project for turning public player market-value tables into structured JSON or CSV. The code emphasizes reproducible parsing, transparent errors, and explicit stop states—not concealing automation or defeating access controls.

## Fields

- player ID and name
- club
- position
- age
- nationality
- displayed market value
- public profile URL

All included players, clubs, values, and HTML are fictional. The complete example runs offline.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .

transfermarkt-values \
  --fixture fixtures/player-values.html \
  --format csv \
  --output sample-output/players.csv
```

Expected result: `Exported 2 players to sample-output/players.csv`.

Use `--format json --output sample-output/players.json` for JSON.

## Example record

```json
{
  "player_id": "DEMO-PLAYER-1",
  "name": "Alex Rivera",
  "club": "Northbridge FC",
  "position": "Central Midfield",
  "age": 24,
  "nationality": "Spain",
  "market_value": "€18.00m",
  "url": "https://www.transfermarkt.com/demo-player-1/profil/spieler/1001"
}
```

## Processing flow

```text
HTML fixture or explicitly enabled public page
                    │
                    ▼
          access-state classifier
          ├─ public value table ──► parser ──► typed records ──► JSON/CSV
          └─ login/verification ──► structured stop result
```

The parser reads market-value table rows, normalizes relative profile links, converts age to an integer, and keeps the displayed market-value text unchanged.

## Tests

```bash
python -m unittest discover -s tests -v
```

The offline suite covers normal parsing, optional fields, URL normalization, verification detection, export, rate limits, and live-mode safety limits.

## Optional live mode

Live requests are disabled unless `--live` is supplied. Before using them, review the current website terms, robots guidance, and applicable rules.

```bash
transfermarkt-values \
  --live \
  --url "https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop" \
  --delay 3 \
  --max-pages 1 \
  --format json \
  --output players.json
```

The CLI enforces a maximum of five pages and a minimum two-second delay. It does not automatically retry HTTP 429 responses. Login, verification, and denied-access pages stop the run and remain visible in the result.

Live markup can change. Passing fixture tests verifies the parser contract, not permanent compatibility with a third-party website.

## Structured stop result

```json
{
  "status": "verification_required",
  "checkpoint": "interactive_verification",
  "retryable": false,
  "manual_action_required": true
}
```

The project does not solve verification challenges, automate login, or collect private account data.

## Repository layout

```text
transfermarkt-market-values-python/
├── src/transfermarkt_values/
├── fixtures/
├── sample-output/
├── tests/
└── .github/workflows/test.yml
```

## Responsible use

Use this project only for public data, authorized research, personal analysis, or other lawful purposes. Respect website terms, robots guidance, rate limits, database rights, copyright, privacy obligations, and applicable law. Do not use it to profile people, infer sensitive traits, automate account actions, or interfere with a service.

Transfermarkt is a trademark of Transfermarkt GmbH & Co. KG. This independent educational project is not affiliated with or endorsed by Transfermarkt.

## FAQ

### Are the market values financial valuations?

No. The tool preserves the public display text as-is; it does not interpret it as a transaction price or financial recommendation.

### Does the project require an account?

No. Fixtures and tests run offline, and the project does not automate login.

### Can I add another public column?

Yes. Extend `PlayerRecord`, update the parser, add a synthetic fixture, and add an offline test.
