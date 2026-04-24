const fs = require('fs');
const path = require('path');

const salesDir = '/Users/admin/.openclaw/workspace/tlh-rebuild/upcoming-sales';
const dirs = fs.readdirSync(salesDir).filter(d => 
  fs.statSync(path.join(salesDir, d)).isDirectory()
);

let fixed = 0;
let skipped = 0;

for (const dir of dirs) {
  // Skip the one we already fixed manually
  if (dir === 'oceanside-via-las-villas') {
    console.log(`⏭️  Skipped (already fixed manually): ${dir}`);
    continue;
  }
  
  const filepath = path.join(salesDir, dir, 'index.html');
  if (!fs.existsSync(filepath)) continue;
  
  let html = fs.readFileSync(filepath, 'utf8');
  
  // Pattern 1: Change gap-8 to gap-6
  html = html.replace('gap-8', 'gap-6');
  
  // Pattern 2: Move About section before grid and restructure
  const pattern = /<div class="max-w-6xl mx-auto px-4 py-8">\s*<div class="grid md:grid-cols-3 gap-6">\s*<div class="md:col-span-2">\s*<div class="bg-white rounded-xl p-6 shadow-sm mb-6">\s*<h2 class="text-2xl font-bold mb-4">About This Sale<\/h2>\s*([\s\S]*?)<\/div>\s*<div class="bg-white rounded-xl p-6 shadow-sm">\s*<h2 class="text-2xl font-bold mb-4">Photos <span class="text-gray-400 text-lg font-normal">\((\d+)\)<\/span><\/h2>\s*<div id="gallery" class="grid grid-cols-1 md:grid-cols-5 gap-2"><\/div>\s*<\/div>\s*<\/div>/;
  
  const match = html.match(pattern);
  
  if (!match) {
    console.log(`⚠️  Skipped (pattern not matched): ${dir}`);
    skipped++;
    continue;
  }
  
  const aboutContent = match[1].trim();
  const photoCount = match[2];
  
  const replacement = `<div class="max-w-6xl mx-auto px-4 py-8">
    <div class="bg-white rounded-xl p-6 shadow-sm mb-6">
      <h2 class="text-2xl font-bold mb-4">About This Sale</h2>
      ${aboutContent}
    </div>

    <div class="grid md:grid-cols-3 gap-6">
      <!-- Photos Section (2/3 width on desktop) -->
      <div class="md:col-span-2">
        <div class="bg-white rounded-xl p-6 shadow-sm">
          <h2 class="text-2xl font-bold mb-4">Photos <span class="text-gray-400 text-lg font-normal">(${photoCount})</span></h2>
          <div id="gallery" class="grid grid-cols-1 md:grid-cols-5 gap-2"></div>
        </div>
      </div>`;
  
  html = html.replace(pattern, replacement);
  
  // Add comment before sidebar
  html = html.replace(
    '      <div class="md:col-span-1">',
    '      <!-- Sale Details Sidebar (1/3 width on desktop) -->\n      <div class="md:col-span-1">'
  );
  
  fs.writeFileSync(filepath, html);
  console.log(`✅ Fixed: ${dir}`);
  fixed++;
}

console.log(`\n✅ Layout update complete! Fixed: ${fixed}, Skipped: ${skipped + 1}`);
