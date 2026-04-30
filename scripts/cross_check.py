"""Cross-check round: validate tags (controlled vocabularies), DOI/URL formats,
and author cross-references across the catalogue.

Reports problems but does NOT mutate JSON. Generates pdf-lists/cross-check-report.md.
"""
import json
import re
import sys
from pathlib import Path
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "data" / "papers"
AUTHORS = ROOT / "data" / "authors"
POLICY = ROOT / "data" / "policy"
PRESS = ROOT / "data" / "press"

# Controlled vocabularies (must match apply_drafts.py)
TOPICS = {
    "labor-markets", "education-skills", "health", "demographics-migration",
    "trade-fdi", "firms-productivity", "innovation-digital", "banking-finance",
    "fiscal-tax", "regional-urban", "energy-environment", "inequality-welfare",
    "political-economy", "transition-postcommunist", "methods",
    "behavioral", "industrial-organization", "macroeconomics", "agriculture-food",
    "market-design", "mechanism-design",
}
METHODS = {
    "rct", "diff-in-diff", "iv", "rd", "panel-data", "synthetic-control",
    "structural", "theory", "time-series", "ml-text", "descriptive-survey",
}
DATA_TYPES = {
    "admin-firm", "admin-tax", "admin-individual", "survey",
    "firm-level-dataset", "field-experiment", "macro-aggregate",
    "digital-trace", "historical",
}

# DOI format: 10.<registrant>/<suffix>
DOI_RE = re.compile(r"^10\.\d{4,9}/.+$")

issues = defaultdict(list)
counts = Counter()
all_topics = Counter()
all_methods = Counter()
all_data_types = Counter()


def check_paper(p, slug):
    counts["papers"] += 1

    # ---- topic / method / data-type vocab validity ----
    for t in p.get("topics") or []:
        all_topics[t] += 1
        if t not in TOPICS:
            issues["bad-topic"].append((slug, t))

    for m in p.get("methods") or []:
        all_methods[m] += 1
        if m not in METHODS:
            issues["bad-method"].append((slug, m))

    for dt in p.get("data_types") or []:
        all_data_types[dt] += 1
        if dt not in DATA_TYPES:
            issues["bad-data-type"].append((slug, dt))

    # ---- DOI format ----
    doi = p.get("doi")
    if doi:
        # Strip URL prefix if accidentally included
        d_clean = doi.removeprefix("https://doi.org/").removeprefix("http://doi.org/").removeprefix("doi:")
        if not DOI_RE.match(d_clean):
            issues["bad-doi-format"].append((slug, doi))
        elif d_clean != doi:
            issues["doi-with-url-prefix"].append((slug, doi))

    # ---- url_published format ----
    url = p.get("url_published")
    if url and not (url.startswith("http://") or url.startswith("https://")):
        issues["bad-url-format"].append((slug, url))

    # ---- url_published vs DOI consistency ----
    if doi and url and "doi.org" in url:
        d = doi.removeprefix("https://doi.org/").removeprefix("http://doi.org/")
        u = url.removeprefix("https://doi.org/").removeprefix("http://doi.org/")
        if d.lower() != u.lower():
            issues["doi-url-mismatch"].append((slug, doi, url))

    # ---- author-slug references ----
    authors = p.get("authors") or []
    for a in authors:
        if not isinstance(a, str):
            issues["bad-author-type"].append((slug, str(type(a))))
            continue
        # Author entries that look like slugs (lowercase-with-hyphens) should resolve
        if re.match(r"^[a-z][a-z-]+[a-z]$", a) and "-" in a and not any(c.isupper() for c in a):
            af = AUTHORS / f"{a}.json"
            if not af.exists():
                issues["unresolved-author-slug"].append((slug, a))

    # ---- empty critical fields on metadata-fetched papers ----
    rs = p.get("review_status") or ""
    if rs in ("ai-drafted", "human-reviewed", "author-approved"):
        if not p.get("summary_en"):
            issues["drafted-but-no-summary"].append((slug, rs))

    # ---- year sanity ----
    yr = p.get("year")
    if yr is not None:
        try:
            yr_i = int(yr)
            if yr_i < 1900 or yr_i > 2030:
                issues["weird-year"].append((slug, yr))
        except (TypeError, ValueError):
            issues["non-integer-year"].append((slug, yr))


def main():
    for f in sorted(PAPERS.glob("*.json")):
        p = json.loads(f.read_text(encoding="utf-8"))
        check_paper(p, f.stem)

    # Same for policy, press (lighter — no topics)
    for f in sorted(POLICY.glob("*.json")):
        counts["policy"] += 1
        p = json.loads(f.read_text(encoding="utf-8"))
        # validate authors
        for a in p.get("authors") or []:
            if isinstance(a, str) and re.match(r"^[a-z][a-z-]+[a-z]$", a):
                af = AUTHORS / f"{a}.json"
                if not af.exists():
                    issues["unresolved-author-slug-policy"].append((f.stem, a))

    for f in sorted(PRESS.glob("*.json")):
        counts["press"] += 1

    # Author files: cross-check primary_fields are in TOPICS
    for f in sorted(AUTHORS.glob("*.json")):
        counts["authors"] += 1
        a = json.loads(f.read_text(encoding="utf-8"))
        for pf in a.get("primary_fields") or []:
            if pf not in TOPICS:
                issues["bad-author-primary-field"].append((f.stem, pf))

    # ---- summary report ----
    out = []
    out.append("# Cross-check report\n")
    out.append(f"Papers checked: {counts['papers']}")
    out.append(f"Policy items checked: {counts['policy']}")
    out.append(f"Press items checked: {counts['press']}")
    out.append(f"Authors checked: {counts['authors']}\n")

    out.append("## Tag usage (top 10 each)\n")
    out.append("**Topics**:")
    for t, c in all_topics.most_common(25):
        marker = "" if t in TOPICS else " ⚠ INVALID"
        out.append(f"- {t}: {c}{marker}")
    out.append("\n**Methods**:")
    for m, c in all_methods.most_common(15):
        marker = "" if m in METHODS else " ⚠ INVALID"
        out.append(f"- {m}: {c}{marker}")
    out.append("\n**Data types**:")
    for dt, c in all_data_types.most_common(15):
        marker = "" if dt in DATA_TYPES else " ⚠ INVALID"
        out.append(f"- {dt}: {c}{marker}")

    out.append("\n## Issues\n")
    if not issues:
        out.append("(no issues)\n")
    else:
        for kind, lst in sorted(issues.items()):
            out.append(f"\n### {kind} ({len(lst)})\n")
            # Show up to 30 examples
            for ex in lst[:30]:
                if isinstance(ex, tuple):
                    out.append(f"- {' | '.join(str(x) for x in ex)}")
                else:
                    out.append(f"- {ex}")
            if len(lst) > 30:
                out.append(f"- ... +{len(lst) - 30} more")

    report_path = ROOT / "pdf-lists" / "cross-check-report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(out), encoding="utf-8")
    print(f"report written: {report_path}")
    # print short summary to console
    print("\nIssue counts:")
    for kind, lst in sorted(issues.items(), key=lambda kv: -len(kv[1])):
        print(f"  {kind}: {len(lst)}")


if __name__ == "__main__":
    main()
