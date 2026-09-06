"""Health reporting + paper-settlement for the weatherbotyes2re live runner.

The live-runner sibling to the pure strategy/execution modules. ``runner_impl``
imports exactly two public entry points here:

  - ``write_health(cfg, state)``  -> persist ``data/yes2re_health.json``
  - ``settle_markets(cfg, state, rules_registry-ish)`` -> credit resolved paper legs

Every number an observer (pi watcher / Hermes summary) may want is summarized
onto the health file so the watcher only ever reads one JSON. Stdlib only.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

from _r_globals import health_extra
from _r_state import log_event
from market_adapter import fetch_market_resolution
from paper_capital import release

ZERO = Decimal("0")


def _iso(dt: datetime | None = None) -> str:
    dt = dt or datetime.now(timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _capital_usdc(state: dict[str, Any]) -> Decimal:
    return Decimal(str(state.get("paper_initial_capital_usdc") or 0))


def _debit_usdc(state: dict[str, Any]) -> Decimal:
    return Decimal(str(state.get("paper_total_debit_usdc") or 0))


def write_health(cfg: dict[str, Any], state: dict[str, Any], *, extra: dict[str, Any] | None = None) -> None:
    tree = state.setdefault("weatherbotyes2re", {})
    armed = tree.get("armed", {})
    fired = tree.get("fired", {})
    positions = state.get("positions", {})
    open_pos = {k: v for k, v in positions.items() if not v.get("settled")}
    debit = _debit_usdc(state)
    remaining = _capital_usdc(state) - debit

    health: dict[str, Any] = {
        "source": "weatherbotyes2re paper runner",
        "mode": cfg.get("mode", "paper"),
        "ts_utc": _iso(),
        "ok": True,
        "state_path": cfg.get("state_path"),
        "armed_count": len(armed),
        "armed": list(armed.keys()),
        "fired_count": len(fired),
        "open_positions": len(open_pos),
        "position_i18n_keys": list(open_pos.keys()),
        "capital_initial_usdc": str(_capital_usdc(state)),
        "debit_usdc": str(debit),
        "remaining_capital_usdc": str(remaining),
        "entry_count": state.get("entry_count", 0),
        "version": state.get("version"),
    }
    if extra:
        health.update({k: v for k, v in extra.items() if v is not None})
    try:
        tel = health_extra()
        if tel:
            health.setdefault("feed", {}).update(tel)
    except Exception:
        pass
    p = Path(cfg.get("health_path", "data/yes2re_health.json"))
    try:
        if p.parent and not p.parent.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(p.suffix + ".tmp")
        tmp.write_text(json.dumps(health, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
        tmp.replace(p)
    except OSError:
        log_event(cfg.get("log_path", "data/yes2re_events.jsonl"), {"type": "health_write_failed"})


def settle_leg(
    state: dict[str, Any],
    position_key: str,
    leg: dict[str, Any],
    *,
    leg_won: bool,
    resolution_source: str | None,
    log_path: str,
) -> dict[str, Any] | None:
    shares = Decimal(str(leg.get("shares") or 0))
    settle: dict[str, Any] = dict(leg)
    settle["settled"] = True
    settle["leg_won"] = bool(leg_won)
    settle["resolution_source"] = resolution_source
    settle["settled_at_utc"] = _iso()
    payout_credit = ZERO
    if leg_won and shares > ZERO:
        release(state, shares)
        payout_credit = shares
    settle["payout_credit_usdc"] = str(payout_credit)
    log_event(
        log_path,
        {
            "type": "position_settled",
            "position_key": position_key,
            "leg": leg.get("leg"),
            "leg_won": bool(leg_won),
            "shares": str(shares),
            "payout_credit_usdc": str(payout_credit),
            "resolution_source": resolution_source,
        },
    )
    return settle


def settle_markets(
    cfg: dict[str, Any],
    state: dict[str, Any],
    *,
    position_meta: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    tree = state.setdefault("weatherbotyes2re", {})
    fired = tree.get("fired", {})
    positions = state.get("positions", {})
    events: list[dict[str, Any]] = []
    for pos_key, saved in list(positions.items()):
        if saved.get("settled"):
            continue
        meta = (position_meta or {}).get(pos_key) or saved.get("meta") or {}
        city = meta.get("city")
        local_date = meta.get("market_local_date") or saved.get("market_local_date")
        direction = meta.get("direction") or saved.get("direction")
        if not (city and isinstance(city, dict) and local_date and direction):
            continue
        for leg in (saved.get("legs") or []):
            if leg.get("settled"):
                continue
            bucket_id = leg.get("bucket_id")
            if not bucket_id:
                continue
            outcome, source = fetch_market_resolution(city, local_date, direction, bucket_id) or (None, None)
            if outcome is None:
                continue
            held = (leg.get("outcome") or "").upper()
            leg_won = (outcome == "YES" and held == "YES") or (outcome == "NO" and held == "NO")
            settled = settle_leg(state, pos_key, leg, leg_won=leg_won, resolution_source=source, log_path=str(cfg.get("log_path")))
            if settled is not None:
                idx = (saved.get("legs") or []).index(leg)
                saved["legs"][idx] = settled
                events.append({"position_key": pos_key, **settled})
        if all(l.get("settled") for l in (saved.get("legs") or [])) and saved.get("legs"):
            saved["settled"] = True
            saved["settled_at_utc"] = _iso()
    _ = fired
    return events
