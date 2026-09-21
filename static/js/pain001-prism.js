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

    var bookmark = document.getElementById("bookmark-page");
    if (!bookmark) return;

    var key = "pain001:bookmarks";
    var saved = [];
    try { saved = JSON.parse(localStorage.getItem(key) || "[]"); } catch (error) {}

    function paint() {
      var active = saved.some(function (item) { return item.url === path; });
      bookmark.setAttribute("aria-pressed", String(active));
      bookmark.querySelector("span").textContent = active ? "Saved" : "Save page";
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
