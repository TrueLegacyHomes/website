#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Template with better layout (icons, styled buttons, etc.)
const betterTemplate = (sale) => `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Estate Sale: ${sale.address}, ${sale.city}</title>
  <meta name="description" content="Estate sale at ${sale.address}, ${sale.city}, CA ${sale.zip}. May 16-17, 2026, 8:00 AM - 2:00 PM.">
  <link rel="icon" href="/images/favicon.png">
  <link rel="stylesheet" href="/css/tailwind.min.css">
</head>
<body class="bg-gray-50">
  <header class="bg-tlh-dark text-white py-4">
    <div class="max-w-6xl mx-auto px-4 flex justify-between items-center">
      <a href="/"><img src="/images/clientLOGO.png" alt="True Legacy Homes" class="h-12 brightness-200"></a>
      <a href="/upcoming-sales/" class="text-sm bg-white/10 px-4 py-2 rounded-lg hover:bg-white/20">← All Sales</a>
    </div>
  </header>

  <div class="max-w-6xl mx-auto px-4 py-8">
    <div class="flex flex-col md:grid md:grid-cols-3 gap-6">
      <!-- Photos Section (2/3 width on desktop) -->
      <div class="md:col-span-2 space-y-6 order-2 md:order-1">
        <div class="bg-white rounded-xl p-6 shadow-sm">
          <h1 class="text-3xl font-bold mb-2">${sale.address}</h1>
          <p class="text-xl text-gray-600 mb-4">${sale.city}, CA ${sale.zip}</p>
          <span class="inline-block bg-red-600 text-white px-3 py-1 rounded-full text-sm font-semibold">May 16-17, 2026</span>
        </div>

        <div class="bg-white rounded-xl p-6 shadow-sm">
          <h2 class="text-2xl font-bold mb-4">Photos <span class="text-gray-400 text-lg font-normal">(${sale.imageCount})</span></h2>
          <div id="gallery" class="grid grid-cols-1 md:grid-cols-5 gap-2"></div>
        </div>
      </div>

      <!-- Sale Details Sidebar (1/3 width on desktop) -->
      <div class="md:col-span-1 order-1 md:order-2">
        <div class="bg-white rounded-xl p-6 shadow-sm sticky top-4">
          <h3 class="text-xl font-bold mb-4">Sale Details</h3>
          <div class="space-y-4 text-sm">
            <div class="flex items-start gap-3">
              <div class="w-10 h-10 bg-tlh-teal/10 rounded-lg flex items-center justify-center flex-shrink-0">
                <svg class="w-5 h-5 text-tlh-teal" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
              </div>
              <div><p class="font-semibold">Dates</p><p class="text-gray-600">Sat-Sun, May 16-17</p></div>
            </div>
            <div class="flex items-start gap-3">
              <div class="w-10 h-10 bg-tlh-teal/10 rounded-lg flex items-center justify-center flex-shrink-0">
                <svg class="w-5 h-5 text-tlh-teal" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              </div>
              <div><p class="font-semibold">Hours</p><p class="text-gray-600">8:00 AM - 2:00 PM</p></div>
            </div>
            <div class="flex items-start gap-3">
              <div class="w-10 h-10 bg-tlh-teal/10 rounded-lg flex items-center justify-center flex-shrink-0">
                <svg class="w-5 h-5 text-tlh-teal" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
              </div>
              <div><p class="font-semibold">Address</p><p class="text-gray-600">${sale.address}<br>${sale.city}, CA ${sale.zip}</p></div>
            </div>
            <a href="https://maps.google.com/?q=${encodeURIComponent(sale.address + ', ' + sale.city + ', CA ' + sale.zip)}" target="_blank" class="block w-full bg-tlh-teal text-white text-center py-3 rounded-lg font-semibold hover:bg-tlh-teal/90 transition">
              Get Directions
            </a>
            <div class="pt-4 border-t border-gray-200">
              <p class="text-gray-600 font-semibold mb-2">Follow Our Sales</p>
              <div class="flex gap-2">
                <a href="https://www.facebook.com/TrueLegacyHomes" target="_blank" class="flex-1 flex items-center justify-center gap-2 bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition text-sm">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                  Facebook
                </a>
                <a href="https://www.instagram.com/truelegacyestatesales/" target="_blank" class="flex-1 flex items-center justify-center gap-2 bg-gradient-to-br from-purple-600 to-pink-500 text-white py-2 rounded hover:from-purple-700 hover:to-pink-600 transition text-sm">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
                  Instagram
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <footer class="bg-tlh-dark text-white py-8 mt-12">
    <div class="max-w-6xl mx-auto px-4 text-center">
      <p>&copy; 2026 True Legacy Homes. All rights reserved.</p>
    </div>
  </footer>

  <script>
    const images = ${JSON.stringify(sale.images, null, 2)};
    const gallery = document.getElementById('gallery');
    images.forEach(url => {
      const img = document.createElement('img');
      img.src = url;
      img.alt = 'Sale item';
      img.className = 'w-full h-32 object-cover rounded cursor-pointer hover:opacity-75 transition';
      img.loading = 'lazy';
      img.onclick = () => window.open(url, '_blank');
      gallery.appendChild(img);
    });
  </script>
</body>
</html>
`;

// Sale configurations for May 16-17, 2026
const sales = [
  {
    folder: 'san-diego-may-16-17',
    address: '5073 Remora Dr',
    city: 'San Diego',
    zip: '92130'
  },
  {
    folder: 'el-cajon-may-16-17',
    address: '945 Jamacha Way',
    city: 'El Cajon',
    zip: '92019'
  },
  {
    folder: 'lake-forest-may-16-17',
    address: '24668 Jutewood Pl',
    city: 'Lake Forest',
    zip: '92630'
  },
  {
    folder: 'mission-viejo-may-16-17',
    address: '24921 Danafir',
    city: 'Mission Viejo',
    zip: '92692'
  },
  {
    folder: 'escondido-may-16-17',
    address: '29221 Rolling Hills Dr',
    city: 'Escondido',
    zip: '92026'
  },
  {
    folder: 'san-diego-92120',
    address: '3955 33rd St',
    city: 'San Diego',
    zip: '92120'
  },
  {
    folder: 'shir-mar-el-cajon',
    address: '1260 Shir Mar Way',
    city: 'El Cajon',
    zip: '92021'
  },
  {
    folder: 'avenida-reposo-escondido',
    address: '1520 Avenida Reposo',
    city: 'Escondido',
    zip: '92027'
  },
  {
    folder: 'carranza-mission-viejo',
    address: '28551 Carranza Dr',
    city: 'Mission Viejo',
    zip: '92692'
  },
  {
    folder: 'jutewood-lake-forest',
    address: '24668 Jutewood Pl',
    city: 'Lake Forest',
    zip: '92630'
  }
];

// Process each sale
sales.forEach(sale => {
  const saleDir = path.join(__dirname, 'upcoming-sales', sale.folder);
  const indexPath = path.join(saleDir, 'index.html');
  
  if (!fs.existsSync(indexPath)) {
    console.log(`⚠️  Skipping ${sale.folder} - file not found`);
    return;
  }

  // Read existing file to extract images
  const existing = fs.readFileSync(indexPath, 'utf8');
  
  // Extract image URLs
  const imageMatches = existing.match(/https:\/\/picturescdn\.estatesales\.net\/[^"'\s]+/g) || [];
  const uniqueImages = [...new Set(imageMatches)];
  
  sale.images = uniqueImages;
  sale.imageCount = uniqueImages.length;

  // Generate new HTML
  const newHTML = betterTemplate(sale);

  // Write to file
  fs.writeFileSync(indexPath, newHTML);
  console.log(`✅ Updated ${sale.folder} (${sale.imageCount} images)`);
});

console.log('\n🎉 Done! All May 16-17 sales updated with better template.');
