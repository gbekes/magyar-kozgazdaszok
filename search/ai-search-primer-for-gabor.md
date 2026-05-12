# AI Paper Search — Primer for Gábor

A short, no-jargon explainer of what we're building and why it works. ~10 minute read.

---

## The problem in one sentence

A journalist or policy adviser pastes "we want to reduce regional wage gaps via wage subsidies for small firms in eastern counties — what's the evidence?" into a box, and gets back the 5–10 most relevant papers from your catalogue, in either language.

Keyword search ("wage subsidy small firm") would miss a paper titled *"Place-based hiring incentives and rural employment in Hungary, 1998–2010"* even though that's exactly the right paper. Semantic search catches it.

---

## The mental model: papers as points in space

Forget AI for a second. Imagine you ran a giant factor analysis on every economics paper ever written, and ended up with, say, 1024 latent factors — things like "labour-supply-ish-ness", "Hungarian-context-ness", "RCT-method-ness", "DSGE-ness", and 1020 others that don't have clean names.

Each paper is now a point in 1024-dimensional space — a vector of factor loadings. Two papers on related topics sit close together; two papers on unrelated topics sit far apart. **An embedding is just that vector of factor loadings, produced by a model instead of by PCA.** That's the whole concept. If factor analysis on stock returns gives you each stock's exposure to size/value/momentum factors, an embedding model gives each paper its exposure to ~1000 latent semantic factors.

The user's 100-word problem description gets the same treatment — projected into the same 1024-dim space. Then we just compute the cosine similarity (the angle) between the user's vector and every paper's vector, and return the closest ones. **That's the entire AI search.**

The cleverness is not in our code. It's in the embedding model — a neural network trained on billions of texts to learn a projection where "semantically close" means "geometrically close". We just call its API.

---

## Why this is cheap

| Step | Cost |
|---|---|
| Embed all papers once | ~$0.05 for 500 papers (one-time, run when you add new papers) |
| Embed one user query | ~$0.00002 |
| Similarity search over 500 papers in browser | $0 (a few milliseconds of JS) |

Even with 10,000 daily users, you're paying cents per day. Embeddings are dramatically cheaper than running an LLM on every query.

---

## The architecture, top-down

```
User types problem (HU or EN)
       │
       ▼
Browser sends text to your tiny Cloudflare Worker
       │
       ▼
Worker calls Voyage/OpenAI Embeddings API ($0.00002)
       │
       ▼
Worker returns 1024-dim vector to browser
       │
       ▼
Browser already has embeddings.json for all papers (loaded once, cached)
       │
       ▼
Browser computes cosine similarity, sorts, shows top 10
```

Three pieces of infrastructure:
1. **`embeddings.json`** — a static file in your repo, ~5 MB for 500 papers. Generated once by a Python script when you add new papers.
2. **A Cloudflare Worker** — 50 lines of JavaScript that holds the API key and forwards user text to the embeddings provider. Free tier handles 100k requests/day.
3. **A search component on the site** — textarea + result list, ~200 lines of JS.

There is no database, no Pinecone, no vector store. For your scale, a JSON file is the database.

---

## Bilingual handling — the elegant bit

Multilingual embedding models (Voyage's `voyage-3-large`, OpenAI's `text-embedding-3-large`, open-source `multilingual-e5`) project Hungarian and English into the *same* space. So:

- A user can paste a Hungarian problem and find papers with English-only abstracts.
- You don't need to translate anything.
- For each paper, just embed `title_hu + abstract_hu + title_en + abstract_en` concatenated. The vector ends up sitting near both Hungarian and English queries on the same topic.

This is the killer feature for Evidence for Hungary — international audiences can query in English and reach Hungarian-only papers, and Hungarian journalists can query in Hungarian and reach English-only ones.

Caveat: Hungarian morphology is rough on embeddings. We should sanity-check on 10 real queries before committing to a model.

---

## What can go wrong (and the trap to avoid)

**The big trap: using Claude (or any LLM) to *generate* the answer.** If you do "Claude, here's a problem description, list relevant papers from Hungarian economics", Claude will confidently invent papers that don't exist. For a policy site, fabricated citations are a credibility-ending disaster. Embeddings retrieve real papers from your real catalogue. The LLM cannot hallucinate what it doesn't generate.

If we want the *feel* of AI on top, we add an optional second stage: take the top-10 embedding results and ask Claude to write a one-sentence rationale per paper, *strictly using only the papers we passed in*. That's safe — Claude is summarizing, not generating citations.

**Other things that bite:**
- **Short queries underperform.** "Inflation" returns garbage; "what does Hungarian evidence say about pass-through of energy price shocks to consumer prices, 2010–2022" returns gold. Hence our ~30-word minimum.
- **Pure semantic search misses exact-keyword cases.** A search for "Békés 2017" should find your paper, but cosine similarity might prefer something topically closer. Solution: hybrid retrieval — combine BM25 (classical keyword) with embeddings via Reciprocal Rank Fusion.
- **Vector search returns *something* for any query.** Even gibberish gets a ranked list. We should show similarity scores so users see when the match is weak, and add a threshold below which we say "no strong matches found".

---

## Why a soft 100-word target makes sense

- **Below ~30 words**: embedding gets too little context; recall collapses.
- **30–200 words**: sweet spot. The user has articulated a real problem.
- **200–500 words**: still works, marginal improvement.
- **Above 500 words**: dilutes the signal — averaging too many topics into one vector. Also opens the door to abuse (people pasting whole reports).

Show users "aim for 80–200 words" with a live counter (green/yellow/red). Hard-stop at 500 words / 3000 chars. **Minimum ~30 words** is more important than a tight maximum.

---

## What this won't do

- It won't *answer* the policy question. It surfaces relevant evidence; the user reads the papers.
- It won't rank by quality, only by topical relevance. A weak paper on the exact topic will rank above a brilliant paper on an adjacent topic. Filters (peer-reviewed, top-5, etc.) handle this separately.
- It won't notice if you've forgotten to include a paper in your catalogue. Garbage in, garbage out.

---

## Glossary (one line each)

- **Embedding**: a vector of numbers representing the meaning of a piece of text. Like factor loadings, but learned by a neural network.
- **Cosine similarity**: cosine of the angle between two vectors. 1 = same direction, 0 = orthogonal, –1 = opposite. Standard similarity measure for embeddings.
- **BM25**: a classical keyword-matching algorithm from information retrieval (basically TF-IDF with smarter normalization). Strong baseline.
- **Hybrid retrieval**: combining keyword (BM25) and semantic (embedding) results. Usually beats either alone.
- **Reciprocal Rank Fusion (RRF)**: simple way to combine rankings from two systems. Score = Σ 1/(60 + rank_i). Robust, parameter-free.
- **Cloudflare Worker**: a tiny JavaScript function that runs at the network edge. Free tier: 100k requests/day. Used here just to hide the API key.
- **Voyage / OpenAI embeddings**: the two leading commercial embedding APIs. Both support multilingual, both cheap.

---

## Decisions you need to make

1. **Embedding provider**: Voyage (slightly better quality, esp. multilingual) or OpenAI (slightly more familiar tooling). Both fine. Default: Voyage.
2. **Hosting for the Worker**: Cloudflare (recommended, generous free tier) or Vercel.
3. **AI rationales on top-K**: ship without them initially; add later as a "Get AI explanation" button.
4. **What counts as a "paper" record**: just abstracts, or also intros / non-technical summaries? More text generally helps recall.

The Claude Code plan in the companion file walks through implementation phase by phase.
