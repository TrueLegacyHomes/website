#!/bin/bash

# Generate sitemap with all pages including blog posts
cat > sitemap.xml << 'SITEMAP_START'
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
SITEMAP_START

# Main pages (existing entries)
for page in index.html about/*.html careers/*.html cash-home-offer/*.html contact/*.html downsize-guide/*.html estate-sales/*.html faq/*.html fiduciaries/*.html locations/*.html locations/*/*.html renovations/*.html renovations/*/*.html schedule-consult/*.html testimonials/*.html upcoming-sales/*.html upcoming-sales/*/*.html; do
  if [ -f "$page" ]; then
    # Convert file path to URL
    url=$(echo "$page" | sed 's|index\.html$||' | sed 's|\.html$|/|' | sed 's|^|https://truelegacyhomes.com/|')
    echo "  <url>" >> sitemap.xml
    echo "    <loc>$url</loc>" >> sitemap.xml
    echo "    <lastmod>$(date +%Y-%m-%d)</lastmod>" >> sitemap.xml
    echo "    <changefreq>weekly</changefreq>" >> sitemap.xml
    echo "    <priority>0.8</priority>" >> sitemap.xml
    echo "  </url>" >> sitemap.xml
  fi
done

# Blog posts (THE MISSING PIECE!)
for post in blog/*.html; do
  if [ -f "$post" ] && [ "$(basename "$post")" != "index.html" ]; then
    url="https://truelegacyhomes.com/${post%.html}"
    echo "  <url>" >> sitemap.xml
    echo "    <loc>$url</loc>" >> sitemap.xml
    echo "    <lastmod>$(date +%Y-%m-%d)</lastmod>" >> sitemap.xml
    echo "    <changefreq>monthly</changefreq>" >> sitemap.xml
    echo "    <priority>0.7</priority>" >> sitemap.xml
    echo "  </url>" >> sitemap.xml
  fi
done

echo "</urlset>" >> sitemap.xml
