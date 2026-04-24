const fs = require('fs');
const path = require('path');

const salesToFix = [
  'san-diego-4255-lochlomond-street',
  'la-mesa-8745-glenira-avenue',
  'west-covina-2405-east-evergreen-avenue',
  'lakewood-5923-fairman-street'
];

const salesDir = '/Users/admin/.openclaw/workspace/tlh-rebuild/upcoming-sales';

for (const saleDir of salesToFix) {
  const filepath = path.join(salesDir, saleDir, 'index.html');
  if (!fs.existsSync(filepath)) {
    console.log(`⚠️  Not found: ${saleDir}`);
    continue;
  }
  
  let html = fs.readFileSync(filepath, 'utf8');
  
  // Pattern: find About section inside the grid's left column
  const pattern = /(<div class="max-w-6xl mx-auto px-4 py-8">)\s*<div class="flex flex-col md:grid md:grid-cols-3 gap-6">\s*<div class="md:col-span-2 space-y-6 order-2 md:order-1">\s*(<div class="bg-white rounded-xl p-6 shadow-sm">[\s\S]*?<\/div>)\s*<div class="bg-white rounded-xl p-6 shadow-sm">\s*<h2 class="text-2xl font-bold mb-4">About This Sale<\/h2>\s*([\s\S]*?)<\/div>/;
  
  const match = html.match(pattern);
  
  if (!match) {
    console.log(`⚠️  Pattern not matched: ${saleDir}`);
    continue;
  }
  
  const containerStart = match[1];
  const titleCard = match[2];
  const aboutContent = match[3].trim();
  
  const replacement = `${containerStart}
    <div class="bg-white rounded-xl p-6 shadow-sm mb-6">
      <h2 class="text-2xl font-bold mb-4">About This Sale</h2>
      ${aboutContent}
    </div>

    <div class="flex flex-col md:grid md:grid-cols-3 gap-6">
      <!-- Photos Section (2/3 width on desktop) -->
      <div class="md:col-span-2 space-y-6 order-2 md:order-1">
        ${titleCard}`;
  
  html = html.replace(pattern, replacement);
  
  // Add sidebar comment
  html = html.replace(
    '      <div class="md:col-span-1 order-1 md:order-2">',
    '      <!-- Sale Details Sidebar (1/3 width on desktop) -->\n      <div class="md:col-span-1 order-1 md:order-2">'
  );
  
  fs.writeFileSync(filepath, html);
  console.log(`✅ Fixed: ${saleDir}`);
}

console.log('\n✅ All live sales fixed!');
