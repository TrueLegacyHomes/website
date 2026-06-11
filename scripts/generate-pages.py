#!/usr/bin/env python3
"""
Generate static website pages from estate sales data.
"""

import json
import os
import sys
import urllib.parse
from pathlib import Path
from datetime import datetime, timedelta

def main():
    if len(sys.argv) < 2:
        print("Usage: generate-pages.py <tmp_dir>")
        sys.exit(1)
    
    tmp_dir = sys.argv[1]
    base_dir = "/Users/admin/.openclaw/workspace/tlh-rebuild/upcoming-sales"
    template_path = "/Users/admin/.openclaw/workspace/tlh-rebuild/estate-sale-template.html"
    
    # Read template
    with open(template_path, 'r') as f:
        template = f.read()
    
    # Read addresses
    addresses = {}
    with open(f"{tmp_dir}/addresses.txt", 'r') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 4:
                sale_id, street, city, zipcode = parts
                addresses[sale_id] = (street, city, zipcode)
    
    # Read sales
    with open(f"{tmp_dir}/sales.json", 'r') as f:
        sales = json.load(f)
    
    # Calculate next weekend dates
    today = datetime.now()
    days_until_saturday = (5 - today.weekday()) % 7
    if days_until_saturday == 0 and today.weekday() == 5:
        next_saturday = today
    else:
        next_saturday = today + timedelta(days=days_until_saturday)
    next_sunday = next_saturday + timedelta(days=1)
    
    date_short = f"{next_saturday.strftime('%b %-d')}-{next_sunday.strftime('%-d')}, {next_saturday.year}"
    date_long = f"{next_saturday.strftime('%a')}-{next_sunday.strftime('%a')}, {next_saturday.strftime('%b %-d')}-{next_sunday.strftime('%-d')}"
    
    print(f"Weekend dates: {date_short}")
    
    # Track created slugs for cleanup
    created_slugs = []
    
    # Process each sale
    for sale in sales:
        sale_id = sale['id']
        
        if sale_id not in addresses:
            print(f"⚠️  Skipping {sale_id} - no address found")
            continue
        
        street, city, zipcode = addresses[sale_id]
        
        if street == "Address TBD":
            print(f"⚠️  Sale {sale_id} has no address yet (not released)")
            continue
        
        # Generate slug from street address
        slug = street.lower()
        slug = slug.replace(' ', '-').replace(',', '').replace('.', '').replace("'", '')
        
        # Read validated images
        validated_file = f"{tmp_dir}/sale-{sale_id}-validated.txt"
        if not os.path.exists(validated_file):
            print(f"⚠️  No validated images for {sale_id}")
            continue
            
        with open(validated_file, 'r') as f:
            guids = [line.strip() for line in f if line.strip()]
        
        if len(guids) < 6:
            print(f"⚠️  Sale {sale_id} has only {len(guids)} images")
        
        # Generate image array for JavaScript
        image_urls = [f'"https://picturescdn.estatesales.net/{sale_id}/1-2/{guid}.jpg"' for guid in guids]
        image_array = '[\n      ' + ',\n      '.join(image_urls) + '\n    ]'
        
        # Build page
        full_address = f"{street}, {city}, CA {zipcode}"
        google_maps_url = f"https://maps.google.com/?q={urllib.parse.quote(full_address)}"
        
        page = template.replace('{{ADDRESS}}', street)
        page = page.replace('{{CITY_STATE_ZIP}}', f"{city}, CA {zipcode}")
        page = page.replace('{{FULL_ADDRESS}}', full_address)
        page = page.replace('{{DATES}}', date_short)
        page = page.replace('{{DATES_LONG}}', date_long)
        page = page.replace('{{HOURS}}', '8:00 AM - 2:00 PM')
        page = page.replace('{{PHOTO_COUNT}}', str(len(guids)))
        page = page.replace('{{GOOGLE_MAPS_URL}}', google_maps_url)
        page = page.replace('{{IMAGE_ARRAY}}', image_array)
        
        # Save
        os.makedirs(f"{base_dir}/{slug}", exist_ok=True)
        with open(f"{base_dir}/{slug}/index.html", 'w') as f:
            f.write(page)
        
        created_slugs.append(slug)
        print(f"✅ Created {slug} ({len(guids)} images)")
    
    # Clean up old sales - remove directories not in created_slugs
    # Write 301 redirects to _redirects before deleting so Google doesn't see bare 404s
    print(f"\n🗑️  Cleaning up old sales...")
    import shutil
    redirects_path = "/Users/admin/.openclaw/workspace/tlh-rebuild/_redirects"
    redirect_marker = "# === Auto-generated sale redirects (managed by generate-pages.py) ==="

    # Read existing _redirects, strip old auto-generated sale redirect block
    with open(redirects_path, 'r') as f:
        existing_content = f.read()
    if redirect_marker in existing_content:
        existing_content = existing_content[:existing_content.index(redirect_marker)].rstrip()

    # Build new redirect lines for stale sales
    new_redirect_lines = []
    deleted_slugs = []
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path) and item not in created_slugs:
            shutil.rmtree(item_path)
            deleted_slugs.append(item)
            new_redirect_lines.append(f"/upcoming-sales/{item} /upcoming-sales/ 301")
            new_redirect_lines.append(f"/upcoming-sales/{item}/ /upcoming-sales/ 301")
            print(f"   Deleted + redirected: {item}")

    # Append updated redirect block
    if new_redirect_lines:
        redirect_block = f"\n\n{redirect_marker}\n" + "\n".join(new_redirect_lines)
        with open(redirects_path, 'w') as f:
            f.write(existing_content + redirect_block + "\n")
        print(f"   Added {len(new_redirect_lines)} redirect rules to _redirects")
    else:
        print(f"   No old sales to clean up")
    
    # Save weekend dates for email script
    with open(f"{tmp_dir}/weekend-dates.txt", 'w') as f:
        f.write(f"{date_short}\n{date_long}")
    
    print(f"\n✅ All pages generated!")
    print(f"   Created: {len(created_slugs)} sales")
    print(f"   Cleaned up old sales")

if __name__ == "__main__":
    main()
