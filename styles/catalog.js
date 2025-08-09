// Automatically insert hamburger navigation button and catalog popup logic
(function () {
  function ensureHamburgerMenu() {
    if (!document.getElementById("menu-toggle")) {
      const btn = document.createElement("button");
      btn.id = "menu-toggle";
      btn.innerHTML = "&#9776;";
      btn.setAttribute("aria-label", "Toggle navigation menu");
      document.body.appendChild(btn);
    }
    if (!document.getElementById("menu-overlay")) {
      const overlay = document.createElement("div");
      overlay.id = "menu-overlay";
      overlay.setAttribute("aria-label", "Menu overlay");
      document.body.appendChild(overlay);
    }
  }

  function getToc() {
    return (
      document.getElementById("toc") ||
      document.querySelector("nav#toc, nav.toc, .toc")
    );
  }

  function ensureSidebarToggle() {
    if (!document.getElementById("sidebar-toggle")) {
      const btn = document.createElement("button");
      btn.id = "sidebar-toggle";
      btn.textContent = "«";
      btn.setAttribute("aria-label", "Toggle sidebar");
      btn.style.display = window.innerWidth > 900 ? "block" : "none";

      const toc = getToc();
      if (toc) toc.appendChild(btn);

      window.addEventListener("resize", () => {
        btn.style.display = window.innerWidth > 900 ? "block" : "none";
      });

      btn.addEventListener("click", function () {
        const toc = getToc();
        if (toc) {
          toc.classList.toggle("collapsed");
          btn.textContent = toc.classList.contains("collapsed") ? "»" : "«";
          btn.setAttribute(
            "aria-expanded",
            !toc.classList.contains("collapsed")
          );
        }
      });
    }
  }

  function setupHamburgerMenu() {
    const menuToggle = document.getElementById("menu-toggle");
    const menuOverlay = document.getElementById("menu-overlay");
    const toc = getToc();
    if (!menuToggle || !menuOverlay || !toc) return;

    function openMenu() {
      toc.classList.add("nav-open");
      menuOverlay.style.display = "block";
      menuToggle.setAttribute("aria-expanded", "true");
      document.body.style.overflow = "hidden";
    }

    function closeMenu() {
      toc.classList.remove("nav-open");
      menuOverlay.style.display = "none";
      menuToggle.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
    }

    menuToggle.addEventListener("click", openMenu);
    menuOverlay.addEventListener("click", closeMenu);

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeMenu();
    });

    const navLinks = toc.querySelectorAll("a");
    navLinks.forEach((link) => {
      link.addEventListener("click", () => {
        if (window.innerWidth <= 900) {
          closeMenu();
        }
      });
    });
  }

  function handleResize() {
    const toc = getToc();
    const menuOverlay = document.getElementById("menu-overlay");
    const menuToggle = document.getElementById("menu-toggle");

    if (toc && window.innerWidth <= 900) {
      toc.classList.remove("collapsed");
    }

    if (window.innerWidth > 900) {
      if (menuOverlay) menuOverlay.style.display = "none";
      if (toc) toc.classList.remove("nav-open");
      if (menuToggle) menuToggle.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
    }
  }

  function tryInit() {
    ensureHamburgerMenu();
    ensureSidebarToggle();
    const toc = getToc();
    if (toc) {
      setupHamburgerMenu();
      window.addEventListener("resize", handleResize);
      handleResize();
      return true;
    }
    return false;
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      if (tryInit()) return;
      const observer = new MutationObserver(() => {
        if (tryInit()) observer.disconnect();
      });
      observer.observe(document.body, { childList: true, subtree: true });
    });
  } else {
    if (tryInit()) return;
    const observer = new MutationObserver(() => {
      if (tryInit()) observer.disconnect();
    });
    observer.observe(document.body, { childList: true, subtree: true });
  }
})();
