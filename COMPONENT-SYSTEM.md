# Global Header/Nav Component System

## What Changed

The site now uses a **component-based system** for the header and navigation. This means:

- **One file to update**: `/components/header-nav.html`
- **Automatic propagation**: Changes appear across all main pages
- **No more copy/paste**: Update once, reflected everywhere

## How It Works

1. **Component file**: `/components/header-nav.html` contains the header/nav HTML
2. **Loader script**: `/js/load-components.js` injects the component into each page
3. **Placeholder**: Pages have `<div id="header-nav-placeholder"></div>` where the header loads

## Pages Using the Component System

✅ **Updated pages** (16 total):
- index.html (homepage)
- san-diego.html
- orange-county.html
- los-angeles.html
- about/index.html
- blog/index.html
- cash-home-offer/index.html
- contact/index.html
- downsize-guide/index.html
- faq/index.html
- fiduciaries/index.html
- legacy-playbook/index.html
- legacy-stories/index.html
- privacy-policy/index.html
- schedule-consult/index.html
- testimonials/index.html

❌ **Excluded pages** (keep their own headers):
- upcoming-sales/index.html (has simpler header)
- Individual sale pages (e.g., upcoming-sales/san-diego-may-16-17/)
- Special landing pages:
  - legacy-assurance-plan/index.html
  - thank-you/index.html
  - wholesalers/index.html
  - 404.html

## How to Update the Header/Nav

**Before**: Had to manually update 16+ HTML files

**Now**: Edit ONE file:

1. Open `/components/header-nav.html`
2. Make your changes
3. Save
4. Push to GitHub
5. Changes appear on all pages automatically

## Example: Adding a New Nav Link

Edit `/components/header-nav.html` and add your link in the desktop nav section:

```html
<div class="hidden md:flex items-center space-x-8 uppercase font-semibold" style="font-size: 13px;">
  <a href="/estate-sales/">Estate Sales</a>
  <a href="/cash-home-offer/">Cash Offers</a>
  <a href="/about/">About</a>
  <a href="/blog/">Blog</a>
  <a href="/faq/">FAQ</a>
  <a href="/new-page/">New Link</a> <!-- ADD HERE -->
</div>
```

And also in the mobile menu section:

```html
<div class="px-4 py-4 space-y-1">
  <a href="/estate-sales/">Estate Sales</a>
  <!-- ... other links ... -->
  <a href="/new-page/">New Link</a> <!-- ADD HERE -->
</div>
```

## Testing

**Staging site**: https://staging.website-252.pages.dev/

Test checklist:
- [ ] Header appears on all main pages
- [ ] Mobile menu toggles correctly
- [ ] All navigation links work
- [ ] Phone number links work
- [ ] Sticky mobile CTA appears on scroll
- [ ] No console errors

## Technical Details

- **Load method**: JavaScript `fetch()` API
- **Performance**: Component loads asynchronously, minimal impact
- **Fallback**: If JS fails, page shows without header (unlikely, but graceful)
- **SEO**: No impact, content loads on page render

## Maintenance Notes

- The component system is only for header/nav
- Footer remains inline in each page (could be componentized later if needed)
- Blog posts in `/blog/` folder also use the component system
- Estate sale pages keep their simpler header by design
