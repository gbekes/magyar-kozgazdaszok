"""For each paper flagged as a DOI mismatch by verify_dois.py, search
OpenAlex by title and propose the correct DOI. Writes a JSON patch file
ready for review.

Usage:
    python scripts/propose_doi_fixes.py

Reads pdf-lists/doi-verification-report.md to find the mismatch list.
For each mismatched paper, queries OpenAlex by title (filter by year and
authorship if possible) and picks the best match.

Output: pdf-lists/doi-fixes-proposed.json — list of {id, old_doi, new_doi,
new_url, new_openalex_id, our_title, found_title, confidence}.

Does NOT mutate JSON files. Editor reviews, then a separate apply step
writes the changes.
"""
import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from difflib import SequenceMatcher
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "data" / "papers"
REPORT = ROOT / "pdf-lists" / "doi-verification-report.md"
OUT = ROOT / "pdf-lists" / "doi-fixes-proposed.json"


def normalize(s):
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


def title_similarity(a, b):
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()


def search_openalex(title, year=None, author_hint=None):
    """Return up to 5 candidate OpenAlex works ranked by title similarity."""
    q = urllib.parse.quote(title)
    url = f"https://api.openalex.org/works?search={q}&per_page=10&mailto=bekesg@ceu.edu"
    if year:
        url += f"&filter=publication_year:{year}"
    req = urllib.request.Request(url, headers={"User-Agent": "magyar-kozgazdaszok-doi-resolver"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.load(r)
    except Exception as e:
        return []
    candidates = []
    for w in data.get("results", []):
        oa_title = w.get("title") or w.get("display_name") or ""
        sim = title_similarity(title, oa_title)
        candidates.append({
            "openalex_id": w.get("id"),
            "doi": (w.get("doi") or "").removeprefix("https://doi.org/"),
            "title": oa_title,
            "year": w.get("publication_year"),
            "host": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
            "similarity": sim,
        })
    candidates.sort(key=lambda c: -c["similarity"])
    return candidates[:5]


def parse_mismatch_ids(report_path):
    """Pull mismatched paper IDs out of the markdown report."""
    text = report_path.read_text(encoding="utf-8")
    ids = []
    for line in text.splitlines():
        m = re.match(r"### ([\w\-]+)  \(sim=", line)
        if m:
            ids.append(m.group(1))
    return ids


def main():
    if not REPORT.exists():
        print(f"Report not found: {REPORT}. Run verify_dois.py first.")
        return
    target_ids = parse_mismatch_ids(REPORT)
    print(f"Resolving correct DOIs for {len(target_ids)} mismatches...")

    proposals = []
    for i, slug in enumerate(target_ids):
        f = PAPERS / f"{slug}.json"
        if not f.exists():
            continue
        p = json.loads(f.read_text(encoding="utf-8"))
        title = p.get("title", "")
        year = p.get("year")
        cands = search_openalex(title, year=year)
        time.sleep(0.12)

        best = cands[0] if cands else None
        proposal = {
            "id": slug,
            "our_title": title,
            "our_year": year,
            "our_journal": p.get("journal"),
            "old_doi": p.get("doi"),
            "candidates": cands,
            "auto_pick": None,
        }
        # Auto-pick if top candidate is high-similarity AND has a DOI AND year matches
        if best and best["similarity"] >= 0.85 and best["doi"] and (year is None or best["year"] == year):
            proposal["auto_pick"] = {
                "doi": best["doi"],
                "openalex_id": best["openalex_id"],
                "title": best["title"],
                "similarity": best["similarity"],
            }
            print(f"  [{i+1}/{len(target_ids)}] {slug}: AUTO -> {best['doi']} (sim={best['similarity']:.2f})")
        else:
            print(f"  [{i+1}/{len(target_ids)}] {slug}: needs review ({len(cands)} candidates)")
        proposals.append(proposal)

    OUT.write_text(json.dumps(proposals, indent=2, ensure_ascii=False), encoding="utf-8")
    auto = sum(1 for p in proposals if p["auto_pick"])
    print()
    print(f"Wrote {OUT.relative_to(ROOT)}")
    print(f"Auto-pickable: {auto} / {len(proposals)}")


if __name__ == "__main__":
    main()
