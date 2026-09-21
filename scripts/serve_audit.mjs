#!/usr/bin/env node
/* Production-like local server for Lighthouse: compression and immutable
 * asset caching match the behaviour expected from the Pages CDN. */
import { createServer } from "node:http";
import { createReadStream, existsSync, statSync } from "node:fs";
import { gzipSync } from "node:zlib";
import { extname, join, normalize, resolve } from "node:path";
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
};
const compressible = new Set([".css", ".html", ".js", ".json", ".svg", ".txt", ".webmanifest", ".xml"]);

createServer(async (request, response) => {
  const pathname = decodeURIComponent(new URL(request.url, "http://localhost").pathname);
  const relative = normalize(pathname).replace(/^(\.\.(\/|\\|$))+/, "").replace(/^[/\\]+/, "");
  let file = join(root, relative);
  if (pathname.endsWith("/") || (existsSync(file) && statSync(file).isDirectory())) file = join(file, "index.html");
  if (!file.startsWith(root) || !existsSync(file) || !statSync(file).isFile()) {
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
    const payload = gzipSync(await readFile(file), { level: 9 });
    response.writeHead(200, { ...headers, "Content-Encoding": "gzip", Vary: "Accept-Encoding", "Content-Length": payload.length });
    response.end(payload);
    return;
  }
  response.writeHead(200, { ...headers, "Content-Length": statSync(file).size });
  createReadStream(file).pipe(response);
}).listen(port, "127.0.0.1", () => {
  console.log(`Audit server: http://127.0.0.1:${port}/ (${root})`);
});
