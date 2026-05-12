# pdf-lists/ — pipeline reports and verification artefacts

This folder is the working directory for the QA/verification pipeline
scripts in `scripts/`. Its contents are mostly script outputs that the
next pipeline stage reads.

## Active files

| File | Producer | Consumer |
|---|---|---|
| `cross-check-report.md` | `scripts/cross_check.py` | Editor reviews; informs `doi-fixes-apply.json` |
| `doi-verification-report.md` | `scripts/verify_dois.py` | `scripts/propose_doi_fixes.py` |
| `no-doi-verification-report.md` | `scripts/verify_no_doi_papers.py` | Editor reviews |
| `doi-fixes-proposed.json` | `scripts/propose_doi_fixes.py` | Editor curates → `doi-fixes-apply.json` |
| `doi-fixes-apply.json` | (hand-curated) | `scripts/apply_doi_fixes.py` |
| `doi-fixes-applied.md` | `scripts/apply_doi_fixes.py` | Audit log only |
| `journal-ranking-report.md` | `scripts/journal_ranking_report.py` | Editor reviews; feeds back into `data/journals.json` |

## Not in this folder

The original April 2026 per-author PDF-list scaffolding
(`<author>.txt`, `_all.csv`, `COWORK.md`) has been removed — the
catalogue is now mature enough that author-by-author batch fetching
is no longer the right workflow. If you need a list of an author's
papers, query `data/papers/` directly.
