"""Apply a curated set of DOI fixes to data/papers/*.json.

Reads a list of {id, new_doi, openalex_id?} entries from a JSON file (default
pdf-lists/doi-fixes-apply.json). For each, updates the paper file:
- doi -> new_doi
- url_published -> https://doi.org/<new_doi>
- openalex_id -> if provided
- last_reviewed_at -> today

Writes a one-line audit log to pdf-lists/doi-fixes-applied.md.
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "data" / "papers"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path, help="Path to fixes JSON")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    fixes = json.loads(args.input.read_text(encoding="utf-8"))
    today = datetime.date.today().isoformat()

    log = []
    for fix in fixes:
        slug = fix["id"]
        new_doi = fix["new_doi"]
        f = PAPERS / f"{slug}.json"
        if not f.exists():
            print(f"  SKIP {slug}: file not found")
            continue
        p = json.loads(f.read_text(encoding="utf-8"))
        old_doi = p.get("doi")
        p["doi"] = new_doi
        p["url_published"] = f"https://doi.org/{new_doi}"
        if fix.get("openalex_id"):
            p["openalex_id"] = fix["openalex_id"]
        p["last_reviewed_at"] = today
        log.append(f"- {slug}: `{old_doi}` -> `{new_doi}`")
        if not args.dry_run:
            f.write_text(json.dumps(p, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  {'[dry] ' if args.dry_run else ''}{slug}: {old_doi} -> {new_doi}")

    if not args.dry_run:
        report = ROOT / "pdf-lists" / "doi-fixes-applied.md"
        existing = ""
        if report.exists():
            existing = report.read_text(encoding="utf-8")
        report.write_text(
            existing + f"\n## Batch {today}\n\n" + "\n".join(log) + "\n",
            encoding="utf-8",
        )
        print(f"\nApplied {len(log)} fixes. Log: {report.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
