import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);
  return worker.fetch(
    new Request("http://localhost/", { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
}

test("server-renders the Phason research site and controlled evidence", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);
  const html = await response.text();
  assert.match(html, /<title>Phason Labs/i);
  assert.match(html, /Measured, then claimed/);
  assert.match(html, /48 \/ 48/);
  assert.match(html, /Controlled benchmark/);
  assert.match(html, /Publication boundary/);
  assert.match(html, /Public telemetry/);
  assert.match(html, /Attention is not adoption/);
  assert.match(html, /mbe-eval/);
  assert.match(html, /traintools/);
  assert.doesNotMatch(html, /codex-preview|Your site is taking shape/i);
});

test("keeps evidence claims linked to public artifacts", async () => {
  const [page, layout] = await Promise.all([
    readFile(new URL("../app/page.tsx", import.meta.url), "utf8"),
    readFile(new URL("../app/layout.tsx", import.meta.url), "utf8"),
  ]);
  assert.match(page, /id="evidence"/);
  assert.match(page, /PROTOCOL\.md/);
  assert.match(page, /benchmark_summary\.json/);
  assert.match(page, /CORRECTION_LOG\.md/);
  assert.match(page, /not used as promotional evidence/);
  assert.match(page, /telemetry-mbe/);
  assert.match(page, /telemetry-traintools/);
  assert.match(page, /122/);
  assert.match(page, /545/);
  assert.match(page, /organic curiosity is plausible/);
  assert.match(layout, /title:\s*"Phason Labs/);
  assert.doesNotMatch(page, /codex-preview|_sites-preview/);
});
