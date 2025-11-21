/**
 * PWA Icon Generator for DataPurity
 * Generates all required PWA icons from a base SVG or PNG
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Icon sizes needed for PWA
const ICON_SIZES = [16, 32, 72, 96, 128, 144, 152, 192, 384, 512];

// Create icons directory if it doesn't exist
const iconsDir = path.join(__dirname, '..', 'public', 'icons');
if (!fs.existsSync(iconsDir)) {
  fs.mkdirSync(iconsDir, { recursive: true });
}

// Create a simple SVG icon as placeholder
const createSVGIcon = (size) => {
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="${size}" height="${size}" rx="${size * 0.2}" fill="url(#grad)" />
  
  <!-- Icon - Database/Document symbol -->
  <g transform="translate(${size * 0.25}, ${size * 0.25})">
    <!-- Document outline -->
    <rect x="${size * 0.05}" y="${size * 0.05}" 
          width="${size * 0.4}" height="${size * 0.5}" 
          rx="${size * 0.02}" fill="white" opacity="0.9" />
    
    <!-- Lines representing data -->
    <line x1="${size * 0.1}" y1="${size * 0.15}" 
          x2="${size * 0.4}" y2="${size * 0.15}" 
          stroke="#667eea" stroke-width="${size * 0.015}" stroke-linecap="round" />
    <line x1="${size * 0.1}" y1="${size * 0.25}" 
          x2="${size * 0.4}" y2="${size * 0.25}" 
          stroke="#667eea" stroke-width="${size * 0.015}" stroke-linecap="round" />
    <line x1="${size * 0.1}" y1="${size * 0.35}" 
          x2="${size * 0.35}" y2="${size * 0.35}" 
          stroke="#667eea" stroke-width="${size * 0.015}" stroke-linecap="round" />
    <line x1="${size * 0.1}" y1="${size * 0.45}" 
          x2="${size * 0.4}" y2="${size * 0.45}" 
          stroke="#667eea" stroke-width="${size * 0.015}" stroke-linecap="round" />
    
    <!-- Sparkle/Clean symbol -->
    <circle cx="${size * 0.42}" cy="${size * 0.12}" r="${size * 0.04}" fill="white" opacity="0.95" />
    <circle cx="${size * 0.38}" cy="${size * 0.08}" r="${size * 0.025}" fill="white" opacity="0.85" />
  </g>
  
  <!-- Text -->
  <text x="${size * 0.5}" y="${size * 0.85}" 
        font-family="Arial, sans-serif" 
        font-size="${size * 0.12}" 
        font-weight="bold" 
        fill="white" 
        text-anchor="middle">DP</text>
</svg>`;
};

// Generate all icon sizes
console.log('🎨 Generating PWA icons...\n');

ICON_SIZES.forEach((size) => {
  const svgContent = createSVGIcon(size);
  const filename = `icon-${size}x${size}.svg`;
  const filepath = path.join(iconsDir, filename);
  
  fs.writeFileSync(filepath, svgContent);
  console.log(`✓ Created ${filename}`);
});

// Create badge icon (for notifications)
const badgeSVG = createSVGIcon(72);
fs.writeFileSync(path.join(iconsDir, 'badge-72x72.svg'), badgeSVG);
console.log('✓ Created badge-72x72.svg');

// Create shortcut icons
const shortcuts = ['upload', 'contacts', 'dashboard'];
shortcuts.forEach((name) => {
  const svg = createSVGIcon(96);
  fs.writeFileSync(path.join(iconsDir, `shortcut-${name}.svg`), svg);
  console.log(`✓ Created shortcut-${name}.svg`);
});

console.log('\n✅ All PWA icons generated successfully!');
console.log('\n📝 Note: These are placeholder SVG icons.');
console.log('   For production, replace with PNG versions using a tool like:');
console.log('   - https://realfavicongenerator.net/');
console.log('   - https://favicon.io/');
console.log('   - Or use a design tool like Figma/Sketch\n');
