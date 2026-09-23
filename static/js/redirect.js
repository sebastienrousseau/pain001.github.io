/* Legacy-URL redirect for the stubs postbuild writes (see
   gen_legacy_redirects). Same-origin, so the stubs' CSP allows it; the
   page's own link is the fallback without scripting. */
(function () {
  "use strict";
  var to = document.currentScript && document.currentScript.getAttribute("data-redirect");
  if (!to || to.charAt(0) !== "/" || to.charAt(1) === "/") return;
  // Resolve against this origin and follow only a same-origin path, so the
  // attribute can never send a visitor to another site or a javascript: URL.
  var url = new URL(to, window.location.origin);
  if (url.origin === window.location.origin) {
    window.location.replace(url.pathname + url.search + url.hash);
  }
})();
