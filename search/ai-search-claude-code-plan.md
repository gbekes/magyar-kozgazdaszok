# Evidence for Hungary — AI Paper Search: Implementation Plan for Claude Code

**Project**: `gbekes/magyar-kozgazdaszok` ("Evidence for Hungary")
**Feature**: Semantic search where users paste a ~100-word problem description and get the top-K most relevant papers from the catalogue, working bilingually (HU ↔ EN).
**Architecture**: Pre-computed embeddings + Cloudflare Worker for query embedding + client-side cosine similarity. Companion primer in `ai-search-primer-for-gabor.md`.

---

## Operating principles

1. **Don't write code yet.** Phase 0 is audit-only. Read the repo, understand the framework and data model, surface decisions Gábor needs to make, then propose a concrete spec before touching anything.
2. **Use real packages.** Verify that the suggested libraries (`MiniSearch`, `voyage` / `openai` SDKs) and embedding model names below are still current at execution time — model names drift.
3. **Bilingual is non-negotiable.** Every embedding, every UI string, every test case lives in HU and EN.
4. **No hallucination surface.** The LLM never *generates* citations. It only re-ranks or summarizes papers already retrieved by embeddings.
5. **Cheap before clever.** Ship hybrid retrieval (BM25 + embeddings) before adding any LLM rationale step.

---

## Phase 0 — Audit (no code, ~30 min)

**Goal**: produce a one-page memo to Gábor with answers to the questions below before any implementation starts.

Tasks:
- [ ] Identify the static-site framework (Quarto? Hugo? Next.js static? Astro?) and the build pipeline.
- [ ] Locate the paper catalogue. Where do paper records live — YAML frontmatter? JSON file? CSV? Database?
- [ ] List the fields available per paper. Required for a good search index: `id`, `title_hu`, `title_en`, `abstract_hu`, `abstract_en`, `authors`, `year`, `jel_codes`, `keywords`, `url`. Note any gaps.
- [ ] Estimate corpus size (count of papers). Determines whether `embeddings.json` shipped to the browser stays under ~5 MB.
- [ ] Check existing JS infrastructure on the site — does it already have a build step that emits JS bundles, or is it pure static HTML?
- [ ] Check for an existing search feature. If one exists, decide whether to replace or augment.
- [ ] Note CI setup — GitHub Actions? Anything that runs on PRs?

**Deliverable**: `docs/ai-search-audit.md` summarizing the above plus three explicit questions Gábor must answer before Phase 1:
1. Voyage or OpenAI as embeddings provider? (Default recommendation: Voyage `voyage-3-large` if available, OpenAI `text-embedding-3-large` as fallback.)
2. Cloudflare Workers or Vercel Edge for the query embedding endpoint? (Default: Cloudflare.)
3. What's a "paper" for indexing — just abstract, or abstract + intro + non-technical summary? (More text → better recall, with diminishing returns past ~1500 tokens per paper.)

**Stop here. Do not proceed to Phase 1 until Gábor answers these three.**

---

## Phase 1 — Indexing pipeline (offline)

**Goal**: a script that reads all papers and writes `static/embeddings.bin` (binary Float32) + `static/embeddings-meta.json` (paper metadata, parallel-indexed to the binary).

### Files to create

```
scripts/build-embeddings.py
scripts/build-embeddings.requirements.txt
.github/workflows/rebuild-embeddings.yml   # optional, can skip initially
```

### `build-embeddings.py` — concrete spec

```python
# Pseudocode — adapt to the actual data layout discovered in Phase 0

import json, os, struct
from pathlib import Path
import numpy as np
import voyageai  # or: from openai import OpenAI

PROVIDER = os.environ.get("EMBEDDING_PROVIDER", "voyage")
MODEL    = os.environ.get("EMBEDDING_MODEL", "voyage-3-large")
DIM      = 1024  # voyage-3-large; check at runtime

def build_text(paper: dict) -> str:
    """Concatenate the fields that should drive retrieval."""
    parts = []
    for key in ("title_hu", "title_en", "authors", "abstract_hu", "abstract_en", "keywords"):
        if v := paper.get(key):
            parts.append(str(v))
    return "\n\n".join(parts)

def embed_batch(texts: list[str]) -> np.ndarray:
    if PROVIDER == "voyage":
        client = voyageai.Client()
        # input_type="document" is the documented hint for indexing-time embeddings
        result = client.embed(texts, model=MODEL, input_type="document")
        return np.array(result.embeddings, dtype=np.float32)
    else:
        from openai import OpenAI
        client = OpenAI()
        result = client.embeddings.create(model=MODEL, input=texts)
        return np.array([d.embedding for d in result.data], dtype=np.float32)

def main():
    papers = load_all_papers()  # implement based on Phase 0 findings
    texts  = [build_text(p) for p in papers]

    # Batch in groups of 64–128 to stay under per-request token limits
    vectors = []
    for i in range(0, len(texts), 64):
        vectors.append(embed_batch(texts[i:i+64]))
        print(f"Embedded {i+64}/{len(texts)}")
    matrix = np.vstack(vectors)

    # L2-normalize so cosine similarity becomes a dot product in the browser
    matrix /= np.linalg.norm(matrix, axis=1, keepdims=True)

    # Write binary: rows of float32, no header
    Path("static/embeddings.bin").write_bytes(matrix.astype(np.float32).tobytes())

    # Parallel metadata file
    meta = [{
        "id": p["id"],
        "title_hu": p.get("title_hu"),
        "title_en": p.get("title_en"),
        "authors": p.get("authors"),
        "year": p.get("year"),
        "url": p.get("url"),
        "abstract_hu_short": (p.get("abstract_hu") or "")[:300],
        "abstract_en_short": (p.get("abstract_en") or "")[:300],
        "jel_codes": p.get("jel_codes", []),
    } for p in papers]
    Path("static/embeddings-meta.json").write_text(json.dumps(meta, ensure_ascii=False))

    Path("static/embeddings-info.json").write_text(json.dumps({
        "model": MODEL, "dim": DIM, "count": len(papers), "provider": PROVIDER
    }))
```

### Make it idempotent
Cache embeddings by hash of input text so re-runs only embed *changed* papers. Add a small SQLite or JSON cache file `scripts/.embedding-cache.json` keyed on `sha256(model + text)`.

### Output sizes (sanity check)
- 500 papers × 1024 dim × 4 bytes = **2 MB** binary. Gzip serves at ~1.4 MB. Fine.
- Metadata JSON: ~200 KB for 500 papers. Fine.

### How to run
```bash
export VOYAGE_API_KEY=...   # or OPENAI_API_KEY
pip install -r scripts/build-embeddings.requirements.txt
python scripts/build-embeddings.py
```

### Verification before declaring done
- [ ] `embeddings.bin` size matches `count × dim × 4` exactly
- [ ] All vectors normalized (norm ≈ 1.0 for every row, check 5 random rows)
- [ ] Spot-check: pick 3 papers, embed their abstracts again, confirm self-similarity > 0.95 (sanity for the cache and pipeline)
- [ ] Cross-lingual sanity: a paper with both HU and EN abstracts should be one of its own nearest neighbors

---

## Phase 2 — Cloudflare Worker for query embedding

**Goal**: a single endpoint that takes user text, embeds it, returns the vector. Hides the API key. Rate-limits.

### Files

```
worker/
  src/index.ts
  wrangler.toml
  package.json
```

### `src/index.ts` — concrete spec

```typescript
// Single endpoint: POST /embed-query  { text: string } -> { vector: number[] }

const MAX_CHARS = 3000;
const MIN_CHARS = 50;
const ALLOWED_ORIGINS = [
  "https://magyar-kozgazdaszok.org",     // replace with real domain
  "https://gbekes.github.io",
  "http://localhost:3000",
];

interface Env {
  VOYAGE_API_KEY: string;
  // OPENAI_API_KEY?: string;
  RATE_LIMIT_KV: KVNamespace;  // for simple per-IP rate limiting
}

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const origin = req.headers.get("Origin") ?? "";
    const corsHeaders = ALLOWED_ORIGINS.includes(origin)
      ? { "Access-Control-Allow-Origin": origin, "Vary": "Origin" }
      : {};

    if (req.method === "OPTIONS") {
      return new Response(null, { headers: { ...corsHeaders,
        "Access-Control-Allow-Methods": "POST",
        "Access-Control-Allow-Headers": "Content-Type" }});
    }
    if (req.method !== "POST") return new Response("Method not allowed", { status: 405 });

    // Per-IP rate limit: 60 requests/hour
    const ip = req.headers.get("CF-Connecting-IP") ?? "unknown";
    const key = `rl:${ip}:${Math.floor(Date.now() / 3_600_000)}`;
    const count = parseInt((await env.RATE_LIMIT_KV.get(key)) ?? "0");
    if (count >= 60) {
      return new Response(JSON.stringify({ error: "rate_limited" }),
        { status: 429, headers: { ...corsHeaders, "Content-Type": "application/json" }});
    }
    await env.RATE_LIMIT_KV.put(key, String(count + 1), { expirationTtl: 3700 });

    const body = await req.json() as { text?: string };
    const text = (body.text ?? "").trim();
    if (text.length < MIN_CHARS || text.length > MAX_CHARS) {
      return new Response(JSON.stringify({
        error: "bad_length", min: MIN_CHARS, max: MAX_CHARS, got: text.length
      }), { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" }});
    }

    // Call Voyage
    const upstream = await fetch("https://api.voyageai.com/v1/embeddings", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${env.VOYAGE_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        input: [text],
        model: "voyage-3-large",
        input_type: "query",   // important: query vs. document
      }),
    });
    if (!upstream.ok) {
      return new Response(JSON.stringify({ error: "upstream", status: upstream.status }),
        { status: 502, headers: { ...corsHeaders, "Content-Type": "application/json" }});
    }
    const data = await upstream.json() as { data: { embedding: number[] }[] };
    return new Response(JSON.stringify({ vector: data.data[0].embedding }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
};
```

### Setup commands

```bash
npm install -g wrangler
cd worker && npm install
wrangler kv namespace create RATE_LIMIT_KV
# add the returned id to wrangler.toml
wrangler secret put VOYAGE_API_KEY
wrangler deploy
```

### Verification
- [ ] `curl -X POST <worker-url>/embed-query -d '{"text":"<60+ char query>"}'` returns a 1024-element array
- [ ] Same call from a non-allowed origin gets no CORS header
- [ ] 61st call within an hour from the same IP returns 429
- [ ] Empty / too-short / too-long text returns 400

---

## Phase 3 — Frontend search component

**Goal**: textarea with live word counter, submit button, results list. Loads `embeddings.bin` once and caches it.

### Files (assuming Quarto/Hugo/Astro — adjust paths)

```
assets/js/ai-search.js
assets/css/ai-search.css
layouts/partials/ai-search.html   # or equivalent shortcode/component
```

### `ai-search.js` — concrete spec

```javascript
// State
let EMBEDDINGS = null;   // Float32Array, length = count * dim
let META       = null;   // array of paper metadata
let INFO       = null;   // { model, dim, count }
const WORKER_URL = "https://embed-query.<your-subdomain>.workers.dev";

// Lazy-load the index on first use
async function loadIndex() {
  if (EMBEDDINGS) return;
  const [binResp, metaResp, infoResp] = await Promise.all([
    fetch("/static/embeddings.bin"),
    fetch("/static/embeddings-meta.json"),
    fetch("/static/embeddings-info.json"),
  ]);
  const buf = await binResp.arrayBuffer();
  EMBEDDINGS = new Float32Array(buf);
  META = await metaResp.json();
  INFO = await infoResp.json();
  if (EMBEDDINGS.length !== INFO.count * INFO.dim) {
    throw new Error("embedding index size mismatch");
  }
}

// Cosine similarity, given normalized vectors, is just a dot product
function dot(a, bOffset, dim) {
  let s = 0;
  for (let i = 0; i < dim; i++) s += a[i] * EMBEDDINGS[bOffset + i];
  return s;
}

async function search(text, k = 10) {
  await loadIndex();
  // Get query vector from Worker
  const resp = await fetch(`${WORKER_URL}/embed-query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!resp.ok) throw new Error(`embed failed: ${resp.status}`);
  const { vector } = await resp.json();
  const q = new Float32Array(vector);
  // Normalize the query (Voyage already does, but be safe)
  let norm = 0; for (const v of q) norm += v*v;
  norm = Math.sqrt(norm);
  for (let i = 0; i < q.length; i++) q[i] /= norm;

  // Score every paper
  const dim = INFO.dim;
  const scores = new Float32Array(INFO.count);
  for (let i = 0; i < INFO.count; i++) {
    scores[i] = dot(q, i * dim, dim);
  }
  // Top-k
  const idx = Array.from({length: INFO.count}, (_, i) => i)
    .sort((a, b) => scores[b] - scores[a])
    .slice(0, k);
  return idx.map(i => ({ ...META[i], score: scores[i] }));
}

// UI wiring
function wireUI() {
  const ta = document.querySelector("#ai-search-input");
  const counter = document.querySelector("#ai-search-counter");
  const btn = document.querySelector("#ai-search-submit");
  const results = document.querySelector("#ai-search-results");

  function updateCounter() {
    const words = ta.value.trim().split(/\s+/).filter(Boolean).length;
    let cls = "ok";
    if (words < 30)  cls = "low";
    if (words > 300) cls = "high";
    if (words > 500) cls = "over";
    counter.textContent = `${words} words`;
    counter.className = `counter counter-${cls}`;
    btn.disabled = words < 20 || words > 500;
  }
  ta.addEventListener("input", updateCounter); updateCounter();

  btn.addEventListener("click", async () => {
    btn.disabled = true; results.innerHTML = "Searching…";
    try {
      const hits = await search(ta.value);
      results.innerHTML = hits.map(h => `
        <article class="result" data-score="${h.score.toFixed(3)}">
          <h3><a href="${h.url}">${h.title_en || h.title_hu}</a></h3>
          <p class="meta">${(h.authors || []).join(", ")} · ${h.year} · score ${h.score.toFixed(2)}</p>
          <p>${h.abstract_en_short || h.abstract_hu_short}</p>
        </article>`).join("");
    } catch (e) {
      results.innerHTML = `<p class="error">Search failed: ${e.message}</p>`;
    } finally { btn.disabled = false; }
  });
}
document.addEventListener("DOMContentLoaded", wireUI);
```

### Counter thresholds (mirrors Gábor's primer)
- < 20 words → submit disabled, message "Add more detail — try 80–200 words"
- 20–30 words → enabled, yellow warning "Short queries return weaker matches"
- 30–300 words → green
- 300–500 words → yellow "Approaching limit"
- 500 words → submit disabled

### Verification
- [ ] Page loads `embeddings.bin` once; second search reuses in-memory copy
- [ ] Top-1 result for "Place-based hiring incentives in Eastern Hungary" matches a relevant paper
- [ ] HU query returns mix of HU and EN titled papers with reasonable scores
- [ ] Score < 0.4 shows a "weak match" indicator

---

## Phase 4 — Hybrid retrieval (BM25 + embeddings)

**Goal**: combine semantic and keyword scores via Reciprocal Rank Fusion. Often catches papers that pure semantic search misses (exact author names, exact JEL codes, paper titles).

### Add `MiniSearch.js` to the bundle

```javascript
import MiniSearch from "minisearch";

const bm25 = new MiniSearch({
  fields: ["title_hu", "title_en", "abstract_hu", "abstract_en",
           "authors_str", "keywords_str"],
  storeFields: ["id"],
  searchOptions: { boost: { title_en: 2, title_hu: 2 }, fuzzy: 0.2, prefix: true },
});
bm25.addAll(META.map((m, i) => ({
  id: i,
  title_hu: m.title_hu, title_en: m.title_en,
  abstract_hu: m.abstract_hu_short, abstract_en: m.abstract_en_short,
  authors_str: (m.authors || []).join(" "),
  keywords_str: (m.keywords || []).join(" "),
})));

// RRF combination
function rrf(rankedLists, k = 60) {
  const scores = new Map();
  for (const list of rankedLists) {
    list.forEach((id, rank) => {
      scores.set(id, (scores.get(id) || 0) + 1 / (k + rank));
    });
  }
  return [...scores.entries()].sort((a, b) => b[1] - a[1]).map(([id]) => id);
}
```

In the `search` function: get top-50 from each system, RRF, slice top-K.

---

## Phase 5 — Filters

**Goal**: hard filters alongside the AI search box.

UI controls:
- Year range slider
- JEL code multi-select (top-level only: A–Z)
- Method tags: RCT, IV/RDD, DiD, Structural, Descriptive
- Language: HU only / EN only / Either

Apply filters *after* retrieval, on the metadata. If filtered set is empty, show "No matches with these filters — relaxing year range" and re-run without the year filter.

---

## Phase 6 — Optional: Claude rationale layer

**Only after Phases 1–5 ship and feedback comes in.**

Add a "Get AI explanations" button on the results page. Calls a second Worker endpoint `/explain-results` that:
1. Takes `{ query: string, papers: PaperMeta[] }` (top-10 from the retrieval).
2. Prompts Claude with a strict template:

```
You are helping a policy researcher understand why each of the following papers
was retrieved as relevant to their question. Write ONE sentence per paper
explaining the connection. Only use information from the paper metadata
provided. Do NOT introduce papers, authors, or claims that are not in the list.
If a paper's relevance is weak or unclear, say so.

User question:
<query>

Papers:
1. <title> (<authors>, <year>) — <abstract excerpt>
2. ...

Output JSON: [{"id": ..., "rationale": "..."}]
```

3. Returns the JSON to the browser, which renders rationales inline.

Use `claude-haiku-4-5-20251001` for cost; the task is light.

**Hard rule in prompt and in code**: drop any rationale that mentions an author or paper not in the input list. Better to show fewer rationales than fabricated ones.

---

## Cost / capacity envelope

- One-time indexing of 500 papers: **~$0.05**
- Per query (just embedding): **~$0.00002**
- Per query (with Claude rationale): **~$0.005**
- Cloudflare Workers free tier: **100,000 requests/day**
- Bandwidth for `embeddings.bin` (gzipped ~1.4 MB): served free from GitHub Pages or whatever static host

Even at 10,000 queries/day with rationale enabled, monthly cost is in single dollars.

---

## Repo layout after implementation

```
.
├── scripts/
│   ├── build-embeddings.py
│   └── build-embeddings.requirements.txt
├── worker/
│   ├── src/index.ts
│   ├── wrangler.toml
│   └── package.json
├── static/
│   ├── embeddings.bin           # generated, committed (small) or in Releases (large)
│   ├── embeddings-meta.json
│   └── embeddings-info.json
├── assets/
│   ├── js/ai-search.js
│   └── css/ai-search.css
└── docs/
    ├── ai-search-audit.md       # Phase 0 output
    └── ai-search-architecture.md  # link to primer
```

---

## Things Claude Code should explicitly NOT do

1. **Don't add a vector database.** No Pinecone, no Weaviate, no Postgres+pgvector. JSON file is the database for this scale.
2. **Don't run embeddings on every page build.** Cache by content hash; only re-embed changed papers.
3. **Don't ship API keys to the client.** All embedding calls go through the Worker.
4. **Don't let Claude generate citations.** The LLM step (Phase 6) only summarizes papers we explicitly pass in. Add a post-hoc check that every cited title/author appears in the input list.
5. **Don't ship Phase 6 in v1.** Hybrid retrieval (Phase 4) plus filters (Phase 5) covers most real use; LLM rationales are polish.

---

## Open questions for Gábor (resolve before Phase 1)

1. **Embedding provider**: Voyage `voyage-3-large` or OpenAI `text-embedding-3-large`?
2. **Worker host**: Cloudflare or Vercel?
3. **Per-paper indexed text**: just abstract, or also intro / non-technical summary if available?
4. **Domain for CORS allowlist**: what's the production URL?
5. **Where does `embeddings.bin` live**: committed to repo, or fetched from GitHub Releases / a CDN at runtime?

---

## Suggested commit sequence

1. `chore: phase 0 audit doc` (no code change)
2. `feat(scripts): add embedding build pipeline` — Phase 1
3. `feat(worker): add query embedding endpoint` — Phase 2
4. `feat(site): add semantic search UI` — Phase 3, behind a feature flag
5. `feat(search): hybrid BM25 + embedding retrieval` — Phase 4
6. `feat(search): filters and weak-match handling` — Phase 5
7. (later) `feat(search): optional Claude rationale layer` — Phase 6

Each commit deployable on its own; nothing in 1–6 depends on the next.
