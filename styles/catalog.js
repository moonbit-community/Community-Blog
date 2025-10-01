// Automatically insert hamburger navigation button and catalog popup logic
(function () {
  function ensureHamburgerMenu() {
    let menuToggle = document.getElementById("menu-toggle");

    if (!menuToggle) {
      const btn = document.createElement("button");
      btn.id = "menu-toggle";
      btn.textContent = "☰";
      btn.setAttribute("aria-label", "Toggle navigation menu");

      const header = document.querySelector("header");
      if (header) {
        header.appendChild(btn);
      } else {
        console.log(
          "No header found, menu-toggle will be floating in top-right corner"
        );
        document.body.appendChild(btn);
      }
      menuToggle = btn;
    } else {
      const header = document.querySelector("header");
      const currentParent = menuToggle.parentNode;

      if (header && currentParent !== header) {
        header.appendChild(menuToggle);
      }
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

  function setupHamburgerMenu() {
    const menuToggle = document.getElementById("menu-toggle");
    const menuOverlay = document.getElementById("menu-overlay");
    const toc = getToc();
    if (!menuToggle || !toc) return;

    function openMenu() {
      if (window.innerWidth <= 900) {
        toc.classList.add("nav-open");
        if (menuOverlay) {
          menuOverlay.style.display = "block";
        }
        document.body.style.overflow = "hidden";
      } else {
        toc.classList.toggle("collapsed");
        menuToggle.textContent = toc.classList.contains("collapsed")
          ? "»"
          : "☰";
      }
      menuToggle.setAttribute("aria-expanded", "true");
    }

    function closeMenu() {
      toc.classList.remove("nav-open");
      if (menuOverlay) {
        menuOverlay.style.display = "none";
      }
      menuToggle.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
    }

    menuToggle.addEventListener("click", openMenu);

    if (menuOverlay) {
      menuOverlay.addEventListener("click", closeMenu);
    }

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

    window.addEventListener("resize", () => {
      if (window.innerWidth > 900) {
        closeMenu();
        menuToggle.textContent = toc.classList.contains("collapsed")
          ? "»"
          : "☰";
      } else {
        menuToggle.textContent = "☰";
        toc.classList.remove("collapsed");
      }
    });
  }

  function handleResize() {
    const toc = getToc();
    const menuOverlay = document.getElementById("menu-overlay");
    const menuToggle = document.getElementById("menu-toggle");

    if (window.innerWidth > 900) {
      if (menuOverlay) menuOverlay.style.display = "none";
      if (toc) toc.classList.remove("nav-open");
      if (menuToggle) menuToggle.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
      if (menuToggle && toc) {
        menuToggle.textContent = toc.classList.contains("collapsed")
          ? "»"
          : "☰";
      }
    } else {
      if (toc) toc.classList.remove("collapsed");
      if (menuToggle) menuToggle.textContent = "☰";
    }
  }

  function tryInit() {
    ensureHamburgerMenu();

    const toc = getToc();
    const header = document.querySelector("header");

    if (toc) {
      const menuToggle = document.getElementById("menu-toggle");
      if (menuToggle && header && menuToggle.parentNode !== header) {
        header.appendChild(menuToggle);
      }

      setupHamburgerMenu();

      if (!window.catalogResizeHandlerAdded) {
        window.addEventListener("resize", handleResize);
        window.catalogResizeHandlerAdded = true;
      }

      handleResize();
      return true;
    }
    return false;
  }

  function initWithObserver() {
    if (tryInit()) return;

    const observer = new MutationObserver((mutations) => {
      let shouldReinit = false;

      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            if (
              node.matches &&
              (node.matches("header") || node.matches("nav#toc, nav.toc, .toc"))
            ) {
              shouldReinit = true;
            } else if (
              node.querySelector &&
              (node.querySelector("header") ||
                node.querySelector("nav#toc, nav.toc, .toc"))
            ) {
              shouldReinit = true;
            }
          }
        });
      });

      if (shouldReinit && tryInit()) {
        observer.disconnect();
      }
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
    });

    setTimeout(() => {
      if (tryInit()) {
        observer.disconnect();
      }
    }, 1000);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initWithObserver);
  } else {
    initWithObserver();
  }
})();
