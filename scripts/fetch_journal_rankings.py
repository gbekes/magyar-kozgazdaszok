"""Fetch OpenAlex source-level metrics for every distinct journal that
appears in the catalogue. Output: data/journal-rankings.json -- one row
per journal, with h_index, 2-year mean citedness, works/cites counts,
country, publisher, etc.

These metrics give us a quality proxy comparable to Scimago's SJR/quartile.
They are programmatically retrievable (no Cloudflare wall) and updated
continuously by OpenAlex.

Usage:
    python scripts/fetch_journal_rankings.py
    python scripts/fetch_journal_rankings.py --no-refresh   # only re-process
"""
import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "data" / "papers"
WHITELIST = ROOT / "journals.json"
OUT = ROOT / "data" / "journal-rankings.json"

OPENALEX_SEARCH = "https://api.openalex.org/sources?search={q}&per_page=5&mailto=bekesg@ceu.edu"
OPENALEX_BY_ID = "https://api.openalex.org/sources/{id}?mailto=bekesg@ceu.edu"


def normalize(s):
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "magyar-kozgazdaszok-journal-ranker"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r)
    except Exception as e:
        return {"_error": str(e)}


def best_match(jname, results):
    """Pick the OpenAlex source whose display_name best matches our journal name."""
    target = normalize(jname)
    best = None
    best_score = -1
    for s in results:
        name = s.get("display_name") or ""
        n = normalize(name)
        # Prefer exact normalized match
        if n == target:
            return s
        # Substring score
        score = 0
        if target in n or n in target:
            score = min(len(target), len(n)) / max(len(target), len(n))
        if score > best_score:
            best_score = score
            best = s
    if best_score >= 0.8:
        return best
    return None


def collect_journals():
    """Gather every distinct journal name from data/papers/*.json plus the
    whitelist. Returns dict: journal_name -> count of papers."""
    counts = Counter()
    for f in PAPERS.glob("*.json"):
        p = json.loads(f.read_text(encoding="utf-8"))
        if p.get("journal"):
            counts[p["journal"]] += 1
    # Also include whitelist entries that may have zero catalogue papers
    if WHITELIST.exists():
        for j in json.loads(WHITELIST.read_text(encoding="utf-8")):
            if j.get("name") and j["name"] not in counts:
                counts[j["name"]] = 0
    return counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-refresh", action="store_true",
                    help="Don't refetch entries already in the output file")
    args = ap.parse_args()

    journals = collect_journals()
    print(f"Distinct journals to look up: {len(journals)}")

    existing = {}
    if OUT.exists():
        try:
            for row in json.loads(OUT.read_text(encoding="utf-8")):
                existing[row["name"]] = row
        except Exception:
            existing = {}

    rows = []
    misses = []
    for i, (jname, papers_count) in enumerate(sorted(journals.items())):
        if args.no_refresh and jname in existing:
            rows.append(existing[jname])
            continue

        results = fetch(OPENALEX_SEARCH.format(q=urllib.parse.quote(jname)))
        time.sleep(0.12)
        if "_error" in results:
            print(f"  [{i+1}/{len(journals)}] ERROR {jname}: {results['_error']}")
            misses.append(jname)
            rows.append({"name": jname, "papers_in_catalogue": papers_count, "openalex": None})
            continue

        match = best_match(jname, results.get("results", []))
        if not match:
            misses.append(jname)
            rows.append({"name": jname, "papers_in_catalogue": papers_count, "openalex": None})
            print(f"  [{i+1}/{len(journals)}] no match: {jname}")
            continue

        sm = match.get("summary_stats") or {}
        bio = {}
        row = {
            "name": jname,
            "papers_in_catalogue": papers_count,
            "openalex": {
                "id": (match.get("id") or "").removeprefix("https://openalex.org/"),
                "display_name": match.get("display_name"),
                "type": match.get("type"),
                "issn_l": match.get("issn_l"),
                "issn": match.get("issn"),
                "host_organization_name": match.get("host_organization_name"),
                "country_code": match.get("country_code"),
                "is_oa": match.get("is_oa"),
                "works_count": match.get("works_count"),
                "cited_by_count": match.get("cited_by_count"),
                "h_index": sm.get("h_index"),
                "two_yr_mean_citedness": sm.get("2yr_mean_citedness"),
                "i10_index": sm.get("i10_index"),
            },
        }
        rows.append(row)
        print(f"  [{i+1}/{len(journals)}] {jname[:40]:40} h={sm.get('h_index') or '-':>4} 2y={sm.get('2yr_mean_citedness'):.2f}" if sm.get('2yr_mean_citedness') is not None else f"  [{i+1}/{len(journals)}] {jname[:40]:40} h={sm.get('h_index') or '-':>4}")

    rows.sort(key=lambda r: -((r.get("openalex") or {}).get("h_index") or 0))
    OUT.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    matched = sum(1 for r in rows if r.get("openalex"))
    print()
    print(f"Wrote {OUT.relative_to(ROOT)}: {len(rows)} journals, {matched} matched, {len(misses)} unmatched")


if __name__ == "__main__":
    main()
