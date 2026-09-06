# weatherbotyes2flash

Paper-only METAR dead-bucket reversal bot (cascade multi-jump + ARM fast path).

## Core insight (why speed alone is not alpha)

Most fires arrive **after the market has already priced the break**.

- Same METAR is read by faster players (push / denser grid) → **book moves first**
- By the time we poll → confirm → fire, rank-1 NO is often **0.85–0.99** (fully priced)
- Cutting poll from 5s → 1s only recovers **controllable 5–70s**, not the information edge

| Only speeding up | What it can do |
|---|---|
| Controllable lag 5–70s → ~1–5s | Stop being the last to see the same METAR |
| Cannot alone make stable alpha | Alpha needs earlier signal **or** better structure/sizing |

**R1 (shipped):** when ARMed, if rank-1 / next-bucket **book structure moves**, interleave METAR pull immediately (`book_lead_metar`) — mirror acceleration, does not change fire semantics.

**R2 (shipped):** idle METAR 20s; scan 10s; fast poll 3s; **METAR path runs before full-universe book REST** so book refresh cannot delay obs.

**B2 (config only, default OFF):** pre-break sleeve — experimental follower trade; do not enable until R1 lead quality is measured.

## Run

```bash
export CHECKWX_API_KEY=...
python3 tests_reversal.py
python3 reversal_runner.py run --config config/yes2re_reversal.json --max-seconds 1200
```

## Config knobs

- `paper_initial_capital_usdc`: 1000
- `fire_budget_usdc`: 100
- `unfilled_cancel_seconds`: 1800
- `idle_metar_interval_seconds`: **20** (R2)
- `arm_metar_interval_seconds`: 3
- `ws_trigger_metar.enabled`: **true** (R1)
- `prebreak_sleeve.enabled`: **false** (B2)

Events: `book_lead_metar`, `arm_book_refresh`, `fire_book_audit`, `fire`
