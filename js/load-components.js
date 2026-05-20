/**
 * TLH Component Loader
 * Loads reusable HTML components (header/nav) into pages
 */

(function() {
  // Load header/nav component
  function loadHeaderNav() {
    const placeholder = document.getElementById('header-nav-placeholder');
    if (!placeholder) return;

    fetch('/components/header-nav.html')
      .then(response => response.text())
      .then(html => {
        placeholder.outerHTML = html;
        initMobileMenu();
        initMobileCTA();
      })
      .catch(err => console.error('Failed to load header-nav:', err));
  }

  // Initialize mobile menu toggle
  function initMobileMenu() {
    const menuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (menuBtn && mobileMenu) {
      menuBtn.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
      });
    }
  }

  // Initialize mobile CTA sticky behavior
  function initMobileCTA() {
    const mobileCTA = document.getElementById('mobile-cta');
    if (!mobileCTA) return;

    let lastScroll = 0;
    window.addEventListener('scroll', () => {
      const currentScroll = window.pageYOffset;
      if (currentScroll > 300) {
        mobileCTA.classList.remove('translate-y-full');
      } else {
        mobileCTA.classList.add('translate-y-full');
      }
      lastScroll = currentScroll;
    });
  }

  // Load components when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadHeaderNav);
  } else {
    loadHeaderNav();
  }
})();
