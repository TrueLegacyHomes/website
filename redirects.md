# TLH URL Redirect Map

## Redirect Options

### Option 1: Cloudflare Page Rules (Recommended)
If using Cloudflare as DNS/CDN, create Page Rules for 301 redirects.

### Option 2: Netlify _redirects
If migrating to Netlify, use this `_redirects` file (place in root):

```
# Core page redirects
/about-us /about 301
/about-us/ /about/ 301
/contact-us /contact 301
/contact-us/ /contact/ 301
/senior-care-placement /care-placement 301
/senior-care-placement/ /care-placement/ 301
/cash-offer /cash-home-offer 301
/cash-offer/ /cash-home-offer/ 301
/locations/orange-county /locations/orangecounty 301
/locations/orange-county/ /locations/orangecounty/ 301
/our-team /about 301
/our-team/ /about/ 301
/realtor-guide /fiduciaries 301
/probate-attorneys /fiduciaries 301
/join-our-list /joinourlist 301
/join-our-list/ /joinourlist/ 301

# Blog posts - redirect from root to /blog/
# These need to be generated from the list of blog posts
/10-best-estate-sale-companies-in-san-diego /blog/10-best-estate-sale-companies-in-san-diego.html 301
/10-ways-to-get-the-most-out-of-estate-sales /blog/10-ways-to-get-the-most-out-of-estate-sales.html 301
# ... (all blog posts)
```

### Option 3: GitHub Pages HTML Redirects
Create stub HTML files at old URLs with meta refresh:

```html
<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="refresh" content="0; url=/about/">
  <link rel="canonical" href="/about/">
  <script>window.location.replace("/about/");</script>
</head>
<body>
  <p>Redirecting to <a href="/about/">/about/</a></p>
</body>
</html>
```

---

## Full Redirect Map

### Core Pages (WP → Static)

| WordPress URL | Static URL | Status |
|--------------|------------|--------|
| `/` | `/` | ✅ Same |
| `/estate-sales/` | `/estate-sales/` | ✅ Same |
| `/care-placement/` | `/care-placement/` | ✅ Same |
| `/cash-home-offer/` | `/cash-home-offer/` | ✅ Same |
| `/about/` | `/about/` | ✅ Same |
| `/blog/` | `/blog/` | ✅ Same |
| `/faq/` | `/faq/` | ✅ Same |
| `/sales/` | `/upcoming-sales/` | ⚠️ Redirect needed |
| `/locations/` | `/locations/` | ✅ Same |
| `/locations/san-diego/` | `/locations/san-diego/` | ✅ Same |
| `/locations/los-angeles/` | `/locations/los-angeles/` | ✅ Same |
| `/schedule-consult/` | `/schedule-consult/` | ✅ Same |
| `/legacy-assurance-plan/` | `/legacy-assurance-plan/` | ✅ Same |
| `/pricing/` | `/pricing/` | ⚠️ Page missing? |

### Redirects Needed

| Old URL | New URL | Type |
|---------|---------|------|
| `/about-us/` | `/about/` | 301 |
| `/contact-us/` | `/contact/` | 301 |
| `/contact/` | `/contact/` | Page missing - create or redirect |
| `/senior-care-placement/` | `/care-placement/` | 301 |
| `/cash-offer/` | `/cash-home-offer/` | 301 |
| `/locations/orange-county/` | `/locations/orangecounty/` | 301 |
| `/our-team/` | `/about/` | 301 |
| `/realtor-guide/` | `/fiduciaries/` | 301 |
| `/probate-attorneys/` | `/fiduciaries/` | 301 |
| `/join-our-list/` | `/joinourlist/` | 301 |
| `/testimonials/` | `/testimonials/` | ✅ Same |
| `/sales/*` | `/upcoming-sales/*` | 301 pattern |

### Blog Posts (CRITICAL)

WordPress: `/post-slug/` (at root)
Static: `/blog/post-slug.html`

~150+ blog posts need redirects from root to `/blog/`

---

## Recommended Action Plan

1. **Use Cloudflare** for DNS + CDN
2. Set up Page Rules for core redirects
3. Use Transform Rules or Bulk Redirects for blog posts
4. Or: Create HTML stub files for each old URL (works on GitHub Pages)

---

## Generate Blog Redirects

Run this to generate all blog redirects:

```bash
cd /Users/admin/.openclaw/workspace/tlh-rebuild/blog
for f in *.html; do
  slug="${f%.html}"
  echo "/${slug} /blog/${f} 301"
  echo "/${slug}/ /blog/${f} 301"
done
```
