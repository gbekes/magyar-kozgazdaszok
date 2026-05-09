# Filling English Gaps

Use these helpers to make the remaining English backfill work mechanical.
They intentionally ignore the Hungarian mirror and focus on the English public
surface: paper summaries, data descriptions, policy relevance, policy-item
summaries, and author trust metadata.

## 1. Generate queues

```bash
python scripts/gap_queues.py
```

This writes Markdown queues under `reports/gaps/`:

- `policy-drafts.md` — policy items missing `summary_en`, `policy_relevance`, or `topics`.
- `paper-drafts-ready.md` — research papers missing English fields where the JSON already has an abstract.
- `paper-drafts-need-source.md` — research papers that need a DOI/page/PDF lookup first.
- `author-metadata.md` — authors missing RePEc, photo, or qualifying publication metadata.

Useful variants:

```bash
python scripts/gap_queues.py --limit 25
python scripts/gap_queues.py --format both
python scripts/gap_queues.py --out reports/gaps-2026-05-01
```

Recommended order:

1. Clear `policy-drafts.md` first. These are short and most policy-facing.
2. Work through `paper-drafts-ready.md` in batches of 10.
3. Use `paper-drafts-need-source.md` only when you have time for web/PDF lookup.
4. Fill `author-metadata.md` before outreach waves.

## 2. Draft papers

For research papers, keep using the existing paper draft flow:

```bash
python scripts/apply_drafts.py scripts/drafts_<batch>.json
python build.py
```

Draft JSON shape:

```json
{
  "paper-id": {
    "summary_en": "...",
    "data_used": "...",
    "policy_relevance": "...",
    "topics": ["labor-markets"],
    "methods": ["diff-in-diff"],
    "data_types": ["admin-individual"],
    "countries_studied": ["HU"],
    "policy_instruments": ["minimum wage"]
  }
}
```

## 3. Draft policy items

Policy items now have a matching apply helper:

```bash
python scripts/apply_policy_drafts.py scripts/drafts_policy_<batch>.json --dry-run
python scripts/apply_policy_drafts.py scripts/drafts_policy_<batch>.json
python build.py
```

Draft JSON shape:

```json
{
  "policy-id": {
    "summary_en": "...",
    "policy_relevance": "...",
    "topics": ["education-skills", "labor-markets"],
    "policy_instruments": ["public employment services", "NEET outreach"]
  }
}
```

The script validates topic ids against `data/topics.json`, caps topics at 3,
preserves untouched fields, and sets `review_status: ai-drafted` plus
`last_reviewed_at`.

## 4. Batch discipline

- Cap drafting batches at 10 records.
- Do not draft from title alone. If the queue says `needs source`, fetch a page,
  DOI abstract, or PDF first.
- Leave tags empty if unsure. A missing tag is cheaper than a wrong tag.
- After applying, run:

```bash
python build.py
python scripts/gap_queues.py
```

The queue counts should fall monotonically.
