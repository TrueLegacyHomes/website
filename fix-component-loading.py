#!/usr/bin/env python3
"""
Fix component loading issues:
1. Remove old inline mobile menu scripts
2. Add load-components.js script before </body>
"""

import re
from pathlib import Path

PAGES_TO_FIX = [
    "index.html",
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
    "legacy-playbook/index.html",
    "legacy-stories/index.html",
    "privacy-policy/index.html",
    "schedule-consult/index.html",
    "testimonials/index.html"
]

# Remove these old inline scripts that reference elements before they exist
OLD_MOBILE_SCRIPT = re.compile(
    r'\s*<script>\s*document\.getElementById\([\'"]mobile-menu-btn[\'"]\)\.addEventListener.*?</script>\s*',
    re.DOTALL
)

# Pattern to find </body>
BODY_CLOSE = '</body>'

# Script to insert before </body>
COMPONENT_LOADER = '  <!-- Component Loader -->\n  <script src="/js/load-components.js"></script>\n</body>'

def fix_page(filepath):
    """Fix a single page"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Remove old mobile menu script
        content = OLD_MOBILE_SCRIPT.sub('', content)
        
        # Add component loader if not already present
        if '/js/load-components.js' not in content:
            content = content.replace(BODY_CLOSE, COMPONENT_LOADER)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed: {filepath}")
            return True
        else:
            print(f"⚠ No changes needed: {filepath}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {filepath} - {e}")
        return False

def main():
    print("Fixing Component Loading Issues")
    print("=" * 50)
    
    fixed = 0
    for page in PAGES_TO_FIX:
        path = Path(page)
        if path.exists():
            if fix_page(path):
                fixed += 1
        else:
            print(f"⚠ Not found: {page}")
    
    print("=" * 50)
    print(f"Fixed {fixed} pages")

if __name__ == "__main__":
    main()
