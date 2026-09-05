# weatherbotyes2flash

Fork of weatherbotyes2re with cascade multi-jump (jump 2–3) + 3s armed METAR path + ARM book hot-cache.

Paper only. No wallet. No live orders.

## Run

```bash
export CHECKWX_API_KEY=...
python3 tests_reversal.py
python3 reversal_runner.py run --config config/yes2re_reversal.json --max-seconds 1200
```

Logs: `data/yes2flash_events.jsonl` · Health: `data/yes2flash_health.json`

## Paper capital & settlement

- `paper_initial_capital_usdc`: **1000**
- `fire_budget_usdc`: **100** (per fire notional target)
- `settle_poll_seconds`: **60**
- `unfilled_cancel_seconds`: **1800** (30 min) — never-filled OPEN positions are cancelled and residual cost released
- `max_open_positions`: removed (never enforced)

## ARM book hot-cache

While a session is ARMed, REST+WS keep **ref bucket + next/cascade window** tokens warm (`arm_book_interval_seconds`, default 5s). Fire uses in-memory `book_cache` first (no blocking full-universe REST). Events: `arm_book_refresh`, `fire_book_audit`.
