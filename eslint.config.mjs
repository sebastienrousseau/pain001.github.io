// SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
//
// The JavaScript coding standard for this repository: ESLint's
// recommended rules, with the right environment per file set. CI runs
// `npm run lint`; see DEVELOPMENT.md.
import js from "@eslint/js";
import globals from "globals";

export default [
  {
    ignores: [
      "static/js/cf-beacon.min.js", // vendored Cloudflare beacon
      "static/pyodide/**", // fetched runtime, never committed
      "site/**", "Pain001/**", "output/**", "public/**", "node_modules/**", ".claude/**", ".a11y-tools/**",
    ],
  },
  js.configs.recommended,
  {
    // The demo's ES modules.
    files: ["static/js/try-*.js"],
    languageOptions: { sourceType: "module", globals: { ...globals.browser } },
  },
  {
    // Classic scripts the pages load directly, and the service worker.
    files: ["static/js/*.js", "static/sw.js"],
    ignores: ["static/js/try-*.js"],
    languageOptions: { sourceType: "script", globals: { ...globals.browser, ...globals.serviceworker } },
  },
  {
    // Node tooling. The audit scripts also pass callbacks to Puppeteer
    // that run inside the page, so browser globals are in scope there.
    files: ["scripts/**/*.mjs", "eslint.config.mjs"],
    languageOptions: { sourceType: "module", globals: { ...globals.node, ...globals.browser } },
  },
  {
    files: ["scripts/**/*.cjs"],
    languageOptions: { sourceType: "commonjs", globals: { ...globals.node, ...globals.browser } },
  },
  {
    files: ["tests/**/*.mjs"],
    languageOptions: { sourceType: "module", globals: { ...globals.node } },
  },
  {
    files: ["tests/**/*.js"],
    languageOptions: { sourceType: "commonjs", globals: { ...globals.node } },
  },
];
