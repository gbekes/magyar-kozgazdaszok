"""For each catalogue paper that has NO DOI, search OpenAlex by title
(filtered by year) and report whether a plausible match exists. Flags
papers where no match is found — those are candidates for editor review
or removal.

Usage:
    python scripts/verify_no_doi_papers.py

Output: pdf-lists/no-doi-verification-report.md
"""
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
REPORT = ROOT / "pdf-lists" / "no-doi-verification-report.md"


def normalize(s):
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


def title_similarity(a, b):
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()


def search_openalex(title, year=None):
    q = urllib.parse.quote(title)
    url = f"https://api.openalex.org/works?search={q}&per_page=5&mailto=bekesg@ceu.edu"
    if year:
        url += f"&filter=publication_year:{year}"
    req = urllib.request.Request(url, headers={"User-Agent": "magyar-kozgazdaszok-no-doi-verifier"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.load(r)
    except Exception as e:
        return []
    cands = []
    for w in data.get("results", []):
        oa_title = w.get("title") or w.get("display_name") or ""
        cands.append({
            "openalex_id": w.get("id"),
            "doi": (w.get("doi") or "").removeprefix("https://doi.org/"),
            "title": oa_title,
            "year": w.get("publication_year"),
            "host": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
            "similarity": title_similarity(title, oa_title),
        })
    cands.sort(key=lambda c: -c["similarity"])
    return cands


def main():
    no_doi = []
    for f in sorted(PAPERS.glob("*.json")):
        p = json.loads(f.read_text(encoding="utf-8"))
        if not p.get("doi"):
            no_doi.append(p)
    print(f"Verifying {len(no_doi)} papers without DOI...")

    found = []
    weak = []
    not_found = []

    for i, p in enumerate(no_doi):
        cands = search_openalex(p.get("title", ""), year=p.get("year"))
        time.sleep(0.12)

        best = cands[0] if cands else None
        sim = best["similarity"] if best else 0
        entry = {"paper": p, "best": best, "sim": sim}

        if sim >= 0.85:
            found.append(entry)
            tag = "FOUND"
        elif sim >= 0.50:
            weak.append(entry)
            tag = "WEAK"
        else:
            not_found.append(entry)
            tag = "NONE"
        print(f"  [{i+1}/{len(no_doi)}] {tag} sim={sim:.2f} {p['id']}")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Papers without DOI — verification report", ""]
    lines.append(f"Checked: {len(no_doi)}")
    lines.append(f"Found in OpenAlex (sim >= 0.85): {len(found)}")
    lines.append(f"Weak match (0.50-0.85): {len(weak)}")
    lines.append(f"No match (< 0.50): {len(not_found)}")
    lines.append("")

    if not_found:
        lines.append("## No match found — editor review needed")
        lines.append("")
        for e in not_found:
            p = e["paper"]
            lines.append(f"### {p['id']}")
            lines.append(f"- title: {p.get('title')}")
            lines.append(f"- journal: {p.get('journal')} ({p.get('year')})")
            lines.append(f"- type: {p.get('publication_type')}")
            lines.append(f"- review_status: {p.get('review_status')}")
            if e["best"]:
                lines.append(f"- closest OpenAlex match: sim={e['sim']:.2f} `{e['best']['doi']}` — {e['best']['title']}")
            lines.append("")

    if weak:
        lines.append("## Weak match — needs review")
        lines.append("")
        for e in weak:
            p = e["paper"]
            b = e["best"]
            lines.append(f"### {p['id']} (sim={e['sim']:.2f})")
            lines.append(f"- our title: {p.get('title')}")
            lines.append(f"- our journal: {p.get('journal')} ({p.get('year')})")
            lines.append(f"- OpenAlex closest: `{b['doi']}` ({b['year']}, {b['host']}) — {b['title']}")
            lines.append("")

    if found:
        lines.append("## Found in OpenAlex (DOI available)")
        lines.append("")
        for e in found:
            p = e["paper"]
            b = e["best"]
            lines.append(f"- {p['id']}: would gain DOI `{b['doi']}` (sim={e['sim']:.2f})")
        lines.append("")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport: {REPORT.relative_to(ROOT)}")
    print(f"Found: {len(found)} | Weak: {len(weak)} | None: {len(not_found)}")


if __name__ == "__main__":
    main()
