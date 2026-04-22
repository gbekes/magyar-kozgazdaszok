#!/usr/bin/env python
"""Apply the journal-whitelist rule to data/papers/*.json.

Rule: a paper is KEPT if any of the following holds:
  1. `publication_type` in {chapter} — books / book chapters always kept.
  2. `publication_type == "working_paper"` — only kept if year >= 2023 AND
     (NBER DOI OR `working_paper_series` ∈ {CEPR, NBER, IZA, CESifo}).
  3. `publication_type == "article"` AND journal is on the whitelist
     (matched case-insensitively against the names in data/journals.json,
     with a few common aliases).

Everything else is dropped.

Usage:
  python scripts/apply_journal_whitelist.py --dry-run   # report only
  python scripts/apply_journal_whitelist.py             # delete
  python scripts/apply_journal_whitelist.py --report not-shared/drop.md

Rationale: we want a public-facing catalogue of Q1-level work. The
editor maintains `data/journals.json` as a positive list; the admission
rule for *authors* is separate.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent
PAPERS = ROOT / "data" / "papers"
JOURNALS = ROOT / "data" / "journals.json"

QUALIFYING_WP_SERIES = {"CEPR", "NBER", "IZA", "CESifo"}

# Aliases / alternate spellings OpenAlex/Crossref emit. Map any variant to
# a canonical whitelisted name (all keys lowercase, stripped).
ALIASES = {
    "the review of economic studies": "Review of Economic Studies",
    "the quarterly journal of economics": "Quarterly Journal of Economics",
    "the journal of finance": "Journal of Finance",
    "journal of finance": "Journal of Finance",
    "the journal of business and economic statistics": "Journal of Business and Economic Statistics",
    "the review of economics and statistics": "Review of Economics and Statistics",
    "the economic journal": "Economic Journal",
    "the journal of economic perspectives": "Journal of Economic Perspectives",
    "the journal of economic education": None,  # pedagogical — not whitelisted
    "journal of economic perspectives": "Journal of Economic Perspectives",
    "journal of economic literature": "Journal of Economic Literature",
    "american economic journal applied economics": "American Economic Journal: Applied Economics",
    "american economic journal microeconomics": "American Economic Journal: Microeconomics",
    "american economic journal macroeconomics": "American Economic Journal: Macroeconomics",
    "american economic journal economic policy": "American Economic Journal: Economic Policy",
    "american economic review insights": "American Economic Review: Insights",
    "review of world economics": "Review of World Economics",
    "the world economy": "World Economy",
    "the rand journal of economics": "RAND Journal of Economics",
    "the annals of regional science": "The Annals of Regional Science",
    "journal of economic behavior & organization": "Journal of Economic Behavior and Organization",
    "journal of banking & finance": "Journal of Banking & Finance",
    "canadian journal of economics/revue canadienne d économique": "Canadian Journal of Economics",
    "canadian journal of economics": "Canadian Journal of Economics",
    "journal of money credit and banking": "Journal of Money, Credit and Banking",
    "european finance review": "Review of Finance",  # historical name
    "international review of economics & finance": "International Review of Economics & Finance",
    "the b e journal of economic analysis & policy": "The B.E. Journal of Economic Analysis & Policy",
    "b e journal of economic analysis & policy": "The B.E. Journal of Economic Analysis & Policy",
    "the b e journal of macroeconomics": "The B.E. Journal of Macroeconomics",
    "b e journal of macroeconomics": "The B.E. Journal of Macroeconomics",
    "the b e journal of theoretical economics": "The B.E. Journal of Theoretical Economics",
    "b e journal of theoretical economics": "The B.E. Journal of Theoretical Economics",
    "finance research letters": "Finance Research Letters",
    "the journal of business": None,  # defunct / not flagship
    "journal of business finance &amp accounting": None,  # not listed
    "journal of business finance & accounting": None,
    "eurasian economic review": None,
    "eurasian economic review :": None,
    "emerging markets review": None,
    "kellogg school of management cases": None,
    "staff papers": None,
    "mnb bulletin (discontinued)": None,
    "mnb bulletin": None,
    "pénzügyi szemle = public finance quarterly": None,  # editor-flag: keep?
    "acta oeconomica": None,
    "tér és társadalom": None,
    "területi statisztika": None,
    "regional statistics": None,
    "magyar tudomány": None,
    "egészségfejlesztés": None,
    "alkalmazott matematikai lapok": None,
    "belügyi szemle": None,
    "demográfia": None,
    "scientometrics": None,
    "scientific reports": None,
    "royal society open science": None,
    "plos one": None,
    "nature communications": "Nature Communications",
    "science advances": "Science Advances",
    "epj data science": None,
    "tijdschrift voor economische en sociale geografie": None,
    "european journal of population / revue européenne de démographie": "European Journal of Population",
    "european journal of population": "European Journal of Population",
    "social indicators research": None,
    "social science research": None,
    "european sociological review": None,
    "rationality and society": None,
    "review of sociology": None,
    "social networks": None,
    "social problems": None,
    "social network analysis and mining": None,
    "applied network science": None,
    "network science": None,
    "entropy": None,
    "omega": None,  # OR — included? keep or drop? we include EJOR only
    "annals of operations research": "Annals of Operations Research",
    "operations research letters": "Operations Research Letters",
    "central european journal of operations research": None,  # second tier OR
    "mathematical social sciences": None,
    "journal of ethnic and migration studies": None,
    "learning and teaching": None,
    "epidemics": None,
    "preventive medicine": None,
    "food policy": None,
    "energy strategy reviews": None,
    "energy policy": None,
    "cities": None,
    "region et developpement": None,
    "science and public policy": None,
    "environment and planning b urban analytics and city science": None,
    "parasitology": None,
    "international journal for parasitology": None,
    "international journal of computers and applications": None,
    "international journal of parallel programming": None,
    "international journal of agent technologies and systems": None,
    "agent-directed simulation": None,
    "central and eastern european edem and egov days": None,
    "corporate governance an international review": "Corporate Governance: An International Review",
    "information economics and policy": None,
    "journal of informetrics": None,
    "advances in theoretical economics": None,
    "economic theory bulletin": None,
    "computers & operations research": None,
    "technology analysis and strategic management": None,
    "das gesundheitswesen": None,
    "current green chemistry": None,
    "tectonophysics": None,
    "concreto & construções": None,
    "physica status solidi (a)": None,
    "physica status solidi (b)": None,
    "periodica polytechnica mechanical engineering": None,
    "statistics & probability letters": None,
    "journal of nonparametric statistics": None,
    "advances in life course research": None,
    "review of economics of the household": None,
    "oxford review of education": None,
    "education economics": None,
    "economics of education review": None,
    "early childhood research quarterly": None,
    "on education journal for research and debate": None,
    "international journal of health economics and management": None,
    "international journal of migration health and social care": None,
    "bmj open": None,
    "bmc public health": None,
    "european journal of public health": None,
    "european journal of ageing": None,
    "scandinavian journal of public health": None,
    "world medical & health policy": None,
    "health policy": None,  # editor flag — keep?
    "journal of small business and enterprise development": None,
    "industrial and labor relations review": "Industrial and Labor Relations Review",
    "the warwick economics research paper series (twerps)": None,  # WP series
    "economic and business review": None,
    "european business review": None,
    "marketing letters": None,
    "8th annual conference of the american society of health economists": None,
    "asian development review": None,
    "games": None,
    "cosp": None,
    "ifac proceedings volumes": None,
    "2004 meeting papers": None,
    "2005 meeting papers": None,
    "2008 meeting papers": None,
    "2009 meeting papers": None,
    "2010 meeting papers": None,
    "2013 meeting papers": None,
    "2017 meeting papers": None,
    "2018 conference, july 28-august 2, 2018, vancouver, british columbia": None,
    "transition studies review": None,
    "regional statistics": None,
    "international journal of computers and applications": None,
    "international journal of migration health and social care": None,
    "manchester school": "Manchester School",
    "eastern european economics": None,
    "journal of economic science research": None,
    "staff papers": None,
    "journal of business cycle measurement and analysis": None,
    "rivista di politica economica": None,
    "international economics": None,
    "international journal of forecasting": "International Journal of Forecasting",
    "economic systems": "Economic Systems",
    "emerging markets finance and trade": "Emerging Markets Finance and Trade",
    "health policy": "Health Policy",
    "international journal of health economics and management": "International Journal of Health Economics and Management",
}


def _norm(s: str) -> str:
    s = (s or "").lower().strip()
    s = s.replace(".", " ")
    s = re.sub(r"\s+", " ", s).strip()
    # Strip a leading "the " — OpenAlex/Crossref are inconsistent about it.
    if s.startswith("the "):
        s = s[4:]
    return s


def load_whitelist() -> set[str]:
    j = json.loads(JOURNALS.read_text(encoding="utf-8"))
    return {_norm(x["name"]) for x in j}


def is_whitelisted(journal: str, wl: set[str]) -> bool:
    if not journal:
        return False
    nj = _norm(journal)
    if nj in wl:
        return True
    alias = ALIASES.get(nj)
    if alias is None and nj in ALIASES:
        return False  # explicitly excluded alias
    if alias:
        return _norm(alias) in wl
    return False


def classify(p: dict, wl: set[str]) -> tuple[str, str]:
    """Return (action, reason) where action in {"keep","drop"}."""
    ptype = p.get("publication_type")
    year = p.get("year") or 0
    doi = p.get("doi") or ""
    series = p.get("working_paper_series")
    j = p.get("journal") or ""

    if ptype == "chapter":
        return ("keep", "book chapter")
    if ptype == "working_paper":
        if year >= 2023 and ("10.3386/" in doi or series in QUALIFYING_WP_SERIES):
            return ("keep", f"qualifying WP ({series or 'NBER'})")
        return ("drop", f"WP not in qualifying series (year={year}, series={series})")
    # article
    if is_whitelisted(j, wl):
        return ("keep", f"journal on whitelist: {j}")
    return ("drop", f"journal not whitelisted: {j or '(none)'}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", default=False)
    ap.add_argument("--report", default=None,
                    help="Also write a markdown report to this path.")
    args = ap.parse_args()

    wl = load_whitelist()
    print(f"whitelist: {len(wl)} journals\n")

    drops = []
    keeps = 0
    for pth in sorted(PAPERS.glob("*.json")):
        d = json.loads(pth.read_text(encoding="utf-8"))
        if d.get("review_status") in ("human-reviewed", "author-approved"):
            keeps += 1
            continue
        action, reason = classify(d, wl)
        if action == "keep":
            keeps += 1
            continue
        drops.append((pth, d, reason))

    print(f"Would keep: {keeps}")
    print(f"Would drop: {len(drops)}\n")

    # Group by reason (journal name)
    from collections import Counter
    reasons = Counter(r for _, _, r in drops)
    print("Top drop reasons:")
    for r, n in reasons.most_common(30):
        print(f"  {n:4d}  {r}")

    if args.report:
        rep = Path(args.report)
        rep.parent.mkdir(exist_ok=True)
        lines = [f"# Journal-whitelist drop report",
                 f"",
                 f"- Whitelist: {len(wl)} journals",
                 f"- Would keep: {keeps} papers",
                 f"- Would drop: {len(drops)} papers",
                 f"",
                 f"## Drops grouped by journal",
                 f""]
        by_journal: dict[str, list] = {}
        for pth, d, reason in drops:
            key = d.get("journal") or "(no journal)"
            by_journal.setdefault(key, []).append(d)
        for jname in sorted(by_journal, key=lambda k: -len(by_journal[k])):
            papers = by_journal[jname]
            lines.append(f"### {jname} ({len(papers)})")
            lines.append("")
            for d in papers[:20]:
                y = d.get("year") or "?"
                t = (d.get("title") or "")[:100]
                lines.append(f"- `{d['id']}` | {y} | {t}")
            if len(papers) > 20:
                lines.append(f"- … and {len(papers) - 20} more")
            lines.append("")
        rep.write_text("\n".join(lines), encoding="utf-8")
        print(f"\nWrote report to {rep}")

    if not args.dry_run:
        for pth, _, _ in drops:
            pth.unlink()
        print(f"\nDeleted {len(drops)} papers.")
    else:
        print("\n(dry-run: nothing deleted. Pass no --dry-run to apply.)")


if __name__ == "__main__":
    main()
