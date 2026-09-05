#!/usr/bin/env python3
"""Thin wrapper: run paper_reversal_sim self-checks."""
from __future__ import annotations
import paper_reversal_sim as sim

if __name__ == "__main__":
    raise SystemExit(sim.main() if hasattr(sim, "main") else 0)
