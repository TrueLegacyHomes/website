#!/usr/bin/env python3
"""Generate sitemap.xml for True Legacy Homes website"""

import os
from datetime import datetime
from pathlib import Path

# Base URL
BASE_URL = "https://truelegacyhomes.com"

# Priority and changefreq settings
URL_PRIORITY = {
    'index.html': ('1.0', 'weekly'),
    'estate-sales': ('0.9', 'weekly'),
    'cash-home-offer': ('0.9', 'weekly'),
    'locations': ('0.8', 'weekly'),
    'blog': ('0.7', 'daily'),
    'upcoming-sales': ('0.8', 'weekly'),
    'default': ('0.6', 'monthly')
}

def get_priority_changefreq(path):
    """Determine priority and changefreq based on path"""
    path_str = str(path)
    
    if path_str == 'index.html':
        return URL_PRIORITY['index.html']
    elif 'estate-sales' in path_str:
        return URL_PRIORITY['estate-sales']
    elif 'cash-home-offer' in path_str:
        return URL_PRIORITY['cash-home-offer']
    elif 'locations' in path_str:
        return URL_PRIORITY['locations']
    elif 'blog' in path_str:
        return URL_PRIORITY['blog']
    elif 'upcoming-sales' in path_str:
        return URL_PRIORITY['upcoming-sales']
    else:
        return URL_PRIORITY['default']

def find_html_files():
    """Find all HTML files to include in sitemap"""
    urls = []
    
    # Root HTML files (except 404)
    for html_file in Path('.').glob('*.html'):
        if html_file.name != '404.html':
            urls.append(html_file)
    
    # Directory index.html files
    for index_file in Path('.').rglob('index.html'):
        # Skip node_modules and hidden directories
        if 'node_modules' not in str(index_file) and not any(part.startswith('.') for part in index_file.parts):
            urls.append(index_file)
    
    return sorted(set(urls))

def generate_sitemap():
    """Generate sitemap.xml"""
    html_files = find_html_files()
    
    # Start XML
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # Get last modified date (use today for all)
    lastmod = datetime.now().strftime('%Y-%m-%d')
    
    for html_file in html_files:
        # Convert file path to URL
        if html_file.name == 'index.html':
            # Directory index
            if str(html_file) == 'index.html':
                url = BASE_URL + '/'
            else:
                url = BASE_URL + '/' + str(html_file.parent) + '/'
        else:
            # Root HTML file
            url = BASE_URL + '/' + html_file.stem + '/'
        
        # Clean up double slashes
        url = url.replace('//', '/').replace(':/', '://')
        
        # Get priority and changefreq
        priority, changefreq = get_priority_changefreq(html_file)
        
        # Add URL entry
        xml.append('  <url>')
        xml.append(f'    <loc>{url}</loc>')
        xml.append(f'    <lastmod>{lastmod}</lastmod>')
        xml.append(f'    <changefreq>{changefreq}</changefreq>')
        xml.append(f'    <priority>{priority}</priority>')
        xml.append('  </url>')
    
    xml.append('</urlset>')
    
    return '\n'.join(xml)

if __name__ == '__main__':
    sitemap_content = generate_sitemap()
    
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    print(f"✅ Generated sitemap.xml with {sitemap_content.count('<url>')} URLs")
