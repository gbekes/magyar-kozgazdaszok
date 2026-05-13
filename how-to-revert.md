# How to revert WIP mode

The public site (gbekes.github.io/magyar-kozgazdaszok/) is currently in
WIP mode — every page shows the bilingual "Munka folyamatban / Work in
progress" maintenance message.

## Restore the live site

```bash
git revert 68a1d67
git push origin main
```

That's it. The revert reinstates every HTML file as it was before the
suspension. Pages workflow redeploys automatically (~1–2 min).

- WIP commit hash: **`68a1d67`** (full: `68a1d679b1339fdd5964db34fcababf3da250d1a`)
- Commit message: "WIP-MODE: suspend public site"
- Date: 2026-05-13

## What WIP mode actually changed

20 HTML files swapped to maintenance content:

- `index.html`, `hu/index.html`, `404.html` → bilingual WIP page
- 9 other root pages + 9 hu/ pages → one-line `<meta refresh>` redirect to `./`

Everything outside HTML is untouched: `data/`, `authors-seed.json`,
`scripts/`, build pipeline, GitHub Actions workflow. The Pages workflow
still runs on every push to main — but the deployed artifact is just
the WIP content.

## Working while suspended

Catalogue work on `data/` keeps flowing as normal:

- Add / edit author + paper + policy + press JSONs
- Run `python build.py` locally to regenerate `data/index.json`
- Commit + push to main — the workflow rebuilds and redeploys, but
  visitors keep seeing WIP

When you're ready to come back online, run the revert above and the
fully-up-to-date catalogue ships.

## If you forget the commit hash

```bash
git log --grep "WIP-MODE" --oneline
```
