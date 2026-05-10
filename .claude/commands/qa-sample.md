---
description: Run the catalogue QA sampling harness (random spot-checks)
argument-hint: [--seed N]
---

# /qa-sample

Run the sampling-based content QA harness and present the result.

## What to do

1. Run `python tests/qa_sample.py --save $ARGUMENTS` from the repo root.
   - If `$ARGUMENTS` is empty, that's fine — the script picks a fresh
     time-based seed.
   - If the user passed `--seed N`, that flag will be in `$ARGUMENTS`
     and is forwarded as-is.

2. Show the user the report verbatim, with the seed, the per-slot
   pass/fail/skip lines, and the summary.

3. **If all 25 PASS:** confirm cleanly and stop. No further action.

4. **If any FAIL lines appear:**
   - Group failures by their tag (`defect` / `format-warning` /
     `plausibility-flag` / `liveness-flag`) — the harness already
     prints them grouped at the end of the report.
   - For each, propose what to do without doing it yet:
     - **defect** — offer to open the relevant `data/papers/<id>.json`
       (or author / policy / press file), show the offending field,
       and suggest the fix.
     - **format-warning** — note the SPEC target the field missed,
       but flag that short `data_used` is often legitimate (theory
       papers, descriptive notes). Offer to read the field and
       check.
     - **plausibility-flag** — open the file, read the relevant
       fields, and report whether it looks like a real issue or a
       false positive. Don't change anything without the user's say.
     - **liveness-flag** — first re-run with `--seed <reported_seed>`
       to confirm the failure is persistent rather than a transient
       network error. Only if it persists, propose updating the URL
       in the JSON.

5. Never edit data files in this command without explicit user
   approval. The harness reads; the editor decides.

## Argument forwarding

The user can pass:
- `--seed N` — for a deterministic run (e.g., to reproduce a previous
  failure)
- `--save` — already passed by default; harmless if repeated

Anything else is passed through too; if `python tests/qa_sample.py`
rejects it, that's a clear error.

## After triage

If you fixed any defects, re-run the same seed once to confirm. Then
suggest a fresh time-based run to confirm the random pool also looks
clean.

Don't commit the report file unless the user asks — the previous
runs in `tests/reports/` already serve as a paper trail.
