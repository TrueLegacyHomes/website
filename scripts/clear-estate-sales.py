#!/usr/bin/env python3
"""
clear-estate-sales.py
Runs every Sunday at 2pm PST via GitHub Actions.
- Removes all sale subdirectories from upcoming-sales/
- Replaces the Current Sales section in index.html with the Friday message
"""

import os
import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SALES_DIR = REPO_ROOT / "upcoming-sales"
INDEX_FILE = SALES_DIR / "index.html"

NO_SALES_SECTION = """  <!-- Current Sales -->
  <section class="py-12 bg-gray-50">
    <div class="max-w-6xl mx-auto px-4">
      <div class="text-center py-12">
        <p class="text-gray-500 text-lg mb-2">This week&#39;s sales will be posted at 9:30am Friday morning.</p>
      </div>
    </div>
  </section>"""

# 1. Remove all sale subdirectories
removed = []
for item in SALES_DIR.iterdir():
    if item.is_dir():
        shutil.rmtree(item)
        removed.append(item.name)

if removed:
    print(f"Removed directories: {', '.join(removed)}")
else:
    print("No sale directories to remove.")

# 2. Update index.html — replace Current Sales section with no-sales message
html = INDEX_FILE.read_text(encoding="utf-8")

# Match everything from <!-- Current Sales --> up to (but not including) the next <!-- comment -->
pattern = r'  <!-- Current Sales -->.*?(?=\n\n    <!-- |\n  <!-- )'
replacement = NO_SALES_SECTION

updated = re.sub(pattern, replacement, html, flags=re.DOTALL)

if updated == html:
    print("WARNING: Current Sales section not found in index.html — no changes made.")
else:
    INDEX_FILE.write_text(updated, encoding="utf-8")
    print("index.html updated with no-sales message.")
