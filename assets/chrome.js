/* Injects the header and footer so they don't have to be duplicated across
 * every HTML file. Called by a <script> tag at the bottom of each page.
 */
(function () {
  const path = window.location.pathname;
  const isHu = /\/hu\/[^?#]*$/.test(path);
  const prefix = isHu ? '../' : '';
  const huPrefix = isHu ? '' : 'hu/';

  // Preserve the current page when switching language.
  // E.g. /papers.html?id=foo  ↔  /hu/papers.html?id=foo
  const page = (path.match(/[^/]+\.html$/) || ['index.html'])[0];
  const search = window.location.search || '';
  const enHref = `${prefix}${page}${search}`;
  const huHref = `${prefix}${huPrefix}${page}${search}`;

  const nav = isHu ? {
    papers: 'Tanulmányok',
    authors: 'Szerzők',
    topics: 'Témák',
    about: 'Bemutatkozás',
    contribute: 'Közreműködés',
    brand: 'Magyar Közgazd<em>ászok</em>',
    brandSub: 'innovatív közgazdászok a döntéshozóknak'
  } : {
    papers: 'Papers',
    authors: 'Authors',
    topics: 'Topics',
    about: 'About',
    contribute: 'Contribute',
    brand: 'Magyar Közgazd<em>ászok</em>',
    brandSub: 'innovative economists for policymakers'
  };

  const header = `
    <header class="site">
      <div class="container">
        <a href="${prefix}index.html" class="brand">
          ${nav.brand}
          <span class="sub">— ${nav.brandSub}</span>
        </a>
        <nav>
          <a href="${prefix}papers.html">${nav.papers}</a>
          <a href="${prefix}authors.html">${nav.authors}</a>
          <a href="${prefix}topics.html">${nav.topics}</a>
          <a href="${prefix}about.html">${nav.about}</a>
          <a href="${prefix}contribute.html">${nav.contribute}</a>
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
          ? 'akadémiai kutatások az innovatív magyar közgazdászoktól, a döntéshozóknak.'
          : 'academic research by innovative Hungarian economists, for policymakers.'}</p>
        <p class="small muted">
          ${isHu
            ? 'Kurátor: Békés Gábor. MVP verzió, 2026 áprilisa. Jelezz hibát vagy hiányt a'
            : 'Edited by Gábor Békés. MVP scaffold, April 2026. Corrections and missing papers welcome — see'}
          <a href="${prefix}contribute.html">${nav.contribute}</a>.
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
