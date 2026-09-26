/*
 * SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
 * SPDX-License-Identifier: Apache-2.0 OR MIT
 */
/* Load the vendored Cloudflare beacon only on deployed hosts. Local preview
 * and CI audits must not attempt the external RUM POST. */
(() => {
  const loader = document.currentScript;
  const localHosts = new Set(["localhost", "127.0.0.1", "[::1]"]);
  const token = loader?.dataset.cfToken;
  if (!token || localHosts.has(window.location.hostname)) return;

  const beacon = document.createElement("script");
  beacon.defer = true;
  beacon.src = "/js/cf-beacon.min.js";
  beacon.dataset.cfBeacon = JSON.stringify({ token });
  document.head.append(beacon);
})();
