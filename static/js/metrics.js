/* pain001.com first-party measurement: cookieless, no identifiers, five named
   events plus a page view, sent to the project's own metrics host. Off when
   the id is unset, when Do-Not-Track or Global Privacy Control is on, and
   silently no-op when the host is unreachable. */
import { EVENTS, configured, optedOut, classify, payload } from "/js/metrics-core.js";

const tag = document.querySelector('script[data-website-id][data-host-url]');
const websiteId = tag ? tag.dataset.websiteId : "";
const hostUrl = tag ? tag.dataset.hostUrl.replace(/\/$/, "") : "";

function send(name, label) {
  if (!configured(websiteId, hostUrl) || optedOut(navigator)) return;
  const body = payload({
    websiteId, name, label, page: location, referrer: document.referrer,
    language: navigator.language, screen: `${screen.width}x${screen.height}`, title: document.title,
  });
  try {
    fetch(`${hostUrl}/api/send`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body), keepalive: true, credentials: "omit", mode: "cors",
    }).catch(() => {});
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
