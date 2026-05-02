"""Verify that the DOI on each catalogue paper resolves to a work whose
title matches our stored title. Hits OpenAlex (free, no auth) for each DOI.

Usage:
    python scripts/verify_dois.py [--pattern <substr>] [--all] [--no-openalex]

By default checks every paper that has a DOI but NO openalex_id (the risky
pool). With --all, checks every paper that has a DOI. With --pattern,
checks only papers whose id contains the substring.

Reports mismatches to pdf-lists/doi-verification-report.md and stdout.
Does not mutate JSON.
"""
import argparse
import json
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from difflib import SequenceMatcher

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "data" / "papers"
REPORT = ROOT / "pdf-lists" / "doi-verification-report.md"

OPENALEX = "https://api.openalex.org/works/doi:{doi}?mailto=bekesg@ceu.edu"


def normalize(s):
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


def title_similarity(a, b):
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()


def fetch_openalex(doi):
    url = OPENALEX.format(doi=doi)
    req = urllib.request.Request(url, headers={"User-Agent": "magyar-kozgazdaszok-doi-verifier"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {"_error": f"HTTP {e.code}"}
    except Exception as e:
        return {"_error": str(e)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pattern", default=None)
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()

    targets = []
    for f in sorted(PAPERS.glob("*.json")):
        p = json.loads(f.read_text(encoding="utf-8"))
        if not p.get("doi"):
            continue
        if args.pattern and args.pattern not in p["id"]:
            continue
        if not args.all and p.get("openalex_id"):
            continue
        targets.append((f, p))

    print(f"Checking {len(targets)} papers...")

    matches = []
    mismatches = []
    not_found = []
    errors = []

    for i, (f, p) in enumerate(targets):
        doi = p["doi"]
        our_title = p.get("title", "")
        oa = fetch_openalex(doi)
        time.sleep(0.12)  # gentle on the API; OpenAlex polite-pool is fine

        if "_error" in oa:
            if "404" in oa["_error"]:
                not_found.append((p["id"], doi, our_title))
                print(f"  [{i+1}/{len(targets)}] {p['id']}: 404 not found")
            else:
                errors.append((p["id"], doi, oa["_error"]))
                print(f"  [{i+1}/{len(targets)}] {p['id']}: {oa['_error']}")
            continue

        oa_title = oa.get("title", "") or oa.get("display_name", "")
        sim = title_similarity(our_title, oa_title)

        if sim >= 0.80:
            matches.append((p["id"], doi, sim))
        else:
            mismatches.append({
                "id": p["id"],
                "doi": doi,
                "our_title": our_title,
                "openalex_title": oa_title,
                "openalex_id": oa.get("id"),
                "similarity": sim,
            })
            print(f"  [{i+1}/{len(targets)}] MISMATCH {p['id']} sim={sim:.2f}")
            print(f"      ours: {our_title[:80]}")
            print(f"      OpenAlex: {oa_title[:80]}")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    lines.append("# DOI verification report")
    lines.append("")
    lines.append(f"Checked: {len(targets)} papers")
    lines.append(f"Matched (similarity >= 0.80): {len(matches)}")
    lines.append(f"Mismatched: {len(mismatches)}")
    lines.append(f"DOI not found in OpenAlex: {len(not_found)}")
    lines.append(f"Errors: {len(errors)}")
    lines.append("")
    if mismatches:
        lines.append("## Mismatches (DOI title differs from catalogue title)")
        lines.append("")
        for m in sorted(mismatches, key=lambda x: x["similarity"]):
            lines.append(f"### {m['id']}  (sim={m['similarity']:.2f})")
            lines.append(f"- our title: {m['our_title']}")
            lines.append(f"- OpenAlex title: {m['openalex_title']}")
            lines.append(f"- our DOI: `{m['doi']}`")
            lines.append(f"- OpenAlex id: {m['openalex_id']}")
            lines.append("")
    if not_found:
        lines.append("## DOIs not found in OpenAlex")
        lines.append("")
        for slug, doi, title in not_found:
            lines.append(f"- {slug}: `{doi}` — {title}")
        lines.append("")
    if errors:
        lines.append("## Lookup errors")
        lines.append("")
        for slug, doi, err in errors:
            lines.append(f"- {slug}: `{doi}` — {err}")
        lines.append("")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print()
    print(f"Report written: {REPORT.relative_to(ROOT)}")
    print(f"Matches: {len(matches)} | Mismatches: {len(mismatches)} | Not found: {len(not_found)} | Errors: {len(errors)}")


if __name__ == "__main__":
    main()
