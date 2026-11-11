// SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
//
// pain001.com events: first-party, cookie-free counts of what visitors
// do (decision D1, 10 Nov 2026). The site posts {event, page, label?}
// to /e on its own origin; one Workers Analytics Engine data point is
// written per accepted event. Nothing else is kept: no IP address, no
// user agent, no referrer, no cookie, no identifier of any kind.
// Workers Analytics Engine keeps data points for three months (Cloudflare
// documents "Data written to Workers Analytics Engine is stored for three
// months"), which is the retention the privacy page states.

/** The events the site may send; anything else is refused. */
export const EVENTS = new Set([
  "hero_cta_click",
  "sandbox_start",
  "sandbox_xsd_run",
  "xml_copy",
  "xml_download",
  "install_copy",
  "outbound_github",
  "outbound_pypi",
  "evidence_pack_download",
  "profile_guide_view",
  "adoption_form_submit",
]);

/** The site's own origin: events from anywhere else are dropped. */
export const ORIGIN = "https://pain001.com";

/** A request body larger than this is refused unread. */
export const MAX_BODY_BYTES = 1024;

import { MAX_CSP_BODY_BYTES, recordViolations, violations } from "./csp.js";

const PAGE_MAX = 200;
const PAGE_CHARS = /^\/[A-Za-z0-9._~\-/]*$/;
const LABEL_CHARS = /^[A-Za-z0-9 ._:-]{1,64}$/;
const COUNTRY = /^[A-Z]{2}$/;

const noContent = () =>
  new Response(null, { status: 204, headers: { "Cache-Control": "no-store" } });
const badRequest = () =>
  new Response(null, { status: 400, headers: { "Cache-Control": "no-store" } });

/**
 * Reduce a page reference to a same-site path, or null.
 *
 * The query string and fragment are dropped before anything is checked,
 * so search terms or tokens in a URL are never stored.
 */
export function cleanPage(raw) {
  if (typeof raw !== "string") return null;
  const path = raw.split(/[?#]/, 1)[0];
  if (path.length === 0 || path.length > PAGE_MAX) return null;
  if (path.startsWith("//") || !PAGE_CHARS.test(path)) return null;
  return path;
}

/** Validate one decoded body; returns the fields to store, or null. */
export function parseEvent(body) {
  if (body === null || typeof body !== "object" || Array.isArray(body)) {
    return null;
  }
  const keys = Object.keys(body);
  if (keys.some((k) => k !== "event" && k !== "page" && k !== "label")) {
    return null;
  }
  if (typeof body.event !== "string" || !EVENTS.has(body.event)) return null;
  const page = cleanPage(body.page);
  if (page === null) return null;
  let label = "";
  if (body.label !== undefined) {
    if (typeof body.label !== "string" || !LABEL_CHARS.test(body.label)) {
      return null;
    }
    label = body.label;
  }
  return { event: body.event, page, label };
}

/** True when the visitor asked not to be tracked (DNT or GPC). */
export function optedOut(headers) {
  return headers.get("DNT") === "1" || headers.get("Sec-GPC") === "1";
}

/** True only for requests the site's own pages could have sent. */
export function sameSite(headers) {
  const origin = headers.get("Origin");
  if (origin !== null && origin !== ORIGIN) return false;
  const site = headers.get("Sec-Fetch-Site");
  return site === null || site === "same-origin";
}

/**
 * Read at most MAX_BODY_BYTES of the body as text; null when larger.
 *
 * The body is streamed and abandoned at the cap rather than buffered
 * whole, so an oversized post costs no more than the cap.
 */
export async function readCapped(request, limit = MAX_BODY_BYTES) {
  const declared = Number(request.headers.get("Content-Length"));
  if (Number.isFinite(declared) && declared > limit) return null;
  if (request.body === null) return "";
  const reader = request.body.getReader();
  const chunks = [];
  let size = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    size += value.byteLength;
    if (size > limit) {
      await reader.cancel();
      return null;
    }
    chunks.push(value);
  }
  const bytes = new Uint8Array(size);
  let at = 0;
  for (const chunk of chunks) {
    bytes.set(chunk, at);
    at += chunk.byteLength;
  }
  return new TextDecoder("utf-8", { fatal: false }).decode(bytes);
}

/** The visitor's country as Cloudflare reports it, or "". */
export function countryOf(request) {
  const country = request.cf && request.cf.country;
  return typeof country === "string" && COUNTRY.test(country) ? country : "";
}

/**
 * Handle one request to /e.
 *
 * Only a same-origin POST of a valid event is written. Opted-out and
 * cross-site posts get 204 and are dropped, so a page can never tell
 * whether it was counted; malformed posts get 400 with no detail.
 */
export async function handle(request, env) {
  const url = new URL(request.url);
  if (url.pathname === "/e/csp") return handleCsp(request, env);
  if (url.pathname !== "/e") {
    return new Response(null, { status: 404 });
  }
  if (request.method !== "POST") {
    return new Response(null, { status: 405, headers: { Allow: "POST" } });
  }
  if (optedOut(request.headers) || !sameSite(request.headers)) {
    return noContent();
  }
  const text = await readCapped(request);
  if (text === null) return badRequest();
  let decoded;
  try {
    decoded = JSON.parse(text);
  } catch {
    return badRequest();
  }
  const fields = parseEvent(decoded);
  if (fields === null) return badRequest();
  try {
    env.EVENTS.writeDataPoint({
      blobs: [fields.event, fields.page, fields.label, countryOf(request)],
      doubles: [1],
      indexes: [fields.event],
    });
  } catch (error) {
    // A failed write is logged without any request data and the visitor
    // still gets 204: counting is best effort and never breaks a page.
    console.error(
      JSON.stringify({ message: "events write failed", error: String(error) }),
    );
  }
  return noContent();
}

/**
 * Handle one CSP violation report posted to /e/csp.
 *
 * Browsers send these themselves, so no Origin check applies; a report
 * is only kept when its document is a page on this site. Opted-out
 * visitors are dropped as on /e. Every outcome but a malformed body is
 * 204, so a report can never learn what was stored.
 */
export async function handleCsp(request, env) {
  if (request.method !== "POST") {
    return new Response(null, { status: 405, headers: { Allow: "POST" } });
  }
  if (optedOut(request.headers)) return noContent();
  const text = await readCapped(request, MAX_CSP_BODY_BYTES);
  if (text === null) return badRequest();
  let decoded;
  try {
    decoded = JSON.parse(text);
  } catch {
    return badRequest();
  }
  recordViolations(violations(decoded), request, env);
  return noContent();
}

export default {
  fetch(request, env) {
    return handle(request, env);
  },
};
