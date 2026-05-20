#!/usr/bin/env python3
"""
Update all main site pages to use component-based header/nav
Excludes: upcoming-sales/ directory and individual sale page directories
"""

import os
import re
from pathlib import Path

# Pages to update (relative paths from repo root)
PAGES_TO_UPDATE = [
    "san-diego.html",
    "orange-county.html",
    "los-angeles.html",
    "about/index.html",
    "blog/index.html",
    "cash-home-offer/index.html",
    "contact/index.html",
    "downsize-guide/index.html",
    "faq/index.html",
    "fiduciaries/index.html",
    "legacy-assurance-plan/index.html",
    "legacy-playbook/index.html",
    "legacy-stories/index.html",
    "privacy-policy/index.html",
    "schedule-consult/index.html",
    "testimonials/index.html",
    "thank-you/index.html",
    "wholesalers/index.html",
    "404.html"
]

# The header/nav block pattern to find and replace
# This matches from "<!-- Sticky Mobile CTA" to "</nav>"
HEADER_NAV_PATTERN = re.compile(
    r'  <!-- Sticky Mobile CTA.*?</nav>',
    re.DOTALL
)

REPLACEMENT = '  <!-- Header & Navigation (loaded from component) -->\n  <div id="header-nav-placeholder"></div>'

# Pattern to find the main.js script tag
MAIN_JS_PATTERN = re.compile(
    r'  <!-- Consolidated JavaScript \(Optimized for Performance\) -->\n  <script src="/js/main\.js" defer></script>'
)

SCRIPT_REPLACEMENT = '''  <!-- Component Loader -->
  <script src="/js/load-components.js"></script>
  
  <!-- Consolidated JavaScript (Optimized for Performance) -->
  <script src="/js/main.js" defer></script>'''

def update_page(filepath):
    """Update a single page file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace header/nav block
        content = HEADER_NAV_PATTERN.sub(REPLACEMENT, content)
        
        # Add component loader script
        content = MAIN_JS_PATTERN.sub(SCRIPT_REPLACEMENT, content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated: {filepath}")
            return True
        else:
            print(f"⚠ No changes: {filepath}")
            return False
            
    except Exception as e:
        print(f"✗ Error updating {filepath}: {e}")
        return False

def main():
    print("TLH Header/Nav Component Migration")
    print("=" * 50)
    print()
    
    updated = 0
    skipped = 0
    errors = 0
    
    for page_path in PAGES_TO_UPDATE:
        filepath = Path(page_path)
        
        if not filepath.exists():
            print(f"⚠ File not found: {page_path}")
            skipped += 1
            continue
        
        if update_page(filepath):
            updated += 1
        else:
            skipped += 1
    
    print()
    print("=" * 50)
    print(f"Summary: {updated} updated, {skipped} skipped, {errors} errors")
    print()
    print("Next steps:")
    print("1. Test the homepage to verify component loading works")
    print("2. Commit changes to staging branch")
    print("3. Deploy to staging site for full testing")

if __name__ == "__main__":
    main()
