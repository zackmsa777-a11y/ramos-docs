(() => {
  const root = document.documentElement;
  let saved;
  try { saved = localStorage.getItem('ramos-book-theme'); } catch {}
  root.dataset.theme = saved || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  document.querySelector('#theme').addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('ramos-book-theme', root.dataset.theme); } catch {}
  });
  const menu = document.querySelector('#menu');
  menu.addEventListener('click', () => {
    const open = document.body.classList.toggle('menu-open');
    menu.setAttribute('aria-expanded', String(open));
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') { document.body.classList.remove('menu-open'); menu.setAttribute('aria-expanded', 'false'); }
  });
  document.querySelectorAll('pre').forEach(pre => {
    if (!navigator.clipboard) return;
    const button = document.createElement('button');
    button.className = 'copy'; button.textContent = 'Copy'; button.setAttribute('aria-label', 'Copy code');
    button.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(pre.querySelector('code').textContent); button.textContent = 'Copied'; }
      catch { button.textContent = 'Select to copy'; }
      setTimeout(() => { button.textContent = 'Copy'; }, 1800);
    });
    pre.append(button);
  });
  const input = document.querySelector('#search'), results = document.querySelector('#results');
  let index, pending;
  input.addEventListener('input', async () => {
    const query = input.value.trim().toLowerCase();
    results.replaceChildren(); results.hidden = !query;
    if (!query) return;
    try {
      pending ||= fetch('assets/search.json').then(response => { if (!response.ok) throw new Error('search'); return response.json(); });
      index ||= await pending;
      if (query !== input.value.trim().toLowerCase()) return;
      const words = query.split(/\s+/);
      const matches = index.filter(chapter => words.every(word => (chapter.title + ' ' + chapter.text).toLowerCase().includes(word)));
      for (const match of matches.slice(0, 12)) {
        const link = document.createElement('a'); link.href = match.url; link.textContent = match.title; results.append(link);
      }
      if (!matches.length) results.textContent = 'No matching chapter.';
    } catch { results.textContent = 'Search needs HTTP hosting. Use the chapter list when reading local files.'; pending = null; }
  });
})();
