const fs = require('fs');
const path = require('path');

const salesDir = '/Users/admin/.openclaw/workspace/tlh-rebuild/upcoming-sales';
const dirs = fs.readdirSync(salesDir).filter(d => 
  fs.statSync(path.join(salesDir, d)).isDirectory()
);

for (const dir of dirs) {
  const filepath = path.join(salesDir, dir, 'index.html');
  if (!fs.existsSync(filepath)) continue;
  
  let html = fs.readFileSync(filepath, 'utf8');
  
  // Skip if already has Tailwind CDN (new template)
  if (html.includes('cdn.tailwindcss.com')) {
    console.log(`⏭️  Skipped (already uses CDN): ${dir}`);
    continue;
  }
  
  // Find the container div
  const containerMatch = html.match(/<div class="max-w-6xl mx-auto px-4 py-8">([\s\S]*?)<div class="max-w-6xl mx-auto px-4 pb-8">/);
  if (!containerMatch) {
    console.log(`⚠️  Skipped (no match): ${dir}`);
    continue;
  }
  
  const sectionHtml = containerMatch[1];
  
  // Extract About section
  const aboutMatch = sectionHtml.match(/<div class="bg-white rounded-xl p-6 shadow-sm mb-6">\s*<h2 class="text-2xl font-bold mb-4">About This Sale<\/h2>([\s\S]*?)<\/div>/);
  
  // Extract Photos section  
  const photosMatch = sectionHtml.match(/<div class="bg-white rounded-xl p-6 shadow-sm">\s*<h2 class="text-2xl font-bold mb-4">Photos([\s\S]*?)<div id="gallery"/);
  
  // Extract Sale Details sidebar
  const sidebarMatch = sectionHtml.match(/(<div class="md:col-span-1">[\s\S]*?Follow Our Sales[\s\S]*?<\/div>\s*<\/div>\s*<\/div>\s*<\/div>)/);
  
  if (!aboutMatch || !photosMatch || !sidebarMatch) {
    console.log(`⚠️  Couldn already parse sections: ${dir}`);
    continue;
  }
  
  const about = `<div class="bg-white rounded-xl p-6 shadow-sm mb-6">
      <h2 class="text-2xl font-bold mb-4">About This Sale</h2>${aboutMatch[1]}</div>`;
  
  const photos = `<div class="bg-white rounded-xl p-6 shadow-sm">
          <h2 class="text-2xl font-bold mb-4">Photos${photosMatch[1]}<div id="gallery" class="grid grid-cols-1 md:grid-cols-5 gap-2"></div>
        </div>`;
  
  const sidebar = sidebarMatch[1];
  
  const newSection = `  <div class="max-w-6xl mx-auto px-4 py-8">
    ${about}

    <div class="grid md:grid-cols-3 gap-6">
      <!-- Photos Section (2/3 width on desktop) -->
      <div class="md:col-span-2">
        ${photos}
      </div>

      <!-- Sale Details Sidebar (1/3 width on desktop) -->
      ${sidebar}
    </div>
  </div>

  `;
  
  // Replace the old section
  const newHtml = html.replace(containerMatch[0], newSection + '<div class="max-w-6xl mx-auto px-4 pb-8">');
  
  fs.writeFileSync(filepath, newHtml);
  console.log(`✅ Fixed: ${dir}`);
}

console.log('\n✅ Layout fixes complete!');
