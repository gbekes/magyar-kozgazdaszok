#!/usr/bin/env python
"""Cross-check the catalogue against an author's RePEc/IDEAS profile.

RePEc lists WPs under their proper series (CEPR DP, NBER WP, IZA DP,
CESifo WP, KRTK-KTI WP, …) and published articles with journal and
year. That makes it the cleanest source for verifying:
  - whether we have an author's real published paper list
  - whether a WP is in a qualifying series (CEPR/NBER/IZA/CESifo)

This tool takes an author_id and their repec_id, fetches the RePEc
page, and prints a side-by-side report vs. what we have in
`data/papers/`. It does not modify any files — output is for the
editor to decide what to add or drop.

Usage:
  python scripts/verify_repec.py bekes-gabor pbk1
  python scripts/verify_repec.py <author_id>           # uses repec_id in author JSON

To find a RePEc ID: visit ideas.repec.org, search for the economist,
take the slug after /e/ in the URL (e.g. pbk1, pli582).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent
AUTHORS_DIR = ROOT / "data" / "authors"
PAPERS_DIR = ROOT / "data" / "papers"


def fetch_repec(repec_id: str) -> str:
    url = f"https://ideas.repec.org/e/{repec_id}.html"
    req = Request(url, headers={"User-Agent": "EvidenceForHungary/0.1 (mailto:bekesg@ceu.edu)"})
    with urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def parse_articles(html: str) -> list[dict]:
    """Pull (year, title, journal) tuples out of the RePEc page's Journal Articles section.

    RePEc's HTML is predictable-ish. Each entry is rendered like:
      <li><a name="...">&</a>1. <a href="...">Békés, G. et al,</a>
      "<i>Favoritism under multiple sources of social pressure</i>,"
      <em>Economic Inquiry</em>, vol. 62(4), pp. 1748-1769, October.</li>

    This parser is deliberately loose — it flags candidates; don't
    trust every match blindly.
    """
    # Restrict to journal-articles block if present
    ja = re.search(
        r"(?is)<h3[^>]*>.*?Journal Articles.*?</h3>(.*?)(?:<h3|\Z)",
        html,
    )
    block = ja.group(1) if ja else html

    items = []
    for m in re.finditer(
        r"(?is)<li[^>]*>.*?<i>(.+?)</i>.*?</li>",
        block,
    ):
        li = m.group(0)
        title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        # Journal is usually in <em>…</em>
        j = re.search(r"<em>(.+?)</em>", li)
        journal = re.sub(r"<[^>]+>", "", j.group(1)).strip() if j else ""
        # Year — pull a 4-digit year from the nearby text
        y = re.search(r"\b(19|20)\d{2}\b", re.sub(r"<[^>]+>", " ", li))
        year = int(y.group(0)) if y else None
        if title:
            items.append({"title": title, "journal": journal, "year": year})
    return items


def catalogue_papers(author_id: str) -> list[dict]:
    out = []
    for p in PAPERS_DIR.glob("*.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        if author_id in (d.get("authors") or []):
            out.append(d)
    return out


def _norm_title(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("author_id")
    ap.add_argument("repec_id", nargs="?", default=None)
    args = ap.parse_args()

    a = json.loads((AUTHORS_DIR / f"{args.author_id}.json").read_text(encoding="utf-8"))
    repec = args.repec_id or a.get("repec_id")
    if not repec:
        sys.exit(f"No repec_id in {args.author_id}.json; pass one as 2nd arg.")

    print(f"=== {a['name_en']} — RePEc: {repec} ===\n")
    html = fetch_repec(repec)
    repec_articles = parse_articles(html)
    print(f"RePEc lists {len(repec_articles)} journal-article candidates.\n")

    have = catalogue_papers(args.author_id)
    have_titles = {_norm_title(p.get("title", "")): p["id"] for p in have}

    missing = []
    for r in repec_articles:
        key = _norm_title(r["title"])
        hit = None
        for t, pid in have_titles.items():
            if key and (key in t or t in key):
                hit = pid
                break
        if not hit:
            missing.append(r)

    print(f"In catalogue for this author: {len(have)} papers.\n")
    if missing:
        print(f"Likely missing ({len(missing)}):")
        for r in missing[:30]:
            y = r["year"] or "?"
            print(f"  {y} | {r['journal'][:35]:35s} | {r['title'][:80]}")
    else:
        print("No obvious missing articles.")


if __name__ == "__main__":
    main()
