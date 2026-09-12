/* Pure helpers for pain001.com's first-party measurement. No DOM, no network:
   metrics.js wires these into the page, tests import them directly. */

/** The only five things the site counts. Anything else is not an event. */
export const EVENTS = Object.freeze([
  "try_run", "try_download_xml", "corpus_zip_download", "install_click", "contact_submit",
]);

const ZERO_ID = /^[0-]+$/;

/** A website id is usable only when it has been set to a real UUID. */
export function configured(websiteId, hostUrl) {
  return typeof websiteId === "string" && websiteId.length >= 32
    && !ZERO_ID.test(websiteId) && typeof hostUrl === "string" && hostUrl.startsWith("https://");
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

/** The body Umami's collector accepts. Referrer is dropped when it is this site. */
export function payload({ websiteId, name, label, page, referrer, language, screen, title }) {
  const sameSite = referrer && page.origin && referrer.startsWith(page.origin);
  const body = {
    website: websiteId, hostname: page.hostname, url: page.pathname,
    referrer: sameSite ? "" : (referrer || ""), language: language || "", screen: screen || "", title: title || "",
  };
  if (name) { body.name = name; if (label) body.data = { label }; }
  return { type: "event", payload: body };
}
