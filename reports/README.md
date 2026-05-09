# Reports

One-off reports, audits, and convenience tables that accompany the
catalogue but aren't part of it.

## Layout

- `audits/` — content audits (per-author audits, per-section gap
  audits, choke-point lists). One file per audit pass, dated.
- `gaps/` — auto-generated English-gap queues (regenerate with
  `python scripts/gap_queues.py`). See `gaps/README.md`.
- Loose files at this level — single-purpose notes (e.g. PDFs to
  source, journal-list discussion logs).

Reports are markdown by default. Machine-readable companions (per-
paper JSON tables) live next to their markdown summary.
