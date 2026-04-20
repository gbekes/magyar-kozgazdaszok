#!/usr/bin/env python
"""Apply Hungarian bios from a JSON file to data/authors/<id>.json.

Usage:
  python scripts/apply_bios_hu.py <bios_hu.json>

Input JSON: { "author-slug": "hu bio text…", … }
"""
from __future__ import annotations
import json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).parent.parent
AUTHORS = ROOT / "data" / "authors"

def main(path):
    bios = json.load(open(path, encoding="utf-8"))
    applied = 0
    for aid, bio in bios.items():
        f = AUTHORS / f"{aid}.json"
        if not f.exists():
            print(f"MISSING: {aid}")
            continue
        a = json.load(open(f, encoding="utf-8"))
        a["bio_hu"] = bio.strip()
        json.dump(a, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        applied += 1
    print(f"applied: {applied}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: apply_bios_hu.py <bios.json>", file=sys.stderr); sys.exit(2)
    main(sys.argv[1])
