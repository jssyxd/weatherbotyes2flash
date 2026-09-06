# Changelog

## 2026-09-05 — weatherbotyes2flash

- Cascade multi-jump (jump 2–max_dead_legs): BUY NO on each dead bucket + optional YES on landing
- ARM METAR fast path 3s; ARM book hot-cache (ref + cascade window) every 5s
- fire_budget_usdc 100; paper_initial_capital_usdc 1000
- unfilled_cancel_seconds 1800 (30m never-filled OPEN cancel + residual release)
- settle_poll_seconds 60
- max_open_positions removed (never enforced)
- Events: arm_book_refresh, fire_book_audit, position_cancelled_unfilled
