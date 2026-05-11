/* Injects the header and footer so they don't have to be duplicated across
 * every HTML file. Called by a <script> tag at the bottom of each page.
 */
(function () {
  const path = window.location.pathname;
  const isHu = /\/hu\/[^?#]*$/.test(path);

  // In-language nav links are RELATIVE: from /hu/authors.html, "papers.html"
  // resolves to /hu/papers.html. No prefix needed.
  // Only the language-toggle links need to cross the /hu/ boundary.
  const page = (path.match(/[^/]+\.html$/) || ['index.html'])[0];
  const search = window.location.search || '';
  const enHref = isHu ? `../${page}${search}` : `${page}${search}`;
  const huHref = isHu ? `${page}${search}` : `hu/${page}${search}`;

  const nav = isHu ? {
    papers: 'Tanulmányok',
    authors: 'Szerzők',
    topics: 'Témák',
    about: 'Bemutatkozás',
    contribute: 'Közreműködés',
    brand: 'Magyar Közgazd<em>ászok</em>',
    brandSub: 'magyar közgazdasági kutatások tárlata'
  } : {
    papers: 'Papers',
    authors: 'Authors',
    topics: 'Topics',
    about: 'About',
    contribute: 'Contribute',
    brand: 'Magyar Közgazd<em>ászok</em>',
    brandSub: 'showcasing economics research'
  };

  const header = `
    <header class="site">
      <div class="container">
        <a href="index.html" class="brand">
          ${nav.brand}
          <span class="sub">— ${nav.brandSub}</span>
        </a>
        <nav>
          <a href="papers.html">${nav.papers}</a>
          <a href="authors.html">${nav.authors}</a>
          <a href="topics.html">${nav.topics}</a>
          <a href="about.html">${nav.about}</a>
          <a href="contribute.html">${nav.contribute}</a>
        </nav>
        <div class="lang">
          <a href="${enHref}" class="${isHu ? '' : 'active'}">EN</a> /
          <a href="${huHref}" class="${isHu ? 'active' : ''}">HU</a>
        </div>
      </div>
    </header>
  `;

  const footer = `
    <footer class="site">
      <div class="container">
        <p><strong>${nav.brand}</strong> — ${isHu
          ? 'magyar közgazdászok akadémiai kutatásainak nyilvános tárlata.'
          : 'a public showcase of academic research by Hungarian economists.'}</p>
        <p class="small muted">
          ${isHu
            ? 'Claude segítségével készült. Kurátor: Békés Gábor. Jelenlegi verzió: 0.3.1, 2026. május 9. Jelezz hibát vagy hiányt a'
            : 'Created with Claude. Edited by Gábor Békés. This is v. 0.3.1, 9 May 2026. Corrections and missing papers welcome — see'}
          <a href="contribute.html">${nav.contribute}</a>.
        </p>
        <p class="small muted">
          ${isHu
            ? 'A teljes tartalom és a kód licence:'
            : 'Content and code are released under'}
          <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en" target="_blank" rel="noopener">CC BY-NC-SA 4.0</a>.
        </p>
      </div>
    </footer>
  `;

  // Insert header at the top of <body>, footer just before </body>.
  const headerSlot = document.getElementById('site-header');
  if (headerSlot) headerSlot.outerHTML = header;
  else document.body.insertAdjacentHTML('afterbegin', header);

  const footerSlot = document.getElementById('site-footer');
  if (footerSlot) footerSlot.outerHTML = footer;
  else document.body.insertAdjacentHTML('beforeend', footer);
})();
