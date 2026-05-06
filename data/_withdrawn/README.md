# Withdrawn authors

Author records for people who asked to be removed from the public site.
Kept here in version control so we can restore quickly if they change
their minds.

These files are **not** loaded by `build.py` (which globs only
`data/authors/*.json`). They will not appear on the public site, in
search, in the author count, or in any listing. Their papers remain in
`data/papers/` — their name still shows on those papers' author lists,
but rendered as plain text (the `authorLink` helper falls back to text
when the slug doesn't resolve to a public author entry).

## To restore an author

1. Move `data/_withdrawn/<slug>.json` → `data/authors/<slug>.json`.
2. Add `{"id": "<slug>"}` to `authors-seed.json`.
3. Run `python build.py`.

That's it. Their author page comes back, the count goes up, search
sees them again. The papers don't need to change — they already
reference the slug.

## Current entries

- `berlinger-edina.json` — withdrew 2026-05-06.
