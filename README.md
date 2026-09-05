# weatherbotyes2flash

Fork of weatherbotyes2re with cascade multi-jump (jump 2–3) + 3s armed METAR path.

Paper only. No wallet. No live orders.

## Run

```bash
export CHECKWX_API_KEY=...
python3 tests_reversal.py
python3 reversal_runner.py run --config config/yes2re_reversal.json --max-seconds 300
```

Logs: `data/yes2flash_events.jsonl` · Health: `data/yes2flash_health.json`

## Paper capital & settlement (2026-09-05)

- `paper_initial_capital_usdc`: **5000** (was 1000)
- `settle_poll_seconds`: **60** (was implicit 3600)
- `max_open_positions`: **removed** — never enforced in code; open count is telemetry only
- Real fire gate is `reserve(actual_fill_cost)` vs remaining capital, not position count
