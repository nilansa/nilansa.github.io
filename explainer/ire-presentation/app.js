(function () {
  'use strict';
  var deck = window.DECK;
  if (!deck || !Array.isArray(deck.slides) || !deck.slides.length) {
    document.getElementById('stage').textContent = 'The presentation content could not be loaded. The script and source ledger remain available alongside this page.';
    return;
  }
  var slides = deck.slides;
  var sources = deck.sources || {};
  var params = new URLSearchParams(window.location.search);
  var presenter = params.get('presenter') === '1';
  var index = Math.min(slides.length - 1, Math.max(0, (parseInt(params.get('page'), 10) || 1) - 1));
  var storageKey = 'queos-presentation-' + (deck.meta.task || 'ire');
  var sourceId = 'window-' + Math.random().toString(36).slice(2) + Date.now().toString(36);
  var channel = null;
  var lastReceivedTimestamp = 0;
  var currentDialog = null;
  var presenterWindow = null;
  var timerRunning = false;
  var timerStartedAt = 0;
  var timerElapsed = 0;
  var stage = document.getElementById('stage');
  var byId = function (id) { return document.getElementById(id); };
  var pad = function (n) { return String(n).padStart(2, '0'); };

  document.title = (presenter ? 'Presenter · ' : '') + deck.meta.title.replace(/\n/g, ' ') + ' — ' + deck.meta.team;
  if (presenter) document.body.classList.add('presenter-mode');

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }
  function multiline(node, value) {
    var lines = String(value || '').split('\n');
    lines.forEach(function (line, lineIndex) {
      if (lineIndex) node.appendChild(document.createElement('br'));
      node.appendChild(document.createTextNode(line));
    });
  }
  function safeUrl(value) {
    if (!value) return 'SOURCE_LEDGER.md';
    if (value.charAt(0) === '#') return 'SOURCE_LEDGER.md';
    try {
      var parsed = new URL(value, window.location.href);
      return /^(https?:|file:)$/.test(parsed.protocol) ? parsed.href : 'SOURCE_LEDGER.md';
    } catch (e) { return 'SOURCE_LEDGER.md'; }
  }
  function sourceLink(ref, label) {
    var source = sources[ref];
    var link = el('a', '', label || (source ? source.title : ref));
    link.href = safeUrl(source && source.url);
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    if (source) link.title = source.locator || source.title;
    return link;
  }
  function allRefs(slide) {
    var refs = (slide.refs || []).slice();
    (slide.notes || []).forEach(function (note) {
      (note.refs || []).forEach(function (ref) { if (refs.indexOf(ref) < 0) refs.push(ref); });
    });
    return refs;
  }
  function visual(slide) {
    var holder = el('div', 'visual-region');
    holder.setAttribute('aria-label', 'Figure for ' + slide.title.replace(/\n/g, ' '));
    if (typeof window.renderVisual === 'function') {
      holder.innerHTML = window.renderVisual(slide);
    } else {
      holder.appendChild(el('div', 'visual-fallback', slide.takeaway || slide.title.replace(/\n/g, ' ')));
    }
    return holder;
  }
  function buildSlide(slide, mode) {
    var article = el('article', mode === 'mini' ? 'mini-slide' : mode === 'print' ? 'print-slide' : 'slide');
    if (slide.kind === 'cover') article.classList.add('cover-slide');
    article.dataset.slide = slide.id;
    article.dataset.kind = slide.kind;
    var header = el('header', 'slide-header');
    var kicker = el('div', 'slide-kicker');
    kicker.appendChild(el('span', 'evidence-label', slide.evidence));
    kicker.appendChild(el('span', '', (mode === 'mini' ? '' : deck.meta.project + ' · ') + pad(slide.number)));
    header.appendChild(kicker);
    var heading = el('h1');
    if (!mode) { heading.id = 'current-slide-title'; article.setAttribute('aria-labelledby', heading.id); }
    multiline(heading, slide.title);
    header.appendChild(heading);
    header.appendChild(el('p', 'slide-subtitle', slide.subtitle));
    article.appendChild(header);
    article.appendChild(visual(slide));
    var conclusion = el('div', 'slide-conclusion');
    conclusion.appendChild(el('p', 'takeaway', slide.takeaway));
    if (!mode) {
      var sourceButton = el('button', 'slide-source-button');
      sourceButton.type = 'button';
      sourceButton.setAttribute('aria-label', 'Read source evidence for this page');
      var primary = (slide.refs || []).map(function (ref) { return sources[ref] && sources[ref].title; }).filter(Boolean).slice(0, 2);
      sourceButton.appendChild(el('span', '', primary.join(' · ')));
      sourceButton.appendChild(el('span', 'source-count', 'Evidence and sentence sources ↗'));
      sourceButton.addEventListener('click', function () { openDialog('sources-dialog'); });
      conclusion.appendChild(sourceButton);
    } else if (mode === 'print') {
      conclusion.appendChild(el('span', 'print-sources', (slide.refs || []).join(' · ') + '\nFull references: SOURCE_LEDGER.md'));
    }
    article.appendChild(conclusion);
    return article;
  }
  function pointerBlock(slide) {
    var block = el('section', 'pointer-block');
    block.appendChild(el('h3', '', 'Where to point'));
    var list = el('ol');
    (slide.pointers || []).forEach(function (pointer) { list.appendChild(el('li', '', pointer)); });
    block.appendChild(list);
    return block;
  }
  function scriptBlock(slide, showTitle) {
    var block = el('section', 'script-block');
    if (showTitle) block.appendChild(el('h3', '', 'What to say'));
    (slide.notes || []).forEach(function (note) {
      var p = el('p', 'script-paragraph');
      p.appendChild(document.createTextNode(note.text));
      var reference = el('button', 'claim-id', note.id);
      reference.type = 'button';
      reference.setAttribute('aria-label', 'Read sources for sentence ' + note.id);
      reference.addEventListener('click', function () {
        openDialog('sources-dialog');
        var detail = byId('claim-' + note.id.replace(/[^a-z0-9]/gi, '-'));
        if (detail) {
          detail.open = true;
          detail.classList.add('highlighted');
          detail.scrollIntoView({block:'center'});
          detail.querySelector('summary').focus({preventScroll:true});
        }
      });
      p.appendChild(reference);
      block.appendChild(p);
    });
    return block;
  }
  function slideMeta(slide) {
    return 'Page ' + slide.number + ' of ' + slides.length + ' · ' + slide.wordCount + ' words · About ' + Math.round(slide.secondsAt130Wpm || slide.wordCount / 130 * 60) + ' seconds at 130 words per minute';
  }
  function buildNotes() {
    var slide = slides[index];
    var content = byId('notes-content');
    content.replaceChildren();
    content.appendChild(el('h3', 'note-slide-title', slide.title.replace(/\n/g, ' ')));
    content.appendChild(el('p', 'note-meta', slideMeta(slide)));
    content.appendChild(pointerBlock(slide));
    content.appendChild(scriptBlock(slide, true));
    if (slide.caveat) content.appendChild(el('p', 'note-caveat', slide.caveat));
  }
  function buildSources() {
    var slide = slides[index];
    var content = byId('sources-content');
    content.replaceChildren();
    content.appendChild(el('h3', 'note-slide-title', slide.title.replace(/\n/g, ' ')));
    content.appendChild(el('p', 'note-meta', 'Page ' + slide.number + ' · Primary sources, project records, and clearly marked original explanations.'));
    content.appendChild(el('h3', 'sources-section-title', 'Sources for this page'));
    var list = el('section', 'source-list');
    allRefs(slide).forEach(function (ref) {
      var source = sources[ref];
      if (!source) return;
      var entry = el('div', 'source-entry');
      entry.id = 'source-' + ref;
      entry.appendChild(el('div', 'source-id', ref));
      entry.appendChild(sourceLink(ref, source.title + ' ↗'));
      entry.appendChild(el('p', '', source.locator));
      list.appendChild(entry);
    });
    content.appendChild(list);
    content.appendChild(el('h3', 'sources-section-title', 'Sentence-by-sentence provenance'));
    (slide.notes || []).forEach(function (note) {
      var detail = el('details', 'claim-entry');
      detail.id = 'claim-' + note.id.replace(/[^a-z0-9]/gi, '-');
      var summary = el('summary');
      var summaryText = el('span');
      summaryText.appendChild(el('span', 'claim-label', note.id));
      summaryText.appendChild(document.createTextNode(note.text));
      summary.appendChild(summaryText);
      detail.appendChild(summary);
      var explanation = el('div', 'claim-detail');
      explanation.appendChild(el('p', 'claim-type', note.type || 'Source-grounded explanation'));
      if (note.exactLocation) explanation.appendChild(el('p', 'claim-location', note.exactLocation));
      var links = el('div', 'claim-links');
      (note.refs || []).forEach(function (ref) { links.appendChild(sourceLink(ref)); });
      explanation.appendChild(links);
      detail.appendChild(explanation);
      content.appendChild(detail);
    });
  }
  function updateTimer() {
    var clock = byId('presenter-clock');
    if (!clock) return;
    var total = timerElapsed + (timerRunning ? performance.now() - timerStartedAt : 0);
    var seconds = Math.floor(total / 1000);
    clock.textContent = pad(Math.floor(seconds / 60)) + ':' + pad(seconds % 60);
    var toggle = byId('timer-toggle');
    if (toggle) toggle.textContent = timerRunning ? 'Pause' : (total > 0 ? 'Resume' : 'Start');
  }
  function toggleTimer() {
    if (timerRunning) { timerElapsed += performance.now() - timerStartedAt; timerRunning = false; }
    else { timerStartedAt = performance.now(); timerRunning = true; }
    updateTimer();
  }
  function buildPresenter(slide) {
    var grid = el('div', 'presenter-stage');
    var left = el('section', 'presenter-left');
    left.setAttribute('aria-label', 'Slide preview and visual cues');
    var timing = el('div', 'presenter-timing');
    var timer = el('div');
    timer.appendChild(el('div', 'timer-label', 'Presentation timer'));
    var group = el('div', 'timer-group');
    var clock = el('span', 'timer-clock', '00:00'); clock.id = 'presenter-clock';
    clock.setAttribute('role', 'timer'); clock.setAttribute('aria-label', 'Elapsed presentation time');
    group.appendChild(clock);
    var toggle = el('button', 'timer-control', 'Start'); toggle.id = 'timer-toggle'; toggle.type = 'button'; toggle.addEventListener('click', toggleTimer); group.appendChild(toggle);
    var reset = el('button', 'timer-control', 'Reset'); reset.type = 'button'; reset.addEventListener('click', function () { timerElapsed = 0; timerStartedAt = performance.now(); updateTimer(); }); group.appendChild(reset);
    timer.appendChild(group); timing.appendChild(timer);
    timing.appendChild(el('div', 'presenter-cue', 'Page ' + pad(slide.number) + ' of ' + slides.length + '\nAbout ' + Math.round(slide.secondsAt130Wpm || 60) + ' seconds'));
    left.appendChild(timing);
    var miniature = el('div', 'presenter-miniature'); miniature.appendChild(buildSlide(slide, 'mini')); left.appendChild(miniature);
    var pointers = el('div', 'presenter-pointers'); pointers.appendChild(pointerBlock(slide));
    if (slides[index + 1]) {
      var next = el('div', 'presenter-next', 'Coming next'); next.appendChild(el('strong', '', slides[index + 1].title.replace(/\n/g, ' '))); pointers.appendChild(next);
    }
    left.appendChild(pointers);
    var right = el('section', 'presenter-right'); right.setAttribute('aria-label', 'Speaker script');
    right.appendChild(el('p', 'eyebrow', 'What to say'));
    right.appendChild(el('h1', 'note-slide-title', slide.title.replace(/\n/g, ' ')));
    right.appendChild(el('p', 'note-meta', slideMeta(slide)));
    right.appendChild(scriptBlock(slide, false));
    if (slide.caveat) right.appendChild(el('p', 'note-caveat', slide.caveat));
    grid.appendChild(left); grid.appendChild(right);
    return grid;
  }
  function publishState() {
    var timestamp = Math.max(Date.now(), lastReceivedTimestamp + 1);
    lastReceivedTimestamp = timestamp;
    var state = {type:'slide', index:index, from:sourceId, timestamp:timestamp};
    if (channel) channel.postMessage(state);
    try { localStorage.setItem(storageKey, JSON.stringify(state)); } catch (e) { /* Private browsing may disable storage. */ }
  }
  function receiveState(state) {
    if (!state || state.from === sourceId) return;
    if (state.type === 'requestState') { if (!presenter) publishState(); return; }
    if (state.type !== 'slide' || !Number.isInteger(state.index)) return;
    if (state.timestamp && state.timestamp <= lastReceivedTimestamp) return;
    lastReceivedTimestamp = state.timestamp || Date.now();
    navigate(state.index, false);
  }
  function updateUrl() {
    var url = new URL(window.location.href);
    if (index === 0) url.searchParams.delete('page'); else url.searchParams.set('page', String(index + 1));
    try { history.replaceState(null, '', url); } catch (e) { /* File previews may restrict URL updates. */ }
  }
  function render(announce) {
    var slide = slides[index];
    stage.replaceChildren(presenter ? buildPresenter(slide) : buildSlide(slide));
    byId('previous').disabled = index === 0;
    byId('next').disabled = index === slides.length - 1;
    byId('page-select').value = String(index);
    byId('page-count').textContent = 'of ' + slides.length;
    byId('progress').style.width = ((index + 1) / slides.length * 100) + '%';
    document.querySelectorAll('.chapter-button').forEach(function (button) {
      if (button.dataset.chapter === slide.chapter) button.setAttribute('aria-current', 'page'); else button.removeAttribute('aria-current');
    });
    document.querySelectorAll('.overview-page').forEach(function (button) {
      if (Number(button.dataset.index) === index) button.setAttribute('aria-current', 'page'); else button.removeAttribute('aria-current');
    });
    buildNotes(); buildSources(); updateTimer(); updateUrl();
    if (announce) byId('live-status').textContent = 'Page ' + slide.number + ' of ' + slides.length + '. ' + slide.title.replace(/\n/g, ' ');
  }
  function navigate(next, publish) {
    var bounded = Math.min(slides.length - 1, Math.max(0, next));
    if (bounded === index) return;
    index = bounded;
    render(true);
    if (publish !== false) publishState();
  }
  function closeDialog(id) {
    var dialog = byId(id || currentDialog);
    if (dialog && dialog.open) dialog.close();
    if (!document.querySelector('dialog[open]')) { currentDialog = null; document.body.classList.remove('dialog-open'); }
  }
  function openDialog(id) {
    if (currentDialog === id) { closeDialog(id); return; }
    if (currentDialog) closeDialog(currentDialog);
    var dialog = byId(id);
    if (!dialog) return;
    currentDialog = id;
    document.body.classList.add('dialog-open');
    dialog.showModal();
    var close = dialog.querySelector('.close-button');
    if (close) close.focus({preventScroll:true});
  }
  function openPresenter() {
    var url = new URL(window.location.href);
    url.searchParams.set('presenter', '1');
    url.searchParams.set('page', String(index + 1));
    publishState();
    presenterWindow = window.open(url.href, 'queos-ire-presenter', 'popup=yes,width=1440,height=940');
    if (presenterWindow) presenterWindow.focus();
    else byId('live-status').textContent = 'Allow the presenter window to open in your browser.';
  }
  async function fullscreen() {
    try {
      if (document.fullscreenElement) await document.exitFullscreen();
      else if (document.documentElement.requestFullscreen) await document.documentElement.requestFullscreen();
      else byId('live-status').textContent = 'Full screen is not available in this browser.';
    } catch (e) { byId('live-status').textContent = 'Use your browser full-screen control to expand the presentation.'; }
  }
  function setupNavigation() {
    var seen = [];
    slides.forEach(function (slide, slideIndex) {
      var option = el('option', '', pad(slide.number)); option.value = String(slideIndex); option.title = slide.title.replace(/\n/g, ' '); byId('page-select').appendChild(option);
      if (seen.indexOf(slide.chapter) < 0) {
        seen.push(slide.chapter);
        var chapter = el('button', 'chapter-button', slide.chapter); chapter.type = 'button'; chapter.dataset.chapter = slide.chapter;
        chapter.addEventListener('click', function () { navigate(slideIndex); });
        byId('chapters').appendChild(chapter);
      }
      var overview = el('button', 'overview-page'); overview.type = 'button'; overview.dataset.index = String(slideIndex);
      var top = el('span', 'overview-page-top'); top.appendChild(el('span', 'overview-number', pad(slide.number))); top.appendChild(el('span', '', slide.chapter)); overview.appendChild(top);
      var title = el('span', 'overview-title'); multiline(title, slide.title); overview.appendChild(title);
      overview.addEventListener('click', function () { navigate(slideIndex); closeDialog('overview-dialog'); stage.focus({preventScroll:true}); });
      byId('overview-pages').appendChild(overview);
    });
    byId('previous').addEventListener('click', function () { navigate(index - 1); });
    byId('next').addEventListener('click', function () { navigate(index + 1); });
    byId('page-select').addEventListener('change', function (event) { navigate(Number(event.target.value)); });
    byId('slide-menu-button').addEventListener('click', function () { openDialog('overview-dialog'); });
    byId('notes-button').addEventListener('click', function () { openDialog('notes-dialog'); });
    byId('sources-button').addEventListener('click', function () { openDialog('sources-dialog'); });
    byId('presenter-button').addEventListener('click', openPresenter);
    byId('notes-presenter').addEventListener('click', openPresenter);
    byId('fullscreen-button').addEventListener('click', fullscreen);
    if (presenter) {
      var label = el('span', 'presenter-label', 'Speaker view');
      document.querySelector('.wordmark').after(label);
      byId('presenter-button').textContent = 'Audience ↗';
      byId('presenter-button').removeEventListener('click', openPresenter);
      byId('presenter-button').addEventListener('click', function () {
        var url = new URL(window.location.href); url.searchParams.delete('presenter');
        window.open(url.href, 'queos-ire-audience');
      });
    }
    document.querySelectorAll('[data-close]').forEach(function (button) { button.addEventListener('click', function () { closeDialog(button.dataset.close); }); });
    document.querySelectorAll('dialog').forEach(function (dialog) {
      dialog.addEventListener('close', function () { if (currentDialog === dialog.id) currentDialog = null; if (!document.querySelector('dialog[open]')) document.body.classList.remove('dialog-open'); });
      dialog.addEventListener('click', function (event) { if (event.target !== dialog) return; var rect = dialog.getBoundingClientRect(); if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) closeDialog(dialog.id); });
    });
    document.addEventListener('fullscreenchange', function () {
      byId('fullscreen-button').setAttribute('aria-label', document.fullscreenElement ? 'Exit full screen' : 'Enter full screen');
    });
    document.addEventListener('keydown', function (event) {
      var target = event.target;
      if (target && (target.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(target.tagName))) return;
      if (event.ctrlKey || event.metaKey || event.altKey) return;
      var key = event.key.toLowerCase();
      if (key === 'escape') { if (currentDialog) closeDialog(currentDialog); return; }
      if (currentDialog) { if (key === 'n' && currentDialog === 'notes-dialog') closeDialog(); else if (key === 's' && currentDialog === 'sources-dialog') closeDialog(); else if (key === 'o' && currentDialog === 'overview-dialog') closeDialog(); return; }
      if (key === 'arrowright' || key === 'pagedown' || (key === ' ' && (!target || target.tagName !== 'BUTTON'))) { event.preventDefault(); navigate(index + 1); }
      else if (key === 'arrowleft' || key === 'pageup') { event.preventDefault(); navigate(index - 1); }
      else if (key === 'home') { event.preventDefault(); navigate(0); }
      else if (key === 'end') { event.preventDefault(); navigate(slides.length - 1); }
      else if (key === 'n') { event.preventDefault(); openDialog('notes-dialog'); }
      else if (key === 's') { event.preventDefault(); openDialog('sources-dialog'); }
      else if (key === 'o') { event.preventDefault(); openDialog('overview-dialog'); }
      else if (key === 'f') { event.preventDefault(); fullscreen(); }
    });
    window.addEventListener('beforeprint', function () {
      var printDeck = byId('print-deck'); printDeck.replaceChildren();
      slides.forEach(function (slide) { printDeck.appendChild(buildSlide(slide, 'print')); });
    });
  }
  setupNavigation();
  try { channel = new BroadcastChannel(storageKey); channel.onmessage = function (event) { receiveState(event.data); }; } catch (e) { /* The storage event remains a fallback. */ }
  window.addEventListener('storage', function (event) { if (event.key === storageKey && event.newValue) { try { receiveState(JSON.parse(event.newValue)); } catch (e) { /* Ignore unrelated or incomplete storage. */ } } });
  if (presenter && !params.has('page')) {
    try { var saved = JSON.parse(localStorage.getItem(storageKey)); if (saved && Number.isInteger(saved.index)) index = Math.min(slides.length - 1, Math.max(0,saved.index)); } catch (e) { /* Use requested page. */ }
  }
  render(false);
  if (presenter) { if (channel) channel.postMessage({type:'requestState', from:sourceId}); }
  else publishState();
  if (presenter) window.setInterval(updateTimer, 250);
})();
