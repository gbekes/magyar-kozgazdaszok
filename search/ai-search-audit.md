# AI Paper Search — Phase 0 Audit

Output of the audit step from `ai-search-claude-code-plan.md`. Locks in decisions and adapts the implementation spec to the actual repo state at 2026-05-12.

---

## 1. Repo state

**Framework / build pipeline**
- Pure static HTML + vanilla JS (`assets/app.js`, `assets/chrome.js`), no bundler, no JS framework.
- `build.py` (Python, ~130 lines) generates `data/index.json` from the per-entity JSON files in `data/`.
- Hosted on GitHub Pages via push-to-`main`. No CI beyond GH Pages' built-in auto-deploy.

**Paper catalogue**
- 852 papers as of 2026-05-12, one JSON file per paper at `data/papers/<slug>.json`.
- 105 authors at `data/authors/<slug>.json`.
- 35 policy items at `data/policy/`, 159 press items at `data/press/`.

**Paper schema — field coverage** (across 852 papers):

| Field | Coverage | Use in search? |
|---|---|---|
| `title` | 100 % | yes (high-weight) |
| `authors` | 100 % | yes |
| `journal` | 98 % | yes (low-weight; mostly noise) |
| `year` | 100 % | filter only |
| `doi` | 99 % | metadata, not search |
| `abstract` | 80 % | **primary search field** |
| `summary_en` | 97 % | **primary search field** |
| `summary_hu` | 59 % | skip per editorial decision |
| `data_used` | 97 % | yes (medium-weight) |
| `policy_relevance` | 97 % | yes (medium-weight) |
| `topics` | 98 % | yes (vocabulary tag) |
| `methods` | 97 % | yes (vocabulary tag) |
| `countries_studied` | 97 % | filter |
| `data_types` | 97 % | filter |
| `publication_type` | 100 % | filter |
| `keywords` | **0 %** | does not exist — drop from plan |

24 papers have under 50 tokens of indexed text combined (very thin abstracts + missing summaries). They will get embedded too, but expect weak retrieval on them. Flag for the editor's spot-check pipeline.

**Existing search**
- Hero search bar on `index.html` uses keyword scoring in `assets/app.js` (`function search`).
- Token-set intersection + partial-match fallback. Returns papers / authors / topics.
- Works fine for known-keyword queries; fails the "100-word problem description" use case (no semantic understanding, no cross-lingual).
- **Plan: keep the keyword search untouched, add the semantic search as a separate component on its own page or as an opt-in box.** Two complementary tools, not a replacement.

---

## 2. Decisions locked in

| # | Decision | Value | Justification |
|---|---|---|---|
| 1 | Embedding provider | **OpenAI** `text-embedding-3-large`, truncated to **1024 dim** | editor already has paid OpenAI credit; quality difference vs. Voyage is small at this corpus size; 1024 dim keeps browser-load reasonable |
| 2 | Worker host | **Cloudflare Workers** | 100k req/day free tier; lower latency in CEE; `wrangler` deployment |
| 3 | Indexed text per paper | `abstract` + `summary_en` + `topics` (joined) | per editor decision; no Hungarian fields, no `keywords` (doesn't exist) |
| 4 | CORS allowlist | `https://gbekes.github.io` + `http://localhost:8000` | production + local dev |
| 5 | `embeddings.bin` location | committed to repo at `static/embeddings.bin` | 3.33 MB binary, ~2 MB gzipped — fine for GH Pages |

---

## 3. Cost / size envelope

- **One-time indexing**: ~290 000 tokens × $0.13/1M = **$0.038**.
- **Per query**: ~50 tokens × $0.13/1M = **$0.0000065** (essentially free).
- **`embeddings.bin` size**: 852 papers × 1024 dim × 4 bytes = **3.33 MB** (≈2 MB gzipped).
- **`embeddings-meta.json` size**: ~250 KB.
- **CF Workers free tier**: 100 000 requests / day — orders of magnitude above any realistic traffic.

Bottom line: even at 1 000 daily queries, monthly bill stays well under $1.

---

## 4. Phase 1 spec — adapted to this repo

### Files to add

```
scripts/build_embeddings.py            # OpenAI embedding pipeline
scripts/build_embeddings_requirements.txt
static/embeddings.bin                  # generated, ~3.3 MB
static/embeddings-meta.json            # generated, ~250 KB
static/embeddings-info.json            # generated, ~200 B
.gitignore                             # add scripts/.embedding-cache.json
```

### Script: `scripts/build_embeddings.py`

Adapts the plan's pseudocode to:
- read `data/papers/<slug>.json` (the actual layout, not the plan's frontmatter assumption)
- use OpenAI `text-embedding-3-large` with `dimensions=1024`
- build indexed text from `abstract + summary_en + ' '.join(topics)` (drop keywords; not in schema)
- write `static/embeddings.bin` (float32, L2-normalised, no header)
- write `static/embeddings-meta.json` parallel to it (`{id, title, authors, year, journal, doi, topics}` per paper)
- write `static/embeddings-info.json` (`{model, dim, count, generated_at, indexed_field_recipe}`)
- cache by `sha256(model + dim + text)` in `scripts/.embedding-cache.json` so re-runs only embed *changed* papers

### Run command
```bash
export OPENAI_API_KEY=sk-...
python scripts/build_embeddings.py
```

### Validation (the script self-checks before writing)
- All vectors L2-normalised (norm ≈ 1.0 ± 0.001)
- `bin` file size == `count × dim × 4` bytes
- Cross-paper sanity: pick 3 papers, expect their top-3 nearest neighbours to share at least one of the same topic tags (otherwise the indexed-text recipe is broken)

---

## 5. Phase 2 spec — Cloudflare Worker adapted

Same as plan, but with OpenAI substituted for Voyage:

```typescript
// POST /embed-query   { text: string }  →  { vector: number[] }
const upstream = await fetch("https://api.openai.com/v1/embeddings", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${env.OPENAI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    input: text,
    model: "text-embedding-3-large",
    dimensions: 1024,           // truncate to match index
    encoding_format: "float",
  }),
});
```

Rate limit: 60 req / IP / hour (KV-backed). CORS allowlist: production + localhost.

`worker/` directory at repo root, deployed via `wrangler deploy`. No relation to `build.py` / GH Pages.

---

## 6. Phase 3 spec — frontend component

The plan's `ai-search.js` works as-is. Two adaptations to this repo:

- The site uses no bundler. The semantic-search component lives at `assets/ai-search.js`, loaded directly (no ES modules in the existing code; use the same global-IIFE pattern as `app.js`).
- The new page: `search.html` (EN) and `hu/search.html` (HU). Linked from the homepage hero (a small "Try the AI search →" link next to the keyword search bar).

Reuse existing patterns:
- `EFH.loadData()` to get authors/topics for filter dropdowns.
- `EFH.paperCardHtml(data, p, lang)` to render result cards consistently with the rest of the site.
- `assets/style.css` design tokens; add a small `assets/ai-search.css` for the textarea and counter UI only.

---

## 7. Phase ordering — proposed

| Phase | Output | Decisions still open |
|---|---|---|
| 0 | this doc | — (DONE) |
| 1 | `build_embeddings.py` + `static/embeddings.*` | none |
| 2 | Cloudflare Worker + deployed endpoint | needs OPENAI_API_KEY (editor) |
| 3 | `search.html` + `hu/search.html` + `assets/ai-search.js` | UI wording for HU |
| 4 | Hybrid retrieval (MiniSearch BM25 + RRF) | none |
| 5 | Filters (year, topic, country, method) | which filters to expose by default |
| 6 | (optional) Claude rationale layer | costs $ per query; defer |

Phases 1, 2, 3 ship a working semantic search. Phases 4–6 are polish.

---

## 8. Risks worth flagging

- **OpenAI API key on a Worker, not the site**. The key never enters the browser. Worker has its own secret store via `wrangler secret put`. This is the correct pattern; flag here so the editor doesn't accidentally drop the key into the repo.
- **HU queries on EN-only corpus**. OpenAI multilingual support is good for HU, but the corpus is monolingual. We should test with 5 real HU queries before declaring the cross-lingual case "works". The audit's first sanity check.
- **24 thin-text papers** (<50 tokens). They'll get embedded but retrieve poorly. Not a blocker. After v1 ships, the editor can backfill abstracts on these.
- **Future re-indexing**. The cache key is `sha256(model + dim + text)`. If the editor switches model later (e.g., to a newer OpenAI model), the cache invalidates correctly and the script re-embeds everything. ~$0.04 cost per full re-index.
- **Worker as a separate codebase**. The `worker/` directory will not be touched by `build.py` and lives alongside the static site. Editor needs a `wrangler` install and a Cloudflare account to deploy. One-time setup, then `wrangler deploy` for updates.

---

## 9. What I need from the editor before Phase 1

Nothing blocking. The five decisions are locked in (section 2). Proceed to Phase 1.

For Phase 2 (Worker deployment), the editor will need to:
1. Create a Cloudflare account (free)
2. Run `wrangler login` once
3. Run `wrangler secret put OPENAI_API_KEY` and paste the key

That can happen in parallel with Phase 1.
