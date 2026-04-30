#!/usr/bin/env python
"""Aggregate summary across authors. Produces a ranked table.

Usage:
  python .claude/skills/audit-author/bulk_audit_summary.py --pattern '^[a-d]'
"""
from __future__ import annotations
import sys, json, glob, re, argparse
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[3]


def load(p):
    return json.load(open(p, encoding="utf-8"))


def authors_in(d):
    a = d.get("authors") or []
    return [x for x in a if isinstance(x, str)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pattern", default="^[a-d]")
    args = ap.parse_args()
    rx = re.compile(args.pattern)

    rows = []
    pap_index = {f: load(f) for f in (ROOT / "data" / "papers").glob("*.json")}
    pol_index = {f: load(f) for f in (ROOT / "data" / "policy").glob("*.json")}
    prs_index = {f: load(f) for f in (ROOT / "data" / "press").glob("*.json")}

    for af in sorted((ROOT / "data" / "authors").glob("*.json")):
        slug = af.stem
        if not rx.search(slug):
            continue
        a = load(af)
        pap = [d for d in pap_index.values() if slug in authors_in(d)]
        pol = [d for d in pol_index.values() if slug in authors_in(d)]
        prs = [d for d in prs_index.values() if slug in authors_in(d)]
        p_meta = sum(1 for p in pap if p.get("review_status") == "metadata-fetched")
        p_drafted_no_hu = sum(1 for p in pap if p.get("summary_en") and not p.get("summary_hu"))
        pol_undrafted = sum(1 for p in pol if not p.get("summary_en"))
        rows.append({
            "slug": slug,
            "papers": len(pap),
            "policy": len(pol),
            "press": len(prs),
            "P1_en": p_meta,
            "P2_hu": p_drafted_no_hu,
            "P3_pol": pol_undrafted,
            "repec": "Y" if a.get("repec_id") else "N",
            "photo": "Y" if a.get("photo_url") else "N",
            "qp": "Y" if a.get("qualifying_publication") else "N",
            "review": a.get("review_status") or "null",
            "fields_filled": sum(1 for k in ["name_en","name_hu","affiliations","website","email","repec_id","scholar_id","orcid","primary_fields","bio_en","bio_hu","photo_url","qualifying_publication"] if a.get(k)),
        })

    rows.sort(key=lambda r: -(r["P1_en"] + r["P2_hu"] + r["P3_pol"]))

    print(f'{"slug":24s} | pap pol prs | P1  P2  P3 | total | repec photo qp | flds review_status')
    print("-" * 110)
    for r in rows:
        total = r["P1_en"] + r["P2_hu"] + r["P3_pol"]
        print(f'{r["slug"]:24s} | {r["papers"]:3d} {r["policy"]:3d} {r["press"]:3d} | '
              f'{r["P1_en"]:2d}  {r["P2_hu"]:2d}  {r["P3_pol"]:2d} | {total:5d} | '
              f'{r["repec"]:5s} {r["photo"]:5s} {r["qp"]:2s} | {r["fields_filled"]:2d}/13 {r["review"]}')

    print()
    print("TOTALS")
    print(f'  authors:            {len(rows)}')
    print(f'  papers in catalogue: {sum(r["papers"] for r in rows)}')
    print(f'  policy in catalogue: {sum(r["policy"] for r in rows)}')
    print(f'  press in catalogue:  {sum(r["press"] for r in rows)}')
    print(f'  P1 EN drafts to write:    {sum(r["P1_en"] for r in rows)}')
    print(f'  P2 HU translations:       {sum(r["P2_hu"] for r in rows)}')
    print(f'  P3 Policy summaries:      {sum(r["P3_pol"] for r in rows)}')
    print(f'  authors with repec_id:    {sum(1 for r in rows if r["repec"]=="Y")}/{len(rows)}')
    print(f'  authors with photo:       {sum(1 for r in rows if r["photo"]=="Y")}/{len(rows)}')
    print(f'  authors with qualifying_publication: {sum(1 for r in rows if r["qp"]=="Y")}/{len(rows)}')


if __name__ == "__main__":
    main()
