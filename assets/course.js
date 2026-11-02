(() => {
  const input = document.querySelector('#paper-search');
  const select = document.querySelector('#paper-category');
  const year = document.querySelector('#paper-year');
  const papers = [...document.querySelectorAll('.paper')];
  const count = document.querySelector('#paper-count');
  function filter() {
    const term = input.value.toLowerCase().trim();
    let visible = 0;
    papers.forEach(paper => {
      const match = (!year.value || paper.dataset.year === year.value) && paper.dataset.search.includes(term) && (!select.value || paper.dataset.category === select.value);
      paper.hidden = !match;
      if (match) visible++;
    });
    count.textContent = `${visible} of ${papers.length} papers`;
    document.querySelector('#no-results').hidden = visible !== 0;
  }
  function reset() { input.value = ''; select.value = ''; year.value = ''; filter(); }
  document.querySelector('#author-papers').addEventListener('click', () => { input.value = 'mudassir shabbir'; select.value = ''; year.value = ''; filter(); });
  input.addEventListener('input', filter);
  select.addEventListener('change', filter);
  year.addEventListener('change', filter);
  document.querySelector('#reset-papers').addEventListener('click', () => { reset(); input.focus(); });
  function revealPaper() {
    if (/^#P\d{2}$/.test(location.hash)) {
      reset();
      const paper = document.getElementById(location.hash.slice(1));
      if (paper) paper.scrollIntoView({ block: 'start' });
    }
  }
  window.addEventListener('hashchange', revealPaper);
  document.querySelectorAll('.paper-ref').forEach(link => link.addEventListener('click', reset));
  revealPaper();
})();
