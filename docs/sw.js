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

/* Bump this on ANY change to /try/, /<locale>/try/, or the assets
 * matched by cacheable() below. The worker is cache-first, so a
 * returning visitor is served the old page forever until the constant
 * changes — the update ships, CI is green, and nobody sees it. This
 * has been missed three times now: v8 is the layer-summary
 * translations, which reached all 34 locales while returning visitors
 * kept the English original. */
const CACHE = "pain001-try-92e3c1c03847";

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
  if (/^\/[a-z-]+\/try\/$/.test(u.pathname)) return true; // locale demos
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
