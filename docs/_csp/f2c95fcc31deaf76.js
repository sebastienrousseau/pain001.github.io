
      (function () {
        var themeToggle = document.getElementById("themeToggle");
        var themeIcon = document.getElementById("themeIcon");
        var themeLabel = document.getElementById("themeLabel");

        function current() {
          var explicit = document.documentElement.getAttribute("data-theme");
          if (explicit) return explicit;
          return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
        }
        function paint(theme) {
          var dark = theme === "dark";
          themeIcon.textContent = dark ? "◑" : "◐";
          themeLabel.textContent = dark ? "Light" : "Dark";
          themeToggle.setAttribute("aria-pressed", dark ? "true" : "false");
          themeToggle.setAttribute("aria-label", dark ? "Switch to light theme" : "Switch to dark theme");
        }
        function setTheme(theme) {
          document.documentElement.setAttribute("data-theme", theme);
          try { localStorage.setItem("theme", theme); } catch (e) {}
          paint(theme);
        }
        paint(current());
        themeToggle.addEventListener("click", function () {
          setTheme(current() === "dark" ? "light" : "dark");
        });

        /* aria-current on the live nav item. */
        var here = window.location.pathname.replace(/\/+$/, "") + "/";
        document.querySelectorAll(".nav-links a").forEach(function (a) {
          if (a.getAttribute("href") === here) a.setAttribute("aria-current", "page");
        });

        /* Back to top. */
        var toTop = document.getElementById("toTop");
        function onScroll() { toTop.hidden = window.scrollY < 900; }
        window.addEventListener("scroll", onScroll, { passive: true });
        onScroll();
        toTop.addEventListener("click", function () {
          window.scrollTo({ top: 0, behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
        });
      })();
    