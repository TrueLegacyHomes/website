#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Find all sale page index.html files
sales_dir = Path('/Users/admin/.openclaw/workspace/tlh-rebuild/upcoming-sales')
sale_pages = list(sales_dir.glob('*/index.html'))

for page_path in sale_pages:
    with open(page_path, 'r') as f:
        content = f.read()
    
    # Check if already using Tailwind CDN (skip old template files)
    if 'tailwindcss.com' not in content:
        # Extract key parts
        # 1. Extract "About This Sale" section
        about_match = re.search(
            r'(<div class="bg-white rounded-xl p-6 shadow-sm mb-6">.*?<h2 class="text-2xl font-bold mb-4">About This Sale</h2>.*?</div>)\s*</div>',
            content,
            re.DOTALL
        )
        
        # 2. Extract Photos section (everything in md:col-span-2)
        photos_match = re.search(
            r'<div class="md:col-span-2">\s*(<div class="bg-white rounded-xl p-6 shadow-sm">.*?<h2 class="text-2xl font-bold mb-4">Photos.*?</div>\s*</div>)\s*</div>',
            content,
            re.DOTALL
        )
        
        # 3. Extract Sale Details sidebar (md:col-span-1)
        sidebar_match = re.search(
            r'(<div class="md:col-span-1">.*?</div>\s*</div>)\s*</div>',
            content,
            re.DOTALL
        )
        
        if about_match and photos_match and sidebar_match:
            about_section = about_match.group(1)
            photos_section = photos_match.group(1)
            sidebar_section = sidebar_match.group(1)
            
            # Find where the grid starts
            grid_start = content.find('<div class="grid md:grid-cols-3 gap-')
            if grid_start == -1:
                continue
            
            # Find the container div before the grid
            container_start = content.rfind('<div class="max-w-6xl mx-auto px-4 py-8">', 0, grid_start)
            if container_start == -1:
                continue
            
            # Find the end of the entire grid structure
            grid_end = content.find('</div>\n  </div>\n\n  <div class="max-w-6xl mx-auto px-4 pb-8">', grid_start)
            if grid_end == -1:
                continue
            grid_end += len('</div>\n  </div>')
            
            # Build the new structure
            new_structure = f'''  <div class="max-w-6xl mx-auto px-4 py-8">
    {about_section}

    <div class="grid md:grid-cols-3 gap-6">
      <!-- Photos Section (2/3 width on desktop) -->
      <div class="md:col-span-2">
        {photos_section}
      </div>

      <!-- Sale Details Sidebar (1/3 width on desktop) -->
      {sidebar_section}
    </div>
  </div>'''
            
            # Replace the old structure
            new_content = content[:container_start] + new_structure + content[grid_end:]
            
            # Write back
            with open(page_path, 'w') as f:
                f.write(new_content)
            
            print(f"✅ Fixed: {page_path.name}")
        else:
            print(f"⚠️  Skipped (couldn't parse): {page_path.name}")

print("\n✅ Layout update complete!")
