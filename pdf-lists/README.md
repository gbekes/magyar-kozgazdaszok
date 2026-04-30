# PDF lists for catalogue drafting

Auxiliary files supporting `pdfs-needed-2026-04-27.md` (at repo root). 247
papers in the catalogue still need EN summary and either lack an abstract
in JSON or have a known-bad one. These files make it easier to fetch them
in batches.

## Files

- `_all.csv` — all 247 papers in CSV form. Columns: `slug, tier, year,
  journal, title, authors, doi, url`. Filter by tier or author for batch
  work. Easy to feed into download scripts.
- `<author-slug>.txt` — per-author lists, one URL per line, with comment
  headers giving the catalogue slug + journal + year + title for each
  paper. Sorted by year desc. 44 authors with 2+ papers each.

## How to use

### Cowork session via institutional library

```bash
# Pick an author batch
cat pdf-lists/temesvary-judit.txt

# Fetch with your institution's proxy/cookies, save to:
not-shared/pdfs/<slug>.pdf
```

The `not-shared/` folder is gitignored — perfect for local PDF storage.
Once a PDF is in `not-shared/pdfs/<slug>.pdf`, a Claude session can read
it via the `pdf` skill and draft the summary.

### Quick path (just paste abstract)

If you have just the abstract text:
1. Open `data/papers/<slug>.json`
2. Set the `abstract` field
3. Next Claude session drafts from there

### Batch download via DOI

Most lines are `https://doi.org/...`. With institutional proxy cookies,
basic curl/wget loop works:

```bash
while read url; do
  [[ "$url" =~ ^# ]] && continue
  [[ -z "$url" ]] && continue
  # ... your fetch logic here
done < pdf-lists/temesvary-judit.txt
```

## Top concentrations (one library run = big yield)

| Author | Papers | Most common journals |
|---|---|---|
| temesvary-judit | 14 | JoBF, JIMF, JIE, JFS, REStat |
| ambrus-attila | 12 | JET, JPubEc, AER, ResStud |
| virag-gabor | 10 | JET, GEB, RAND |
| csoka-peter | 10 | JBF, GEB, EJOR |
| szerb-laszlo | 10 | Small Business Econ, RegStud |
| biro-aniko | 8 | Health Econ, J Pop Econ |
| bekes-gabor | 7 | various trade / FDI |
| koczy-laszlo | 7 | political economy / matching |
| koszegi-botond | 7 | QJE, ResStud, AER |
| simonovits-andras | 7 | KSZ, theory |

## Out of scope

Papers in `_all.csv` flagged `tier: -` or `?` are not on the journals
whitelist. Some are book chapters or working papers that may not warrant
catalogue inclusion at all — those are an editor decision before fetching.
