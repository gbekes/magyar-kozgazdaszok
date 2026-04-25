# Skills — Magyar Közgazdászok

Project-local skills that Claude Code auto-loads when working in this
repo. Each skill lives in its own folder with a `SKILL.md` (frontmatter
+ instructions) and any supporting files.

## Available skills

| Skill | What it does | Trigger phrases |
|---|---|---|
| [research-author](research-author/SKILL.md) | Step-by-step research pass on one author: bio (EN+HU), photo, RePEc / Scholar / ORCID, qualifying publication, RePEc-vs-catalogue paper diff. | "research X", "build out Y's page", "fill in what's missing for Z", "find a photo for W" |
| [audit-author](audit-author/SKILL.md) | Read-only QA on one author: gaps in fields, draft completeness, broken DOIs, TBD co-authors, linked-paper opportunities, external coverage gaps. Returns a prioritised numbered task list. | "audit X", "what's missing for Y", "qa Z", "review W's catalogue" |
| [draft-summary](draft-summary/SKILL.md) | Author the policymaker-facing fields (`summary_*`, `data_used`, `policy_relevance`) for paper / policy / press, single-item or batch, EN and HU. Produces JSON for `apply_drafts.py` / `apply_summaries_hu.py`. | "draft X", "translate Y to Hungarian", "fill in policy_relevance for W", "do drafts for author A" |
| [media-scan](media-scan/SKILL.md) | Walk the curated outlet list ([sources.md](media-scan/sources.md)) for press / policy items by Hungarian economists not yet in the catalogue. Author-driven or outlet-driven. | "scan press", "find new columns", "media coverage of X", "sweep VoxEU", "what did we miss on Portfolio" |

The repo also has the standalone [hu-econ-verifier](../../hu-econ-verifier-SKILL.md)
skill (packaged as `hu-econ-verifier.skill`), which handles two narrow
fact-checks: is X a Hungarian economist, and does paper Y actually
exist. The skills above defer to it for those questions.

## How they fit together

```
                    ┌──────────────────┐
                    │  hu-econ-verifier │   (eligibility + paper-existence checks)
                    └────────┬──────────┘
                             │
                             ▼
   ┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
   │ research-author │ ─▶ │   audit-author   │ ─▶ │  draft-summary   │
   │  (build entry)  │    │  (find gaps)     │    │  (fill content)  │
   └─────────────────┘    └────────┬──────────┘    └──────────────────┘
                                   │
                                   ▼
                          ┌────────────────┐
                          │   media-scan   │   (find press/policy items)
                          └────────────────┘
```

A typical full pass on an author from cold:

1. `hu-econ-verifier` → confirm eligibility
2. `research-author <slug>` → build / refresh `data/authors/<slug>.json`,
   get RePEc paper backlog
3. `audit-author <slug>` → ranked task list of remaining gaps
4. `draft-summary --research <slug>` → fill `data/papers/` summaries
5. `media-scan --author <slug>` → find press/policy not yet captured
6. `draft-summary --policy <slug>` → fill any new policy item drafts

For "improve everything we have" (the current editor priority), the
shortest path is: pick the top-N authors with the biggest gaps from the
2026-04-25 handover, run `audit-author` on each, then work the resulting
task lists by skill.

## Conventions

- **Default is dry-run.** Skills produce review blocks / proposed JSON;
  the editor approves before any file is written. Only commit on
  explicit "apply" / "go ahead".
- **Per-author scope.** All skills work on one author at a time
  except `media-scan --outlet`. Bulk operations live in `scripts/`.
- **Stopping rules.** Each skill has a hard fetch / item cap. Stop
  early and surface what you have rather than pad the response.
- **No invention.** Never fabricate URLs, DOIs, photo URLs, or paper
  metadata. Null is better than wrong.
- **Schema fidelity.** All proposed JSON must match SPEC.md (§2.1
  paper, §2.2 author, §2.6 policy, §2.7 press). Validate against the
  schemas before proposing.

## Editing the skills

Each skill is a single Markdown file with YAML frontmatter. Edit
in-place and the next session picks up the changes — no rebuild step.

The `media-scan/sources.md` list is data, not skill logic; edit it
when an outlet should be added, dropped, or its search pattern
updated.

## Where these skills live

`.claude/skills/` is **not** in `.gitignore` for this repo, so skills
are checked in and travel with the project. Future Claude Code
sessions opened in this directory load them automatically.
