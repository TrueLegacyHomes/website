// TLH Main JavaScript - Consolidated from inline scripts
// Optimized for performance - loads after DOM ready

(function() {
  'use strict';

  // ===== Mobile CTA Scroll Behavior =====
  const mobileCta = document.getElementById('mobile-cta');
  if (mobileCta) {
    let shown = false;
    window.addEventListener('scroll', function() {
      if (window.scrollY > 250 && !shown) {
        mobileCta.classList.remove('translate-y-full');
        shown = true;
      }
    }, { passive: true });
  }

  // ===== Mobile Menu Toggle =====
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', function() {
      mobileMenu.classList.toggle('hidden');
    });
  }

  // ===== Location-based Address Swap (Simplified) =====
  const params = new URLSearchParams(window.location.search);
  const region = params.get('region');
  const addresses = {
    sd: '3635 Ruffin Rd, Suite 100<br>San Diego, CA 92123',
    oc: '15375 Barranca Parkway, Suite A-107<br>Irvine, CA 92618',
    la: 'Coming Soon<br>Los Angeles, CA'
  };
  
  const officeAddress = document.getElementById('office-address');
  if (officeAddress && region && addresses[region]) {
    officeAddress.innerHTML = addresses[region];
  }

  // Also update phone numbers if region-specific
  const phoneNumbers = {
    sd: '(619) 450-1702',
    oc: '(949) 409-6600',
    la: '(619) 450-1702' // Default to SD for now
  };
  
  if (region && phoneNumbers[region]) {
    const phoneLinks = document.querySelectorAll('a[href^="tel:"]');
    phoneLinks.forEach(function(link) {
      const cleanPhone = phoneNumbers[region].replace(/[^0-9]/g, '');
      link.href = 'tel:' + cleanPhone;
      const textNode = link.querySelector('span, .phone-number');
      if (textNode) {
        textNode.textContent = phoneNumbers[region];
      }
    });
  }

  // ===== FAQ Accordion (if present) =====
  const faqItems = document.querySelectorAll('.faq-item');
  if (faqItems.length > 0) {
    faqItems.forEach(function(item) {
      const question = item.querySelector('.faq-question');
      const answer = item.querySelector('.faq-answer');
      
      if (question && answer) {
        question.addEventListener('click', function() {
          const isOpen = answer.classList.contains('hidden');
          
          // Close all other FAQs
          faqItems.forEach(function(otherItem) {
            otherItem.querySelector('.faq-answer').classList.add('hidden');
            const icon = otherItem.querySelector('.faq-icon');
            if (icon) icon.textContent = '+';
          });
          
          // Toggle current FAQ
          if (isOpen) {
            answer.classList.remove('hidden');
            const icon = question.querySelector('.faq-icon');
            if (icon) icon.textContent = '−';
          }
        });
      }
    });
  }

})();
