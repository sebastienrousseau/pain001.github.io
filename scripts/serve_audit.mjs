#!/usr/bin/env node
// SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
/* Production-like local server for Lighthouse: compression and immutable
 * asset caching match the behaviour expected from the Pages CDN. */
import { createServer } from "node:http";
import { gzipSync } from "node:zlib";
import { extname, join, normalize, resolve, sep } from "node:path";
import { readFile } from "node:fs/promises";

const root = resolve(process.argv[2] || "site");
const port = Number(process.argv[3] || 8898);
const types = {
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".txt": "text/plain; charset=utf-8",
  ".webmanifest": "application/manifest+json",
  ".xml": "application/xml; charset=utf-8",
  // The rest match what GitHub Pages sends. Without `.wasm` the demo's
  // Python runtime cannot compile (browsers require application/wasm for
  // streaming compilation), so every audit of /try/ saw only the page
  // before validation, never a result.
  ".wasm": "application/wasm",
  ".avif": "image/avif",
  ".webp": "image/webp",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".ico": "image/x-icon",
  ".woff2": "font/woff2",
  ".csv": "text/csv; charset=utf-8",
  ".xsd": "application/xml; charset=utf-8",
  ".zip": "application/zip",
  ".whl": "application/zip",
};
const compressible = new Set([".css", ".html", ".js", ".json", ".svg", ".txt", ".webmanifest", ".xml"]);

createServer(async (request, response) => {
  const pathname = decodeURIComponent(new URL(request.url, "http://localhost").pathname);
  const relative = normalize(pathname).replace(/^(\.\.(\/|\\|$))+/, "").replace(/^[/\\]+/, "");
  let file = resolve(root, relative);
  if (pathname.endsWith("/")) file = join(file, "index.html");
  if (file !== root && !file.startsWith(root + sep)) {
    response.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
    response.end("Not found\n");
    return;
  }
  let payload;
  try {
    payload = await readFile(file);
  } catch {
    response.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
    response.end("Not found\n");
    return;
  }
  const extension = extname(file).toLowerCase();
  const headers = {
    "Content-Type": types[extension] || "application/octet-stream",
    "Cache-Control": extension === ".html" ? "no-cache" : "public, max-age=31536000, immutable",
    "X-Content-Type-Options": "nosniff",
  };
  if (compressible.has(extension) && /\bgzip\b/.test(request.headers["accept-encoding"] || "")) {
    const compressed = gzipSync(payload, { level: 9 });
    response.writeHead(200, { ...headers, "Content-Encoding": "gzip", Vary: "Accept-Encoding", "Content-Length": compressed.length });
    response.end(compressed);
    return;
  }
  response.writeHead(200, { ...headers, "Content-Length": payload.length });
  response.end(payload);
}).listen(port, "127.0.0.1", () => {
  console.log(`Audit server: http://127.0.0.1:${port}/ (${root})`);
});
