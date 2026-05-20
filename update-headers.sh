#!/bin/bash
# Update all main site pages to use the component-based header/nav
# Excludes: upcoming-sales/index.html and individual sale pages

# List of pages to update (relative to repo root)
PAGES=(
  "san-diego.html"
  "orange-county.html"
  "los-angeles.html"
  "about/index.html"
  "blog/index.html"
  "cash-home-offer/index.html"
  "contact/index.html"
  "downsize-guide/index.html"
  "faq/index.html"
  "fiduciaries/index.html"
  "legacy-assurance-plan/index.html"
  "legacy-playbook/index.html"
  "legacy-stories/index.html"
  "privacy-policy/index.html"
  "schedule-consult/index.html"
  "testimonials/index.html"
  "thank-you/index.html"
  "wholesalers/index.html"
  "404.html"
)

echo "Updating headers on main site pages..."
echo "Excludes: upcoming-sales and individual sale pages"
echo ""

for page in "${PAGES[@]}"; do
  if [ -f "$page" ]; then
    echo "Processing: $page"
    # This would need to be done manually or with more complex sed/awk
    # For now, just list the files that need updating
  else
    echo "SKIP (not found): $page"
  fi
done

echo ""
echo "Manual update required for each file:"
echo "1. Find the header/nav block (starts with <!-- Sticky Mobile CTA or <!-- Navigation)"
echo "2. Replace entire block with: <div id=\"header-nav-placeholder\"></div>"
echo "3. Add before </body>: <script src=\"/js/load-components.js\"></script>"
echo ""
echo "OR: Use find/replace in your editor"
