#!/usr/bin/env python3
"""
Generate comprehensive sitemap for True Legacy Homes
Includes all existing pages PLUS the missing 101 blog posts
"""

import os
from datetime import datetime
from pathlib import Path

def generate_sitemap():
    base_url = "https://truelegacyhomes.com"
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Start sitemap
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # Define page groups with their priorities
    page_groups = {
        # High priority pages
        'homepage': (['index.html'], 1.0, 'weekly'),
        'services': (['estate-sales/index.html', 'cash-home-offer/index.html'], 0.9, 'weekly'),
        'locations': (['locations/index.html', 'locations/san-diego/index.html', 
                       'locations/orangecounty/index.html', 'locations/los-angeles/index.html'], 0.8, 'weekly'),
        
        # Medium priority
        'upcoming_sales': ([], 0.8, 'weekly'),  # Will scan directory
        'renovations': ([], 0.6, 'monthly'),  # Will scan directory
        'blog': ([], 0.7, 'monthly'),  # Will scan directory - THE MISSING PIECE!
        
        # Standard pages
        'standard': (['about/index.html', 'contact/index.html', 'faq/index.html', 
                      'testimonials/index.html', 'schedule-consult/index.html',
                      'fiduciaries/index.html', 'careers/index.html'], 0.6, 'monthly'),
    }
    
    # Process static pages
    for group_name, (pages, priority, changefreq) in page_groups.items():
        if pages:  # If specific pages listed
            for page in pages:
                if os.path.exists(page):
                    url = f"{base_url}/{page.replace('index.html', '')}"
                    add_url(sitemap, url, today, changefreq, priority)
    
    # Scan and add upcoming-sales pages
    if os.path.exists('upcoming-sales'):
        for file in sorted(os.listdir('upcoming-sales')):
            if file.endswith('.html') and file != 'index.html':
                url = f"{base_url}/upcoming-sales/{file.replace('.html', '')}"
                add_url(sitemap, url, today, 'weekly', 0.8)
    
    # Scan and add renovations pages
    if os.path.exists('renovations'):
        for file in sorted(os.listdir('renovations')):
            if file.endswith('.html') and file != 'index.html':
                url = f"{base_url}/renovations/{file.replace('.html', '')}"
                add_url(sitemap, url, today, 'monthly', 0.6)
    
    # Scan and add BLOG POSTS (THE CRITICAL FIX!)
    if os.path.exists('blog'):
        blog_count = 0
        for file in sorted(os.listdir('blog')):
            if file.endswith('.html') and file != 'index.html':
                url = f"{base_url}/blog/{file.replace('.html', '')}"
                add_url(sitemap, url, today, 'monthly', 0.7)
                blog_count += 1
        print(f"✅ Added {blog_count} blog posts to sitemap")
    
    # Close sitemap
    sitemap.append('</urlset>')
    
    # Write to file
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write('\n'.join(sitemap))
    
    # Count total URLs
    url_count = sitemap.count('<url>')
    print(f"✅ Generated sitemap with {url_count} URLs")
    print(f"📁 Saved to: sitemap.xml")
    
    return url_count

def add_url(sitemap, url, lastmod, changefreq, priority):
    """Add a URL entry to the sitemap"""
    sitemap.append('  <url>')
    sitemap.append(f'    <loc>{url}</loc>')
    sitemap.append(f'    <lastmod>{lastmod}</lastmod>')
    sitemap.append(f'    <changefreq>{changefreq}</changefreq>')
    sitemap.append(f'    <priority>{priority}</priority>')
    sitemap.append('  </url>')

if __name__ == '__main__':
    print("🔧 Generating comprehensive sitemap for True Legacy Homes...")
    print("🎯 Including ALL blog posts (previously missing!)")
    print()
    count = generate_sitemap()
    print()
    print(f"🚀 Ready to commit and push to trigger Google re-crawl")
