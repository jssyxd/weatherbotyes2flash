# Changelog

## 2026-09-06 — R1 book-lead METAR + R2 speed

- **Core insight documented**: confirmation-after-price-in; speed alone ≠ alpha
- **R1**: `ws_trigger_metar` — armed rank1 YES drop / NO rise / next YES drop → immediate METAR (`book_lead_metar` event, 3s cooldown)
- **R2**: idle METAR 60→20s, scan 15→10s, fast_poll 5→3s; METAR path **before** full book REST
- **B2**: `prebreak_sleeve.enabled=false` placeholder only

## 2026-09-05 — weatherbotyes2flash

- Cascade multi-jump (jump 2–max_dead_legs)
- ARM METAR fast path 3s; ARM book hot-cache
- fire_budget_usdc 100; paper_initial_capital_usdc 1000
- unfilled_cancel_seconds 1800
