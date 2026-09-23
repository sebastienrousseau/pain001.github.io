/* Legacy-URL redirect for the stubs postbuild writes (see
   gen_legacy_redirects). Same-origin, so the stubs' CSP allows it; the
   page's own link is the fallback without scripting. */
(function () {
  "use strict";
  var to = document.currentScript && document.currentScript.getAttribute("data-redirect");
  if (to && to.charAt(0) === "/" && to.charAt(1) !== "/") {
    window.location.replace(to);
  }
})();
