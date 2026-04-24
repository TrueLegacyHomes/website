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
  
  // Simple replacement: change grid-cols-3 gap-8 to gap-6
  html = html.replace(
    'class="grid md:grid-cols-3 gap-8"',
    'class="grid md:grid-cols-3 gap-6"'
  );
  
  // Move "About This Sale" before the grid
  // Pattern: find the grid div, then find About section inside it, move it before grid
  
  // Step 1: Find the py-8 container
  const containerStart = '  <div class="max-w-6xl mx-auto px-4 py-8">\n    <div class="grid md:grid-cols-3 gap-6">';
  const idx = html.indexOf(containerStart);
  
  if (idx === -1) {
    console.log(`⚠️  Skipped (pattern not found): ${dir}`);
    continue;
  }
  
  // Step 2: Find About section (it's in the first md:col-span-2)
  const aboutStart = html.indexOf('<div class="bg-white rounded-xl p-6 shadow-sm mb-6">', idx);
  const aboutEnd = html.indexOf('</div>\n      </div>', aboutStart) + '</div>\n      </div>'.length;
  
  if (aboutStart === -1 || aboutEnd === -1) {
    console.log(`⚠️  Couldn't find About section: ${dir}`);
    continue;
  }
  
  const aboutSection = html.substring(aboutStart, aboutEnd).replace('      ', '    ');
  
  // Step 3: Build new structure
  // Remove About from inside grid, add it before grid
  const beforeContainer = html.substring(0, idx + '  <div class="max-w-6xl mx-auto px-4 py-8">'.length);
  const afterAbout = html.substring(aboutEnd);
  
  // Clean up the remaining structure
  let middle = `\n    ${aboutSection.trim()}\n\n    <div class="grid md:grid-cols-3 gap-6">`;
  
  // Remove the old About section from the grid
  const newHtml = beforeContainer + middle + afterAbout.replace(aboutSection, '');
  
  fs.writeFileSync(filepath, newHtml);
  console.log(`✅ Updated: ${dir}`);
}

console.log('\n✅ All pages updated!');
