# Soak report (2026-09-05)

Paper runner: `reversal_runner.py run --max-seconds 1200`  
CheckWX key via env. Initial capital **1000 USDC**, `fire_budget_usdc` **100**, `unfilled_cancel_seconds` **1800**.

## What was verified

| Check | Result |
|---|---|
| Unit tests (`tests_reversal.py`) | 7/7 PASS |
| CheckWX METAR | OK |
| ARM sessions | ~15–16 cities armed |
| ARM book hot-cache | `arm_book_refresh` every ~5s; n_fresh matches n_hot; book_age ~0.01s |
| Natural fires | **4 fires** (busan jump=2 cascade, chengdu, chongqing, tokyo jump=2) |
| `fire_book_audit` | budget_usdc=100 on each fire |
| YES leg sizing | 52.08 shares (= 25 USDC / 0.48 cap path; dust ask 0.001 → cost ~0.05) |
| Paper ledger | debit **0.20832** after 4 fires; remaining ~999.79 |
| Positions recorded | 4 OPEN with legs + costs |
| Cascade legs | jump=2 emits `buy_no_broken` + `buy_no_dead_1` + `buy_yes_new` |

## Market microstructure note

NO legs often **0 shares**: dead-bucket NO asks sit above `no_max_ask` / `no_cap_jump_ge2` (or empty). YES landing legs fill at dust prices (0.001). This is pricing structure, not a runner bug.

## Config knobs pushed

```json
{
  "paper_initial_capital_usdc": 1000.0,
  "fire_budget_usdc": 100.0,
  "settle_poll_seconds": 60,
  "unfilled_cancel_seconds": 1800,
  "arm_book_interval_seconds": 5,
  "arm_metar_interval_seconds": 3
}
```

`max_open_positions` removed (never enforced).

## Source layout

Full tree (including `_r_cycle.py` ARM hot-token + cancel path, `reversal_strategy.py` cascade) is maintained in the working sandbox / release tarball. Config + entrypoints + capital ledger are on this repo main branch.
