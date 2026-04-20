#!/usr/bin/env python
"""Apply Hungarian paper summaries from a JSON file to data/papers/<id>.json.

Input JSON: {
  "paper-slug": {
    "summary_hu": "...",
    "data_used_hu": "...",
    "policy_relevance_hu": "..."
  },
  ...
}

Only sets fields that are present in the input; won't overwrite with empty strings.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).parent.parent
PAPERS = ROOT / "data" / "papers"

def main(path):
    drafts = json.load(open(path, encoding="utf-8"))
    applied = 0
    for pid, d in drafts.items():
        f = PAPERS / f"{pid}.json"
        if not f.exists():
            print(f"MISSING: {pid}")
            continue
        p = json.load(open(f, encoding="utf-8"))
        for key in ("summary_hu", "data_used_hu", "policy_relevance_hu"):
            if d.get(key):
                p[key] = d[key].strip()
        json.dump(p, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        applied += 1
    print(f"applied: {applied}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: apply_summaries_hu.py <drafts.json>", file=sys.stderr); sys.exit(2)
    main(sys.argv[1])
