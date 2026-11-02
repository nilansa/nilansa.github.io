(() => {
  "use strict";
  const years = [2022, 2023, 2024, 2025, 2026];
  const topics = ["3D & geometry", "Vision & language", "Generative models", "Video & motion", "Medical imaging", "Robotics & embodied", "Recognition & detection", "Learning & robustness", "Other vision"];
  const pinKey = "cvpr-research-hub-pins-v1";
  const $ = selector => document.querySelector(selector);
  const elements = {
    form:$("#search-form"), query:$("#query"), yearFilters:$("#year-filters"), topicFilters:$("#topic-filters"), sort:$("#sort-order"),
    status:$("#search-status"), resultCount:$("#result-count"), results:$("#results"), more:$("#more-results"), progressWrap:$("#load-progress"), progress:$("#progress"), progressLabel:$("#progress-label"),
    heroCount:$("#hero-count"), integrity:$("#integrity-content"), pinCount:$("#pin-count"), pinned:$("#pinned-papers"), exportPins:$("#export-pins"), importPins:$("#import-pins"),
    dialog:$("#paper-dialog"), dialogBody:$("#dialog-body"), closeDialog:$("#close-dialog"), problemPick:$("#problem-pick"), methodPick:$("#method-pick"), clearProblem:$("#clear-problem"), clearMethod:$("#clear-method"), ideaStatus:$("#idea-status"), hypothesis:$("#hypothesis-card")
  };
  const worker = new Worker(new URL("search-worker.js", document.currentScript.src));
  let requestId = 0;
  let debounce = 0;
  let currentTotal = 0;
  let currentOffset = 0;
  let problemPaper = null;
  let methodPaper = null;
  let currentPacket = null;
  const pins = loadPins();

  function node(tag, className, value) {
    const item = document.createElement(tag);
    if (className) item.className = className;
    if (value !== undefined) item.textContent = value;
    return item;
  }

  function safeCvfLink(value, extension) {
    try {
      const url = new URL(value);
      const allowedHost = ["openaccess.thecvf.com", "www.openaccess.thecvf.com"].includes(url.hostname);
      const paperLink = url.pathname.startsWith("/content/") && url.pathname.toLowerCase().endsWith(extension) && !url.search;
      const listingLink = extension === ".html" && /^\/CVPR20\d{2}$/i.test(url.pathname) && url.search === "?day=all";
      return url.protocol === "https:" && allowedHost && !url.username && !url.password && !url.hash && (paperLink || listingLink);
    } catch { return false; }
  }

  function safePaper(paper) {
    return paper && typeof paper.id === "string" && typeof paper.title === "string" &&
      typeof paper.authors === "string" && typeof paper.abstract === "string" &&
      Number.isInteger(paper.year) && paper.year >= 2022 && paper.year <= 2026 &&
      safeCvfLink(paper.cvf_url, ".html") && safeCvfLink(paper.pdf_url, ".pdf");
  }

  function loadPins() {
    try {
      const stored = JSON.parse(localStorage.getItem(pinKey) || "[]");
      return Array.isArray(stored) ? stored.filter(safePaper).slice(0, 500) : [];
    } catch { return []; }
  }

  function persistPins() {
    try { localStorage.setItem(pinKey, JSON.stringify(pins)); }
    catch { elements.status.textContent = "Browser storage is full. Export pins, then remove some."; }
    renderPins();
  }

  function selectedYears() {
    return [...elements.yearFilters.querySelectorAll("input:checked")].map(input => Number(input.value));
  }

  function selectedTopic() {
    const active = elements.topicFilters.querySelector("button[aria-pressed='true']");
    return active ? active.dataset.topic : "";
  }

  function setupFilters() {
    for (const year of years) {
      const label = node("label", "year-option");
      const input = node("input"); input.type = "checkbox"; input.value = String(year); input.checked = year === 2026;
      const text = node("span", "", String(year));
      label.append(input, text); elements.yearFilters.append(label);
      input.addEventListener("change", () => runSearch(true));
    }
    for (const topic of topics) {
      const wrap = node("span", "topic-chip");
      const button = node("button", "", topic); button.type = "button"; button.setAttribute("aria-pressed", "false"); button.dataset.topic = topic;
      button.addEventListener("click", () => {
        const wasActive = button.getAttribute("aria-pressed") === "true";
        for (const other of elements.topicFilters.querySelectorAll("button")) other.setAttribute("aria-pressed", "false");
        if (!wasActive) button.setAttribute("aria-pressed", "true");
        runSearch(true);
      });
      wrap.append(button); elements.topicFilters.append(wrap);
    }
  }

  function emptyState(title, message) {
    const box = node("div", "empty-state");
    box.append(node("span", "empty-symbol", "⌕"), node("h3", "", title), node("p", "", message));
    elements.results.replaceChildren(box);
  }

  function runSearch(reset) {
    if (reset) currentOffset = 0;
    const query = elements.query.value.trim();
    const topic = selectedTopic();
    const yearsSelected = selectedYears();
    if (!query && !topic) {
      currentTotal = 0; elements.resultCount.textContent = "No search yet"; elements.more.hidden = true;
      elements.status.textContent = "Choose a topic or enter a search. Year files load only when needed.";
      elements.progressWrap.hidden = true;
      emptyState("Your next question starts here.", "Search a phrase or choose a topic. The paper files are fetched one year at a time.");
      return;
    }
    if (!yearsSelected.length) {
      elements.status.textContent = "Select at least one year."; elements.resultCount.textContent = "0 papers"; elements.more.hidden = true;
      emptyState("Choose a year to search.", "Select one or more publication years above."); return;
    }
    const id = ++requestId;
    elements.status.textContent = "Preparing the selected year files…";
    elements.progressWrap.hidden = false; elements.progress.max = yearsSelected.length; elements.progress.value = 0;
    elements.progressLabel.textContent = "Starting";
    if (reset) emptyState("Searching the archive…", "Year files load one at a time. Your search stays in this browser.");
    worker.postMessage({type:"search", requestId:id, query, topic, years:yearsSelected, sort:elements.sort.value, offset:currentOffset, limit:40});
  }

  function addMeta(paper) {
    const row = node("div", "card-meta");
    row.append(node("span", "", String(paper.year)), node("span", "meta-dot"), node("span", "", paper.source || "Hugging Face dataset"));
    return row;
  }

  function isPinned(id) { return pins.some(paper => paper.id === id); }

  function pinPaper(paper) {
    const index = pins.findIndex(item => item.id === paper.id);
    if (index >= 0) pins.splice(index, 1); else pins.unshift(paper);
    persistPins();
    for (const card of elements.results.querySelectorAll(".paper-card")) {
      const button = card.querySelector("[data-action='pin']");
      if (button && card.__paper) {
        const active = isPinned(card.__paper.id);
        button.textContent = active ? "Pinned ★" : "Pin +";
        button.setAttribute("aria-pressed", String(active));
      }
    }
  }

  function renderPaperCard(paper) {
    const card = node("article", "paper-card");
    const top = node("div", "card-top");
    const meta = addMeta(paper);
    const cluster = node("span", "cluster-tag", paper.cluster);
    const pin = node("button", "pin-button", isPinned(paper.id) ? "Pinned ★" : "Pin +"); pin.type = "button"; pin.dataset.action = "pin"; pin.setAttribute("aria-pressed", String(isPinned(paper.id)));
    top.append(meta, cluster, pin);
    const track = node("span", "track-tag", paper.track_status || "CVPR main candidate");
    const title = node("button", "paper-title", paper.title); title.type = "button"; title.dataset.action = "detail";
    const authors = node("p", "paper-authors", paper.authors);
    const abstract = node("p", "paper-abstract", paper.abstract || "Abstract unavailable in source metadata.");
    const actions = node("div", "card-actions");
    const problem = node("button", "", "Use as problem"); problem.type = "button"; problem.dataset.action = "problem";
    const method = node("button", "", "Use as method"); method.type = "button"; method.dataset.action = "method";
    const sourceLabel = paper.pdf_status && paper.pdf_status.startsWith("HTTP 404") ? "CVF listing · PDF unavailable ↗" : (paper.cvf_reference_type === "year proceedings listing" ? "CVF listing ↗" : "CVF paper ↗");
    const source = node("a", "source-link", sourceLabel); source.href = paper.cvf_url; source.target = "_blank"; source.rel = "noopener";
    actions.append(problem, method, source);
    card.append(top, track, title, authors, abstract, actions);
    card.dataset.paperId = paper.id;
    return card;
  }

  function renderResults(message) {
    currentTotal = message.total; currentOffset += message.results.length;
    elements.resultCount.textContent = `${message.total.toLocaleString()} matching paper${message.total === 1 ? "" : "s"}`;
    elements.status.textContent = message.total ? `Showing ${Math.min(currentOffset, message.total).toLocaleString()} of ${message.total.toLocaleString()} matches. Search stays on this device.` : "No matches for these filters. Try fewer terms, another year, or a different topic.";
    if (message.offset === 0) elements.results.replaceChildren();
    if (message.results.length) {
      const fragment = document.createDocumentFragment();
      for (const paper of message.results) {
        const card = renderPaperCard(paper); card.__paper = paper; fragment.append(card);
      }
      elements.results.append(fragment);
    } else if (message.offset === 0) emptyState("No papers found.", "Try a shorter phrase or remove a filter.");
    elements.more.hidden = currentOffset >= currentTotal;
  }

  function renderPins() {
    elements.pinCount.textContent = String(pins.length);
    if (!pins.length) { elements.pinned.replaceChildren(node("p", "empty-note", "No pinned papers yet.")); return; }
    const list = document.createDocumentFragment();
    for (const paper of pins) {
      const item = node("div", "pinned-item");
      const title = node("button", "", `${paper.year} · ${paper.title}`); title.type = "button"; title.dataset.action = "detail"; title.dataset.pinId = paper.id;
      const remove = node("button", "", "Remove"); remove.type = "button"; remove.dataset.action = "unpin"; remove.dataset.pinId = paper.id; remove.setAttribute("aria-label", `Remove ${paper.title} from pins`);
      item.append(title, remove); list.append(item);
    }
    elements.pinned.replaceChildren(list);
  }

  function showDetail(paper) {
    elements.dialogBody.replaceChildren();
    const title = node("h2", "detail-title", paper.title); title.id = "detail-title";
    const meta = node("div", "detail-meta");
    meta.append(node("span", "cluster-tag", paper.cluster), node("span", "track-tag", paper.track_status || "CVPR main candidate"), node("span", "card-meta", String(paper.year)));
    const authors = node("p", "detail-authors", paper.authors);
    const abstractLabel = node("h3", "", "Abstract"); abstractLabel.style.margin = "23px 0 0";
    const abstract = node("p", "detail-abstract", paper.abstract || "Abstract unavailable in source metadata.");
    const links = node("div", "detail-links");
    const cvfLabel = paper.cvf_reference_type === "year proceedings listing" ? "Open CVF year listing ↗" : "Open CVF paper page ↗";
    const cvf = node("a", "", cvfLabel); cvf.href = paper.cvf_url; cvf.target = "_blank"; cvf.rel = "noopener";
    links.append(cvf);
    if (paper.pdf_status && paper.pdf_status.startsWith("HTTP 404")) {
      const unavailable = node("span", "detail-note", `PDF link returned HTTP 404 on ${paper.pdf_status.split(" on ").pop()}. The CVF year listing is linked above; no PDF was downloaded.`);
      links.append(unavailable);
    } else {
      const pdf = node("a", "", "Open PDF at CVF ↗"); pdf.href = paper.pdf_url; pdf.target = "_blank"; pdf.rel = "noopener"; links.append(pdf);
    }
    const buttons = node("div", "packet-actions");
    const asProblem = node("button", "secondary", "Use as problem paper"); asProblem.type = "button"; asProblem.addEventListener("click", () => setIdeaPaper("problem", paper));
    const asMethod = node("button", "secondary", "Use as method paper"); asMethod.type = "button"; asMethod.addEventListener("click", () => setIdeaPaper("method", paper));
    buttons.append(asProblem, asMethod);
    const note = node("p", "detail-note", `${paper.source}. Track label basis: ${paper.track_basis || "source metadata"}. Topic clusters are keyword labels.`);
    elements.dialogBody.append(title, meta, authors, abstractLabel, abstract, links, buttons, note);
    if (!elements.dialog.open) elements.dialog.showModal();
  }

  function setIdeaPaper(role, paper) {
    if (!paper.abstract || !paper.abstract.trim()) { elements.ideaStatus.textContent = "This source record has no abstract. Choose a paper with an abstract for evidence-based snippets."; return; }
    const other = role === "problem" ? methodPaper : problemPaper;
    if (other && other.id === paper.id) { elements.ideaStatus.textContent = "Choose two different papers."; return; }
    if (other && other.cluster === paper.cluster) { elements.ideaStatus.textContent = "Choose papers with different topic clusters. Change one paper or clear a selection."; return; }
    if (role === "problem") problemPaper = paper; else methodPaper = paper;
    elements.ideaStatus.textContent = problemPaper && methodPaper ? "Different clusters selected. Review the evidence before you copy the packet." : "One paper selected. Choose another paper from a different cluster.";
    renderIdea();
    if (elements.dialog.open) elements.dialog.close();
    const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
    document.querySelector("#idea-lab").scrollIntoView({behavior:reduceMotion ? "auto" : "smooth", block:"start"});
  }

  function sentenceList(abstract) {
    return String(abstract || "").match(/[^.!?]+(?:[.!?]+|$)/g)?.map(sentence => sentence.trim()).filter(Boolean) || [];
  }

  function evidenceFor(paper, role) {
    const sentences = sentenceList(paper.abstract);
    const pattern = role === "problem"
      ? /\b(however|challenges?|limitations?|remain(?:s|ed)?|still|difficult(?:y)?|despite|lack of|not address(?:ed)?|cannot|future work|open question)\b/i
      : /\b(we propose|we introduce|we present|we develop|our method|our approach|framework|architecture|algorithm|we design)\b/i;
    const match = sentences.find(sentence => pattern.test(sentence));
    return {text:match || sentences[0] || "No abstract sentence was available.", matched:Boolean(match), kind:match ? (role === "problem" ? "Limitation or challenge pattern" : "Method pattern") : "Opening abstract excerpt; check the full abstract"};
  }

  function paperRef(paper) {
    return {id:paper.id, title:paper.title, year:paper.year, cluster:paper.cluster, cvf_url:paper.cvf_url, pdf_url:paper.pdf_url};
  }

  function makePacket() {
    if (!problemPaper || !methodPaper) return null;
    const problemEvidence = evidenceFor(problemPaper, "problem");
    const methodEvidence = evidenceFor(methodPaper, "method");
    return {
      schema:"cvpr-hypothesis-packet-v1",
      status:"UNTESTED",
      created_at:new Date().toISOString(),
      hypothesis:`A method described in “${methodPaper.title}” may provide a useful test for the challenge discussed in “${problemPaper.title}” in ${problemPaper.cluster} tasks. Test it with one score (metric) named before the test and a matched compute budget.`,
      evidence:[
        {role:"problem paper", paper:paperRef(problemPaper), extraction:problemEvidence.kind, sentence:problemEvidence.text},
        {role:"method paper", paper:paperRef(methodPaper), extraction:methodEvidence.kind, sentence:methodEvidence.text}
      ],
      comparison:{baseline:"Select and cite a strong, task-matched public baseline (a reference method) before the test.", controls:"Use the same data split, inputs, training budget, compute budget, and score for both methods.", report:"Record repeated runs and uncertainty; do not treat abstract claims as results."},
      falsification:"The idea fails this test if the adapted method does not improve the preselected score over the baseline in the matched test, or if it breaks a quality rule set before the test.",
      novelty_warning:"Novelty means a new contribution compared with earlier work. A cross-paper combination does not prove novelty. Search related work and inspect both papers before making a claim."
    };
  }

  function citationLine(paper) {
    return `[${paper.title} (${paper.year})](${paper.cvf_url})`;
  }

  function renderIdea() {
    for (const [paper, label, clear] of [[problemPaper, elements.problemPick, elements.clearProblem], [methodPaper, elements.methodPick, elements.clearMethod]]) {
      label.className = paper ? "pick-name" : "pick-empty";
      label.textContent = paper ? `${paper.title} · ${paper.year} · ${paper.cluster}` : "Choose from a search result.";
      clear.hidden = !paper;
    }
    elements.hypothesis.replaceChildren();
    currentPacket = makePacket();
    if (!currentPacket) {
      const placeholder = node("div", "hypothesis-placeholder");
      placeholder.append(node("span", "placeholder-mark", "↗"), node("h3", "", "Your evidence packet will appear here."), node("p", "", "It will include source sentences, paper links, a controlled comparison, and a step that can disprove the idea."));
      elements.hypothesis.append(placeholder); return;
    }
    const badge = node("span", "untested-badge", "UNTESTED HYPOTHESIS");
    const heading = node("h3", "", "A question to test");
    const statement = node("p", "hypothesis-text", currentPacket.hypothesis);
    const evidence = node("div", "evidence-pair");
    for (const item of currentPacket.evidence) {
      const box = node("div", "evidence-box");
      box.append(node("small", "", `${item.role} · ${item.extraction}`), node("blockquote", "", `“${item.sentence}”`));
      const link = node("a", "idea-source", `${item.paper.title} (${item.paper.year}) ↗`); link.href = item.paper.cvf_url; link.target = "_blank"; link.rel = "noopener"; box.append(link);
      evidence.append(box);
    }
    const methods = node("div", "method-block");
    const comparison = node("div"); comparison.append(node("h4", "", "Controlled comparison"), node("p", "", `${currentPacket.comparison.baseline} ${currentPacket.comparison.controls}`));
    const falsification = node("div"); falsification.append(node("h4", "", "Falsification step"), node("p", "", currentPacket.falsification));
    methods.append(comparison, falsification);
    const warning = node("p", "detail-note", currentPacket.novelty_warning);
    const actions = node("div", "packet-actions");
    const copyJson = node("button", "", "Copy packet JSON"); copyJson.type = "button"; copyJson.addEventListener("click", () => copyPacket("json"));
    const copyMarkdown = node("button", "secondary", "Copy as Markdown"); copyMarkdown.type = "button"; copyMarkdown.addEventListener("click", () => copyPacket("markdown"));
    const notice = node("span", "packet-notice", "No results or novelty claims are generated."); notice.id = "packet-notice";
    actions.append(copyJson, copyMarkdown, notice);
    elements.hypothesis.append(badge, heading, statement, evidence, methods, warning, actions);
  }

  function markdownPacket(packet) {
    return `# UNTESTED hypothesis\n\n${packet.hypothesis}\n\n## Evidence\n\n${packet.evidence.map(item => `### ${item.role}\n\n> ${item.sentence}\n\nSource: ${citationLine(item.paper)}\n\nExtraction: ${item.extraction}`).join("\n\n")}\n\n## Controlled comparison\n\n- Baseline: ${packet.comparison.baseline}\n- Controls: ${packet.comparison.controls}\n- Reporting: ${packet.comparison.report}\n\n## Falsification step\n\n${packet.falsification}\n\n## Novelty warning\n\n${packet.novelty_warning}\n`;
  }

  async function copyPacket(format) {
    if (!currentPacket) return;
    const text = format === "json" ? JSON.stringify(currentPacket, null, 2) : markdownPacket(currentPacket);
    try {
      await navigator.clipboard.writeText(text);
    } catch {
      const textarea = node("textarea"); textarea.value = text; textarea.style.position = "fixed"; textarea.style.opacity = "0"; document.body.append(textarea); textarea.select();
      const copied = document.execCommand("copy"); textarea.remove();
      if (!copied) { elements.ideaStatus.textContent = "Clipboard access is unavailable. Use a secure browser context and try again."; return; }
    }
    const notice = $("#packet-notice"); if (notice) notice.textContent = `${format === "json" ? "JSON" : "Markdown"} copied.`;
  }

  async function loadIntegrity() {
    try {
      const response = await fetch(new URL("provenance.json", document.baseURI));
      if (!response.ok) throw new Error("Provenance metadata could not be loaded.");
      const provenance = await response.json();
      elements.heroCount.textContent = `${provenance.total_papers.toLocaleString()} papers · 5 years`;
      elements.integrity.replaceChildren();
      const generated = node("p", "", `Metadata snapshot generated ${provenance.generated_at}. Counts and SHA256 values below are from files written by the ingester.`);
      const table = node("table");
      const head = node("thead"); const headerRow = node("tr");
      for (const label of ["Year", "Papers", "Empty abstracts", "CVF title matches", "Links replaced", "PDF HEAD 404", "File size", "SHA256"]) headerRow.append(node("th", "", label));
      head.append(headerRow); const body = node("tbody");
      for (const [year, item] of Object.entries(provenance.years)) {
        const row = node("tr");
        row.append(node("td", "", year), node("td", "", item.count.toLocaleString()), node("td", "", String(item.empty_abstracts)), node("td", "", `${item.cvf_listing_matched}/${item.count}`), node("td", "", String(item.source_links_replaced)), node("td", "", String(item.checked_404_pdf_links)), node("td", "", `${item.output_bytes.toLocaleString()} bytes`));
        const hashCell = node("td"); hashCell.append(node("code", "", item.output_sha256)); row.append(hashCell); body.append(row);
      }
      table.append(head, body); elements.integrity.append(generated, table);
    } catch (error) {
      elements.heroCount.textContent = "2022–2026 archive";
      elements.integrity.replaceChildren(node("p", "", error.message));
    }
  }

  async function importPins(file) {
    if (!file) return;
    try {
      const data = JSON.parse(await file.text());
      const incoming = Array.isArray(data) ? data : data.pins;
      if (!Array.isArray(incoming)) throw new Error("Expected an array of pinned paper records.");
      for (const paper of incoming.slice(0, 500)) {
        if (safePaper(paper)) {
          const old = pins.findIndex(item => item.id === paper.id);
          if (old >= 0) pins.splice(old, 1);
          pins.push(paper);
        }
      }
      persistPins(); elements.status.textContent = `Imported pins from ${file.name}. They remain in this browser.`;
    } catch (error) { elements.status.textContent = `Could not import pins: ${error.message}`; }
    elements.importPins.value = "";
  }

  function exportPins() {
    const file = new Blob([JSON.stringify({schema:"cvpr-hub-pins-v1", exported_at:new Date().toISOString(), pins}, null, 2)], {type:"application/json"});
    const link = node("a"); link.href = URL.createObjectURL(file); link.download = "cvpr-hub-pins.json"; link.click();
    setTimeout(() => URL.revokeObjectURL(link.href), 1000);
  }

  function paperById(id) { return pins.find(paper => paper.id === id); }

  elements.form.addEventListener("submit", event => { event.preventDefault(); clearTimeout(debounce); runSearch(true); });
  elements.query.addEventListener("input", () => { clearTimeout(debounce); debounce = setTimeout(() => runSearch(true), 260); });
  elements.sort.addEventListener("change", () => runSearch(true));
  elements.more.addEventListener("click", () => runSearch(false));
  elements.exportPins.addEventListener("click", exportPins);
  elements.importPins.addEventListener("change", () => importPins(elements.importPins.files[0]));
  elements.closeDialog.addEventListener("click", () => elements.dialog.close());
  elements.clearProblem.addEventListener("click", () => { problemPaper = null; renderIdea(); elements.ideaStatus.textContent = "Problem paper cleared."; });
  elements.clearMethod.addEventListener("click", () => { methodPaper = null; renderIdea(); elements.ideaStatus.textContent = "Method paper cleared."; });
  elements.results.addEventListener("click", event => {
    const button = event.target.closest("[data-action]"); if (!button) return;
    const card = button.closest("[data-paper-id]"); if (!card) return;
    const paperId = card.dataset.paperId;
    const paper = [...elements.results.querySelectorAll("[data-paper-id]")].map(item => item.__paper).find(item => item && item.id === paperId);
    if (!paper) return;
    if (button.dataset.action === "detail") showDetail(paper);
    if (button.dataset.action === "pin") pinPaper(paper);
    if (button.dataset.action === "problem" || button.dataset.action === "method") setIdeaPaper(button.dataset.action, paper);
  });
  elements.pinned.addEventListener("click", event => {
    const button = event.target.closest("[data-action]"); if (!button) return;
    const paper = paperById(button.dataset.pinId); if (!paper) return;
    if (button.dataset.action === "detail") showDetail(paper);
    if (button.dataset.action === "unpin") pinPaper(paper);
  });
  worker.addEventListener("message", event => {
    const message = event.data;
    if (message.requestId !== requestId) return;
    if (message.type === "progress") {
      elements.progress.max = message.total; elements.progress.value = message.current;
      elements.progressLabel.textContent = `${message.stage === "indexed" ? "Indexed" : "Loading"} ${message.year} · ${message.current}/${message.total}`;
      elements.status.textContent = message.stage === "indexed" ? `${message.yearCount.toLocaleString()} papers added from ${message.year}.` : `Loading ${message.year} papers…`;
    } else if (message.type === "results") {
      elements.progressWrap.hidden = true; renderResults(message);
    } else if (message.type === "error") {
      elements.progressWrap.hidden = true; elements.status.textContent = message.message; elements.resultCount.textContent = "Search unavailable";
      emptyState("The search could not finish.", `${message.message} Check that this site is served over HTTP or HTTPS.`);
    }
  });

  setupFilters(); renderPins(); loadIntegrity();
  document.addEventListener("keydown", event => {
    if (event.key === "/" && !elements.dialog.open && !["INPUT", "TEXTAREA", "SELECT"].includes(document.activeElement.tagName)) { event.preventDefault(); elements.query.focus(); }
  });
})();
