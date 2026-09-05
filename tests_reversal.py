#!/usr/bin/env python3
"""Lightweight test runner for paper_reversal_sim scenarios."""
from __future__ import annotations
import sys
from paper_reversal_sim import run_scenarios

def main() -> int:
    results = run_scenarios()
    failed = [r for r in results if not r.get("ok")]
    for r in results:
        status = "PASS" if r.get("ok") else "FAIL"
        print(status, r.get("name"))
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
