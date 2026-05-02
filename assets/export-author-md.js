/* Evidence for Hungary — client-side per-author markdown export.
 *
 * Builds a single editable markdown record for one author from data/index.json,
 * matching the format produced by scripts/export_author_md.py. Used by
 * author.html and contribute.html for the "Download my record" feature.
 */
(function () {
  'use strict';

  const EMPTY = '—';

  function fld(label, value) {
    if (value == null || value === '') return `- **${label}:** ${EMPTY}`;
    if (Array.isArray(value)) {
      if (value.length === 0) return `- **${label}:** ${EMPTY}`;
      return `- **${label}:** ${value.join(', ')}`;
    }
    return `- **${label}:** ${value}`;
  }

  function block(label, text) {
    if (!text) return `### ${label}\n\n_(empty)_\n`;
    return `### ${label}\n\n${text}\n`;
  }

  function authorDisplayName(authorsById, slug) {
    const a = authorsById[slug];
    if (a) return a.name_en || a.name_hu || slug;
    return slug;
  }

  function formatAuthors(authors, authorsById) {
    return (authors || []).map(s => authorDisplayName(authorsById, s)).join(', ');
  }

  function renderHeader(a, lang) {
    const name = lang === 'hu' ? (a.name_hu || a.name_en) : (a.name_en || a.name_hu);
    const altName = lang === 'hu' ? a.name_en : a.name_hu;
    const lines = [];
    lines.push(`# ${name || a.id}`);
    if (altName && altName !== name) lines.push(`_(${altName})_`);
    lines.push('');
    lines.push(`<!-- author-slug: ${a.id} -->`);
    lines.push('');
    if (lang === 'hu') {
      lines.push('> **Hogyan használd ezt a fájlt**');
      lines.push('>');
      lines.push('> Ez egy pillanatfelvétel mindenről, ami rólad a katalógusban szerepel.');
      lines.push('> Bármelyik mezőt szabadon szerkesztheted. `[ADD]` jelölést tegyél új tételhez,');
      lines.push('> `[REMOVE]` jelölést egy hibás vagy törlendő tétel mellé,');
      lines.push('> és `[FIX]` jelölést bármi javítandó mellé. Küldd vissza emailben,');
      lines.push('> vagy csatold egy GitHub issue-hoz. A változtatásokat bevezetjük.');
    } else {
      lines.push('> **How to use this file**');
      lines.push('>');
      lines.push('> This is a snapshot of everything we have on you in the catalogue.');
      lines.push('> Edit any field directly. Add `[ADD]` to introduce a new item, mark');
      lines.push('> `[REMOVE]` next to an item that is wrong or shouldn\'t be listed,');
      lines.push('> and `[FIX]` next to anything that needs correction. Email the edited');
      lines.push('> file back, or attach it to a GitHub issue. We\'ll apply the changes.');
    }
    lines.push('');
    lines.push('---');
    lines.push('');
    return lines.join('\n');
  }

  function renderPersonal(a, lang) {
    const out = [];
    out.push(lang === 'hu' ? '## Személyes adatok' : '## Personal info', '');
    out.push(fld(lang === 'hu' ? 'Név (EN)' : 'Name (EN)', a.name_en));
    out.push(fld(lang === 'hu' ? 'Név (HU)' : 'Name (HU)', a.name_hu));
    out.push(fld(lang === 'hu' ? 'Honlap' : 'Website', a.website));
    out.push(fld('Email', a.email));
    out.push(fld(lang === 'hu' ? 'Fotó URL' : 'Photo URL', a.photo_url));
    out.push(fld('RePEc ID', a.repec_id));
    out.push(fld('Google Scholar ID', a.scholar_id));
    out.push(fld('ORCID', a.orcid));
    out.push(fld('OpenAlex ID', a.openalex_id));
    out.push(fld(lang === 'hu' ? 'Médiamegkeresésre nyitott (EN)' : 'Open to media (EN)',
                 a.open_to_media_en ? (lang === 'hu' ? 'Igen' : 'Yes') : (lang === 'hu' ? 'Nem' : 'No')));
    out.push(fld(lang === 'hu' ? 'Médiamegkeresésre nyitott (HU)' : 'Open to media (HU)',
                 a.open_to_media_hu ? (lang === 'hu' ? 'Igen' : 'Yes') : (lang === 'hu' ? 'Nem' : 'No')));
    out.push(fld(lang === 'hu' ? 'Megjegyzés' : 'Media note', a.media_note));
    out.push(fld(lang === 'hu' ? 'Fő területek' : 'Primary fields', a.primary_fields));
    out.push('');

    out.push(lang === 'hu' ? '### Affiliációk' : '### Affiliations', '');
    const affs = a.affiliations || [];
    if (!affs.length) {
      out.push(lang === 'hu' ? '_(nincs rögzítve)_' : '_(none recorded)_');
    } else {
      affs.forEach((af, i) => {
        const nameEn = af.name || '';
        const nameHu = af.name_hu || '';
        const roleEn = af.role || '';
        const roleHu = af.role_hu || '';
        let line = `${i + 1}. **${nameEn}**`;
        if (nameHu && nameHu !== nameEn) line += ` / ${nameHu}`;
        if (roleEn || roleHu) {
          line += ' — ';
          if (roleEn) line += roleEn;
          if (roleHu && roleHu !== roleEn) line += ` (${roleHu})`;
        }
        out.push(line);
      });
    }
    out.push('');

    out.push(block(lang === 'hu' ? 'Bemutatkozás (EN)' : 'Bio (EN)', a.bio_en));
    out.push(block(lang === 'hu' ? 'Bemutatkozás (HU)' : 'Bio (HU)', a.bio_hu));

    const qp = a.qualifying_publication || {};
    if (qp.title) {
      out.push(lang === 'hu' ? '### Beválasztó publikáció' : '### Qualifying publication', '');
      out.push(fld(lang === 'hu' ? 'Cím' : 'Title', qp.title));
      out.push(fld(lang === 'hu' ? 'Folyóirat' : 'Journal', qp.journal));
      out.push(fld(lang === 'hu' ? 'Év' : 'Year', qp.year));
      out.push('');
    }
    return out.join('\n');
  }

  function renderPaper(p, authorsById, lang) {
    const out = [];
    out.push(`### ${p.title || (lang === 'hu' ? '(cím nélkül)' : '(untitled)')}`);
    out.push('');
    out.push(`<!-- paper-slug: ${p.id} -->`);
    out.push('');
    out.push(fld(lang === 'hu' ? 'Szerzők' : 'Authors', formatAuthors(p.authors, authorsById)));
    out.push(fld(lang === 'hu' ? 'Folyóirat' : 'Journal', p.journal));
    out.push(fld(lang === 'hu' ? 'Év' : 'Year', p.year));
    out.push(fld(
      lang === 'hu' ? 'Évf./Szám/Oldalak' : 'Volume / Issue / Pages',
      [p.volume, p.issue, p.pages].map(v => v == null || v === '' ? '—' : v).join(' / ')
    ));
    out.push(fld('DOI', p.doi));
    out.push(fld(lang === 'hu' ? 'URL (megjelent)' : 'URL (published)', p.url_published));
    out.push(fld('PDF URL', p.url_pdf));
    out.push(fld(lang === 'hu' ? 'Replikációs URL' : 'Replication URL', p.url_replication));
    out.push(fld(lang === 'hu' ? 'Working paper sorozat' : 'Working paper series', p.working_paper_series));
    out.push(fld(lang === 'hu' ? 'Témák' : 'Topics', p.topics));
    out.push(fld(lang === 'hu' ? 'Módszerek' : 'Methods', p.methods));
    out.push(fld(lang === 'hu' ? 'Vizsgált országok' : 'Countries studied', p.countries_studied));
    out.push(fld(lang === 'hu' ? 'Adattípusok' : 'Data types', p.data_types));
    out.push(fld(lang === 'hu' ? 'Szakpolitikai eszközök' : 'Policy instruments', p.policy_instruments));
    out.push('');
    out.push(block(lang === 'hu' ? 'Absztrakt' : 'Abstract', p.abstract));
    out.push(block(lang === 'hu' ? 'Összefoglaló (EN)' : 'Summary (EN)', p.summary_en));
    out.push(block(lang === 'hu' ? 'Összefoglaló (HU)' : 'Summary (HU)', p.summary_hu));
    out.push(block(lang === 'hu' ? 'Felhasznált adatok (EN)' : 'Data used (EN)', p.data_used));
    out.push(block(lang === 'hu' ? 'Felhasznált adatok (HU)' : 'Data used (HU)', p.data_used_hu));
    out.push(block(lang === 'hu' ? 'Szakpolitikai relevancia (EN)' : 'Policy relevance (EN)', p.policy_relevance));
    out.push(block(lang === 'hu' ? 'Szakpolitikai relevancia (HU)' : 'Policy relevance (HU)', p.policy_relevance_hu));
    return out.join('\n');
  }

  function renderPolicy(p, authorsById, lang) {
    const out = [];
    out.push(`### ${p.title || (lang === 'hu' ? '(cím nélkül)' : '(untitled)')}`);
    out.push('');
    out.push(`<!-- policy-slug: ${p.id} -->`);
    out.push('');
    out.push(fld(lang === 'hu' ? 'Szerzők' : 'Authors', formatAuthors(p.authors, authorsById)));
    out.push(fld(lang === 'hu' ? 'Típus' : 'Outlet kind', p.outlet_kind));
    out.push(fld(lang === 'hu' ? 'Kiadás' : 'Outlet', p.outlet));
    out.push(fld(lang === 'hu' ? 'Szám/Évfolyam' : 'Outlet issue', p.outlet_issue));
    out.push(fld(lang === 'hu' ? 'Intézmény' : 'Institution', p.institution));
    out.push(fld(lang === 'hu' ? 'Év' : 'Year', p.year));
    out.push(fld(lang === 'hu' ? 'Nyelv' : 'Language', p.language));
    out.push(fld('URL', p.url));
    out.push(fld('DOI', p.doi));
    out.push(fld(lang === 'hu' ? 'Kapcsolt cikk' : 'Linked paper', p.linked_paper_id));
    out.push(fld(lang === 'hu' ? 'Témák' : 'Topics', p.topics));
    out.push(fld(lang === 'hu' ? 'Országok' : 'Countries', p.countries_studied));
    out.push('');
    out.push(block(lang === 'hu' ? 'Összefoglaló (EN)' : 'Summary (EN)', p.summary_en));
    out.push(block(lang === 'hu' ? 'Összefoglaló (HU)' : 'Summary (HU)', p.summary_hu));
    out.push(block(lang === 'hu' ? 'Szakpolitikai relevancia (EN)' : 'Policy relevance (EN)', p.policy_relevance));
    out.push(block(lang === 'hu' ? 'Szakpolitikai relevancia (HU)' : 'Policy relevance (HU)', p.policy_relevance_hu));
    return out.join('\n');
  }

  function renderPress(p, authorsById, lang) {
    const out = [];
    out.push(`### ${p.title || (lang === 'hu' ? '(cím nélkül)' : '(untitled)')}`);
    if (p.title_hu) out.push(`_${p.title_hu}_`);
    out.push('');
    out.push(`<!-- press-slug: ${p.id} -->`);
    out.push('');
    out.push(fld(lang === 'hu' ? 'Szerzők' : 'Authors', formatAuthors(p.authors, authorsById)));
    out.push(fld(lang === 'hu' ? 'Típus' : 'Kind', p.kind));
    out.push(fld(lang === 'hu' ? 'Megjelenés helye' : 'Venue', p.venue));
    out.push(fld(lang === 'hu' ? 'Dátum' : 'Date', p.date));
    out.push(fld(lang === 'hu' ? 'Nyelv' : 'Language', p.language));
    out.push(fld('URL', p.url));
    out.push(fld(lang === 'hu' ? 'Kapcsolt cikk' : 'Linked paper', p.linked_paper_id));
    out.push('');
    out.push(block(lang === 'hu' ? 'Rövid leírás' : 'Blurb', p.blurb));
    return out.join('\n');
  }

  function buildAuthorMarkdown(data, slug, lang) {
    lang = lang || 'en';
    const a = data.authorsById[slug];
    if (!a) return null;

    const authorsById = data.authorsById;
    const papers = (data.papers || []).filter(p => (p.authors || []).includes(slug));
    const policy = (data.policy || []).filter(p => (p.authors || []).includes(slug));
    const press  = (data.press  || []).filter(p => (p.authors || []).includes(slug));

    papers.sort((x, y) => (y.year || 0) - (x.year || 0));
    policy.sort((x, y) => (y.year || 0) - (x.year || 0));
    press.sort((x, y) => String(y.date || y.year || '').localeCompare(String(x.date || x.year || '')));

    const parts = [];
    parts.push(renderHeader(a, lang));
    parts.push(renderPersonal(a, lang));

    parts.push((lang === 'hu' ? `## Cikkek (${papers.length})` : `## Papers (${papers.length})`) + '\n');
    if (papers.length) {
      papers.forEach(p => { parts.push(renderPaper(p, authorsById, lang)); parts.push('---\n'); });
    } else {
      parts.push((lang === 'hu' ? '_(nincs a katalógusban)_' : '_(none in catalogue)_') + '\n');
    }

    parts.push((lang === 'hu' ? `## Szakpolitikai munkák (${policy.length})` : `## Policy items (${policy.length})`) + '\n');
    if (policy.length) {
      policy.forEach(p => { parts.push(renderPolicy(p, authorsById, lang)); parts.push('---\n'); });
    } else {
      parts.push((lang === 'hu' ? '_(nincs a katalógusban)_' : '_(none in catalogue)_') + '\n');
    }

    parts.push((lang === 'hu' ? `## Sajtó (${press.length})` : `## Press items (${press.length})`) + '\n');
    if (press.length) {
      press.forEach(p => { parts.push(renderPress(p, authorsById, lang)); parts.push('---\n'); });
    } else {
      parts.push((lang === 'hu' ? '_(nincs a katalógusban)_' : '_(none in catalogue)_') + '\n');
    }

    return parts.join('\n');
  }

  function downloadAuthorMarkdown(data, slug, lang) {
    const md = buildAuthorMarkdown(data, slug, lang);
    if (!md) return;
    const blob = new Blob([md], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${slug}.md`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  window.EFH = window.EFH || {};
  window.EFH.buildAuthorMarkdown = buildAuthorMarkdown;
  window.EFH.downloadAuthorMarkdown = downloadAuthorMarkdown;
})();
