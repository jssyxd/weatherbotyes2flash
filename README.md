# weatherbotyes2flash

Fork of weatherbotyes2re with cascade multi-jump (jump 2–3) + 3s armed METAR path + ARM book hot-cache.

Paper only. No wallet. No live orders.

## Quick start (full tree)

Some large modules ship as a packed archive on `main` (see `source_pack/` + `unpack_source.py`). After clone:

```bash
git clone https://github.com/jssyxd/weatherbotyes2flash.git
cd weatherbotyes2flash
# If source_pack/ is present:
python3 unpack_source.py
# Or pull shared modules from the parent paper repo (identical for many files):
# curl -sL https://raw.githubusercontent.com/jssyxd/weatherbotyes2re/main/_r_cycle.py -o _r_cycle.py
export CHECKWX_API_KEY=...
python3 tests_reversal.py
python3 reversal_runner.py run --config config/yes2re_reversal.json --max-seconds 1200
```

Logs: `data/yes2flash_events.jsonl` · Health: `data/yes2flash_health.json`

## Paper capital & settlement

- `paper_initial_capital_usdc`: **1000**
- `fire_budget_usdc`: **100** (per fire notional target)
- `settle_poll_seconds`: **60**
- `unfilled_cancel_seconds`: **1800** (30 min) — never-filled OPEN positions cancelled
- `max_open_positions`: removed (never enforced)

## ARM book hot-cache

While ARMed, REST+WS keep **ref bucket + next/cascade window** tokens warm (`arm_book_interval_seconds`=5). Fire uses in-memory `book_cache` first. Events: `arm_book_refresh`, `fire_book_audit`.

## On this branch already

Config, runner entrypoints, capital ledger, state I/O, health/settle, WS bridge, unpack helpers, soak report.

## Still unpack / copy if missing after clone

`_r_cycle.py`, `reversal_strategy.py`, `re_execution.py`, `research/common.py`, CLOB/METAR adapters, `config/contract_cities.json` — via `python3 unpack_source.py` once `source_pack/part_*.b64` is complete, or from parent `weatherbotyes2re` + apply flash patches.
