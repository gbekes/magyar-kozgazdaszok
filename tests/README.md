# tests/

Sampling-based content QA. Each script in this folder picks a small
number of items at random and applies one verifiable check per slot.
The point is to spot-check the catalogue without manually re-reading
every paper after each batch of edits.

## Conventions

Every test in this folder follows the same pattern:

1. **Eligibility filter** — only consider items whose `review_status`
   is *not* `human-reviewed` or `author-approved`. Editor-blessed
   work is out of scope; the harness should target ai-drafted /
   metadata-fetched layers where regressions live.

2. **Sample, don't enumerate** — pick **one** item per test slot.
   The same N test slots run every time; the items vary.

3. **Pass / fail / skip** — every slot returns one of three
   outcomes. `SKIP` means the eligible pool was empty (e.g., no
   policy items currently have a `linked_paper_id`).

4. **Tag failures by category**:
   - `defect` — schema or cross-reference violation; should be
     fixed.
   - `format-warning` — SPEC length / shape target not met;
     informative, sometimes legitimately ignorable.
   - `plausibility-flag` — looks suspicious; editor should glance
     at it.
   - `liveness-flag` — external URL or ID didn't resolve; could be
     wrong, could be transient.

5. **Output is plain text** — one line per test slot, plus a
   summary block. Save into `tests/reports/` with `--save`.

## Tooling

| File | What it does |
|---|---|
| [`qa_sample.py`](qa_sample.py) | Sampling harness — one item per test slot (currently 26 slots: structural, format, plausibility, liveness, plus T26 for HU→EN link leaks). Run with `python tests/qa_sample.py [--seed N] [--save]`. |
| `reports/` | Saved run output. `qa-sample-YYYY-MM-DD-HHMM.txt` per run. |

Add a new test by:

1. Writing a `tNN_*` function in `qa_sample.py` (or a new file).
2. Listing it in the `tests` table in `run_all()`.
3. Re-running and committing the updated `tests/reports/` file
   (optional but useful as a paper trail).

See `.claude/qa-tests.md` for the design philosophy and pattern
to follow when adding new test slots.

## When to run

- Right after a big content batch (a translation pass, a stocktake
  application, a journal-whitelist update).
- Before a public release or a redeploy of the site.
- Periodically — once a week is plenty for a static catalogue
  this size.

There is no CI hookup yet. If runs become routine, see the
"propose a way to run this" section at the end of the v1 build
notes for how to wire it into a slash command or scheduled task.
