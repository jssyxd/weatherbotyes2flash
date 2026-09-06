#!/usr/bin/env python3
"""Reassemble source from source_pack/part_*.b64 and extract into repo root."""
from __future__ import annotations
import base64, io, tarfile
from pathlib import Path
ROOT = Path(__file__).resolve().parent
parts_dir = ROOT / "source_pack"
blob = "".join(p.read_text() for p in sorted(parts_dir.glob("part_*.b64")))
data = base64.b64decode(blob)
with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
    names = tar.getnames()
    tar.extractall(path=ROOT)
print("extracted", len(names), "entries")
for n in names:
    print(" ", n)
