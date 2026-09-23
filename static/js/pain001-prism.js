/* Pain001 behaviour layered on the unmodified PRISM interaction script. */
(function () {
  "use strict";

  function ready(callback) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", callback, { once: true });
    } else {
      callback();
    }
  }

  ready(function () {
    var path = window.location.pathname.replace(/\/+$/, "") + "/";
    document.querySelectorAll(".nav-link").forEach(function (link) {
      var href = link.getAttribute("href");
      if (href === path || (href === "/" && path === "/")) {
        link.setAttribute("aria-current", "page");
      }
    });

    var locale = (document.documentElement.lang || "en").toUpperCase();
    var localeLabel = document.querySelector(".ap-lang-current");
    if (localeLabel) localeLabel.textContent = locale.split("-")[0];

    /* Local navigation and article contents rails: mark the section in
       view with aria-current. */
    document.querySelectorAll("[data-local-nav]").forEach(function (localNav) {
      if (!("IntersectionObserver" in window)) return;
      var links = Array.prototype.slice.call(localNav.querySelectorAll('a[href^="#"]'));
      var byId = {};
      links.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          links.forEach(function (a) { a.removeAttribute("aria-current"); });
          var link = byId[entry.target.id];
          if (link) link.setAttribute("aria-current", "location");
        });
      }, { rootMargin: "-30% 0px -60% 0px" });
      Object.keys(byId).forEach(function (id) {
        var section = document.getElementById(id);
        if (section) observer.observe(section);
      });
    });

    var root = document.documentElement;

    /* Motion toggle in the footer (WCAG 2.3.3): stored on this device only. */
    var motion = document.getElementById("motion-toggle");
    if (motion) {
      var off = root.classList.contains("motion-off");
      motion.setAttribute("aria-pressed", String(off));
      motion.addEventListener("click", function () {
        off = !off;
        root.classList.toggle("motion-off", off);
        root.classList.toggle("js-motion", !off && !(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches));
        motion.setAttribute("aria-pressed", String(off));
        if (off) document.querySelectorAll("[data-reveal], [data-settle]").forEach(function (el) { el.classList.add("is-visible"); });
        try {
          if (off) localStorage.setItem("motion", "off"); else localStorage.removeItem("motion");
        } catch (e) {}
      });
    }

    /* A table wider than its box scrolls sideways; keyboard users can
       only scroll what they can focus. Only wrappers that actually
       overflow become focusable regions, named after their section so
       every landmark is distinct. */
    var tableNames = {};
    document.querySelectorAll(".table-responsive").forEach(function (box) {
      if (box.hasAttribute("tabindex") || box.querySelector("[tabindex], .ssg-table-scroll") ||
          (box.parentElement && box.parentElement.closest('[role="region"], .ssg-table-scroll'))) return;
      if (box.scrollWidth <= box.clientWidth + 1) return;
      var heading = null;
      document.querySelectorAll("main h2, main h3, main h4").forEach(function (h) {
        if (h.compareDocumentPosition(box) & Node.DOCUMENT_POSITION_FOLLOWING) heading = h;
      });
      var th = box.querySelector("th");
      var base = ((heading ? heading.textContent : "") || "").replace(/\s*#\s*$/, "").trim();
      var name = base + (th ? ": " + th.textContent.trim() : "");
      name = name || document.title;
      tableNames[name] = (tableNames[name] || 0) + 1;
      if (tableNames[name] > 1) name += " (" + tableNames[name] + ")";
      box.setAttribute("tabindex", "0");
      box.setAttribute("role", "region");
      box.setAttribute("aria-label", name);
    });

    var bookmark = document.getElementById("bookmark-page");
    if (!bookmark) return;

    var key = "pain001:bookmarks";
    var saved = [];
    try { saved = JSON.parse(localStorage.getItem(key) || "[]"); } catch (error) {}

    function paint() {
      var active = saved.some(function (item) { return item.url === path; });
      /* The label stays "Save page" (translated per locale); the pressed
         state carries "saved" to assistive technology and the icon fills. */
      bookmark.setAttribute("aria-pressed", String(active));
    }

    paint();
    bookmark.addEventListener("click", function () {
      var index = saved.findIndex(function (item) { return item.url === path; });
      if (index >= 0) saved.splice(index, 1);
      else saved.push({ url: path, title: document.title });
      try { localStorage.setItem(key, JSON.stringify(saved)); } catch (error) {}
      paint();
    });
  });
})();
