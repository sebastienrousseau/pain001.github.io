
      /* Pre-paint theme init: honour saved choice, else OS preference. */
      (function () {
        try {
          var t = localStorage.getItem("theme");
          if (t === "dark" || t === "light") {
            document.documentElement.setAttribute("data-theme", t);
          }
        } catch (e) {}
      })();
    