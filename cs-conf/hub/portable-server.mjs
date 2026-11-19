#!/usr/bin/env node
/* Portable, dependency-free CS Research Hub. Static GitHub Pages files remain unchanged.
 * Optional local read-only API: /api/v1/health, catalog, schema, search.
 * Default bind is loopback only. No outbound traffic, authentication, paid API, or writes.
 */
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const VERSION = "1.0.0";
const catalog = JSON.parse(fs.readFileSync(path.join(ROOT, "catalog.json"), "utf8"));
const args = process.argv.slice(2);
let host = "127.0.0.1", port = 8765;
for (let i = 0; i < args.length; i++) {
  if (args[i] === "--host") host = String(args[++i] || "");
  else if (args[i] === "--port") port = Number(args[++i]);
  else if (args[i] === "--help") {
    console.log("node portable-server.mjs [--host 127.0.0.1] [--port 8765]");
    process.exit(0);
  } else { console.error("Unknown argument: " + args[i]); process.exit(2); }
}
if (!host || !Number.isInteger(port) || port < 1 || port > 65535) {
  console.error("Invalid host or port"); process.exit(2);
}
const count = Object.values(catalog.venues).reduce((n, v) => n + Number(v.total_records || 0), 0);
const baseHeaders = {
  "X-Content-Type-Options": "nosniff", "Referrer-Policy": "no-referrer",
  "X-Frame-Options": "DENY", "Cache-Control": "no-store",
  "Content-Security-Policy": "default-src 'self'; script-src 'self'; worker-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'"
};
const mime = {
  ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8", ".txt": "text/plain; charset=utf-8",
  ".md": "text/plain; charset=utf-8"
};
function send(req, res, code, body, headers = {}) {
  const buf = Buffer.isBuffer(body) ? body : Buffer.from(body, "utf8");
  res.writeHead(code, { ...baseHeaders, ...headers, "Content-Length": buf.length });
  res.end(req.method === "HEAD" ? undefined : buf);
}
function json(req, res, code, payload) {
  send(req, res, code, JSON.stringify(payload), { "Content-Type": "application/json; charset=utf-8" });
}
function error(req, res, code, label, message) {
  json(req, res, code, { api_version: VERSION, error: { code: label, message } });
}
function csv(params, key) {
  return params.getAll(key).flatMap(s => s.split(",")).map(s => s.trim()).filter(Boolean);
}
function validHttps(u) {
  if (typeof u !== "string" || !u) return "";
  try {
    const parsed = new URL(u);
    if (parsed.protocol !== "https:" || parsed.username || parsed.password || parsed.hash) return "";
    return parsed.toString();
  } catch { return ""; }
}
function normalize(p, venue, score) {
  const abstract = typeof p.abstract === "string" ? p.abstract : "";
  return {
    id: String(p.id || ""), venue, year: Number(p.year), title: String(p.title || ""),
    authors: Array.isArray(p.authors) ? p.authors.join(", ") : String(p.authors || ""),
    abstract, abstract_status: abstract.trim() ? "available" : "missing in source metadata",
    paper_url: validHttps(p.paper_url || p.cvf_url || ""),
    pdf_url: validHttps(p.pdf_url || ""),
    source: String(p.source || "Unknown source"),
    track_status: String(p.track_status || "Unverified"),
    cluster: p.cluster ? String(p.cluster) : null,
    primary_area: p.primary_area ? String(p.primary_area) : null,
    doi: p.doi ? String(p.doi) : null,
    source_verification: p.cvf_reference_type === "paper page" ? "publisher_verified" : "dataset_metadata",
    score
  };
}
function parseSearch(searchParams) {
  const q = String(searchParams.get("q") || "").trim();
  if (!q || q.length > 200) throw new Error("q must have 1–200 characters.");
  const venues = [...new Set(csv(searchParams, "venue"))];
  const requestedVenues = venues.length ? venues : ["CVPR"];
  if (requestedVenues.some(v => !Object.hasOwn(catalog.venues, v))) throw new Error("Unknown venue. Use names in catalog.json.");
  const requestedYears = [...new Set(csv(searchParams, "year"))];
  const years = requestedYears.length ? requestedYears.map(y => Number(y)) : [2026];
  if (years.some(y => !Number.isInteger(y) || y < 2017 || y > 2026)) throw new Error("Years must be integers from 2017 to 2026.");
  const limit = searchParams.has("limit") ? Number(searchParams.get("limit")) : 20;
  const offset = searchParams.has("offset") ? Number(searchParams.get("offset")) : 0;
  if (!Number.isInteger(limit) || limit < 1 || limit > 50) throw new Error("limit must be an integer from 1 to 50.");
  if (!Number.isInteger(offset) || offset < 0 || offset > 200) throw new Error("offset must be an integer from 0 to 200.");
  const shards = [];
  for (const venue of requestedVenues) {
    for (const year of years) {
      const entry = catalog.venues[venue].years[String(year)];
      if (entry && entry.file) shards.push({ venue, year, file: entry.file });
    }
  }
  if (shards.length > 20) throw new Error("Search too broad for local API (maximum 20 venue-year shards per request).");
  return { q, venue: requestedVenues, year: years, limit, offset, shards };
}
function scorePaper(p, terms, wholeQuery) {
  const t = String(p.title || "").toLowerCase();
  const a = String(p.abstract || "").toLowerCase();
  const by = Array.isArray(p.authors) ? p.authors.join(" ").toLowerCase() : String(p.authors || "").toLowerCase();
  let score = 0, matched = 0;
  for (const term of terms) {
    const hitTitle = t.includes(term), hitAbstract = a.includes(term), hitAuthor = by.includes(term);
    if (hitTitle || hitAbstract || hitAuthor) matched++;
    if (hitTitle) score += 6;
    if (hitAbstract) score += 2;
    if (hitAuthor) score += 1;
  }
  if (!matched) return 0;
  if (t.includes(wholeQuery)) score += 7;
  else if (a.includes(wholeQuery)) score += 3;
  if (matched === terms.length) score += 4;
  return score;
}
function search(query) {
  const terms = [...new Set((query.q.toLowerCase().match(/[\p{L}\p{N}_+#.-]+/gu) || []))];
  if (!terms.length) throw new Error("q must include searchable words or numbers.");
  let scanned = 0, matched = 0, missing = 0;
  const resultCandidates = [];
  for (const { venue, year, file } of query.shards) {
    const full = path.resolve(ROOT, file);
    if (!full.startsWith(ROOT + path.sep) || !full.endsWith(".json"))
      throw new Error("Unsafe catalog data path.");
    const block = JSON.parse(fs.readFileSync(full, "utf8"));
    if (block.year !== year || !Array.isArray(block.papers))
      throw new Error("Invalid data shard for " + venue + " " + year);
    const local = [];
    for (const raw of block.papers) {
      scanned++;
      if (!raw.abstract || !String(raw.abstract).trim()) missing++;
      const relevance = scorePaper(raw, terms, query.q.toLowerCase());
      if (!relevance) continue;
      matched++;
      local.push(normalize(raw, venue, relevance));
    }
    local.sort((a, b) => b.score - a.score || b.year - a.year || a.title.localeCompare(b.title));
    resultCandidates.push(...local.slice(0, 251));
  }
  resultCandidates.sort((a, b) => b.score - a.score || b.year - a.year || a.title.localeCompare(b.title));
  const slice = resultCandidates.slice(query.offset, query.offset + query.limit);
  const { shards, ...publicQuery } = query;
  return {
    api_version: VERSION, query: publicQuery, results: slice,
    meta: {
      matched_records: matched, scanned_records: scanned, selected_shards: shards.length,
      returned_records: slice.length, missing_abstracts: missing,
      limitations: [
        "Lexical ranking, not semantic search; counts may include duplicate papers across venues.",
        "Records and track labels are attributed to sources, not independently verified acceptance.",
        "At most 251 ranked candidates from each shard are retained for pagination.",
        "No external APIs, models or websites are contacted by the local server."
      ]
    }
  };
}
const server = http.createServer((req, res) => {
  try {
    if (req.method !== "GET" && req.method !== "HEAD") {
      error(req, res, 405, "method_not_allowed", "Only GET and HEAD are supported."); return;
    }
    const u = new URL(req.url || "/", "http://localhost");
    if (u.pathname === "/api/v1/health") {
      json(req, res, 200, { status: "ok", api_version: VERSION, dataset_schema: catalog.schema,
        venue_count: Object.keys(catalog.venues).length, paper_records: count, source: "local_catalog" }); return;
    }
    if (u.pathname === "/api/v1/catalog") { json(req, res, 200, catalog); return; }
    if (u.pathname === "/api/v1/schema") {
      send(req, res, 200, fs.readFileSync(path.join(ROOT, "api-contract.json")), { "Content-Type": mime[".json"] }); return;
    }
    if (u.pathname === "/api/v1/search") {
      try { json(req, res, 200, search(parseSearch(u.searchParams))); }
      catch (e) { error(req, res, e.message.startsWith("Invalid data shard") ? 503 : 400, "invalid_search", e.message); }
      return;
    }
    let decoded;
    try { decoded = decodeURIComponent(u.pathname); }
    catch { error(req, res, 400, "bad_path", "Invalid path encoding."); return; }
    if (decoded.includes("\\") || decoded.includes("\0") || decoded.split("/").some(s => s.startsWith("."))) {
      error(req, res, 403, "forbidden", "Path not allowed."); return;
    }
    const relative = decoded === "/" ? "/index.html" : decoded;
    const full = path.resolve(ROOT, "." + relative);
    if (!full.startsWith(ROOT + path.sep) || !Object.hasOwn(mime, path.extname(full).toLowerCase())) {
      error(req, res, 403, "forbidden", "Path not allowed."); return;
    }
    let stat;
    try { stat = fs.statSync(full); } catch { error(req, res, 404, "not_found", "File not found."); return; }
    if (!stat.isFile()) { error(req, res, 404, "not_found", "File not found."); return; }
    send(req, res, 200, fs.readFileSync(full), { "Content-Type": mime[path.extname(full).toLowerCase()] });
  } catch (e) {
    error(req, res, 500, "internal_error", "Local server error: " + String(e.message || "unknown"));
  }
});
server.listen(port, host, () => console.log("CS Research Hub: http://" + host + ":" + port + "/ (local read-only API /api/v1/health)"));
