# Catalogue QA — design notes for sampling-based tests

Where the harness lives: [`tests/`](../tests/) at repo root.
Entry point: [`tests/qa_sample.py`](../tests/qa_sample.py).

This file explains the **pattern** to follow when adding or
modifying tests. Read it before extending the harness.

---

## What the harness is for

A static catalogue with hand-edited JSON files needs spot-checking
after every batch of edits, but reading every paper after every pass
isn't feasible. Sampling-based QA addresses this: pick one random
item per test slot, apply a verifiable check, and report. Run
periodically; over many runs the harness covers the catalogue
broadly while costing seconds, not hours.

It is **not** a comprehensive validator. A green run does not mean
the catalogue is clean — it means the slots that fired this time
passed. A red run is a real signal.

## Core invariants

Any test added to this harness must satisfy:

1. **Eligibility filter** — skip items whose `review_status` is
   `human-reviewed` or `author-approved`. Editor-blessed work is
   out of scope; the harness targets the ai-drafted /
   metadata-fetched layer where regressions live.

2. **One item per slot** — sample, don't enumerate. The same N
   slots run every time; the items vary.

3. **Pool-empty becomes SKIP, not FAIL** — a pool emptying
   typically means the catalogue grew or shrank and there's
   nothing left in scope. SKIP keeps the report length stable.

4. **Network access is allowed but tagged** — liveness checks
   (DOI / URL / RePEc) are useful but slow and can fail
   transiently. Mark them `liveness-flag` so red lines don't
   block content work.

5. **Failure category is one of four** —
   - `defect` (real schema / cross-reference violation),
   - `format-warning` (SPEC length target not met),
   - `plausibility-flag` (looks suspicious; editor glance),
   - `liveness-flag` (external resource didn't resolve).

6. **No mutation** — tests read JSON. They never write to
   `data/` or to files outside `tests/reports/`.

## How to add a test slot

```python
def tNN_<short_name>(papers, rng):
    pool = [p for p in papers
            if not is_locked(p)             # invariant 1
            and has(p, "<the_field_you_test>")]
    if not pool:
        return skip("TNN", "Human-readable name", "<category>", "pool empty")
    p = rng.choice(pool)                    # invariant 2
    if <fail_condition>:
        return Result("TNN", "Human-readable name", "<category>", "FAIL",
                      f"paper {p['id']}", "<one-line diagnostic>")
    return Result("TNN", "Human-readable name", "<category>", "PASS",
                  f"paper {p['id']}")
```

Then list it in the `tests` table inside `run_all()` so the slot
runs every time.

Helpers available: `is_locked`, `has`, `is_slug`,
`author_file_exists`, `paper_file_exists`, `word_count`,
`looks_hungarian`, `http_status`, plus the loaded vocabularies
(`TOPIC_IDS`, `JOURNAL_NAMES`, `METHODS`, `DATA_TYPES`,
`SEMANTIC_COUNTRIES`, `HU_INSTITUTIONS`).

## Pool-design pitfalls

- **Don't filter so tightly the pool is always empty.** A test
  that always SKIPs is dead weight. If the eligibility criterion
  is rare (e.g., "papers with `url_replication` set"), check
  pool size before adding the slot.

- **Don't sample without a stable seed.** The default `seed=time()`
  varies per run; pass `--seed N` for reproducible debugging. The
  CLI accepts both.

- **Don't double-count locked items.** Always start with
  `not is_locked(item)`. The same item can appear as a paper, an
  author entry, and a press item; each has its own review_status.

- **Don't conflate plausibility with defect.** "summary mentions
  Hungary but HU isn't in countries_studied" is a plausibility
  flag (editor judgement), not a defect (the data shape is fine).

## Triage rules

When a run fails:

| Category | Rule of thumb |
|---|---|
| `defect` | Fix the JSON, commit, re-run with the same seed to confirm. |
| `format-warning` | Read the field — sometimes a 20-word `data_used` is correct (theory paper, no data). Don't auto-rewrite. |
| `plausibility-flag` | Open the paper and check. Often nothing's wrong; sometimes you find a real issue. |
| `liveness-flag` | First retry with `--seed N` from the report; if it persists, fix the URL or RePEc id. |

## Reports

Saved with `--save` into `tests/reports/qa-sample-<timestamp>.txt`.
Reports are committed to git as a paper trail; over time they show
where the catalogue had soft spots and how they got cleaned up.

## Eventual run mechanism (to be designed after iteration)

Once the harness has been iterated a few times — slots refined,
categories tightened, eligibility criteria stable — wire it into
one of:

- A **slash command** (e.g., `/qa-sample`) under `.claude/commands/`
  that runs the script and posts the report inline.
- A **scheduled task** (`scripts/scheduled-tasks/` or via the
  `schedule` skill) that runs nightly and emails / opens an issue
  on red.
- A **pre-deploy hook** that blocks the GitHub-Pages push on a
  red `defect`-category result (but not on flags).

Pick when there's a reason to. Until then, manual `python tests/qa_sample.py`
is enough.
