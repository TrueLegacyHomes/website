#!/usr/bin/env python3
"""
Update the main /upcoming-sales/index.html listing page with new sales.
Replaces the entire <!-- Current Sales --> section regardless of whether it
contains the "no sales" placeholder (set by clear-estate-sales.py on Sunday)
or an existing grid from a prior week.
"""

import json
import sys
import os
import re

def create_sale_card(sale_id, title, street, city, zipcode, slug, hero_image, dates, dates_short):
    """Generate HTML for a sale card."""
    return f'''        <!-- {title} -->
        <div class="bg-white rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition">
          <div class="relative">
            <img src="{hero_image}" alt="Estate Sale" class="w-full h-48 object-cover">
            <div class="absolute top-3 left-3 bg-tlh-teal text-white px-3 py-1 rounded-full text-sm font-semibold">
              {dates}
            </div>
          </div>
          <div class="p-4">
            <h3 class="text-xl font-bold mb-2">{title}</h3>
            <p class="text-gray-600 mb-4">{street}<br>{city}, CA {zipcode}</p>
            <div class="flex items-center text-sm text-gray-500 mb-4">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              8:00 AM - 2:00 PM
            </div>
            <a href="/upcoming-sales/{slug}/" class="block w-full bg-tlh-dark text-white text-center py-3 rounded-lg font-semibold hover:bg-gray-800 transition">
              View Sale &rarr;
            </a>
          </div>
        </div>'''

def main():
    if len(sys.argv) < 2:
        print("Usage: update-listing-page.py <tmp_dir>")
        sys.exit(1)

    tmp_dir = sys.argv[1]
    index_path = "/Users/admin/.openclaw/workspace/tlh-rebuild/upcoming-sales/index.html"

    # Load weekend dates
    with open(f"{tmp_dir}/weekend-dates.txt", 'r') as f:
        lines = f.readlines()
        dates_short = lines[0].strip()  # "Oct 24-25, 2026"
        dates_long = lines[1].strip()   # "Sat-Sun, Oct 24-25"

    # Load sales data
    with open(f"{tmp_dir}/sales.json", 'r') as f:
        sales = json.load(f)

    # Load addresses
    addresses = {}
    with open(f"{tmp_dir}/addresses.txt", 'r') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 4:
                sale_id, street, city, zipcode = parts
                addresses[sale_id] = (street, city, zipcode)

    # Read current index.html
    with open(index_path, 'r') as f:
        content = f.read()

    # Generate sale cards
    cards = []
    for sale in sales:
        sale_id = sale['id']

        if sale_id not in addresses:
            continue

        street, city, zipcode = addresses[sale_id]
        if street == "Address TBD":
            continue

        # Generate slug
        slug = street.lower().replace(' ', '-').replace(',', '').replace('.', '').replace("'", '')

        # Get first validated image
        validated_file = f"{tmp_dir}/sale-{sale_id}-validated.txt"
        if os.path.exists(validated_file):
            with open(validated_file, 'r') as f:
                first_guid = f.readline().strip()
                hero_image = f"https://picturescdn.estatesales.net/{sale_id}/1-2/{first_guid}.jpg"
        else:
            hero_image = "https://via.placeholder.com/400x300?text=No+Image"

        # Create title
        title = f"{city} Estate Sale"

        card = create_sale_card(sale_id, title, street, city, zipcode, slug, hero_image, dates_long, dates_short)
        cards.append(card)

    if not cards:
        print("⚠️  No sale cards generated — check addresses and sales data")
        sys.exit(1)

    # Build the new Current Sales section with the grid
    cards_html = '\n'.join(cards)
    new_section = f"""  <!-- Current Sales -->
  <section class="py-12 bg-gray-50">
    <div class="max-w-6xl mx-auto px-4">
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
{cards_html}
      </div>
    </div>
  </section>"""

    # Replace the entire <!-- Current Sales --> section.
    # This handles BOTH states:
    #   1. "No sales" placeholder (set by clear-estate-sales.py on Sunday)
    #   2. Existing grid from a prior week
    pattern = r'  <!-- Current Sales -->.*?</section>'
    updated = re.sub(pattern, new_section, content, count=1, flags=re.DOTALL)

    if updated == content:
        print("❌ ERROR: Could not find '<!-- Current Sales -->' section in index.html")
        sys.exit(1)

    # Write updated content
    with open(index_path, 'w') as f:
        f.write(updated)

    print(f"✅ Updated listing page with {len(cards)} sales")
    print(f"   Date: {dates_short}")
    print(f"   Path: {index_path}")

if __name__ == "__main__":
    main()
