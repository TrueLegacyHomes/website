const fs = require('fs');
const path = require('path');

const filesToFix = [
  'costa-mesa-antiques',
  'del-mar-13027-via-latina',
  'encinitas-barbara-lane',
  'fullerton-camino-rey',
  'la-jolla-top-floor',
  'la-mesa-8745-glenira-avenue',
  'la-mesa-avocado',
  'lakewood-5923-fairman-street',
  'long-beach-village',
  'san-diego-4255-lochlomond-street',
  'west-covina-2405-east-evergreen-avenue'
];

const salesDir = '/Users/admin/.openclaw/workspace/tlh-rebuild/upcoming-sales';

for (const dir of filesToFix) {
  const filepath = path.join(salesDir, dir, 'index.html');
  if (!fs.existsSync(filepath)) {
    console.log(`⚠️  Not found: ${dir}`);
    continue;
  }
  
  let html = fs.readFileSync(filepath, 'utf8');
  
  // 1. Change gap-8 to gap-6
  html = html.replace(/gap-8/g, 'gap-6');
  
  // 2. Find and extract About section (it's always in the first part of md:col-span-2)
  const aboutRegex = /<div class="bg-white rounded-xl p-6 shadow-sm mb-6">\s*<h2 class="text-2xl font-bold mb-4">About This Sale<\/h2>\s*([\s\S]*?)<\/div>/;
  const aboutMatch = html.match(aboutRegex);
  
  if (!aboutMatch) {
    console.log(`⚠️  Couldn't match About section: ${dir}`);
    continue;
  }
  
  const fullAboutSection = aboutMatch[0];
  const aboutContent = aboutMatch[1].trim();
  
  // 3. Find the container div and grid
  const containerPattern = /<div class="max-w-6xl mx-auto px-4 py-8">\s*<div class="grid md:grid-cols-3 gap-6">/;
  const containerMatch = html.match(containerPattern);
  
  if (!containerMatch) {
    console.log(`⚠️  Couldn't match container: ${dir}`);
    continue;
  }
  
  // 4. Build the new About section (pulled out before grid)
  const newAboutSection = `  <div class="max-w-6xl mx-auto px-4 py-8">
    <div class="bg-white rounded-xl p-6 shadow-sm mb-6">
      <h2 class="text-2xl font-bold mb-4">About This Sale</h2>
      ${aboutContent}
    </div>

    <div class="grid md:grid-cols-3 gap-6">`;
  
  // 5. Replace the container start + remove the old About section
  html = html.replace(containerMatch[0], newAboutSection);
  
  // Remove the old About section from inside the grid
  // It should be right after md:col-span-2
  html = html.replace(fullAboutSection + '\n\n        ', '');
  
  // 6. Add comments if not present
  if (!html.includes('<!-- Photos Section')) {
    html = html.replace(
      /<div class="md:col-span-2(?: order-\d md:order-\d)?">/,
      '<!-- Photos Section (2/3 width on desktop) -->\n      <div class="md:col-span-2$1">'
    );
  }
  
  if (!html.includes('<!-- Sale Details Sidebar')) {
    html = html.replace(
      /<div class="md:col-span-1(?: order-\d md:order-\d)?">/,
      '<!-- Sale Details Sidebar (1/3 width on desktop) -->\n      <div class="md:col-span-1$1">'
    );
  }
  
  fs.writeFileSync(filepath, html);
  console.log(`✅ Fixed: ${dir}`);
}

console.log('\n✅ Remaining layouts fixed!');
