/* pain001.com first-party measurement: cookieless, no identifiers, five named
   events plus a page view, sent as a GET to GoatCounter's /count on the
   project's own host. Off unless the layout enables it, off under
   Do-Not-Track and Global Privacy Control, and silently no-op when the host
   is unreachable. */
import { EVENTS, configured, optedOut, classify, countQuery } from "/js/metrics-core.js";

const tag = document.querySelector("script[data-host-url][data-enabled]");
const enabled = tag ? tag.dataset.enabled : "false";
const hostUrl = tag ? tag.dataset.hostUrl.replace(/\/$/, "") : "";

function send(name, label) {
  if (!configured(enabled, hostUrl) || optedOut(navigator)) return;
  const query = countQuery({
    name, label, page: location, referrer: document.referrer,
    screen: `${screen.width},${screen.height},${Math.round(window.devicePixelRatio || 1)}`, title: document.title,
  });
  try {
    fetch(`${hostUrl}/count?${query}`, { method: "GET", mode: "no-cors", keepalive: true, credentials: "omit" }).catch(() => {});
  } catch (_) { /* never surface measurement failures */ }
}

window.pain001Track = (name, label) => { if (EVENTS.includes(name)) send(name, label); };

send();

document.addEventListener("click", (event) => {
  const el = event.target.closest("[data-track], a[href]");
  const hit = classify(el);
  if (hit) send(hit.name, hit.label);
}, { passive: true });

document.addEventListener("submit", (event) => {
  const form = event.target;
  if (form && /formspree\.io/.test(form.getAttribute("action") || "")) send("contact_submit", form.dataset.form || "contact");
}, { passive: true });
