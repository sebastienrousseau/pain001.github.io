/*
 * SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
 * SPDX-License-Identifier: Apache-2.0 OR MIT
 */
/* First-party, cookie-free event counts (decision D1, see METRICS.md).
 *
 * Each event is one `navigator.sendBeacon` to /e on this origin, served by
 * a Cloudflare Worker that writes it to Workers Analytics Engine. The
 * payload is the event name, the page path and an optional short label:
 * no identifier, no cookie, nothing typed or loaded into the demo. Only
 * the names below are sent. Nothing is sent from a local preview, when
 * the browser asks not to be tracked (Do Not Track or Global Privacy
 * Control), or when sendBeacon is missing; a failed send is ignored.
 *
 * Elements opt in with data-event="<name>" (and data-event-label); links
 * to GitHub and PyPI are counted by their host, and
 * the first interaction with the demo (data-event-start) counts once, and
 * opening the bank-profile guide counts as profile_guide_view. */
(() => {
  const EVENTS = new Set([
    "hero_cta_click", "sandbox_start", "sandbox_xsd_run", "xml_copy",
    "xml_download", "install_copy", "outbound_github", "outbound_pypi",
    "evidence_pack_download", "profile_guide_view", "adoption_form_submit",
  ]);
  const LOCAL = new Set(["localhost", "127.0.0.1", "[::1]"]);
  const nav = window.navigator;
  const optedOut = nav.doNotTrack === "1" || window.doNotTrack === "1" || nav.globalPrivacyControl === true;
  const quiet = LOCAL.has(window.location.hostname) || optedOut || typeof nav.sendBeacon !== "function";

  function send(event, label) {
    if (quiet || !EVENTS.has(event)) return false;
    const payload = { event, page: window.location.pathname };
    if (label) payload.label = String(label).slice(0, 64);
    try {
      return nav.sendBeacon("/e", new Blob([JSON.stringify(payload)], { type: "text/plain" }));
    } catch {
      return false;
    }
  }

  function outbound(link) {
    let url;
    try {
      url = new URL(link.href, window.location.href);
    } catch {
      return null;
    }
    if (url.hostname === "github.com") return "outbound_github";
    if (url.hostname === "pypi.org") return "outbound_pypi";
    return null;
  }

  document.addEventListener("click", (e) => {
    const target = e.target instanceof Element ? e.target : null;
    const tagged = target && target.closest("[data-event]");
    if (tagged) {
      send(tagged.dataset.event, tagged.dataset.eventLabel);
      return;
    }
    const link = target && target.closest("a[href]");
    const event = link && outbound(link);
    if (event) send(event);
  });

  const demo = document.querySelector("[data-event-start]");
  if (demo) {
    let started = false;
    const start = () => {
      if (started) return;
      started = true;
      send("sandbox_start");
    };
    for (const type of ["click", "input", "change", "drop", "paste"]) demo.addEventListener(type, start);
  }

  if (window.location.pathname === "/docs/bank-profiles/") send("profile_guide_view");

  window.pain001Event = send;
})();
