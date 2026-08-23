/* ============================================================
   CodeHub — Main JavaScript
   Theme toggle, mobile nav, copy buttons, TOC scroll-spy.
   No dependencies. Works without a build step.
   ============================================================ */
(function () {
  "use strict";

  /* ---------- Theme toggle (persisted) ---------- */
  var root = document.documentElement;
  var saved = localStorage.getItem("codehub-theme");
  if (saved) {
    root.setAttribute("data-theme", saved);
  } else if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
    root.setAttribute("data-theme", "dark");
  }

  function setTheme(theme) {
    if (theme) {
      root.setAttribute("data-theme", theme);
      localStorage.setItem("codehub-theme", theme);
    } else {
      root.removeAttribute("data-theme");
      localStorage.removeItem("codehub-theme");
    }
  }

  var themeBtn = document.querySelector(".theme-toggle");
  if (themeBtn) {
    var sun = "☀️";
    var moon = "🌙";
    function updateIcon() {
      themeBtn.textContent = root.getAttribute("data-theme") === "dark" ? sun : moon;
      themeBtn.setAttribute(
        "aria-label",
        root.getAttribute("data-theme") === "dark" ? "Switch to light mode" : "Switch to dark mode"
      );
    }
    updateIcon();
    themeBtn.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      setTheme(next);
      updateIcon();
    });
  }

  /* ---------- Mobile nav ---------- */
  var navToggle = document.querySelector(".nav-toggle");
  var navLinks = document.querySelector(".nav-links");
  if (navToggle && navLinks) {
    navToggle.addEventListener("click", function () {
      var open = navLinks.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    navLinks.addEventListener("click", function (e) {
      if (e.target.tagName === "A") navLinks.classList.remove("open");
    });
  }

  /* ---------- Copy buttons for code blocks ---------- */
  document.querySelectorAll(".codeblock").forEach(function (block) {
    var btn = block.querySelector(".copy-btn");
    var pre = block.querySelector("pre");
    if (!btn || !pre) return;
    btn.addEventListener("click", function () {
      var text = pre.innerText;
      var done = function () {
        var old = btn.textContent;
        btn.textContent = "Copied!";
        setTimeout(function () { btn.textContent = old; }, 1400);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done).catch(done);
      } else {
        var ta = document.createElement("textarea");
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand("copy"); } catch (e) {}
        document.body.removeChild(ta);
        done();
      }
    });
  });

  /* ---------- TOC scroll-spy ---------- */
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll(".toc a"));
  if (tocLinks.length) {
    var sections = tocLinks
      .map(function (a) {
        var id = a.getAttribute("href");
        if (id && id.charAt(0) === "#") return document.querySelector(id);
        return null;
      })
      .filter(Boolean);

    function onScroll() {
      var pos = window.scrollY + 120;
      var current = sections[0];
      sections.forEach(function (sec) {
        if (sec.offsetTop <= pos) current = sec;
      });
      tocLinks.forEach(function (a) {
        a.classList.toggle("active", a.getAttribute("href") === "#" + current.id);
      });
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }
/* ---------- Level Tabs ---------- */
  document.querySelectorAll('.level-tabs').forEach(function (tabs) {
    var tabButtons = tabs.querySelectorAll('.level-tab');
    var panels = tabs.parentElement.querySelectorAll('.level-panel');
    if (!tabButtons.length || !panels.length) return;

    tabButtons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var level = btn.getAttribute('data-level');
        tabButtons.forEach(function (b) { b.classList.remove('active'); });
        btn.classList.add('active');
        panels.forEach(function (p) {
          p.classList.toggle('active', p.getAttribute('data-level') === level);
        });
      });
    });

    // Activate first by default
    if (tabButtons[0]) tabButtons[0].click();
  });

  /* ---------- Scroll reveal (IntersectionObserver) ---------- */
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var revealEls = Array.prototype.slice.call(document.querySelectorAll("[data-reveal]"));
  if (revealEls.length) {
    revealEls.forEach(function (el) {
      el.classList.add("reveal");
      var d = el.getAttribute("data-reveal-delay");
      if (d) el.classList.add("reveal-delay-" + d);
    });
    if (reduce || !("IntersectionObserver" in window)) {
      revealEls.forEach(function (el) { el.classList.add("in"); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            io.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
      revealEls.forEach(function (el) { io.observe(el); });
    }
  }

  /* ---------- Hero typewriter terminal ---------- */
  var typeTarget = document.getElementById("typeTarget");
  if (typeTarget && !reduce) {
    var snippet = [
      { t: "# Say hello to code", c: "cm" },
      { t: "def ", c: "kw" }, { t: "greet", c: "fn" }, { t: "(name):", c: "kw" },
      { t: "\n    ", c: "" }, { t: "return", c: "kw" }, { t: " ", c: "" },
      { t: '"Hello, "', c: "str" }, { t: " + name", c: "" },
      { t: "\n\n", c: "" }, { t: "print", c: "fn" }, { t: "(", c: "" },
      { t: "greet", c: "fn" }, { t: "(", c: "" }, { t: '"World"', c: "str" }, { t: "))", c: "" }
    ];
    // Flatten into chars with class
    var chars = [];
    snippet.forEach(function (part) {
      part.t.split("").forEach(function (ch) { chars.push({ ch: ch, c: part.c }); });
    });
    var currentLine = document.createElement("span");
    currentLine.className = "ht-line";
    typeTarget.appendChild(currentLine);
    var cursor = document.createElement("span");
    cursor.className = "cursor";
    var i = 0;
    function tick() {
      if (i < chars.length) {
        var ch = chars[i].ch;
        if (ch === "\n") {
          var nl = document.createElement("span");
          nl.className = "ht-line";
          typeTarget.insertBefore(nl, cursor);
          currentLine = nl;
        } else {
          var span = document.createElement("span");
          if (chars[i].c) span.className = chars[i].c;
          span.textContent = ch;
          currentLine.appendChild(span);
        }
        i++;
        typeTarget.appendChild(cursor);
        setTimeout(tick, 38 + Math.random() * 55);
      } else {
        // loop: erase and retype
        setTimeout(function () {
          typeTarget.innerHTML = "";
          currentLine = document.createElement("span");
          currentLine.className = "ht-line";
          typeTarget.appendChild(currentLine);
          i = 0;
          tick();
        }, 3200);
      }
    }
    typeTarget.appendChild(cursor);
    setTimeout(tick, 600);
  } else if (typeTarget) {
    typeTarget.innerHTML = '<span class="ht-line"><span class="kw">def </span><span class="fn">greet</span><span class="kw">(name):</span>\n    <span class="kw">return</span> <span class="str">"Hello, "</span> + name\n\n<span class="fn">print</span>(<span class="fn">greet</span>(<span class="str">"World"</span>))</span>';
  }

  /* ---------- Floating hero particles ---------- */
  var pWrap = document.getElementById("heroParticles");
  if (pWrap && !reduce) {
    var tokens = ["</>", "{}", "fn()", "=>", "10+", "#", "[]", "&&", "++", "=>", "const", "λ", "0x1F", "✓"];
    var count = 14;
    for (var p = 0; p < count; p++) {
      var s = document.createElement("span");
      s.textContent = tokens[Math.floor(Math.random() * tokens.length)];
      s.style.left = Math.random() * 100 + "%";
      s.style.animationDuration = (9 + Math.random() * 12) + "s";
      s.style.animationDelay = (Math.random() * 12) + "s";
      s.style.fontSize = (0.7 + Math.random() * 0.7) + "rem";
      pWrap.appendChild(s);
    }
  }
})();
