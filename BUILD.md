# Building and running the site

No Node. No bundler. Pure static HTML + CSS + vanilla JS, reading data from JSON files.

## Run locally

From the project root:

```bash
python build.py           # regenerate data/index.json from data/authors and data/papers
python -m http.server 8080
```

Open <http://localhost:8080/>. The Hungarian mirror is at <http://localhost:8080/hu/>.

## Add a paper

1. Copy `sample-paper.json` to `data/papers/<slug>.json`.
2. Edit the fields. Required: `id`, `title`, `authors`, `publication_type`, `year`, `abstract`, `topics`.
3. Run `python build.py`.
4. Refresh the browser.

## Add an author

1. Create `data/authors/<slug>.json` (schema in `SPEC.md` § 2.2).
2. Run `python build.py`.

`build.py` also expands any new entries in `authors-seed.json` into per-author files, skipping existing ones.

## Deploy

Any static host will do — drop the project directory, exclude `*.md` / `*.zip` / `*.skill` if you want:

- **GitHub Pages**: push to `main`, set Pages source to the root of the branch.
- **Vercel / Netlify**: point at the repo root, no build command, output directory `.`.
- **Cloudflare Pages**: same.

The site works over `file://` for most pages, but the search and data-driven pages need an HTTP server because they `fetch('data/index.json')`.

## Ingestion pipeline

The content pipeline lives in `scripts/ingest.py`. Three stages, mirroring `WORKFLOW.md`:

```bash
python -m pip install -r scripts/requirements.txt

# POSIX:    export ANTHROPIC_API_KEY=sk-ant-...
# PowerShell: $env:ANTHROPIC_API_KEY = "sk-ant-..."
# cmd.exe:    set ANTHROPIC_API_KEY=sk-ant-...

# For one author:
python scripts/ingest.py discover bekes-gabor     # OpenAlex → paper stubs
python scripts/ingest.py metadata <paper_id>      # Crossref → abstract + bibliographic
python scripts/ingest.py draft <paper_id>         # Claude → summary / data / policy / tags
# …or all three in one go:
python scripts/ingest.py run bekes-gabor --max-works 20

# Inspect the state:
python scripts/ingest.py status

# Preview the Claude prompt without calling the API:
python scripts/ingest.py draft <paper_id> --dry-run
```

Guarantees:

- Never overwrites a paper that has `review_status` of `human-reviewed` or `author-approved` (pass `--force` if you actually mean to).
- Skips draft for papers without abstracts (run `metadata` first, or pass `--force`).
- Only touches `data/papers/<slug>.json` and the one author JSON it's resolving.
- OpenAlex calls include a `mailto` header (polite pool); ~0.3s sleep between calls.

Drafting model defaults to `claude-opus-4-7`. System prompt is cached (`cache_control: ephemeral`) so batch runs amortise the cost.

After any pipeline run, re-run `python build.py` to refresh `data/index.json` that the site reads.

## Structure

```
/                        site root — HTML pages
  index.html
  papers.html  paper.html
  authors.html author.html
  topics.html  topic.html
  about.html   contribute.html
  hu/                    Hungarian mirror (landing stubbed, links back to EN for details)
  assets/
    style.css            viridis-flavoured, ~300 lines
    app.js               data loader + render helpers + search
    chrome.js            header/footer injection
  data/
    index.json           aggregated — rebuilt by build.py
    authors/<id>.json    one per author
    papers/<id>.json     one per paper
    topics.json
    journals.json
build.py                 expand seed authors + regenerate index
```
