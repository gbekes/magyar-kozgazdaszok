"""Fix the 8 issues surfaced by scripts/cross_check.py:

1. 6 papers where DOI != URL (DOI was set incorrectly in earlier batches;
   URL values from the cowork session were the canonical correct ones).
   Action: align DOI to URL.

2. 2 policy items reference 'varga-kinga' which is a typo for Júlia Varga
   (editor of Munkaerőpiaci Tükör). Action: replace the slug-style reference
   with the plain string 'Júlia Varga' (matching how non-catalogued
   coauthors are stored elsewhere).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "data" / "papers"
POLICY = ROOT / "data" / "policy"


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def save(p, data):
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ---- 1. align DOI to URL on 6 papers ----
DOI_ALIGN = [
    "kiss-rodriguez-lara-et-al-2015-jbee",
    "kiss-selei-2017-edec",
    "koczy-2006-jmathe",
    "koczy-2008-geb",
    "koczy-2015-jmathe",
    "koczy-nichifor-2012-ecth",
]
fixed = 0
for slug in DOI_ALIGN:
    f = PAPERS / f"{slug}.json"
    p = load(f)
    url = p.get("url_published") or ""
    if url.startswith("https://doi.org/"):
        correct_doi = url.removeprefix("https://doi.org/")
        old_doi = p.get("doi")
        if old_doi != correct_doi:
            p["doi"] = correct_doi
            save(f, p)
            print(f"DOI fix: {slug}: {old_doi} -> {correct_doi}")
            fixed += 1

# ---- 2. fix varga-kinga typo in 2 policy items ----
for slug in ["hermann-kertesi-varga-2022-mt-test-segregation",
             "hermann-varga-eds-2024-mt"]:
    f = POLICY / f"{slug}.json"
    p = load(f)
    authors = p.get("authors") or []
    new_authors = ["Júlia Varga" if a == "varga-kinga" else a for a in authors]
    if new_authors != authors:
        p["authors"] = new_authors
        save(f, p)
        print(f"author typo fix: {slug}: varga-kinga -> 'Júlia Varga'")
        fixed += 1

print(f"\nFixed {fixed} issues total")
