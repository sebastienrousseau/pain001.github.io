// SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
//
// Content-Security-Policy violation reports for pain001.com. The site's
// policy is served as Content-Security-Policy-Report-Only for a week
// before it is enforced; browsers post each violation here, to
// /e/csp on the site's own origin. One Analytics Engine data point is
// written per report, holding only the directive, the blocked origin
// (never a full URL), the page path and the country, the same privacy
// line as the events endpoint: no IP address, user agent, referrer,
// cookie or identifier.

import { cleanPage, countryOf } from "./index.js";

/** CSP reports carry the policy and a sample, so they get more room. */
export const MAX_CSP_BODY_BYTES = 4096;

const DIRECTIVE = /^[a-z-]{1,40}$/;
const KEYWORDS = new Set([
  "inline",
  "eval",
  "self",
  "data",
  "blob",
  "wasm-eval",
]);

/**
 * Reduce a blocked URI to a keyword or a scheme and host, or "other".
 *
 * Paths and query strings are dropped, so a report never stores a
 * full address the visitor loaded.
 */
export function blockedOrigin(raw) {
  if (typeof raw !== "string" || raw.length === 0) return "other";
  if (KEYWORDS.has(raw)) return raw;
  try {
    const url = new URL(raw);
    if (url.protocol === "http:" || url.protocol === "https:") {
      return `${url.protocol}//${url.host}`;
    }
    return url.protocol.replace(/:$/, "");
  } catch {
    return "other";
  }
}

/** The page path of a document URI on the site's origin, or null. */
function pageOf(raw) {
  if (typeof raw !== "string") return null;
  try {
    const url = new URL(raw);
    if (url.origin !== "https://pain001.com") return null;
    return cleanPage(url.pathname);
  } catch {
    return null;
  }
}

/**
 * Turn one report body into the fields to store, or null.
 *
 * Accepts the report-uri form ({"csp-report": {...}}, kebab-case keys)
 * and one entry of the Reporting API form ({"type": "csp-violation",
 * "body": {...}}, camelCase keys).
 */
export function parseViolation(report) {
  if (report === null || typeof report !== "object") return null;
  let body;
  let directive;
  let blocked;
  let document;
  if (report["csp-report"] && typeof report["csp-report"] === "object") {
    body = report["csp-report"];
    directive = body["effective-directive"] ?? body["violated-directive"];
    blocked = body["blocked-uri"];
    document = body["document-uri"];
  } else if (report.type === "csp-violation" && report.body) {
    body = report.body;
    directive = body.effectiveDirective;
    blocked = body.blockedURL;
    document = body.documentURL;
  } else {
    return null;
  }
  if (typeof directive !== "string") return null;
  directive = directive.split(" ", 1)[0];
  if (!DIRECTIVE.test(directive)) return null;
  const page = pageOf(document);
  if (page === null) return null;
  return { directive, blocked: blockedOrigin(blocked), page };
}

/** Every violation in a decoded body (one object or a Reporting API list). */
export function violations(decoded) {
  const reports = Array.isArray(decoded) ? decoded.slice(0, 10) : [decoded];
  return reports.map(parseViolation).filter((v) => v !== null);
}

/** Write one data point per violation; failures are logged, not raised. */
export function recordViolations(found, request, env) {
  for (const v of found) {
    try {
      env.EVENTS.writeDataPoint({
        blobs: [
          "csp_violation",
          v.page,
          v.directive,
          countryOf(request),
          v.blocked,
        ],
        doubles: [1],
        indexes: ["csp_violation"],
      });
    } catch (error) {
      console.error(
        JSON.stringify({ message: "csp write failed", error: String(error) }),
      );
    }
  }
}
