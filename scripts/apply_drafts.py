#!/usr/bin/env python
"""Apply pre-generated drafts from a JSON file to paper stubs.

Usage:
  python scripts/apply_drafts.py <drafts.json>

The drafts.json file is an object keyed by paper id:
{
  "paper-id-slug": {
    "summary_en": "...",
    "data_used": "...",
    "policy_relevance": "...",
    "topics": ["trade-fdi", "firms-productivity"],
    "methods": ["structural", "panel-data"],
    "data_types": ["admin-firm"],
    "countries_studied": ["HU"]
  },
  ...
}

For each key, we:
  - load data/papers/<key>.json
  - apply the fields
  - validate tags against the controlled vocabularies
  - set review_status = "ai-drafted"
  - set last_reviewed_at = today
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent
PAPERS = ROOT / "data" / "papers"

TOPICS = {"labor-markets", "education-skills", "health", "demographics-migration",
          "trade-fdi", "firms-productivity", "innovation-digital", "banking-finance",
          "fiscal-tax", "regional-urban", "energy-environment", "inequality-welfare",
          "political-economy", "transition-postcommunist", "methods",
          "behavioral", "industrial-organization", "macroeconomics", "agriculture-food"}
METHODS = {"rct", "diff-in-diff", "iv", "rd", "panel-data", "synthetic-control",
           "structural", "theory", "time-series", "ml-text", "descriptive-survey"}
DATA_TYPES = {"admin-firm", "admin-tax", "admin-individual", "survey",
              "firm-level-dataset", "field-experiment", "macro-aggregate",
              "digital-trace", "historical"}


def apply(drafts_path: str) -> None:
    drafts = json.load(open(drafts_path, encoding="utf-8"))
    today = time.strftime("%Y-%m-%d")
    applied, missing, invalid = 0, 0, 0
    for pid, d in drafts.items():
        f = PAPERS / f"{pid}.json"
        if not f.exists():
            print(f"MISSING: {pid}")
            missing += 1
            continue
        p = json.load(open(f, encoding="utf-8"))
        if p.get("review_status") in ("human-reviewed", "author-approved"):
            print(f"SKIP (reviewed): {pid}")
            continue

        for key in ("summary_en", "data_used", "policy_relevance",
                    "summary_hu", "data_used_hu", "policy_relevance_hu"):
            if d.get(key):
                p[key] = d[key].strip()

        topics = [t for t in d.get("topics", []) if t in TOPICS][:3]
        methods = [m for m in d.get("methods", []) if m in METHODS][:2]
        data_types = [dt for dt in d.get("data_types", []) if dt in DATA_TYPES][:3]
        countries = [c for c in d.get("countries_studied", []) if isinstance(c, str)][:5]
        # policy_instruments is free-text, capped at 5.
        instruments = [
            str(x).strip() for x in d.get("policy_instruments", [])
            if isinstance(x, str) and x.strip()
        ][:5]

        if topics: p["topics"] = topics
        if methods: p["methods"] = methods
        if data_types: p["data_types"] = data_types
        if countries: p["countries_studied"] = countries
        if instruments: p["policy_instruments"] = instruments

        # sanity flag: missing topic/summary left as defaults
        if not (p["topics"] and p.get("summary_en") and p.get("policy_relevance")):
            invalid += 1
            print(f"WARN (incomplete): {pid}")

        p["review_status"] = "ai-drafted"
        p["last_reviewed_at"] = today
        json.dump(p, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        applied += 1

    print(f"\napplied: {applied}, missing: {missing}, incomplete: {invalid}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: apply_drafts.py <drafts.json>", file=sys.stderr)
        sys.exit(2)
    apply(sys.argv[1])
