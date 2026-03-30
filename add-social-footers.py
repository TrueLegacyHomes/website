#!/usr/bin/env python3
import os
import re

FOOTER_HTML = '''  <!-- Footer -->
  <footer class="bg-tlh-dark text-white py-8 mt-12">
    <div class="max-w-6xl mx-auto px-4">
      <div class="flex flex-col items-center gap-4">
        <div class="flex items-center gap-4">
          <img src="/images/tlhLOGO.webp" alt="True Legacy Homes" class="h-10 brightness-200">
        </div>
        <div class="flex gap-6 text-sm">
          <a href="/" class="hover:text-tlh-teal">Home</a>
          <a href="/upcoming-sales/" class="hover:text-tlh-teal">All Sales</a>
          <a href="/estate-sales/" class="hover:text-tlh-teal">Hire Us</a>
          <a href="/contact/" class="hover:text-tlh-teal">Contact</a>
        </div>
        <div class="flex gap-4 mt-2">
          <a href="https://facebook.com/truelegacyhomes" target="_blank" rel="noopener" aria-label="Facebook" class="w-10 h-10 bg-gray-700 hover:bg-tlh-teal rounded-full flex items-center justify-center transition">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
          </a>
          <a href="https://instagram.com/truelegacyhomes" target="_blank" rel="noopener" aria-label="Instagram" class="w-10 h-10 bg-gray-700 hover:bg-tlh-teal rounded-full flex items-center justify-center transition">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
          </a>
        </div>
        <div class="text-center text-sm text-gray-400 mt-4">
          © 2026 True Legacy Homes. All rights reserved.
        </div>
      </div>
    </div>
  </footer>
'''

os.chdir('/Users/admin/.openclaw/workspace/tlh-rebuild/upcoming-sales')

for entry in os.listdir('.'):
    if os.path.isdir(entry):
        html_file = os.path.join(entry, 'index.html')
        if os.path.isfile(html_file):
            with open(html_file, 'r') as f:
                content = f.read()
            
            # Skip if footer already exists
            if '<!-- Footer -->' in content:
                print(f"Footer already exists in: {html_file}")
                continue
            
            # Insert footer before closing </main>
            content = content.replace('  </main>', FOOTER_HTML + '\n  </main>')
            
            with open(html_file, 'w') as f:
                f.write(content)
            
            print(f"Added footer to: {html_file}")

print("\nDone!")
