(() => {
  'use strict';
  const box = document.getElementById('source-filter');
  if (!box) return;
  const input = document.getElementById('study-query');
  const cards = [...document.querySelectorAll('.resource')];
  const count = document.getElementById('study-count');
  const panel = document.getElementById('study-player');
  const container = document.getElementById('study-video');
  const title = document.getElementById('study-playing');
  const direct = document.getElementById('study-direct');
  let last = null;
  const norm = v => v.toLowerCase().normalize('NFKD');
  function filter() {
    const words = norm(input.value.trim()).split(/\s+/).filter(Boolean);
    const kind = box.querySelector('input[name="kind"]:checked').value;
    let n = 0;
    cards.forEach(card => {
      const text = norm(card.textContent + ' ' + card.dataset.keys);
      const show = (kind === 'all' || card.dataset.kind.split(' ').includes(kind)) && words.every(w => text.includes(w));
      card.hidden = !show;
      if (show) n++;
    });
    count.textContent = n ? n + (n === 1 ? ' resource' : ' resources') : 'No matches. Try fewer words or choose All.';
  }
  box.addEventListener('input', filter);
  box.addEventListener('change', filter);
  box.addEventListener('submit', event => {event.preventDefault(); filter();});
  document.getElementById('study-list').addEventListener('click', event => {
    const btn = event.target.closest('button[data-video],button[data-deck]');
    if (!btn) return;
    last = btn;
    const slides = {
      wsdm:['https://drive.google.com/file/d/1-sRsFkG4juBHqqQ-ces3HRvtYHpR0l7U/preview','https://drive.google.com/file/d/1-sRsFkG4juBHqqQ-ces3HRvtYHpR0l7U/view','WSDM tutorial slides · see pages 13–22'],
      webconf:['https://ilps.github.io/webconf2020-tutorial-unbiased-ltr/WWW2020handout.pdf#page=37','https://ilps.github.io/webconf2020-tutorial-unbiased-ltr/WWW2020handout.pdf#page=37','WebConf slides · pages 37–40'],
    };
    if (btn.dataset.deck && Object.hasOwn(slides,btn.dataset.deck)) {
      const [src,link,label] = slides[btn.dataset.deck];
      const frame = document.createElement('iframe');
      frame.src = src; frame.title = label; frame.className = 'slide-preview';
      container.replaceChildren(frame); direct.href=link; direct.textContent='Open original slides';
      title.textContent=label; panel.hidden=false; title.focus();
      return;
    }
    if (!/^[a-zA-Z0-9_-]{11}$/.test(btn.dataset.video)) return;
    const s = new URL('https://www.youtube-nocookie.com/embed/' + btn.dataset.video);
    s.searchParams.set('rel','0');
    if (btn.dataset.start) s.searchParams.set('start',btn.dataset.start);
    if (btn.dataset.end) s.searchParams.set('end',btn.dataset.end);
    const frame = document.createElement('iframe');
    frame.src = s.href;
    frame.title = btn.closest('.resource').querySelector('h3').textContent + ' video';
    frame.allow = 'encrypted-media; picture-in-picture; fullscreen';
    frame.allowFullscreen = true;
    frame.referrerPolicy = 'strict-origin-when-cross-origin';
    container.replaceChildren(frame);
    direct.href = 'https://www.youtube.com/watch?v=' + btn.dataset.video + (btn.dataset.start ? '&t=' + btn.dataset.start + 's' : '');
    direct.textContent = 'Open on YouTube';
    title.textContent = frame.title;
    panel.hidden = false;
    title.focus();
  });
  document.getElementById('study-close').addEventListener('click', () => {
    container.replaceChildren();
    panel.hidden = true;
    if (last && !last.closest('.resource').hidden) last.focus();
    else input.focus();
  });
  filter();
})();
