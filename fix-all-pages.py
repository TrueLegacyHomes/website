#!/usr/bin/env python3
"""
Comprehensive fix: Update ALL site pages to use component-based header/nav
Excludes ONLY: upcoming-sales directory, blog posts, and special minimal-header pages
"""

import os
import re
from pathlib import Path

# Directories and files to EXCLUDE
EXCLUDE_DIRS = ['upcoming-sales', 'node_modules', '.git', 'blog']
EXCLUDE_FILES = [
    'components/header-nav.html',
    'scripts/sale-page-template.html',
    'legacy-assurance-plan/index.html',  # Has different minimal header
    'thank-you/index.html',
    'wholesalers/index.html',
    '404.html',
    'admin/index.html',
    'site-analysis/index.html',
    'joinourlist/index.html',
    'refer-a-friend/index.html',
    'tos/index.html',
    'accessibility/index.html',
    'playbook-after-passing/index.html',
    'sale-example/index.html',
    'shop-sales/index.html',
    'why-local/index.html'
]

def should_process(filepath):
    """Check if this file should be processed"""
    filepath_str = str(filepath)
    
    # Skip excluded directories
    for exclude_dir in EXCLUDE_DIRS:
        if f'/{exclude_dir}/' in filepath_str or filepath_str.startswith(exclude_dir):
            return False
    
    # Skip excluded files
    for exclude_file in EXCLUDE_FILES:
        if filepath_str.endswith(exclude_file) or filepath_str == exclude_file:
            return False
    
    return True

def find_all_html_files():
    """Find all HTML files that should be updated"""
    files = []
    for root, dirs, filenames in os.walk('.'):
        # Remove excluded directories from search
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        
        for filename in filenames:
            if filename.endswith('.html'):
                filepath = Path(root) / filename
                if should_process(filepath):
                    files.append(filepath)
    
    return sorted(files)

# Pattern to match the old header/nav block
HEADER_NAV_PATTERN = re.compile(
    r'  <!-- Sticky Mobile CTA.*?</nav>',
    re.DOTALL
)

REPLACEMENT = '  <!-- Header & Navigation (loaded from component) -->\n  <div id="header-nav-placeholder"></div>'

# Remove old inline mobile menu scripts
OLD_MOBILE_SCRIPT = re.compile(
    r'\s*<script>\s*document\.getElementById\([\'"]mobile-menu-btn[\'"]\)\.addEventListener.*?</script>\s*',
    re.DOTALL
)

# Pattern to add component loader before </body>
BODY_CLOSE = '</body>'
COMPONENT_LOADER = '  <!-- Component Loader -->\n  <script src="/js/load-components.js"></script>\n</body>'

def fix_page(filepath):
    """Update a single page"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Check if it has the old header/nav structure
        if '<!-- Sticky Mobile CTA' in content or ('<nav class="bg-white shadow-sm sticky top-0 z-50">' in content):
            # Replace old header/nav with placeholder
            content = HEADER_NAV_PATTERN.sub(REPLACEMENT, content)
            
            # Remove old inline mobile menu script
            content = OLD_MOBILE_SCRIPT.sub('', content)
            
            # Add component loader if not present
            if '/js/load-components.js' not in content:
                content = content.replace(BODY_CLOSE, COMPONENT_LOADER)
            
            if content != original:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✓ Updated: {filepath}")
                return True
        
        # Check if it already has the placeholder (no update needed)
        elif 'header-nav-placeholder' in content:
            print(f"⊙ Already updated: {filepath}")
            return False
        else:
            print(f"⚠ Skipped (different structure): {filepath}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {filepath} - {e}")
        return False

def main():
    print("=" * 60)
    print("Comprehensive Header/Nav Component Migration")
    print("=" * 60)
    print()
    
    html_files = find_all_html_files()
    
    print(f"Found {len(html_files)} HTML files to check")
    print()
    
    updated = 0
    already_updated = 0
    skipped = 0
    
    for filepath in html_files:
        result = fix_page(filepath)
        if result:
            updated += 1
    
    print()
    print("=" * 60)
    print(f"Summary:")
    print(f"  - {updated} files updated")
    print(f"  - Check output above for 'Already updated' and 'Skipped' counts")
    print("=" * 60)

if __name__ == "__main__":
    main()
