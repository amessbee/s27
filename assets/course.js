(() => {
  const panels = [...document.querySelectorAll('[data-panel]')];
  const navLinks = [...document.querySelectorAll('.view-link')];
  const input = document.querySelector('#paper-search');
  const category = document.querySelector('#paper-category');
  const year = document.querySelector('#paper-year');
  const papers = [...document.querySelectorAll('.paper')];
  const authorButton = document.querySelector('#author-papers');
  const yearButtons = [...document.querySelectorAll('[data-year-filter]')];
  let authorOnly = false;

  function filter() {
    const term = input.value.toLowerCase().trim();
    let visible = 0;
    papers.forEach(paper => {
      const match = (!year.value || paper.dataset.year === year.value)
        && (!authorOnly || paper.dataset.author === 'true')
        && paper.dataset.search.includes(term)
        && (!category.value || paper.dataset.category === category.value);
      paper.hidden = !match;
      if (match) visible++;
    });
    document.querySelector('#paper-count').textContent = `${visible} of ${papers.length} papers`;
    document.querySelector('#no-results').hidden = visible !== 0;
    authorButton.setAttribute('aria-pressed', String(authorOnly));
    yearButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.yearFilter === year.value)));
  }
  function reset() {
    input.value = ''; category.value = ''; year.value = ''; authorOnly = false; filter();
  }
  authorButton.addEventListener('click', () => { authorOnly = !authorOnly; filter(); });
  yearButtons.forEach(button => button.addEventListener('click', () => {
    year.value = year.value === button.dataset.yearFilter ? '' : button.dataset.yearFilter;
    filter();
  }));
  input.addEventListener('input', filter);
  category.addEventListener('change', filter);
  year.addEventListener('change', filter);
  document.querySelector('#reset-papers').addEventListener('click', () => { reset(); input.focus(); });

  function navigate(scroll = false) {
    const id = decodeURIComponent(location.hash.slice(1));
    const target = document.getElementById(id);
    const panel = target?.closest('[data-panel]');
    const view = panel?.dataset.panel || (id ? document.body.dataset.view : 'overview') || 'overview';
    panels.forEach(item => { item.hidden = item.dataset.panel !== view; });
    document.body.dataset.view = view;
    navLinks.forEach(link => {
      if (link.dataset.view === view) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
    if (target?.classList.contains('paper')) { reset(); target.open = true; }
    if (scroll && target) requestAnimationFrame(() => target.scrollIntoView({ block: 'start' }));
  }
  window.addEventListener('hashchange', () => navigate(true));
  document.querySelectorAll('a[href^="#"]').forEach(link => link.addEventListener('click', () => {
    if (link.hash === location.hash) navigate(true);
  }));
  navigate(Boolean(location.hash));
})();
