#!/usr/bin/env python3
"""Lightweight tests without pytest."""
from paper_reversal_sim import run_scenarios
from tests_r1r2 import run_r1r2


def main():
    results, failed = run_scenarios()
    r2, f2 = run_r1r2()
    results.extend(r2)
    failed += f2
    for r in results:
        mark = "PASS" if r.get("ok") else "FAIL"
        extra = f" {r.get('error')}" if r.get("error") else ""
        print(f"{mark} {r['name']}{extra}")
    if failed:
        raise SystemExit(failed)


if __name__ == "__main__":
    main()
