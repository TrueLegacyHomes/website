#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// CORRECT addresses from EstateSales.net
const corrections = [
  {
    folder: 'san-diego-92120',
    address: '6111 Del Cerro Boulevard',
    city: 'San Diego',
    zip: '92120'
  },
  {
    folder: 'shir-mar-el-cajon',
    address: '8060 Shir Mar Place',
    city: 'El Cajon',
    zip: '92021'
  },
  {
    folder: 'avenida-reposo-escondido',
    address: '3207 Avenida Reposo',
    city: 'Escondido',
    zip: '92029'
  },
  {
    folder: 'jutewood-lake-forest',
    address: '24668 Jutewood Pl',
    city: 'Lake Forest',
    zip: '92630'
  },
  {
    folder: 'carranza-mission-viejo',
    address: '26791 Carranza Drive',
    city: 'Mission Viejo',
    zip: '92691'
  }
];

corrections.forEach(sale => {
  const filePath = path.join(__dirname, 'upcoming-sales', sale.folder, 'index.html');
  
  if (!fs.existsSync(filePath)) {
    console.log(`⚠️  Skipping ${sale.folder} - file not found`);
    return;
  }

  let html = fs.readFileSync(filePath, 'utf8');
  
  // Update title
  html = html.replace(/<title>.*?<\/title>/, `<title>Estate Sale: ${sale.address}, ${sale.city}</title>`);
  
  // Update meta description
  html = html.replace(
    /<meta name="description" content=".*?">/,
    `<meta name="description" content="Estate sale at ${sale.address}, ${sale.city}, CA ${sale.zip}. May 16-17, 2026, 8:00 AM - 2:00 PM.">`
  );
  
  // Update H1
  html = html.replace(
    /<h1 class="text-3xl font-bold mb-2">.*?<\/h1>/,
    `<h1 class="text-3xl font-bold mb-2">${sale.address}</h1>`
  );
  
  // Update subheading
  html = html.replace(
    /<p class="text-xl text-gray-600 mb-4">.*?<\/p>/,
    `<p class="text-xl text-gray-600 mb-4">${sale.city}, CA ${sale.zip}</p>`
  );
  
  // Update sidebar address
  html = html.replace(
    /<p class="text-gray-600">.*?<br>.*?, CA \d{5}<\/p>/,
    `<p class="text-gray-600">${sale.address}<br>${sale.city}, CA ${sale.zip}</p>`
  );
  
  // Update Google Maps link
  const mapsQuery = encodeURIComponent(`${sale.address}, ${sale.city}, CA ${sale.zip}`);
  html = html.replace(
    /href="https:\/\/maps\.google\.com\/\?q=[^"]*"/,
    `href="https://maps.google.com/?q=${mapsQuery}"`
  );
  
  fs.writeFileSync(filePath, html);
  console.log(`✅ Fixed ${sale.folder}: ${sale.address}`);
});

console.log('\n✅ All addresses corrected!');
