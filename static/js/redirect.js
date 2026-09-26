/*
 * SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
 * SPDX-License-Identifier: Apache-2.0 OR MIT
 */
/* Legacy-URL redirect for the stubs postbuild writes (see
   gen_legacy_redirects). Same-origin, so the stubs' CSP allows it; the
   page's own link is the fallback without scripting.

   The destinations are not read from the page: postbuild's --stamp-sw
   pass writes LEGACY_REDIRECTS into the object below, so this script can
   only ever send a visitor to one of those same-origin paths. */
(function () {
  "use strict";
  var REDIRECTS = {};
  var to = Object.prototype.hasOwnProperty.call(REDIRECTS, window.location.pathname)
    ? REDIRECTS[window.location.pathname]
    : null;
  if (to) window.location.replace(to);
})();
