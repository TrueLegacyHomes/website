#!/usr/bin/env python3
"""
Replace all footers with component-based footer
Includes: ALL pages (main site, upcoming-sales, individual sale pages, etc.)
"""

import os
import re
from pathlib import Path

# Directories to EXCLUDE
EXCLUDE_DIRS = ['node_modules', '.git', 'scripts']
EXCLUDE_FILES = [
    'components/footer.html',
    'components/header-nav.html'
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

# Pattern to match footer blocks - handle various formats
FOOTER_PATTERNS = [
    # Full footer with bg-tlh-dark
    re.compile(r'  <footer class="bg-tlh-dark.*?</footer>', re.DOTALL),
    # Simpler footer patterns
    re.compile(r'<footer.*?</footer>', re.DOTALL),
]

REPLACEMENT = '  <!-- Footer (loaded from component) -->\n  <div id="footer-placeholder"></div>'

def replace_footer(content):
    """Try to replace footer with placeholder"""
    for pattern in FOOTER_PATTERNS:
        if pattern.search(content):
            content = pattern.sub(REPLACEMENT, content)
            return content, True
    return content, False

def fix_page(filepath):
    """Update a single page"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Check if already has footer placeholder
        if 'footer-placeholder' in content:
            print(f"⊙ Already updated: {filepath}")
            return False
        
        # Try to replace footer
        content, replaced = replace_footer(content)
        
        if replaced and content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated: {filepath}")
            return True
        elif '<footer' not in content:
            print(f"⚠ No footer found: {filepath}")
            return False
        else:
            print(f"⚠ Footer pattern not matched: {filepath}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {filepath} - {e}")
        return False

def main():
    print("=" * 60)
    print("Global Footer Component Migration")
    print("=" * 60)
    print()
    
    html_files = find_all_html_files()
    
    print(f"Found {len(html_files)} HTML files to check")
    print()
    
    updated = 0
    
    for filepath in html_files:
        result = fix_page(filepath)
        if result:
            updated += 1
    
    print()
    print("=" * 60)
    print(f"Summary: {updated} files updated")
    print("=" * 60)

if __name__ == "__main__":
    main()
