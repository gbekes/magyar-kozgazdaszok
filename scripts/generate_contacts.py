#!/usr/bin/env python
"""Generate not-shared/contacts.json — a PII file of author contact info.

Reads all `data/authors/*.json`, extracts name / affiliations / email /
website, and writes `not-shared/contacts.json`. The `not-shared/` folder is
gitignored; this file is for local editorial use only (e.g. mass outreach).

Re-run after adding authors or filling in emails. Existing email values in
`not-shared/contacts.json` are preserved across runs — the script merges
them back in so you can hand-edit emails in contacts.json without having
them wiped.

Usage:
  python scripts/generate_contacts.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
AUTHORS_DIR = ROOT / "data" / "authors"
OUT_DIR = ROOT / "not-shared"
OUT = OUT_DIR / "contacts.json"


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)

    # Preserve any hand-entered emails / notes from a previous run.
    prior: dict[str, dict] = {}
    if OUT.exists():
        for c in json.loads(OUT.read_text(encoding="utf-8")).get("contacts", []):
            prior[c["id"]] = c

    contacts = []
    for p in sorted(AUTHORS_DIR.glob("*.json")):
        a = json.loads(p.read_text(encoding="utf-8"))
        aid = a["id"]
        prev = prior.get(aid, {})
        contacts.append({
            "id": aid,
            "name_en": a.get("name_en"),
            "name_hu": a.get("name_hu"),
            "affiliations": [
                aff.get("name") for aff in (a.get("affiliations") or [])
                if aff.get("name")
            ],
            # Email: keep what's in contacts.json if hand-entered; else
            # fall back to whatever the author JSON has (usually null).
            "emails": prev.get("emails") or (
                [a["email"]] if a.get("email") else []
            ),
            "website": a.get("website"),
            "notes": prev.get("notes", ""),
        })

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"contacts": contacts}, f, ensure_ascii=False, indent=2)

    n = len(contacts)
    with_email = sum(1 for c in contacts if c["emails"])
    print(f"Wrote {n} contacts to {OUT.relative_to(ROOT)} "
          f"({with_email} with email, {n - with_email} missing).")


if __name__ == "__main__":
    main()
