#!/usr/bin/env python3
"""
Generate Mailchimp email from estate sales data and templates.
Reads validated sales data from /tmp and creates a Mailchimp campaign draft.
"""

import json
import sys
import os
import subprocess
from datetime import datetime

# Mailchimp config - API key must be set in environment
API_KEY = os.environ.get('MAILCHIMP_API_KEY')
if not API_KEY:
    print("❌ ERROR: MAILCHIMP_API_KEY environment variable not set!")
    print("   Export it before running: export MAILCHIMP_API_KEY='your-key-here'")
    sys.exit(1)
SERVER = "us12"
AUDIENCE_ID = "eb811b621b"
BASE_URL = f"https://{SERVER}.api.mailchimp.com/3.0"

def load_template(path):
    """Load HTML template from file."""
    with open(path, 'r') as f:
        return f.read()

def load_sales_data(tmp_dir):
    """Load sales data from temp directory."""
    # Load sales JSON
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
    
    # Load validated images for each sale
    for sale in sales:
        sale_id = sale['saleId']
        validated_file = f"{tmp_dir}/sale-{sale_id}-validated.txt"
        if os.path.exists(validated_file):
            with open(validated_file, 'r') as f:
                sale['validated_images'] = [line.strip() for line in f if line.strip()]
        else:
            sale['validated_images'] = []
        
        # Add address info
        if sale_id in addresses:
            sale['street'], sale['city'], sale['zip'] = addresses[sale_id]
            sale['full_address'] = f"{sale['street']}, {sale['city']}, CA {sale['zip']}"
        else:
            sale['street'] = sale['city'] = sale['zip'] = sale['full_address'] = "Address TBD"
    
    return sales

def generate_slug(street):
    """Generate URL slug from street address."""
    return street.lower().replace(' ', '-').replace(',', '').replace('.', '')

def build_email_html(sales, email_template, card_template, date_range="TBD"):
    """Build complete email HTML from templates."""
    
    # Build individual sale cards
    cards_html = []
    
    for sale in sales:
        # Get first 6 validated images
        images = sale.get('validated_images', [])[:6]
        
        # Pad with placeholder if less than 6
        while len(images) < 6:
            images.append("placeholder")  # Will be replaced with actual placeholder URL
        
        # Build image URLs
        sale_id = sale['saleId']
        image_vars = {}
        for i, guid in enumerate(images, 1):
            if guid == "placeholder":
                image_vars[f'IMAGE_{i}'] = "https://via.placeholder.com/200x150?text=No+Image"
            else:
                image_vars[f'IMAGE_{i}'] = f"https://picturescdn.estatesales.net/{sale_id}/1-2/{guid}.jpg"
        
        # Build sale page URL
        slug = generate_slug(sale.get('street', 'tbd'))
        sale_url = f"https://www.truelegacyhomes.com/upcoming-sales/{slug}/"
        
        # Generate card HTML
        card = card_template
        card = card.replace('{{DATE_TIME}}', f"SATURDAY & SUNDAY, {date_range.upper()} • 8AM-2PM")
        card = card.replace('{{TITLE}}', f"{sale.get('city', 'TBD')} Estate Sale")
        card = card.replace('{{ADDRESS}}', sale.get('full_address', 'Address TBD'))
        card = card.replace('{{DESCRIPTION}}', sale.get('description', 'Quality furniture, collectibles, and household items.'))
        card = card.replace('{{LINK}}', sale_url)
        
        # Replace image placeholders
        for key, url in image_vars.items():
            card = card.replace('{{' + key + '}}', url)
        
        cards_html.append(card)
    
    # Build final email
    email_html = email_template
    email_html = email_html.replace('{{DATE_RANGE}}', date_range)
    email_html = email_html.replace('{{SALES_CARDS}}', '\n'.join(cards_html))
    
    return email_html

def create_mailchimp_campaign(subject, html_content):
    """Create Mailchimp campaign via API."""
    import requests
    
    # Create campaign
    create_payload = {
        "type": "regular",
        "recipients": {"list_id": AUDIENCE_ID},
        "settings": {
            "subject_line": subject,
            "from_name": "True Legacy Homes",
            "reply_to": "info@truelegacyhomes.com",
            "title": f"Estate Sales - {datetime.now().strftime('%Y-%m-%d')}"
        }
    }
    
    print("📧 Creating Mailchimp campaign...")
    response = requests.post(
        f"{BASE_URL}/campaigns",
        auth=("anystring", API_KEY),
        json=create_payload
    )
    
    if response.status_code != 200:
        print(f"❌ Failed to create campaign: {response.text}")
        return None
    
    campaign = response.json()
    campaign_id = campaign['id']
    web_id = campaign['web_id']
    print(f"✅ Campaign created: {campaign_id}")
    
    # Set content
    print("📝 Setting email content...")
    content_response = requests.put(
        f"{BASE_URL}/campaigns/{campaign_id}/content",
        auth=("anystring", API_KEY),
        json={"html": html_content}
    )
    
    if content_response.status_code != 200:
        print(f"❌ Failed to set content: {content_response.text}")
        return None
    
    print(f"✅ Email content set")
    print(f"📧 Campaign ID: {campaign_id}")
    print(f"🌐 Web ID: {web_id}")
    print(f"🔗 Preview: https://us12.campaign-archive.com/?u=d000ea6786220cdf01bdde2cd&id={web_id}")
    print(f"⚠️  Status: DRAFT (ready for Brett to review/send)")
    
    return campaign_id

def main():
    if len(sys.argv) < 2:
        print("Usage: generate-mailchimp-email.py <tmp_dir>")
        sys.exit(1)
    
    tmp_dir = sys.argv[1]
    workspace = "/Users/admin/.openclaw/workspace/tlh-rebuild"
    
    # Load templates
    print("📄 Loading email templates...")
    email_template = load_template(f"{workspace}/estate-sales-email-template.html")
    card_template = load_template(f"{workspace}/estate-sale-card-template.html")
    
    # Load sales data
    print("📊 Loading sales data...")
    sales = load_sales_data(tmp_dir)
    print(f"✅ Loaded {len(sales)} sales")
    
    # Load weekend dates from Part 1
    date_file = f"{tmp_dir}/weekend-dates.txt"
    if os.path.exists(date_file):
        with open(date_file, 'r') as f:
            lines = f.readlines()
            date_range = lines[0].strip() if lines else "TBD"
    else:
        date_range = "TBD"
    
    # Build email HTML
    print("🔨 Building email HTML...")
    email_html = build_email_html(sales, email_template, card_template, date_range)
    
    # Save to temp file for inspection
    output_file = f"{tmp_dir}/email.html"
    with open(output_file, 'w') as f:
        f.write(email_html)
    print(f"💾 Email HTML saved: {output_file}")
    
    # Create Mailchimp campaign
    subject = "This Weekend: Estate Sales"
    if len(sales) == 1:
        subject = f"This Weekend: Estate Sale in {sales[0].get('city', 'San Diego')}"
    else:
        subject = f"This Weekend: {len(sales)} Estate Sales"
    
    campaign_id = create_mailchimp_campaign(subject, email_html)
    
    if campaign_id:
        print("\n✅ MAILCHIMP EMAIL CREATED!")
    else:
        print("\n❌ Failed to create email")
        sys.exit(1)

if __name__ == "__main__":
    main()
