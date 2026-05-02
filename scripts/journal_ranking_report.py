"""Build a markdown report from data/journal-rankings.json showing every
journal in the catalogue ranked by h-index, with paper counts and how
each whitelist tier maps to the ranking.

Output: pdf-lists/journal-ranking-report.md

Helps the editor pick a cutoff (e.g. h-index >= 50) for the qualifying-
journals list.
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
RANKINGS = ROOT / "data" / "journal-rankings.json"
WHITELIST = ROOT / "journals.json"
OUT = ROOT / "pdf-lists" / "journal-ranking-report.md"


def main():
    rows = json.loads(RANKINGS.read_text(encoding="utf-8"))
    wl = {j["name"]: j for j in json.loads(WHITELIST.read_text(encoding="utf-8"))}

    # Sort by h_index desc, then 2yr_mean
    def key(r):
        oa = r.get("openalex") or {}
        return (-(oa.get("h_index") or 0), -(oa.get("two_yr_mean_citedness") or 0))

    rows.sort(key=key)

    lines = []
    lines.append("# Journal ranking report")
    lines.append("")
    lines.append(f"Source: OpenAlex sources API. {len(rows)} journals, "
                 f"{sum(1 for r in rows if r.get('openalex'))} matched.")
    lines.append("")
    lines.append("Metrics:")
    lines.append("- **h-index**: career H-index of the journal (long-term stature; rewards age)")
    lines.append("- **2yr**: 2-year mean citedness (≈ JCR/Scimago impact factor; current activity)")
    lines.append("- **papers**: count of catalogue papers in this journal")
    lines.append("- **tier**: current whitelist assignment (A / B / blank if not in whitelist)")
    lines.append("")

    # Cutoff distribution table
    lines.append("## Cutoff suggestions (count of journals at or above each h-index)")
    lines.append("")
    lines.append("| h-index ≥ | journals | catalogue papers in those journals |")
    lines.append("|---:|---:|---:|")
    for cut in [500, 300, 200, 150, 100, 75, 50, 30, 20, 10, 5]:
        js = [r for r in rows if (r.get("openalex") or {}).get("h_index", 0) >= cut]
        papers_at_cut = sum(r.get("papers_in_catalogue", 0) for r in js)
        lines.append(f"| {cut} | {len(js)} | {papers_at_cut} |")
    lines.append("")

    lines.append("## All journals (sorted by h-index)")
    lines.append("")
    lines.append("| journal | h-index | 2yr | papers | tier | OpenAlex |")
    lines.append("|---|---:|---:|---:|---|---|")
    for r in rows:
        oa = r.get("openalex") or {}
        h = oa.get("h_index")
        two_yr = oa.get("two_yr_mean_citedness")
        papers = r.get("papers_in_catalogue", 0)
        tier = wl.get(r["name"], {}).get("tier", "")
        oa_id = oa.get("id") or ""
        oa_link = f"[{oa_id}](https://openalex.org/{oa_id})" if oa_id else "-"
        lines.append(
            f"| {r['name']} "
            f"| {h if h is not None else '-'} "
            f"| {two_yr:.2f} " if two_yr is not None else f"| {r['name']} | {h if h is not None else '-'} | - "
        )
    # Rebuild the table cleanly (the f-string above mid-loop got tangled)
    lines = lines[: lines.index("| journal | h-index | 2yr | papers | tier | OpenAlex |") + 2]
    for r in rows:
        oa = r.get("openalex") or {}
        h = oa.get("h_index")
        two_yr = oa.get("two_yr_mean_citedness")
        papers = r.get("papers_in_catalogue", 0)
        tier = wl.get(r["name"], {}).get("tier", "")
        oa_id = oa.get("id") or ""
        oa_link = f"[{oa_id}](https://openalex.org/{oa_id})" if oa_id else "-"
        h_str = str(h) if h is not None else "-"
        two_str = f"{two_yr:.2f}" if two_yr is not None else "-"
        lines.append(f"| {r['name']} | {h_str} | {two_str} | {papers} | {tier} | {oa_link} |")
    lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
