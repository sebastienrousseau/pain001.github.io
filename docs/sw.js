/* Pain001 demo service worker.
 *
 * Purpose: make the /try/ validator — including the WASM XSD engine —
 * work fully offline after one visit, so the "nothing leaves your
 * machine" claim is falsifiable: load the page once, go offline, and
 * everything still works.
 *
 * Scope discipline: only the demo page and its assets are cached
 * (cache-first). Every other request passes straight through to the
 * network untouched, so the rest of the site can never go stale
 * because of this worker. No request is ever created that the page
 * would not have made itself.
 */

const CACHE = "pain001-try-v2";

const CACHEABLE = [
  "/try/",
  "/sw.js",
];

function cacheable(url) {
  const u = new URL(url);
  if (u.origin !== self.location.origin) return false;
  if (u.pathname.startsWith("/pyodide/")) return true;
  if (u.pathname.startsWith("/js/")) return true;
  if (u.pathname.startsWith("/samples/")) return true;
  if (u.pathname.startsWith("/_csp/")) return true;
  return CACHEABLE.includes(u.pathname);
}

self.addEventListener("install", (event) => {
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET" || !cacheable(event.request.url)) return;
  event.respondWith(
    caches.open(CACHE).then((cache) =>
      cache.match(event.request).then((hit) => {
        if (hit) return hit;
        return fetch(event.request).then((resp) => {
          if (resp.ok) cache.put(event.request, resp.clone());
          return resp;
        });
      })
    )
  );
});
