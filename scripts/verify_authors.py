#!/usr/bin/env python
"""Check a list of candidate author names against the journals.json admission list.

Usage:
  python scripts/verify_authors.py "Name One" "Name Two" ...

For each name:
  1. Search OpenAlex for the author
  2. Pull their top ~15 works by citations
  3. Flag those whose venue matches any journal on data/journals.json
  4. Print a concise verdict: QUALIFIES (with first matching journal) or NO MATCH.

Purely read-only — creates no files.
"""
from __future__ import annotations
import json, os, re, sys, time, unicodedata
from pathlib import Path
import requests

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).parent.parent
JOURNALS = json.load(open(ROOT / "data" / "journals.json", encoding="utf-8"))

EMAIL = os.environ.get("OPENALEX_EMAIL", "bekesg@ceu.edu")
HEADERS = {"User-Agent": f"EvidenceForHungary/0.1 (mailto:{EMAIL})"}


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s).lower()
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"^the\s+", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


JOURNAL_MAP = {_norm(j["name"]): j for j in JOURNALS}


def search_author(name: str) -> dict | None:
    r = requests.get("https://api.openalex.org/authors",
                     params={"search": name, "per_page": 5, "mailto": EMAIL},
                     headers=HEADERS, timeout=30)
    if not r.ok:
        return None
    results = r.json().get("results", [])
    if not results:
        return None
    # Best of: prefer ones with Hungarian institution in last-known or any
    def score(a):
        inst = (a.get("last_known_institution") or {}).get("display_name", "") or ""
        inst_l = inst.lower()
        hu = any(k in inst_l for k in ["hungar", "krtk", "ceu", "corvinus", "budapest", "eotvos", "debrecen", "szeged", "pecs"])
        return (1 if hu else 0, a.get("works_count", 0))
    results.sort(key=score, reverse=True)
    return results[0]


def top_works(oid: str, n: int = 15) -> list[dict]:
    r = requests.get("https://api.openalex.org/works",
                     params={"filter": f"author.id:{oid}", "sort": "cited_by_count:desc",
                             "per_page": n, "mailto": EMAIL},
                     headers=HEADERS, timeout=30)
    if not r.ok:
        return []
    return r.json().get("results", [])


def venue_name(w: dict) -> str:
    src = (w.get("primary_location") or {}).get("source") or {}
    return src.get("display_name", "") or ""


def check(name: str) -> None:
    a = search_author(name)
    if not a:
        print(f"  {name}: NO OPENALEX HIT")
        return
    inst = (a.get("last_known_institution") or {}).get("display_name", "—")
    oid = a["id"].split("/")[-1]
    works = top_works(oid)
    matches = []
    for w in works[:15]:
        v = venue_name(w)
        if not v:
            continue
        j = JOURNAL_MAP.get(_norm(v))
        if j:
            matches.append((j["short"], j["tier"], w.get("publication_year"), w.get("title", "")[:70]))
    verdict = "QUALIFIES" if matches else "no match"
    print(f"  {name}  [{inst}]  → {verdict}")
    for short, tier, y, t in matches[:3]:
        print(f"      - {short} (Tier {tier}), {y}: {t}")
    time.sleep(0.3)


def main() -> None:
    names = sys.argv[1:]
    if not names:
        print("usage: verify_authors.py \"Name One\" \"Name Two\" ...", file=sys.stderr)
        sys.exit(2)
    for n in names:
        check(n)


if __name__ == "__main__":
    main()
