
      document.documentElement.classList.add("has-js");
      (function () {
        "use strict";

        /* Theme: sun/moon toggle, aria-pressed, meta theme-color. */
        function currentTheme() {
          var t = document.documentElement.getAttribute("data-theme");
          if (t) return t;
          return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
        }
        function paintTheme(theme) {
          document.querySelectorAll(".theme-toggle").forEach(function (btn) {
            btn.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
            btn.setAttribute("aria-label", theme === "dark" ? "Switch to light theme" : "Switch to dark theme");
          });
        }
        paintTheme(currentTheme());
        document.addEventListener("click", function (e) {
          var btn = e.target.closest(".theme-toggle");
          if (!btn) return;
          var next = currentTheme() === "dark" ? "light" : "dark";
          document.documentElement.setAttribute("data-theme", next);
          try { localStorage.setItem("theme", next); } catch (err) {}
          paintTheme(next);
        });

        /* Search: the in-nav button opens ssg's search overlay. */
        document.querySelectorAll(".ap-search-btn").forEach(function (btn) {
          btn.addEventListener("click", function () {
            var trigger = document.getElementById("ssg-search-btn");
            if (trigger) trigger.click();
          });
        });

        /* Submenu disclosures: click toggles; Esc closes and refocuses;
           outside click/focus closes all. Hover stays pure CSS. */
        var subToggles = Array.prototype.slice.call(document.querySelectorAll(".ap-sub-toggle"));
        function closeAllSubs(except) {
          subToggles.forEach(function (t) {
            if (t !== except) t.setAttribute("aria-expanded", "false");
          });
        }
        subToggles.forEach(function (t) {
          t.addEventListener("click", function () {
            var open = t.getAttribute("aria-expanded") === "true";
            closeAllSubs(t);
            t.setAttribute("aria-expanded", open ? "false" : "true");
          });
        });
        document.addEventListener("keydown", function (e) {
          if (e.key !== "Escape") return;
          var open = subToggles.filter(function (t) { return t.getAttribute("aria-expanded") === "true"; })[0];
          if (open) { open.setAttribute("aria-expanded", "false"); open.focus(); return; }
          var langMenu = document.querySelector(".ap-lang-menu");
          if (langMenu && !langMenu.hidden) {
            langMenu.hidden = true;
            var lt = document.querySelector(".ap-lang-toggle");
            lt.setAttribute("aria-expanded", "false");
            lt.focus();
            return;
          }
          var burger = document.getElementById("ap-menu-toggle");
          if (burger && burger.checked) {
            burger.checked = false;
            burger.dispatchEvent(new Event("change"));
            var burgerLabel = document.querySelector(".ap-burger");
            if (burgerLabel) burgerLabel.focus();
          }
        });
        document.addEventListener("click", function (e) {
          if (!e.target.closest(".has-sub")) closeAllSubs(null);
          var lang = document.querySelector(".ap-lang");
          var menu = document.querySelector(".ap-lang-menu");
          if (menu && !menu.hidden && lang && !lang.contains(e.target)) {
            menu.hidden = true;
            document.querySelector(".ap-lang-toggle").setAttribute("aria-expanded", "false");
          }
        });

        /* Language selector: toggle, current marking. */
        var langToggle = document.querySelector(".ap-lang-toggle");
        var langMenu = document.querySelector(".ap-lang-menu");
        if (langToggle && langMenu) {
          var currentLang = (document.documentElement.getAttribute("lang") || "en").toLowerCase();
          var short = currentLang.split("-")[0].toUpperCase();
          langToggle.querySelector(".ap-lang-current").textContent = short;
          langMenu.querySelectorAll(".ap-lang-item").forEach(function (a) {
            if ((a.getAttribute("lang") || "").toLowerCase() === currentLang) {
              a.setAttribute("aria-current", "true");
            }
          });
          langToggle.addEventListener("click", function () {
            var open = !langMenu.hidden;
            langMenu.hidden = open;
            langToggle.setAttribute("aria-expanded", open ? "false" : "true");
          });
        }

        /* Burger: reflect state for AT; focus first item on open. */
        var burger = document.getElementById("ap-menu-toggle");
        if (burger) {
          burger.setAttribute("aria-controls", "ap-primary-nav");
          var syncBurger = function () {
            burger.setAttribute("aria-expanded", burger.checked ? "true" : "false");
            if (burger.checked) {
              var first = document.querySelector(".ap-menu a");
              if (first) first.focus();
            }
          };
          burger.setAttribute("aria-expanded", "false");
          burger.addEventListener("change", syncBurger);
        }

        /* aria-current on the matching menu link. */
        var here = window.location.pathname.replace(/\/+$/, "") + "/";
        document.querySelectorAll(".ap-menu a").forEach(function (a) {
          var href = a.getAttribute("href");
          if (href === here || (href === "/" && here === "/")) {
            a.setAttribute("aria-current", "page");
          }
        });
      })();
    