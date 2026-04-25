#!/usr/bin/env python
"""Ingest hand-corrected policy/press rows from the markdown seed.

Reads `not-shared/policy-press-seed.md` (or whichever path is passed),
parses the markdown tables under each `## Author / ### Policy|Press`
section, and writes:
  - data/policy/<slug>.json (for Policy rows)
  - data/press/<slug>.json (for Press rows)

Behaviour:
  - Only rows marked `[x]` are ingested. Rows with `[ ]` or `[-]` are skipped.
  - If a JSON file with the same id already exists, it is left alone unless
    --force is passed (avoids overwriting editor-curated text).
  - For Policy rows we leave summary_en / policy_relevance blank — those get
    drafted in a second pass with apply_drafts.py-style tooling.

Usage:
  python scripts/ingest_policy_press.py
  python scripts/ingest_policy_press.py not-shared/policy-press-seed.md --force
"""
from __future__ import annotations
import argparse
import json
import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
POLICY_DIR = DATA / "policy"
PRESS_DIR = DATA / "press"
SEED_DEFAULT = ROOT / "not-shared" / "policy-press-seed.md"

POLICY_KIND_DEFAULT = "report"  # if the seed doesn't say


def split_pipe(line: str) -> list[str]:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells


def parse_authors(s: str) -> list[str]:
    """Author column: comma-separated mix of catalogue slugs (e.g. bekes-gabor)
    and plain names (`Carlo Altomonte`). Empty / "TBD" / "—" → []."""
    if not s or s.strip() in {"TBD", "—", "-", "(TBD)", ""}:
        return []
    parts = [p.strip() for p in re.split(r"\s*,\s*", s) if p.strip()]
    return parts


def parse_int_year(s: str) -> int | None:
    if not s:
        return None
    m = re.search(r"\b(19|20)\d{2}\b", s)
    return int(m.group(0)) if m else None


def policy_kind_from_outlet(outlet: str) -> str:
    o = (outlet or "").lower()
    if "working paper" in o or "discussion paper" in o or "wp " in o or " wp" in o:
        return "working_paper"
    if "chapter" in o or "yearbook" in o or "munkaerőpiaci tükör" in o or "ed." in o:
        return "chapter"
    return "report"


def slug_check(s: str) -> str:
    s = (s or "").strip()
    s = re.sub(r"[^a-z0-9\-]", "-", s.lower())
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def parse_seed(path: Path) -> dict:
    """Returns {'policy': [row, ...], 'press': [row, ...]}."""
    txt = path.read_text(encoding="utf-8")
    out = {"policy": [], "press": []}

    section_kind = None  # "policy" | "press" | None
    table_header = None  # list of column names

    for raw in txt.splitlines():
        line = raw.rstrip()

        # Section header: "### Policy" / "### Press"
        m = re.match(r"^###\s+(Policy|Press)\b", line)
        if m:
            section_kind = m.group(1).lower()
            table_header = None
            continue

        # New top-level section resets context
        if re.match(r"^##\s+", line):
            section_kind = None
            table_header = None
            continue

        if section_kind is None:
            continue

        # Table header row
        if line.startswith("|") and "proposed slug" in line.lower():
            table_header = [c.strip().lower() for c in split_pipe(line)]
            continue

        if line.startswith("|---") or line.startswith("|:--"):
            continue  # alignment row

        # Data row
        if line.startswith("|") and table_header:
            cells = split_pipe(line)
            if len(cells) < len(table_header):
                continue
            row = dict(zip(table_header, cells))
            check = (row.get("✓") or row.get("") or "").strip()
            # Accept [x] or [X]
            if not re.match(r"^\[[xX]\]", check):
                continue
            row["_section"] = section_kind
            out[section_kind].append(row)

    return out


def policy_from_row(row: dict) -> dict:
    pid = slug_check(row.get("proposed slug", ""))
    title = row.get("title") or ""
    year = parse_int_year(row.get("year") or "")
    venue = row.get("venue") or ""
    co_authors = parse_authors(row.get("co-authors") or "")
    url = (row.get("url") or "").strip()
    if url == "(TBD)":
        url = None

    # Authors come from <slug-prefix>-<other>-<year> + co-authors col.
    # We rely on the co-authors column to be the full list when ambiguous;
    # the editor is expected to keep slugs there.
    authors = co_authors[:]
    # Heuristic: if pid starts with a slug-like prefix that matches an existing
    # author file, prepend it.
    first_token = pid.split("-")[0]
    candidate = None
    for a in (DATA / "authors").glob("*.json"):
        if a.stem.startswith(f"{first_token}-"):
            candidate = a.stem
            break
    if candidate and candidate not in authors:
        authors.insert(0, candidate)

    outlet_kind = policy_kind_from_outlet(venue)

    today = time.strftime("%Y-%m-%d")
    return {
        "id": pid,
        "title": title,
        "title_hu": None,
        "authors": authors,
        "outlet_kind": outlet_kind,
        "outlet": venue,
        "outlet_issue": None,
        "institution": None,
        "year": year,
        "language": "en" if any(c.isalpha() and ord(c) < 128 for c in title) and not any("á" in title or "é" in title or "ű" in title or "ő" in title for _ in [0]) else "en",
        "url": url,
        "doi": None,
        "summary_en": None,
        "summary_hu": None,
        "policy_relevance": None,
        "policy_relevance_hu": None,
        "topics": [],
        "countries_studied": [],
        "policy_instruments": [],
        "linked_paper_id": None,
        "added_at": today,
        "last_reviewed_at": today,
        "review_status": "metadata-fetched",
    }


def press_from_row(row: dict) -> dict:
    pid = slug_check(row.get("proposed slug", ""))
    title = row.get("title") or ""
    date = (row.get("date") or "").strip()
    venue = row.get("venue") or ""
    kind = (row.get("kind") or "").strip() or "op-ed"
    language = (row.get("language") or "").strip() or None
    url = (row.get("url") or "").strip()
    if url == "(TBD)":
        url = None

    co_authors_col = row.get("co-authors") or ""
    authors = parse_authors(co_authors_col)
    first_token = pid.split("-")[0]
    candidate = None
    for a in (DATA / "authors").glob("*.json"):
        if a.stem.startswith(f"{first_token}-"):
            candidate = a.stem
            break
    if candidate and candidate not in authors:
        authors.insert(0, candidate)

    today = time.strftime("%Y-%m-%d")
    return {
        "id": pid,
        "title": title,
        "authors": authors,
        "kind": kind,
        "venue": venue,
        "date": date or None,
        "language": language,
        "url": url,
        "blurb": None,
        "linked_paper_id": None,
        "added_at": today,
        "last_reviewed_at": today,
    }


def write_json(target: Path, payload: dict, force: bool) -> str:
    if target.exists() and not force:
        return "skip-exists"
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return "written"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("seed", nargs="?", default=str(SEED_DEFAULT))
    ap.add_argument("--force", action="store_true", default=False)
    args = ap.parse_args()

    seed_path = Path(args.seed)
    if not seed_path.exists():
        raise SystemExit(f"seed not found: {seed_path}")

    POLICY_DIR.mkdir(exist_ok=True)
    PRESS_DIR.mkdir(exist_ok=True)

    parsed = parse_seed(seed_path)

    pol_w = pol_s = 0
    for r in parsed["policy"]:
        item = policy_from_row(r)
        if not item["id"]:
            continue
        out = POLICY_DIR / f"{item['id']}.json"
        result = write_json(out, item, args.force)
        if result == "written":
            pol_w += 1
            print(f"policy: {item['id']}")
        else:
            pol_s += 1

    pr_w = pr_s = 0
    for r in parsed["press"]:
        item = press_from_row(r)
        if not item["id"]:
            continue
        out = PRESS_DIR / f"{item['id']}.json"
        result = write_json(out, item, args.force)
        if result == "written":
            pr_w += 1
            print(f"press:  {item['id']}")
        else:
            pr_s += 1

    print(f"\npolicy: wrote {pol_w}, skipped {pol_s}")
    print(f"press:  wrote {pr_w}, skipped {pr_s}")


if __name__ == "__main__":
    main()
