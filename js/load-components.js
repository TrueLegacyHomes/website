/**
 * TLH Component Loader
 * Loads reusable HTML components (header/nav and footer) into pages
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
        initEstateSaleBanner();
      })
      .catch(err => console.error('Failed to load header-nav:', err));
  }

  // Load footer component
  function loadFooter() {
    const placeholder = document.getElementById('footer-placeholder');
    if (!placeholder) return;

    fetch('/components/footer.html')
      .then(response => response.text())
      .then(html => {
        placeholder.outerHTML = html;
      })
      .catch(err => console.error('Failed to load footer:', err));
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

  // Estate Sale Weekend Banner - Show Fridays 9:30am PST through Sundays 2pm PST
  function initEstateSaleBanner() {
    function shouldShowBanner() {
      const now = new Date();
      
      // Convert to PST (UTC-8) / PDT (UTC-7)
      const pstTime = new Date(now.toLocaleString('en-US', { timeZone: 'America/Los_Angeles' }));
      const day = pstTime.getDay(); // 0=Sun, 5=Fri
      const hours = pstTime.getHours();
      const minutes = pstTime.getMinutes();
      
      // Friday from 9:30am onwards
      if (day === 5 && (hours > 9 || (hours === 9 && minutes >= 30))) {
        return true;
      }
      
      // All day Saturday
      if (day === 6) {
        return true;
      }
      
      // Sunday until 2pm (14:00)
      if (day === 0 && hours < 14) {
        return true;
      }
      
      return false;
    }
    
    function updateBanner() {
      const banner = document.getElementById('estate-sale-banner');
      if (banner) {
        if (shouldShowBanner()) {
          banner.classList.remove('hidden');
        } else {
          banner.classList.add('hidden');
        }
      }
    }
    
    // Run on page load
    updateBanner();
    
    // Check every 5 minutes in case user keeps page open
    setInterval(updateBanner, 5 * 60 * 1000);
  }

  // Load components when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      loadHeaderNav();
      loadFooter();
    });
  } else {
    loadHeaderNav();
    loadFooter();
  }
})();
