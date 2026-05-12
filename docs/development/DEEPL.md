# DeepL HU translation pipeline

The chosen path for filling Hungarian summaries on the catalogue
(`summary_hu`, `data_used_hu`, `policy_relevance_hu`). Replaces the
LLM-based translation discussed in `docs/roadmap-2026-04-30.md` §4.

> **Fast path when the key arrives** (after stocktake on 2026-05-09:
> 1 529 fields / 614 745 chars in the queue):
>
> ```bash
> echo 'YOUR-KEY-HERE:fx' > not-shared/deepl_api_key.txt   # free-tier key ends in :fx
> python scripts/deepl_translate.py --usage                  # confirm endpoint + quota
> python scripts/deepl_translate.py --dry-run                # preview the queue
> python scripts/deepl_translate.py --apply --author szentes-balazs   # pilot one author
> # eyeball 3-5 translations, commit, then run --apply with no filter for the bulk
> ```
>
> Free tier (500 K chars/month) covers ~80 % of today's queue; one
> Pro month (~€25) covers all of it in a single sweep.

**Why DeepL over an LLM:** higher fluency on Hungarian, deterministic
output, cheap (DeepL API Free tier is 500 000 chars / month; Pro is
€20 / 1 M chars after a flat €4.99 / month), no per-paper review
needed for the bulk pass.

**Estimated total cost:** the open queue today is ~482 P2 paper
translations + the policy-item HU gap. At ~700 chars per field × 3
fields per paper × 482 papers ≈ **~1 M chars**. That fits inside two
months on Free tier, or one Pro month for ~€25.

---

## 1. Setup

### 1.1 Get a key

Sign up at <https://www.deepl.com/en/pro-api>. Free-tier keys end
with `:fx`. Pro keys do not. The pipeline auto-detects which
endpoint to use.

### 1.2 Store the key

Pick one:

```bash
# Option A: file (gitignored under not-shared/)
echo 'YOUR-KEY-HERE:fx' > not-shared/deepl_api_key.txt

# Option B: env var
export DEEPL_API_KEY='YOUR-KEY-HERE:fx'
```

### 1.3 Verify

```bash
python scripts/deepl_translate.py --usage
```

Expected output:

```
DeepL usage: 0 / 500 000 chars  (0.0%)
Remaining:   500 000 chars
Endpoint:    https://api-free.deepl.com
```

### 1.4 (Optional) Create the glossary

The glossary keeps econ jargon and Hungarian institution names
stable across the whole catalogue. Use it after a successful
pilot — not before, so you can compare with vs without.

```bash
python scripts/deepl_glossary.py create scripts/deepl_glossary_en_hu.tsv
# -> "Created glossary <id>"
export DEEPL_GLOSSARY_ID=<id>
```

`list`, `show <id>`, and `delete <id>` are also available.

To edit the glossary: edit the TSV, delete the old glossary ID,
recreate. (DeepL has no in-place edit.)

---

## 2. Daily workflow

### 2.1 Inspect the queue

```bash
python scripts/deepl_translate.py --dry-run
```

Reports number of fields needing translation, total chars, and a
preview of the first five. No API call.

Filter to one author:

```bash
python scripts/deepl_translate.py --dry-run --author szentes-balazs
```

### 2.2 Pilot: translate one author

```bash
python scripts/deepl_translate.py --apply --author szentes-balazs
```

Translates and writes back to `data/papers/*.json` (and
`data/policy/*.json` if applicable). Skips fields where the HU
side is already populated (resumable). Updates
`last_reviewed_at`.

After the run, eyeball 3–5 random translations:

```bash
git diff data/papers/szentes-*.json | head -100
```

If quality is fine, commit. If not, see §4.

### 2.3 Two-stage (review before commit)

For more cautious batches, produce a staging JSON the editor
can read and edit before the data files change:

```bash
python scripts/deepl_translate.py --produce drafts_hu_$(date +%F).json \
  --author szentes-balazs

# editor reads / tweaks the JSON

python scripts/apply_summaries_hu.py drafts_hu_2026-05-01.json
```

Same format `apply_summaries_hu.py` already consumes from manual
LLM batches — drop-in compatible.

### 2.4 Bulk sweep

Once piloted, just:

```bash
python scripts/deepl_translate.py --apply
```

It iterates papers then policy, batches 25 fields per API call,
and refuses to start if the queue exceeds remaining quota. It
writes a state file (`not-shared/deepl_state.json`) and per-field
log (`not-shared/deepl_log.jsonl`) on every run.

Cap the run by chars or items if you want to stay under a budget:

```bash
python scripts/deepl_translate.py --apply --max-chars 100000
python scripts/deepl_translate.py --apply --limit 50
```

### 2.5 Filter by field

If only `summary_hu` should be filled this round (skip
`data_used_hu` / `policy_relevance_hu`):

```bash
python scripts/deepl_translate.py --apply --fields summary_hu
```

### 2.6 Commit + push

The repo is auto-push to `main`; every commit goes live. So:

1. Run `--apply`.
2. Skim the diff (`git diff --stat`).
3. Run `python build.py` to refresh `data/index.json`.
4. Run `python scripts/cross_check.py` (no new issues expected).
5. `git add -A && git commit -m "DeepL HU pass: <author or batch>"
   && git push`.

Keep batches small enough that diffs are reviewable — ~one author
per commit is the convention.

---

## 3. What the pipeline does and doesn't do

**Does:**
- Walks `data/papers/*.json` and `data/policy/*.json`.
- Finds fields where the EN source is set and the HU target is
  empty.
- Calls DeepL `/v2/translate` with `target_lang=HU`,
  `source_lang=EN`, `preserve_formatting=1`, plus glossary if set.
- Writes results back; updates `last_reviewed_at`.
- Logs per-field char counts to `not-shared/deepl_log.jsonl`.
- Records run summary in `not-shared/deepl_state.json`.

**Doesn't:**
- Re-translate already-populated HU fields (use git revert + run
  again if you want to redo).
- Translate `title_hu` or `bio_hu` (different fields, different
  workflow — bios go through `apply_bios_hu.py` and the editor's
  style memory rule).
- Translate press items (Press is mostly Hungarian-origin; English
  is the translation, not the other way around).
- Touch `review_status`. DeepL output is *not* author-approved;
  status stays whatever it was.
- Set formality. DeepL doesn't support formality on HU target as
  of 2026 — request silently ignored if passed.

---

## 4. Quality control

DeepL on EN→HU is genuinely good for prose, but not perfect on:

- **Econ jargon** — "spillover" can become "kiömlés" (literal
  spillage) instead of "tovagyűrűzés" (the canonical econ term).
  Mitigate via glossary.
- **Institution names** — DeepL sometimes translates "World Bank"
  to "Világbank" (correct) but may translate "Bank of Hungary" to
  "Magyarországi Bank" instead of "Magyar Nemzeti Bank". Glossary.
- **Effect sizes** — units are usually preserved, but "percentage
  points" sometimes becomes "százalék" (percent). Spot-check.
- **Long compound noun phrases** — Hungarian agglutination can
  produce overlong constructions. Read aloud.

Spot-check protocol for the bulk pass:

1. After each author batch, open 1 random paper from that author.
2. Read `summary_hu` against `summary_en`. Note any term DeepL
   mistranslated.
3. If the same term recurs across authors, add it to
   `scripts/deepl_glossary_en_hu.tsv` and recreate the glossary.

If 2+ batches show systematic drift (>1 mistranslated term per
summary), pause and investigate before continuing.

---

## 5. Cost & quota guardrails

The pipeline:

- Calls `/v2/usage` before and after each run.
- Refuses to start a run if the queued char count exceeds
  remaining quota.
- Records each run's char usage in `not-shared/deepl_state.json`.

Free-tier resets monthly. Pro is metered.

To check remaining budget without running: `--usage`.

---

## 6. Troubleshooting

**`429 Too Many Requests`** — DeepL rate-limit. The script exits;
re-run a minute later.

**`456 Quota Exceeded`** — month exhausted. Wait, or switch to
Pro key, or use `--limit` / `--max-chars`.

**Translation looks like English** — your key may be missing the
`:fx` suffix when it should have it (or vice versa). Check
`--usage`; it shows which endpoint was used.

**`requests` import error** — `pip install -r scripts/requirements.txt`.

**A whole field is blank in the result** — DeepL returns "" for
empty input. The pipeline skips empty `src_text`, so this
shouldn't happen unless an EN field is whitespace-only. Inspect
the JSON.

**Glossary not applied** — DeepL only applies glossary entries
when the source matches the entry literally and case-sensitively.
If "Minimum wage" appears in a summary and the glossary only has
"minimum wage", DeepL ignores it. Add Title-case variants to the
TSV if needed.

---

## 7. Files

| Path | Purpose |
|---|---|
| `scripts/deepl_translate.py` | Main pipeline |
| `scripts/deepl_glossary.py` | Glossary CRUD |
| `scripts/deepl_glossary_en_hu.tsv` | Seed glossary (curated) |
| `not-shared/deepl_api_key.txt` | API key (gitignored) |
| `not-shared/deepl_state.json` | Last-run summary |
| `not-shared/deepl_log.jsonl` | Per-field translation log |
| `scripts/apply_summaries_hu.py` | Existing apply tool — works on staging JSON from `--produce` |
