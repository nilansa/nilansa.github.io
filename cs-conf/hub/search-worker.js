/* A small per-year inverted index. It keeps the UI thread free while searching abstracts. */
const documents = [];
const postings = new Map();
const loadedYears = new Set();
const loadingYears = new Map();
const tokenPattern = /[\p{L}\p{N}_+#.-]+/gu;

function words(value) {
  return (String(value || "").toLocaleLowerCase().match(tokenPattern) || []).map(word => word.replace(/^[.-]+|[.-]+$/g, "")).filter(Boolean);
}

function normalized(value) { return words(value).join(" "); }
function containsWholePhrase(haystack, phrase) {
  return Boolean(phrase) && (` ${haystack} `).includes(` ${phrase} `);
}

function addDocument(paper) {
  const id = documents.length;
  const fields = [
    ["title", 3], ["authors", 1.2], ["abstract", 1]
  ];
  const termWeights = new Map();
  const normalizedFields = {};
  let length = 0;
  for (const [field, weight] of fields) {
    const fieldWords = words(paper[field]);
    normalizedFields[field] = fieldWords.join(" ");
    length += fieldWords.length * (field === "title" ? 2 : 1);
    const frequencies = new Map();
    for (const word of fieldWords) frequencies.set(word, (frequencies.get(word) || 0) + 1);
    for (const [word, frequency] of frequencies) termWeights.set(word, (termWeights.get(word) || 0) + weight * frequency);
  }
  const record = {...paper, _id: id, _length: length, _title: normalizedFields.title, _authors: normalizedFields.authors, _abstract: normalizedFields.abstract};
  documents.push(record);
  for (const [term, frequency] of termWeights) {
    if (!postings.has(term)) postings.set(term, []);
    postings.get(term).push([id, frequency]);
  }
}

async function ensureYear(year, requestId, position, total) {
  if (loadedYears.has(year)) return;
  if (loadingYears.has(year)) return loadingYears.get(year);
  const promise = (async () => {
    self.postMessage({type:"progress", requestId, current:position, total, year, stage:"download"});
    const url = new URL(`data/${year}.json`, self.location.href);
    const response = await fetch(url);
    if (!response.ok) throw new Error(`Could not load ${year} metadata (HTTP ${response.status}).`);
    const bundle = await response.json();
    if (bundle.year !== year || !Array.isArray(bundle.papers)) throw new Error(`The ${year} data file has an invalid format.`);
    for (const paper of bundle.papers) addDocument(paper);
    loadedYears.add(year);
    self.postMessage({type:"progress", requestId, current:position, total, year, yearCount:bundle.papers.length, stage:"indexed"});
  })();
  loadingYears.set(year, promise);
  try { await promise; }
  finally { loadingYears.delete(year); }
}

function search(message) {
  const yearSet = new Set(message.years);
  const terms = [...new Set(words(message.query))];
  const rawPhrases = [...String(message.query || "").matchAll(/"([^\"]+)"/g)].map(match => normalized(match[1])).filter(Boolean);
  const unquoted = String(message.query || "").replace(/"[^\"]+"/g, " ").trim();
  if (words(unquoted).length > 1) rawPhrases.push(normalized(unquoted));
  const selected = documents.filter(document => yearSet.has(document.year) && (!message.topic || document.cluster === message.topic));
  if (!selected.length || (!terms.length && !message.topic)) {
    self.postMessage({type:"results", requestId:message.requestId, total:0, offset:Math.max(0, Number(message.offset) || 0), results:[]});
    return;
  }
  const selectedCount = selected.length;
  let averageLength = selected.reduce((sum, document) => sum + document._length, 0) / selectedCount;
  averageLength = Math.max(averageLength, 1);
  const selectedIds = new Set(selected.map(document => document._id));
  const scores = new Map();
  for (const term of terms) {
    const list = postings.get(term) || [];
    let df = 0;
    for (const [id] of list) if (selectedIds.has(id)) df++;
    if (!df) continue;
    const idf = Math.log(1 + (selectedCount - df + 0.5) / (df + 0.5));
    for (const [id, frequency] of list) {
      if (!selectedIds.has(id)) continue;
      const document = documents[id];
      const denominator = frequency + 1.2 * (0.25 + 0.75 * document._length / averageLength);
      const score = idf * (frequency * 2.2) / denominator;
      scores.set(id, (scores.get(id) || 0) + score);
    }
  }
  const queryWords = words(message.query);
  for (const document of selected) {
    let score = scores.get(document._id) || 0;
    const fields = [document._title, document._authors, document._abstract];
    for (const phrase of rawPhrases) {
      if (containsWholePhrase(document._title, phrase)) score += 10;
      else if (fields.some(field => containsWholePhrase(field, phrase))) score += 5;
    }
    for (let i = 0; i < queryWords.length - 1; i++) {
      const bigram = `${queryWords[i]} ${queryWords[i + 1]}`;
      if (fields.some(field => containsWholePhrase(field, bigram))) score += 1.6;
    }
    if (message.topic || score > 0) scores.set(document._id, score);
  }
  const matching = selected.filter(document => scores.has(document._id));
  const sort = message.sort || "relevance";
  matching.sort((a, b) => {
    if (sort === "newest") return b.year - a.year || a.title.localeCompare(b.title);
    if (sort === "oldest") return a.year - b.year || a.title.localeCompare(b.title);
    if (sort === "title") return a.title.localeCompare(b.title) || b.year - a.year;
    return (scores.get(b._id) - scores.get(a._id)) || b.year - a.year || a.title.localeCompare(b.title);
  });
  const start = Math.max(0, Number(message.offset) || 0);
  const end = start + Math.max(1, Number(message.limit) || 40);
  const results = matching.slice(start, end).map(document => {
    const {_id, _length, _title, _authors, _abstract, ...paper} = document;
    return {...paper, score:Math.round((scores.get(_id) || 0) * 10000) / 10000};
  });
  self.postMessage({type:"results", requestId:message.requestId, total:matching.length, offset:start, results});
}

self.onmessage = async event => {
  const message = event.data || {};
  if (message.type !== "search") return;
  const years = [...new Set((message.years || []).map(Number))].filter(year => year >= 2022 && year <= 2026).sort((a,b) => b-a);
  try {
    for (let index = 0; index < years.length; index++) await ensureYear(years[index], message.requestId, index + 1, years.length);
    search({...message, years});
  } catch (error) {
    self.postMessage({type:"error", requestId:message.requestId, message:error.message || "Search failed."});
  }
};
