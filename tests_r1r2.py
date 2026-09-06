#!/usr/bin/env python3
"""Unit tests for R1 book-lead METAR trigger and R2 speed config."""
from __future__ import annotations

import json
import time
from pathlib import Path


def test_r1_book_lead_triggers():
    from _r_cycle import _detect_book_lead_icaos, _BOOK_LEAD_LAST, _BOOK_LEAD_COOLDOWN
    _BOOK_LEAD_LAST.clear()
    _BOOK_LEAD_COOLDOWN.clear()
    _BOOK_LEAD_LAST["YES-31"] = 0.55
    _BOOK_LEAD_LAST["NO-31"] = 0.40
    cache = {
        "YES-31": {"best_ask": "0.48", "asks": [{"price": "0.48", "size": "10"}]},
        "NO-31": {"best_ask": "0.48", "asks": [{"price": "0.48", "size": "10"}]},
    }
    rules = {
        "shanghai|2026-09-01|high": {
            "buckets": [
                {"bucket_id": "h31", "mid_c": 31.0, "yes_token_id": "YES-31", "no_token_id": "NO-31"},
                {"bucket_id": "h32", "mid_c": 32.0, "yes_token_id": "YES-32", "no_token_id": "NO-32"},
            ]
        }
    }
    armed = {"shanghai|2026-09-01|high": {"taf_bucket_id": "h31", "direction": "high"}}
    cities = [{"city_id": "shanghai", "icao": "ZSPD"}]
    cfg = {
        "ws_trigger_metar": {
            "enabled": True,
            "cooldown_seconds": 0.0,
            "yes_ask_drop": 0.05,
            "no_ask_rise": 0.05,
            "next_yes_drop": 0.04,
        }
    }
    ev = _detect_book_lead_icaos(cfg, rules, armed, cities, cache, now_epoch=time.time())
    reasons = [r for e in ev for r in (e.get("reasons") or [])]
    assert len(ev) == 1 and ev[0]["icao"] == "ZSPD"
    assert "rank1_yes_drop" in reasons and "rank1_no_rise" in reasons
    return {"name": "r1_book_lead_triggers", "ok": True, "reasons": reasons}


def test_r1_book_lead_cooldown():
    from _r_cycle import _detect_book_lead_icaos, _BOOK_LEAD_LAST, _BOOK_LEAD_COOLDOWN
    _BOOK_LEAD_LAST.clear()
    _BOOK_LEAD_COOLDOWN.clear()
    _BOOK_LEAD_LAST["YES-31"] = 0.55
    cache = {"YES-31": {"best_ask": "0.40", "asks": [{"price": "0.40", "size": "10"}]}}
    rules = {
        "shanghai|2026-09-01|high": {
            "buckets": [
                {"bucket_id": "h31", "mid_c": 31.0, "yes_token_id": "YES-31", "no_token_id": "NO-31"},
            ]
        }
    }
    armed = {"shanghai|2026-09-01|high": {"taf_bucket_id": "h31", "direction": "high"}}
    cities = [{"city_id": "shanghai", "icao": "ZSPD"}]
    cfg = {
        "ws_trigger_metar": {
            "enabled": True,
            "cooldown_seconds": 60.0,
            "yes_ask_drop": 0.05,
            "no_ask_rise": 0.05,
            "next_yes_drop": 0.04,
        }
    }
    now = time.time()
    first = _detect_book_lead_icaos(cfg, rules, armed, cities, cache, now_epoch=now)
    _BOOK_LEAD_LAST["YES-31"] = 0.40
    cache["YES-31"] = {"best_ask": "0.20", "asks": [{"price": "0.20", "size": "10"}]}
    second = _detect_book_lead_icaos(cfg, rules, armed, cities, cache, now_epoch=now + 1.0)
    assert len(first) == 1 and len(second) == 0
    return {"name": "r1_book_lead_cooldown", "ok": True}


def test_r1_disabled():
    from _r_cycle import _detect_book_lead_icaos, _BOOK_LEAD_LAST, _BOOK_LEAD_COOLDOWN
    _BOOK_LEAD_LAST.clear()
    _BOOK_LEAD_COOLDOWN.clear()
    _BOOK_LEAD_LAST["YES-31"] = 0.55
    cache = {"YES-31": {"best_ask": "0.10", "asks": [{"price": "0.10", "size": "10"}]}}
    rules = {
        "shanghai|2026-09-01|high": {
            "buckets": [
                {"bucket_id": "h31", "mid_c": 31.0, "yes_token_id": "YES-31", "no_token_id": "NO-31"},
            ]
        }
    }
    armed = {"shanghai|2026-09-01|high": {"taf_bucket_id": "h31", "direction": "high"}}
    cities = [{"city_id": "shanghai", "icao": "ZSPD"}]
    cfg = {"ws_trigger_metar": {"enabled": False}}
    ev = _detect_book_lead_icaos(cfg, rules, armed, cities, cache, now_epoch=time.time())
    assert len(ev) == 0
    return {"name": "r1_disabled", "ok": True}


def test_r2_config_speed():
    root = Path(__file__).resolve().parent
    cfg = json.loads((root / "config" / "yes2re_reversal.json").read_text(encoding="utf-8"))
    cycle = (root / "_r_cycle.py").read_text(encoding="utf-8")
    assert float(cfg["idle_metar_interval_seconds"]) <= 20
    assert float(cfg["scan_interval_seconds"]) <= 10
    assert float(cfg["fast_poll_interval_seconds"]) <= 3
    assert cfg["ws_trigger_metar"]["enabled"] is True
    assert cfg["prebreak_sleeve"]["enabled"] is False
    assert "METAR BEFORE books" in cycle
    assert "book_lead_metar" in cycle
    return {"name": "r2_config_speed", "ok": True}


def run_r1r2():
    results = []
    failed = 0
    for fn in (
        test_r1_book_lead_triggers,
        test_r1_book_lead_cooldown,
        test_r1_disabled,
        test_r2_config_speed,
    ):
        try:
            r = fn()
            r["ok"] = bool(r.get("ok", True))
        except Exception as exc:
            r = {"name": fn.__name__, "ok": False, "error": f"{type(exc).__name__}: {exc}"}
        results.append(r)
        if not r.get("ok"):
            failed += 1
    return results, failed


if __name__ == "__main__":
    results, failed = run_r1r2()
    for r in results:
        print(("PASS" if r.get("ok") else "FAIL"), r.get("name"), r.get("error", ""))
    raise SystemExit(failed)
