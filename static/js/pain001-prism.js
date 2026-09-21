/* Pain001's PRISM theme integration: three-state colour mode and bookmarks. */
(function () {
  "use strict";

  var root = document.documentElement;
  var order = ["system", "light", "dark"];

  function explicitMode() {
    var value = root.getAttribute("data-theme");
    return value === "light" || value === "dark" ? value : "system";
  }

  function labelFor(mode) {
    return mode.charAt(0).toUpperCase() + mode.slice(1) + " colour mode";
  }

  function paintMode(mode) {
    document.querySelectorAll("#mode-toggle").forEach(function (button) {
      var state = button.querySelector("#mode-state");
      if (state) state.textContent = labelFor(mode);
      button.setAttribute("aria-label", labelFor(mode) + ". Activate next mode.");
      button.setAttribute("title", labelFor(mode));
    });
  }

  function applyMode(mode) {
    if (mode === "system") {
      root.removeAttribute("data-theme");
      try { localStorage.removeItem("theme"); } catch (error) {}
    } else {
      root.setAttribute("data-theme", mode);
      try { localStorage.setItem("theme", mode); } catch (error) {}
    }
    paintMode(mode);
  }

  paintMode(explicitMode());

  /* Capture prevents the legacy two-state listener from also processing the
     same activation while the templates transition to the shared PRISM shell. */
  document.addEventListener("click", function (event) {
    var toggle = event.target.closest("#mode-toggle");
    if (!toggle) return;
    event.stopImmediatePropagation();
    var current = explicitMode();
    applyMode(order[(order.indexOf(current) + 1) % order.length]);
  }, true);

  var bookmark = document.getElementById("bookmark-page");
  if (bookmark) {
    var key = "pain001:bookmarks";
    var url = window.location.pathname;
    var saved = [];
    try { saved = JSON.parse(localStorage.getItem(key) || "[]"); } catch (error) {}
    function paintBookmark() {
      var active = saved.some(function (item) { return item.url === url; });
      bookmark.setAttribute("aria-pressed", String(active));
      bookmark.querySelector("span").textContent = active ? "Saved" : "Save page";
    }
    paintBookmark();
    bookmark.addEventListener("click", function () {
      var index = saved.findIndex(function (item) { return item.url === url; });
      if (index >= 0) saved.splice(index, 1);
      else saved.push({ url: url, title: document.title });
      try { localStorage.setItem(key, JSON.stringify(saved)); } catch (error) {}
      paintBookmark();
    });
  }
})();
