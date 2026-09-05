# weatherbotyes2flash

Fork of [weatherbotyes2re](https://github.com/jssyxd/weatherbotyes2re) with two upgrades:

1. **Cascade multi-jump (jump 2–3)** — BUY NO on each METAR-confirmed dead bucket + optional BUY YES on the landing bucket (bounded by `max_dead_legs=3`).
2. **Faster armed path** — armed-station METAR poll ~3s, scan 15s / fast 5s, memory-book first FAK.

Paper only. No wallet. No live orders.

## Strategy (unchanged safety core)

- Reference: TAF TX/TN if present, else market rank-1 TWAP consensus.
- Consensus filter still only on the **reference** broken bucket.
- Obs sanity window (90min lookback / 15min future), not absolute 180s age.
- Local hour window: high ≥14 / low ≤10.
- One fire per `city|date|direction` session.

### Legs

| jump | NO legs | YES leg | NO cap |
|------|---------|---------|--------|
| 1 | broken ref | landing (optional) | 0.85 |
| 2–3 | each dead bucket (ref…landing-1) | landing (optional) | 0.70 |
| >3 | skip (`jump_too_large`) | — | — |

## Run

```bash
export CHECKWX_API_KEY=...
python3 tests_reversal.py
python3 reversal_runner.py once --config config/yes2re_reversal.json
python3 reversal_runner.py run  --config config/yes2re_reversal.json --max-seconds 300
```

Logs: `data/yes2flash_events.jsonl` · Health: `data/yes2flash_health.json`

## Config highlights

- `arm_metar_interval_seconds`: 3
- `fast_poll_interval_seconds`: 5
- `strategy.multi_jump.max_dead_legs`: 3
- `paper_initial_capital_usdc`: 1000
