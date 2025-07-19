// Automatically insert hamburger navigation button and catalog popup logic
(function() {
  function ensureHamburgerMenu() {
    if (!document.getElementById('menu-toggle')) {
      const btn = document.createElement('button');
      btn.id = 'menu-toggle';
      btn.innerHTML = '&#9776;'; 
      btn.style.position = 'fixed';
      btn.style.top = '16px';
      btn.style.right = '16px';
      btn.style.zIndex = '1001';
      btn.style.background = 'none';
      btn.style.border = 'none';
      btn.style.fontSize = '2em';
      btn.style.cursor = 'pointer';
      document.body.appendChild(btn);
    }
    if (!document.getElementById('menu-overlay')) {
      const overlay = document.createElement('div');
      overlay.id = 'menu-overlay';
      overlay.style.display = 'none';
      overlay.style.position = 'fixed';
      overlay.style.top = '0';
      overlay.style.left = '0';
      overlay.style.width = '100vw';
      overlay.style.height = '100vh';
      overlay.style.background = 'rgba(0,0,0,0.3)';
      overlay.style.zIndex = '1000';
      document.body.appendChild(overlay);
    }
  }

  function getToc() {
    return document.getElementById('toc') || document.querySelector('nav#toc, nav.toc, .toc');
  }

  function ensureSidebarToggle() {
    if (!document.getElementById('sidebar-toggle')) {
      const btn = document.createElement('button');
      btn.id = 'sidebar-toggle';
      btn.textContent = '«';
      btn.style.display = window.innerWidth > 900 ? 'block' : 'none';
      btn.style.position = 'absolute';
      btn.style.top = '10px';
      btn.style.right = '10px';
      btn.style.zIndex = '20';
      btn.style.background = '#eee';
      btn.style.border = 'none';
      btn.style.borderRadius = '4px';
      btn.style.cursor = 'pointer';
      btn.style.width = '24px';
      btn.style.height = '24px';
      btn.style.fontSize = '1.2em';
      const toc = getToc();
      if (toc) toc.appendChild(btn);
      window.addEventListener('resize', () => {
        btn.style.display = window.innerWidth > 900 ? 'block' : 'none';
      });
      btn.addEventListener('click', function() {
        const toc = getToc();
        if (toc) {
          toc.classList.toggle('collapsed');
          btn.textContent = toc.classList.contains('collapsed') ? '»' : '«';
        }
      });
    }
  }

  function setupHamburgerMenu() {
    const menuToggle = document.getElementById('menu-toggle');
    const menuOverlay = document.getElementById('menu-overlay');
    const toc = getToc();
    if (!menuToggle || !menuOverlay || !toc) return;

    function openMenu() {
      toc.classList.add('nav-open');
      menuOverlay.style.display = 'block';
    }
    function closeMenu() {
      toc.classList.remove('nav-open');
      menuOverlay.style.display = 'none';
    }
    menuToggle.addEventListener('click', openMenu);
    menuOverlay.addEventListener('click', closeMenu);
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') closeMenu();
    });
  }

  function handleResize() {
    const toc = getToc();
    const menuOverlay = document.getElementById('menu-overlay');
    if (toc && window.innerWidth <= 900) {
      toc.classList.remove('collapsed');
    }
    if (window.innerWidth > 900) {
      if (menuOverlay) menuOverlay.style.display = 'none';
      if (toc) toc.classList.remove('nav-open');
    }
  }

  function tryInit() {
    ensureHamburgerMenu();
    ensureSidebarToggle();
    const toc = getToc();
    if (toc) {
      setupHamburgerMenu();
      window.addEventListener('resize', handleResize);
      handleResize();
      return true;
    }
    return false;
  }

  document.addEventListener('DOMContentLoaded', function() {
    if (tryInit()) return;
    const observer = new MutationObserver(() => {
      if (tryInit()) observer.disconnect();
    });
    observer.observe(document.body, { childList: true, subtree: true });
  });
})(); 