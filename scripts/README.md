# scripts/ — content pipeline

Tools for the catalogue's ingestion, drafting, verification, and HU translation flows. Each is invoked from the repo root (`python scripts/<name>.py ...`).

## Ingestion

| Script | Purpose |
|---|---|
| `ingest.py` | Three-stage pipeline (discover → metadata → draft) for a new author's papers. Reads `data/papers/`, writes Claude-drafted summaries. See `docs/development/WORKFLOW.md` for details. |
| `ingest_policy_press.py` | Sister pipeline for `data/policy/` and `data/press/`. |

## Apply-from-batch (editor curates a JSON, script writes back to data/)

| Script | Input | Touches |
|---|---|---|
| `apply_drafts.py` | per-batch JSON (gitignored) | `data/papers/*.json` summary/data/policy fields |
| `apply_summaries_hu.py` | per-batch JSON (gitignored) | `data/papers/*.json` HU summary fields |
| `apply_bios_hu.py` | `bios_hu.json` (gitignored) | `data/authors/*.json` bio_hu |
| `apply_policy_drafts.py` | per-batch JSON | `data/policy/*.json` |
| `apply_doi_fixes.py` | `pdf-lists/doi-fixes-apply.json` | `data/papers/*.json` DOI fields |
| `apply_journal_whitelist.py` | `data/journals.json` | recomputes tier flags |
| `apply_repec_ids.py` | per-batch JSON | `data/authors/*.json` repec_id |

## Verification (read-only, write reports to `pdf-lists/`)

| Script | Output |
|---|---|
| `cross_check.py` | `pdf-lists/cross-check-report.md` |
| `verify_dois.py` | `pdf-lists/doi-verification-report.md` |
| `verify_no_doi_papers.py` | `pdf-lists/no-doi-verification-report.md` |
| `verify_repec.py` | (stdout) |
| `verify_authors.py` | (stdout) |
| `propose_doi_fixes.py` | `pdf-lists/doi-fixes-proposed.json` |
| `journal_ranking_report.py` | `pdf-lists/journal-ranking-report.md` |
| `fetch_journal_rankings.py` | external fetch helper |

## Translation

| Script | Purpose |
|---|---|
| `deepl_translate.py` | Bulk EN→HU translation. Needs `DEEPL_AUTH_KEY` env var. |
| `deepl_glossary.py` | Maintains `deepl_glossary_en_hu.tsv` (technical terms, institution names). |

## Author-facing helpers

| Script | Purpose |
|---|---|
| `export_author_md.py` | Generates per-author Markdown snapshot for submission to `submissions/`. |
| `generate_dossier.py` | PII-bearing local dossier (outreach folder, gitignored). |
| `generate_contacts.py` | Contact CSV for outreach. |

## Gap analysis

| Script | Purpose |
|---|---|
| `gap_queues.py` | Per-field gap counts (missing photo, bio, summary_hu, etc.). |

## Conventions

- All scripts are idempotent and only mutate `data/*.json` / `pdf-lists/*` — never touch HTML, never delete files.
- Per-batch input JSONs (`drafts_*.json`, `summaries_hu_*.json`, `bios_hu.json`, etc.) are gitignored: the editorial decisions land in commit history via the data files they write, not via the input JSON itself.
- Skipped papers: anything with `review_status` in `{human-reviewed, author-approved}` is locked against pipeline rewrites unless `--force` is passed.
