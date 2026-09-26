/*
 * SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
 * SPDX-License-Identifier: Apache-2.0 OR MIT
 */
/* Homepage behaviour: recorded-run tabs, scroll reveals, the pipeline
   gallery, copy buttons, and dated content. Loaded only by the homepage
   layout, so the other 667 pages (the /try/ demo above all, which has a
   50 KB script budget) do not carry it. */
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
    var root = document.documentElement;
    /* Recorded-run tabs (WAI-ARIA tabs pattern). Without this script
       every panel is shown and the tab strip is hidden by CSS. Arrow
       keys, Home and End move between tabs; activation follows focus. */
    document.querySelectorAll("[data-tabs]").forEach(function (group) {
      var tabs = Array.prototype.slice.call(group.querySelectorAll('[role="tab"]'));
      function select(tab, focus) {
        tabs.forEach(function (t) {
          var on = t === tab;
          t.setAttribute("aria-selected", String(on));
          t.tabIndex = on ? 0 : -1;
          var panel = document.getElementById(t.getAttribute("aria-controls"));
          if (panel) panel.hidden = !on;
        });
        if (focus) tab.focus();
      }
      tabs.forEach(function (tab, i) {
        tab.addEventListener("click", function () { select(tab, false); });
        tab.addEventListener("keydown", function (event) {
          var next = null;
          if (event.key === "ArrowRight") next = tabs[(i + 1) % tabs.length];
          else if (event.key === "ArrowLeft") next = tabs[(i - 1 + tabs.length) % tabs.length];
          else if (event.key === "Home") next = tabs[0];
          else if (event.key === "End") next = tabs[tabs.length - 1];
          if (next) { event.preventDefault(); select(next, true); }
        });
      });
    });

    var hasIO = "IntersectionObserver" in window;

    /* Scroll reveals (transform only; see prism.css). Everything is
       marked visible at once when motion is off or unsupported. */
    var revealables = document.querySelectorAll("[data-reveal], [data-settle]");
    if (!root.classList.contains("js-motion") || !hasIO) {
      revealables.forEach(function (el) { el.classList.add("is-visible"); });
    } else {
      var revealer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            revealer.unobserve(entry.target);
          }
        });
      }, { rootMargin: "0px 0px -10% 0px" });
      revealables.forEach(function (el) { revealer.observe(el); });
    }

    /* Gallery: native scrolling; the buttons scroll it and the dots
       follow whichever slide is in view. */
    document.querySelectorAll("[data-gallery]").forEach(function (gallery) {
      var track = gallery.querySelector(".gallery-track");
      var slides = Array.prototype.slice.call(track.children);
      var dots = Array.prototype.slice.call(gallery.querySelectorAll("[data-gallery-to]"));
      var current = 0;
      function go(i) {
        current = Math.max(0, Math.min(slides.length - 1, i));
        var rtl = getComputedStyle(track).direction === "rtl";
        var slide = slides[current];
        var left = rtl ? slide.offsetLeft - (track.clientWidth - slide.offsetWidth) : slide.offsetLeft - track.offsetLeft;
        track.scrollTo({ left: left, behavior: root.classList.contains("js-motion") ? "smooth" : "auto" });
      }
      function mark(i) {
        current = i;
        dots.forEach(function (d, k) {
          if (k === i) d.setAttribute("aria-current", "true"); else d.removeAttribute("aria-current");
        });
      }
      dots.forEach(function (d) {
        d.addEventListener("click", function () { go(Number(d.getAttribute("data-gallery-to"))); });
      });
      var prev = gallery.querySelector("[data-gallery-prev]");
      var next = gallery.querySelector("[data-gallery-next]");
      if (prev) prev.addEventListener("click", function () { go(current - 1); });
      if (next) next.addEventListener("click", function () { go(current + 1); });
      if (hasIO) {
        var seen = new IntersectionObserver(function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) mark(slides.indexOf(entry.target));
          });
        }, { root: track, threshold: 0.6 });
        slides.forEach(function (sl) { seen.observe(sl); });
      }
    });

    /* Copy buttons: the command's text, a visible "Copied" state, and a
       polite announcement for screen readers. */
    document.querySelectorAll("[data-copy]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var src = document.getElementById(btn.getAttribute("data-copy"));
        var status = btn.closest("[data-copy-group]") && btn.closest("[data-copy-group]").querySelector("[data-copy-status]");
        if (!src || !navigator.clipboard) return;
        var label = btn.textContent;
        navigator.clipboard.writeText(src.textContent).then(function () {
          btn.setAttribute("data-copied", "");
          btn.textContent = btn.getAttribute("data-label-copied") || "Copied";
          if (status) status.textContent = btn.textContent;
          setTimeout(function () {
            btn.removeAttribute("data-copied");
            btn.textContent = label;
            if (status) status.textContent = "";
          }, 2000);
        });
      });
    });

    /* Dated content re-checked against the visitor's clock, so a stale
       build never shows an expired ribbon or a past date as "Next". The
       build does the same from its own date (postbuild_fix.py). */
    var today = new Date().toISOString().slice(0, 10);
    document.querySelectorAll("[data-expires]").forEach(function (el) {
      if (el.getAttribute("data-expires") < today) el.remove();
    });
    document.querySelectorAll("[data-timeline]").forEach(function (list) {
      var foundNext = false;
      list.querySelectorAll(".milestone").forEach(function (item) {
        var t = item.querySelector("time[datetime]");
        var date = t ? t.getAttribute("datetime") : "9999-12-31";
        var past = date < today;
        item.classList.toggle("is-past", past);
        var isNext = !past && !foundNext;
        if (isNext) foundNext = true;
        item.classList.toggle("is-next", isNext);
        var flag = item.querySelector(".milestone-flag");
        if (flag) flag.hidden = !isNext;
      });
    });

  });
})();
