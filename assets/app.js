/* Evidence for Hungary — client-side data layer and helpers.
 *
 * Loads data/index.json once, caches on window.__data, and exposes
 * render helpers used by the various pages.
 */

(function () {
  'use strict';

  // Resolve data/index.json relative to the site root, regardless of
  // whether the page is under / or /hu/.
  function dataUrl() {
    const path = window.location.pathname;
    const atRoot = !/\/hu\/[^?#]*$/.test(path);
    return atRoot ? 'data/index.json' : '../data/index.json';
  }

  function rootPrefix() {
    return /\/hu\/[^?#]*$/.test(window.location.pathname) ? '../' : '';
  }

  async function loadData() {
    if (window.__data) return window.__data;
    const res = await fetch(dataUrl());
    if (!res.ok) throw new Error('Failed to load data/index.json');
    const data = await res.json();

    // Index lookups for speed.
    data.authorsById = Object.fromEntries(data.authors.map(a => [a.id, a]));
    data.topicsById  = Object.fromEntries(data.topics.map(t => [t.id, t]));
    data.papersById  = Object.fromEntries(data.papers.map(p => [p.id, p]));
    data.journalsByName = Object.fromEntries(
      data.journals.map(j => [j.name, j])
    );

    window.__data = data;
    return data;
  }

  // -------- formatting helpers --------

  function esc(s) {
    if (s == null) return '';
    return String(s).replace(/[&<>"]/g, c => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'
    }[c]));
  }

  function authorName(data, id, lang) {
    const a = data.authorsById[id];
    if (!a) return id;
    return (lang === 'hu' && a.name_hu) ? a.name_hu : a.name_en;
  }

  function authorLink(data, id, lang) {
    const name = authorName(data, id, lang);
    const prefix = rootPrefix();
    return `<a href="${prefix}author.html?id=${encodeURIComponent(id)}">${esc(name)}</a>`;
  }

  function topicName(data, id, lang) {
    const t = data.topicsById[id];
    if (!t) return id;
    return (lang === 'hu' && t.name_hu) ? t.name_hu : t.name_en;
  }

  function topicLink(data, id, lang) {
    const prefix = rootPrefix();
    return `<a class="tag" href="${prefix}topic.html?id=${encodeURIComponent(id)}">${esc(topicName(data, id, lang))}</a>`;
  }

  function methodLabel(id) {
    const labels = {
      'rct': 'RCT / field experiment',
      'diff-in-diff': 'Difference-in-differences',
      'iv': 'Instrumental variables',
      'rd': 'Regression discontinuity',
      'panel-data': 'Panel / fixed effects',
      'synthetic-control': 'Synthetic control',
      'structural': 'Structural model',
      'theory': 'Theory',
      'time-series': 'Time series / VAR',
      'ml-text': 'ML / text analysis',
      'descriptive-survey': 'Descriptive / survey'
    };
    return labels[id] || id;
  }

  function dataTypeLabel(id) {
    const labels = {
      'admin-firm': 'Administrative firm',
      'admin-tax': 'Administrative tax',
      'admin-individual': 'Administrative individual',
      'survey': 'Survey',
      'firm-level-dataset': 'Firm-level commercial data',
      'field-experiment': 'Field experiment',
      'macro-aggregate': 'Macro / aggregate',
      'digital-trace': 'Digital trace',
      'historical': 'Historical / archival'
    };
    return labels[id] || id;
  }

  function firstSentence(text, maxWords) {
    if (!text) return '';
    const words = text.split(/\s+/);
    if (words.length <= maxWords) return text;
    return words.slice(0, maxWords).join(' ') + '…';
  }

  // -------- paper card renderer (shared) --------

  function paperCardHtml(data, paper, lang) {
    const authors = (paper.authors || []).map(id => authorLink(data, id, lang)).join(', ');
    const journal = paper.journal ? `<span class="journal">${esc(paper.journal)}</span>` : '';
    const year = paper.year || '';
    const summary = (lang === 'hu' && paper.summary_hu) ? paper.summary_hu : paper.summary_en;
    const blurb = firstSentence(summary || paper.abstract || '', 40);
    const topics = (paper.topics || []).map(t => topicLink(data, t, lang)).join(' ');
    const featured = paper.featured ? `<span class="tag tag-featured">Featured</span>` : '';
    const typeTag = paper.publication_type === 'working_paper'
      ? `<span class="tag tag-type">Working paper</span>`
      : paper.publication_type === 'chapter'
      ? `<span class="tag tag-type">Chapter</span>`
      : '';
    const prefix = rootPrefix();
    return `
      <article class="paper-card">
        <h3><a href="${prefix}paper.html?id=${encodeURIComponent(paper.id)}">${esc(paper.title)}</a></h3>
        <div class="meta">${authors} &middot; ${journal} &middot; ${year}</div>
        <div class="blurb">${esc(blurb)}</div>
        <div class="tags">${topics} ${featured} ${typeTag}</div>
      </article>
    `;
  }

  // -------- URL helpers --------

  function getParam(name) {
    const u = new URL(window.location.href);
    return u.searchParams.get(name);
  }

  // -------- very simple client-side search --------
  //
  // Scores each paper / author / topic by token match count over key
  // fields. Good enough for a few hundred entries. Swap for Pagefind
  // or a proper index if the catalogue passes ~1k items.

  function tokenize(s) {
    if (!s) return [];
    return s.toLowerCase()
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')  // strip diacritics
      .split(/[^a-z0-9]+/)
      .filter(Boolean);
  }

  function indexText(p) {
    return [
      p.title, p.abstract, p.summary_en, p.summary_hu,
      (p.authors || []).join(' '),
      (p.topics || []).join(' '),
      p.journal, p.policy_relevance
    ].filter(Boolean).join(' ');
  }

  function search(data, query) {
    const q = tokenize(query);
    if (q.length === 0) return { papers: [], authors: [], topics: [] };

    function score(text) {
      const toks = tokenize(text);
      const set = new Set(toks);
      let s = 0;
      for (const t of q) if (set.has(t)) s += 1;
      // partial match
      for (const t of q) {
        if (toks.some(x => x.includes(t))) s += 0.4;
      }
      return s;
    }

    const papers = data.papers
      .map(p => ({ p, s: score(indexText(p)) }))
      .filter(x => x.s > 0)
      .sort((a, b) => b.s - a.s)
      .slice(0, 12)
      .map(x => x.p);

    const authors = data.authors
      .map(a => ({ a, s: score(`${a.name_en} ${a.name_hu || ''} ${(a.affiliations || []).map(x => x.name).join(' ')} ${a.bio_en || ''}`) }))
      .filter(x => x.s > 0)
      .sort((a, b) => b.s - a.s)
      .slice(0, 8)
      .map(x => x.a);

    const topics = data.topics
      .map(t => ({ t, s: score(`${t.name_en} ${t.name_hu || ''} ${t.description_en || ''}`) }))
      .filter(x => x.s > 0)
      .sort((a, b) => b.s - a.s)
      .slice(0, 6)
      .map(x => x.t);

    return { papers, authors, topics };
  }

  function attachSearchBar(input, resultsEl) {
    let debounce;
    const prefix = rootPrefix();
    async function run() {
      const q = input.value.trim();
      if (!q) { resultsEl.classList.add('hidden'); resultsEl.innerHTML = ''; return; }
      const data = await loadData();
      const r = search(data, q);
      const total = r.papers.length + r.authors.length + r.topics.length;
      if (total === 0) {
        resultsEl.innerHTML = `<div class="empty">No matches for "${esc(q)}"</div>`;
      } else {
        let h = '';
        if (r.papers.length) {
          h += `<div class="group-label">Papers (${r.papers.length})</div>`;
          h += r.papers.map(p => `
            <a class="sr-item" href="${prefix}paper.html?id=${encodeURIComponent(p.id)}">
              <div>${esc(p.title)}</div>
              <div class="meta">${esc(p.journal || '')} &middot; ${p.year || ''}</div>
            </a>`).join('');
        }
        if (r.authors.length) {
          h += `<div class="group-label">Authors (${r.authors.length})</div>`;
          h += r.authors.map(a => `
            <a class="sr-item" href="${prefix}author.html?id=${encodeURIComponent(a.id)}">
              <div>${esc(a.name_en)}</div>
              <div class="meta">${esc((a.affiliations || [])[0]?.name || '')}</div>
            </a>`).join('');
        }
        if (r.topics.length) {
          h += `<div class="group-label">Topics (${r.topics.length})</div>`;
          h += r.topics.map(t => `
            <a class="sr-item" href="${prefix}topic.html?id=${encodeURIComponent(t.id)}">
              <div>${esc(t.name_en)}</div>
            </a>`).join('');
        }
        resultsEl.innerHTML = h;
      }
      resultsEl.classList.remove('hidden');
    }
    input.addEventListener('input', () => {
      clearTimeout(debounce);
      debounce = setTimeout(run, 120);
    });
    // focus handler
    document.addEventListener('keydown', (e) => {
      if (e.key === '/' && document.activeElement !== input) {
        e.preventDefault();
        input.focus();
        input.select();
      }
    });
    document.addEventListener('click', (e) => {
      if (!resultsEl.contains(e.target) && e.target !== input) {
        resultsEl.classList.add('hidden');
      }
    });
  }

  // expose
  window.EFH = {
    loadData, esc, authorName, authorLink, topicName, topicLink,
    methodLabel, dataTypeLabel, firstSentence, paperCardHtml,
    getParam, search, attachSearchBar, rootPrefix
  };
})();
