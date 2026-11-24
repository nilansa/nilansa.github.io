import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
const root = new URL("../", import.meta.url);
const base = process.env.HUB_API_URL || "http://127.0.0.1:18765";
const schema = JSON.parse(fs.readFileSync(new URL("../api-contract.json", import.meta.url), "utf8"));
test("API contract", () => {
  assert.equal(schema.api_version, "1.0.0");
  for (const key of ["Paper","Catalog","SearchRequest","SearchResponse","HypothesisPacket","APIError"])
    assert.ok(schema.$defs[key], key);
  for (const key of ["abstract_status","source","track_status","paper_url"])
    assert.ok(schema.$defs.Paper.required.includes(key), key);
});
test("local API endpoints and static site", async () => {
  const health = await (await fetch(base+"/api/v1/health")).json();
  assert.equal(health.venue_count, 12);
  assert.equal(health.paper_records, 130361);
  assert.equal((await (await fetch(base+"/api/v1/schema")).json()).api_version, "1.0.0");
  assert.equal(Object.keys((await (await fetch(base+"/api/v1/catalog")).json()).venues).length, 12);
  const response = await fetch(base+"/api/v1/search?q=diffusion&venue=CVPR&year=2025&limit=3");
  assert.equal(response.status, 200);
  const search = await response.json();
  assert.equal(search.results.length, 3);
  assert.ok(search.results.every(p => p.venue === "CVPR" && p.year === 2025 && p.source));
  assert.equal((await fetch(base+"/api/v1/search?q=diffusion&venue=INVALID")).status, 400);
  assert.equal((await fetch(base+"/api/v1/search?q=diffusion&venue=CVPR&limit=500")).status, 400);
  assert.equal((await fetch(base+"/api/v1/search?q=diffusion&year=1970")).status, 400);
  assert.equal((await fetch(base+"/api/v1/health", {method:"POST"})).status, 405);
  assert.equal((await fetch(base+"/")).status, 200);
  assert.ok(!response.headers.get("access-control-allow-origin"));
});
