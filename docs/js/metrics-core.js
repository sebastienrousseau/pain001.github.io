/* Pure helpers for pain001.com's first-party measurement. No DOM, no network:
   metrics.js wires these into the page, tests import them directly. The
   collector is GoatCounter's /count endpoint (open source, cookieless),
   reached at the project's own host. */

/** The only five things the site counts. Anything else is not an event. */
export const EVENTS = Object.freeze([
  "try_run", "try_download_xml", "corpus_zip_download", "install_click", "contact_submit",
]);

/** Measurement runs only when the layout says so and names an https host. */
export function configured(enabled, hostUrl) {
  return String(enabled) === "true" && typeof hostUrl === "string" && hostUrl.startsWith("https://");
}

/** Do-Not-Track and Global Privacy Control both switch measurement off. */
export function optedOut(nav) {
  return !nav || nav.doNotTrack === "1" || nav.globalPrivacyControl === true;
}

/** Map a clicked element to an event name and label, or null. */
export function classify(el) {
  if (!el) return null;
  const explicit = el.dataset && el.dataset.track;
  if (explicit) {
    const [name, label = ""] = explicit.split(":");
    return EVENTS.includes(name) ? { name, label: label.slice(0, 64) } : null;
  }
  const href = el.getAttribute ? el.getAttribute("href") || "" : "";
  if (/\/corpus\/[^?#]*\.zip$/.test(href)) return { name: "corpus_zip_download", label: href.split("/").pop() };
  if (/^https:\/\/pypi\.org\/project\/pain001/.test(href)) return { name: "install_click", label: href.replace(/^https:\/\/pypi\.org\/project\//, "").replace(/\/$/, "") };
  return null;
}

/**
 * The query string GoatCounter's /count accepts. A page view carries the
 * path; an event carries its name as the path with e=true. The referrer
 * is dropped when it is this site; no identifier of any kind is sent.
 */
export function countQuery({ name, label, page, referrer, screen, title }) {
  const sameSite = referrer && page.origin && referrer.startsWith(page.origin);
  const params = new URLSearchParams();
  if (name) {
    params.set("p", label ? `${name}:${label}` : name);
    params.set("e", "true");
    params.set("t", name);
  } else {
    params.set("p", page.pathname || "/");
    params.set("t", (title || "").slice(0, 200));
  }
  params.set("r", sameSite ? "" : (referrer || ""));
  if (screen) params.set("s", screen);
  params.set("rnd", String(Date.now() % 1e9));
  return params.toString();
}
