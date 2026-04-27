#!/usr/bin/env python
"""Bulk audit-author runner. Read-only, local-data only.

Usage:
  python .claude/skills/audit-author/bulk_audit.py <slug> [<slug> ...]
  python .claude/skills/audit-author/bulk_audit.py --pattern '^[a-d]'

Produces one terse block per author. No web fetches; the per-author
RePEc and external-coverage checks are run separately (this is the
fast scan).
"""
from __future__ import annotations
import json, sys, re, glob, argparse
from pathlib import Path
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[3]
AUTHORS = ROOT / "data" / "authors"
PAPERS = ROOT / "data" / "papers"
POLICY = ROOT / "data" / "policy"
PRESS = ROOT / "data" / "press"
JOURNALS = json.load(open(ROOT / "data" / "journals.json", encoding="utf-8"))
JOURNAL_TIER = {e["name"]: e.get("tier", "?") for e in JOURNALS}

PRIORITY_TIER = {"A": 0, "B": 1, "B-hu": 2, "C": 3, "?": 4}

AUTHOR_FIELDS = [
    ("name_en", True), ("name_hu", True),
    ("affiliations", True), ("website", False), ("email", False),
    ("repec_id", False), ("scholar_id", False), ("orcid", False),
    ("primary_fields", True), ("bio_en", True), ("bio_hu", True),
    ("photo_url", False), ("qualifying_publication", False),
]


def load(p: Path) -> dict | None:
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return None


def authors_in(record: dict) -> list[str]:
    a = record.get("authors") or []
    return [x for x in a if isinstance(x, str)]


def has(d: dict, k: str) -> bool:
    v = d.get(k)
    if v is None:
        return False
    if isinstance(v, (list, dict, str)) and len(v) == 0:
        return False
    return True


def affiliation_under_specified(aff_list) -> bool:
    if not aff_list:
        return True
    primary = aff_list[0]
    return not (primary.get("role") and primary.get("start"))


def collect_for(slug: str):
    papers = []
    for f in PAPERS.glob("*.json"):
        d = load(f)
        if not d:
            continue
        if slug in authors_in(d):
            papers.append(d)
    policies = []
    for f in POLICY.glob("*.json"):
        d = load(f)
        if not d:
            continue
        if slug in authors_in(d):
            policies.append(d)
    presses = []
    for f in PRESS.glob("*.json"):
        d = load(f)
        if not d:
            continue
        if slug in authors_in(d):
            presses.append(d)
    return papers, policies, presses


def best_qualifying_pub(papers: list[dict]) -> dict | None:
    cand = []
    for p in papers:
        j = p.get("journal") or ""
        t = JOURNAL_TIER.get(j, "?")
        if t in ("A", "B"):
            cand.append((PRIORITY_TIER[t], -(p.get("year") or 0), p))
    if not cand:
        # fall back to B-hu
        for p in papers:
            j = p.get("journal") or ""
            t = JOURNAL_TIER.get(j, "?")
            if t == "B-hu":
                cand.append((PRIORITY_TIER[t], -(p.get("year") or 0), p))
    if not cand:
        return None
    cand.sort(key=lambda x: (x[0], x[1]))
    p = cand[0][2]
    return {"title": p.get("title"), "journal": p.get("journal"), "year": p.get("year")}


def admission_check(papers: list[dict]) -> tuple[bool, int, int, list[str]]:
    """SPEC §1.2 (AND rule, 2026-04-27):
       (i) ≥1 paper in Tier A/B journal AND
       (ii) ≥3 publications in international good journals
            (= on journals.json, any tier except B-hu, publication_type=article).
    """
    tier_ab = 0
    intl_good = 0
    tier_ab_titles = []
    for p in papers:
        if p.get("publication_type") != "article":
            continue
        j = p.get("journal") or ""
        t = JOURNAL_TIER.get(j)
        if t is None:
            continue  # journal not on the whitelist → not "good"
        if t == "B-hu":
            continue  # Hungarian-language outlet, not "international"
        intl_good += 1
        if t in ("A", "B"):
            tier_ab += 1
            tier_ab_titles.append(f"{j} ({p.get('year')})")
    qualifies = tier_ab >= 1 and intl_good >= 3
    return qualifies, tier_ab, intl_good, tier_ab_titles


def audit_one(slug: str) -> str:
    af = AUTHORS / f"{slug}.json"
    if not af.exists():
        return f"## {slug}\n  ERROR: data/authors/{slug}.json not found.\n"
    a = load(af)
    if not a:
        return f"## {slug}\n  ERROR: could not parse data/authors/{slug}.json\n"

    name = a.get("name_en") or slug
    papers, policies, presses = collect_for(slug)
    qualifies, tier_ab_n, intl_n, tier_ab_titles = admission_check(papers)

    # field completeness
    missing_fields = []
    for k, _ in AUTHOR_FIELDS:
        if not has(a, k):
            missing_fields.append(k)
    aff_under = affiliation_under_specified(a.get("affiliations") or [])

    # paper drafts
    paper_total = len(papers)
    paper_metaonly = sum(1 for p in papers if p.get("review_status") == "metadata-fetched")
    paper_drafted = sum(1 for p in papers if has(p, "summary_en"))
    paper_hu = sum(1 for p in papers if has(p, "summary_hu"))
    drafted_no_hu = sum(1 for p in papers if has(p, "summary_en") and not has(p, "summary_hu"))
    paper_doi_missing = [p["id"] for p in papers if not has(p, "doi") and p.get("publication_type") == "article"]
    paper_tbd = [p["id"] for p in papers if any("TBD" in str(x) or "tbd" in str(x).lower() for x in p.get("authors", []))]

    # policy completeness
    pol_total = len(policies)
    pol_summary = sum(1 for p in policies if has(p, "summary_en"))
    pol_polrel = sum(1 for p in policies if has(p, "policy_relevance"))
    pol_summary_hu = sum(1 for p in policies if has(p, "summary_hu"))
    pol_metaonly = [p["id"] for p in policies if p.get("review_status") == "metadata-fetched"]

    # press completeness
    press_total = len(presses)
    press_hu_origin = [p for p in presses if p.get("language") == "hu"]
    press_hu_origin_no_titlehu = [p["id"] for p in press_hu_origin if not has(p, "title_hu")]
    press_no_title_en = [p["id"] for p in presses if not has(p, "title")]
    press_no_link = sum(1 for p in presses if not has(p, "linked_paper_id"))

    # qualifying publication suggestion
    qp_suggest = None
    if not has(a, "qualifying_publication"):
        qp_suggest = best_qualifying_pub(papers)

    # build output block
    lines = []
    lines.append(f"## {slug}  ({name})")
    if not qualifies:
        lines.append(f"  ⚠ ADMISSION RULE FAIL (SPEC §1.2 AND): "
                     f"tier A/B papers = {tier_ab_n} (need ≥1), "
                     f"international good-journal papers = {intl_n} (need ≥3) — flag for editor")
    lines.append(f"  filled fields: {sum(1 for k,_ in AUTHOR_FIELDS if has(a,k))}/13"
                 f"  | review_status: {a.get('review_status') or 'null'}"
                 f"  | repec_id: {a.get('repec_id') or 'null'}"
                 f"  | photo: {'Y' if has(a,'photo_url') else 'N'}"
                 f"  | tier-A/B: {tier_ab_n}, intl good: {intl_n}")
    lines.append(f"  catalogue: papers {paper_total} ({paper_drafted}/{paper_total} EN draft, {paper_hu}/{paper_total} HU)"
                 f"  | policy {pol_total} ({pol_summary}/{pol_total} EN summary)"
                 f"  | press {press_total}")

    # P1 — research drafts missing
    if paper_metaonly:
        meta_ids = [p["id"] for p in papers if p.get("review_status") == "metadata-fetched"]
        lines.append(f"  [P1] {paper_metaonly} research papers need EN draft:")
        for pid in meta_ids[:8]:
            lines.append(f"        - {pid}")
        if len(meta_ids) > 8:
            lines.append(f"        ... +{len(meta_ids)-8} more")
    # P2 — HU translations missing
    if drafted_no_hu:
        ids = [p["id"] for p in papers if has(p,"summary_en") and not has(p,"summary_hu")]
        lines.append(f"  [P2] {drafted_no_hu} drafted papers need HU translation:")
        for pid in ids[:5]:
            lines.append(f"        - {pid}")
        if len(ids) > 5:
            lines.append(f"        ... +{len(ids)-5} more")
    # P3 — policy drafts missing
    if pol_metaonly:
        lines.append(f"  [P3] {len(pol_metaonly)} policy items need EN summary + policy_relevance:")
        for pid in pol_metaonly[:6]:
            lines.append(f"        - {pid}")
        if len(pol_metaonly) > 6:
            lines.append(f"        ... +{len(pol_metaonly)-6} more")
    # P4-P9 — author fields
    af_gaps = []
    if "photo_url" in missing_fields: af_gaps.append("photo_url")
    if "bio_en" in missing_fields:    af_gaps.append("bio_en")
    if "bio_hu" in missing_fields:    af_gaps.append("bio_hu")
    if a.get("review_status") == "stub": af_gaps.append("bio: review_status=stub (rewrite needed)")
    if "qualifying_publication" in missing_fields: af_gaps.append("qualifying_publication")
    if "repec_id" in missing_fields:  af_gaps.append("repec_id")
    if "scholar_id" in missing_fields: af_gaps.append("scholar_id")
    if "orcid" in missing_fields:     af_gaps.append("orcid")
    if "website" in missing_fields:   af_gaps.append("website")
    if "email" in missing_fields:     af_gaps.append("email")
    if aff_under: af_gaps.append("affiliation under-specified (role/start null)")
    if af_gaps:
        lines.append(f"  [P4–P9] author fields missing: {', '.join(af_gaps)}")
    if qp_suggest:
        lines.append(f"        → suggested qualifying_publication: "
                     f"{qp_suggest['journal']!r} ({qp_suggest['year']}) — "
                     f"{(qp_suggest.get('title') or '')[:60]}")
    # P10 — linked_paper_id opportunities (heuristic only)
    if press_total and press_no_link == press_total and paper_total > 0:
        lines.append(f"  [P10] press has 0 linked_paper_id (of {press_total}); spot-check")
    # P11 — HU title gaps for HU-origin press
    if press_hu_origin_no_titlehu:
        lines.append(f"  [P11] {len(press_hu_origin_no_titlehu)} HU-origin press items missing title_hu:")
        for pid in press_hu_origin_no_titlehu[:5]:
            lines.append(f"        - {pid}")
    if press_no_title_en:
        lines.append(f"        {len(press_no_title_en)} press items missing canonical title (EN)")

    # data health
    if paper_doi_missing:
        lines.append(f"  [DH] {len(paper_doi_missing)} articles missing DOI: {', '.join(paper_doi_missing[:3])}{'...' if len(paper_doi_missing)>3 else ''}")
    if paper_tbd:
        lines.append(f"  [DH] {len(paper_tbd)} papers have TBD/unknown co-authors: {', '.join(paper_tbd[:3])}")

    # if nothing to report
    if (not paper_metaonly and not drafted_no_hu and not pol_metaonly
            and not af_gaps and not press_hu_origin_no_titlehu
            and not paper_doi_missing and not paper_tbd
            and not (press_total and press_no_link == press_total and paper_total > 0)):
        lines.append("  ✓ no gaps detected at file-level (RePEc diff + media-scan still pending)")

    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slugs", nargs="*", help="author slugs")
    ap.add_argument("--pattern", help="regex against filename (without .json)")
    args = ap.parse_args()

    slugs = list(args.slugs)
    if args.pattern:
        rx = re.compile(args.pattern)
        for f in sorted(AUTHORS.glob("*.json")):
            stem = f.stem
            if rx.search(stem):
                slugs.append(stem)

    if not slugs:
        print("Usage: bulk_audit.py <slug> [...] | --pattern '^[a-d]'")
        sys.exit(2)

    print(f"# Bulk audit — {len(slugs)} authors\n")
    for s in slugs:
        print(audit_one(s))


if __name__ == "__main__":
    main()
