// Sample pre-loaded wardrobe items
const INITIAL_ITEMS = [
  { id: '1', name: 'Camisa Oxford Blanca', category: 'top', color: 'blanco', warmth: 2, formality: 4, style: 'elegante' },
  { id: '2', name: 'Camiseta Negra Básica', category: 'top', color: 'negro', warmth: 1, formality: 1, style: 'casual' },
  { id: '3', name: 'Buzo de Lana Gris', category: 'top', color: 'gris', warmth: 4, formality: 2, style: 'casual' },
  { id: '4', name: 'Chaqueta de Jean', category: 'outerwear', color: 'azul', warmth: 3, formality: 2, style: 'urbano' },
  { id: '5', name: 'Abrigo Paño Negro', category: 'outerwear', color: 'negro', warmth: 5, formality: 5, style: 'elegante' },
  { id: '6', name: 'Jeans Azules Oscuros', category: 'bottom', color: 'azul', warmth: 3, formality: 2, style: 'casual' },
  { id: '7', name: 'Pantalón de Vestir Negro', category: 'bottom', color: 'negro', warmth: 3, formality: 5, style: 'elegante' },
  { id: '8', name: 'Pantalón Chino Beige', category: 'bottom', color: 'beige', warmth: 2, formality: 3, style: 'casual' },
  { id: '9', name: 'Tenis Blancos Urbano', category: 'shoes', color: 'blanco', warmth: 2, formality: 1, style: 'urbano' },
  { id: '10', name: 'Zapatos de Cuero Café', category: 'shoes', color: 'cafe', warmth: 3, formality: 5, style: 'elegante' },
  { id: '11', name: 'Botas de Cuero Negras', category: 'shoes', color: 'negro', warmth: 4, formality: 3, style: 'urbano' },
  { id: '12', name: 'Sudadera Deportiva Gris', category: 'bottom', color: 'gris', warmth: 2, formality: 1, style: 'deportivo' }
];

// Presets Packs
const PRESET_PACKS = {
  minimal: [
    { id: 'm1', name: 'Camiseta Blanca Básica', category: 'top', color: 'blanco', warmth: 1, formality: 1, style: 'casual' },
    { id: 'm2', name: 'Camisa Oxford Gris', category: 'top', color: 'gris', warmth: 2, formality: 3, style: 'elegante' },
    { id: 'm3', name: 'Jeans Negros Minimal', category: 'bottom', color: 'negro', warmth: 3, formality: 2, style: 'minimalista' },
    { id: 'm4', name: 'Pantalón Chino Beige', category: 'bottom', color: 'beige', warmth: 2, formality: 3, style: 'casual' },
    { id: 'm5', name: 'Tenis Blancos Minimal', category: 'shoes', color: 'blanco', warmth: 2, formality: 1, style: 'urbano' },
    { id: 'm6', name: 'Chaqueta Ligera Negra', category: 'outerwear', color: 'negro', warmth: 3, formality: 3, style: 'minimalista' }
  ],
  executive: [
    { id: 'e1', name: 'Camisa Oxford Azul', category: 'top', color: 'azul', warmth: 2, formality: 4, style: 'elegante' },
    { id: 'e2', name: 'Camisa Blanco Formal', category: 'top', color: 'blanco', warmth: 2, formality: 5, style: 'elegante' },
    { id: 'e3', name: 'Pantalón de Vestir Azul Marino', category: 'bottom', color: 'azul', warmth: 3, formality: 5, style: 'elegante' },
    { id: 'e4', name: 'Pantalón de Vestir Negro', category: 'bottom', color: 'negro', warmth: 3, formality: 5, style: 'elegante' },
    { id: 'e5', name: 'Zapatos de Cuero Café', category: 'shoes', color: 'cafe', warmth: 3, formality: 5, style: 'elegante' },
    { id: 'e6', name: 'Abrigo Elegante Paño Negro', category: 'outerwear', color: 'negro', warmth: 5, formality: 5, style: 'elegante' }
  ],
  urban: [
    { id: 'u1', name: 'Buzo Oversize Negro', category: 'top', color: 'negro', warmth: 3, formality: 1, style: 'urbano' },
    { id: 'u2', name: 'Camiseta Estampada Streetwear', category: 'top', color: 'blanco', warmth: 1, formality: 1, style: 'urbano' },
    { id: 'u3', name: 'Jeans Rasgados Azules', category: 'bottom', color: 'azul', warmth: 3, formality: 1, style: 'urbano' },
    { id: 'u4', name: 'Pantalón Cargo Beige', category: 'bottom', color: 'beige', warmth: 3, formality: 2, style: 'urbano' },
    { id: 'u5', name: 'Tenis High Top Negros', category: 'shoes', color: 'negro', warmth: 2, formality: 1, style: 'urbano' },
    { id: 'u6', name: 'Chaqueta de Jean Azul', category: 'outerwear', color: 'azul', warmth: 3, formality: 2, style: 'urbano' }
  ]
};

let wardrobe = [];

// Icons map
const CATEGORY_ICONS = {
  top: '👔',
  bottom: '👖',
  shoes: '👟',
  outerwear: '🧥'
};

const CATEGORY_LABELS = {
  top: 'Superior',
  bottom: 'Inferior',
  shoes: 'Calzado',
  outerwear: 'Abrigo'
};

// Target parameters for context
const OCCASION_CONFIG = {
  casual: { formality: 2, label: 'Universidad / Casual' },
  trabajo: { formality: 4, label: 'Oficina / Trabajo' },
  fiesta: { formality: 3, label: 'Fiesta / Noche' },
  formal: { formality: 5, label: 'Evento Formal' },
  deporte: { formality: 1, label: 'Deporte' },
  cita: { formality: 4, label: 'Cita / Salida Especial' }
};

const WEATHER_CONFIG = {
  frio: { minWarmth: 4, maxWarmth: 5, label: 'Frío' },
  templado: { minWarmth: 2, maxWarmth: 3, label: 'Templado' },
  calido: { minWarmth: 1, maxWarmth: 2, label: 'Cálido' },
  lluvioso: { minWarmth: 4, maxWarmth: 5, label: 'Lluvioso' }
};

// Color compatibility matrix
const NEUTRAL_COLORS = ['negro', 'blanco', 'gris', 'beige'];

function checkColorHarmony(c1, c2, c3) {
  let score = 70; // base score
  let neutrals = [c1, c2, c3].filter(c => NEUTRAL_COLORS.includes(c)).length;
  if (neutrals >= 2) score += 20;

  if ((c1 === 'negro' && c2 === 'blanco') || (c1 === 'blanco' && c2 === 'negro')) score += 10;
  if ((c1 === 'azul' && c2 === 'beige') || (c1 === 'beige' && c2 === 'azul')) score += 10;
  if (c1 === c2) score += 10;

  return Math.min(100, score);
}

// Interactive Visual Chip Selection for Weather & Occasion
function selectChipOption(type, value, element) {
  const container = element.parentElement;
  container.querySelectorAll('.option-chip').forEach(chip => chip.classList.remove('active'));
  element.classList.add('active');

  if (type === 'weather') {
    document.getElementById('weather-select').value = value;
  } else if (type === 'event') {
    document.getElementById('event-select').value = value;
  }
}

// Preset Loader
function loadPresetPack(packType) {
  if (packType === 'full') {
    wardrobe = [...INITIAL_ITEMS];
  } else if (PRESET_PACKS[packType]) {
    wardrobe = [...PRESET_PACKS[packType]];
  }
  saveWardrobe();
  renderWardrobe('all');
  alert(`¡Armario cargado con éxito! (${wardrobe.length} prendas)`);
}

// Load Wardrobe
function initWardrobe() {
  const saved = localStorage.getItem('styleai_wardrobe');
  if (saved) {
    try {
      wardrobe = JSON.parse(saved);
    } catch(e) {
      wardrobe = [...INITIAL_ITEMS];
    }
  } else {
    wardrobe = [...INITIAL_ITEMS];
    saveWardrobe();
  }
  renderWardrobe('all');
  updateBadges();
}

function saveWardrobe() {
  localStorage.setItem('styleai_wardrobe', JSON.stringify(wardrobe));
  updateBadges();
}

function updateBadges() {
  document.getElementById('items-count-badge').innerText = wardrobe.length;
  updateStatsDashboard();
}

function updateStatsDashboard() {
  const total = wardrobe.length;
  document.getElementById('stat-total').innerText = total;

  if (total === 0) {
    document.getElementById('stat-color').innerText = '-';
    document.getElementById('stat-warmth').innerText = '0.0/5';
    document.getElementById('stat-formality').innerText = '0.0/5';
    return;
  }

  // Count colors
  const colorCounts = {};
  let totalWarmth = 0;
  let totalFormality = 0;

  wardrobe.forEach(i => {
    colorCounts[i.color] = (colorCounts[i.color] || 0) + 1;
    totalWarmth += i.warmth;
    totalFormality += i.formality;
  });

  const dominantColor = Object.keys(colorCounts).reduce((a, b) => colorCounts[a] > colorCounts[b] ? a : b);
  document.getElementById('stat-color').innerText = dominantColor.toUpperCase();
  document.getElementById('stat-warmth').innerText = (totalWarmth / total).toFixed(1) + '/5';
  document.getElementById('stat-formality').innerText = (totalFormality / total).toFixed(1) + '/5';
}

// Toggle Add Item Form
function toggleAddForm() {
  const form = document.getElementById('add-item-form');
  form.classList.toggle('show');
}

// Handle Add Item
function handleAddItem(event) {
  event.preventDefault();
  const name = document.getElementById('item-name').value.trim();
  const category = document.getElementById('item-category').value;
  const color = document.getElementById('item-color').value;
  const warmth = parseInt(document.getElementById('item-warmth').value);
  const formality = parseInt(document.getElementById('item-formality').value);

  const newItem = {
    id: Date.now().toString(),
    name,
    category,
    color,
    warmth,
    formality,
    style: formality >= 4 ? 'elegante' : formality === 1 ? 'deportivo' : 'casual'
  };

  wardrobe.push(newItem);
  saveWardrobe();
  renderWardrobe('all');

  document.getElementById('add-item-form').reset();
  toggleAddForm();
  alert(`¡Prenda "${name}" agregada exitosamente a tu armario!`);
}

// Delete Item
function deleteItem(id) {
  if (confirm('¿Deseas eliminar esta prenda del armario?')) {
    wardrobe = wardrobe.filter(i => i.id !== id);
    saveWardrobe();
    renderWardrobe('all');
  }
}

// Filter and Render Wardrobe Catalog
function renderWardrobe(categoryFilter = 'all') {
  const container = document.getElementById('wardrobe-container');
  container.innerHTML = '';

  const filtered = categoryFilter === 'all' 
    ? wardrobe 
    : wardrobe.filter(i => i.category === categoryFilter);

  if (filtered.length === 0) {
    container.innerHTML = `<div class="empty-state"><div class="empty-icon">👕</div><p>No hay prendas registradas en esta categoría.</p></div>`;
    return;
  }

  filtered.forEach(item => {
    const card = document.createElement('div');
    card.className = 'item-card';
    card.innerHTML = `
      <button class="btn-delete" onclick="deleteItem('${item.id}')" title="Eliminar prenda">✕</button>
      <div class="item-icon-box">${CATEGORY_ICONS[item.category] || '👔'}</div>
      <div class="item-title">${item.name}</div>
      <div class="item-meta">
        <span class="tag">${CATEGORY_LABELS[item.category]}</span>
        <span class="tag">Color: ${item.color}</span>
        <span class="tag">Abrigo: ${item.warmth}/5</span>
        <span class="tag">Formal: ${item.formality}/5</span>
      </div>
    `;
    container.appendChild(card);
  });
}

function filterCategory(cat, btn) {
  document.querySelectorAll('.filter-chip').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderWardrobe(cat);
}

// Switch Tabs
function switchTab(tab) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

  if (tab === 'outfits') {
    document.getElementById('tab-outfits-btn').classList.add('active');
    document.getElementById('tab-outfits').classList.add('active');
  } else {
    document.getElementById('tab-wardrobe-btn').classList.add('active');
    document.getElementById('tab-wardrobe').classList.add('active');
  }
}

// Recommendation Engine
async function generateOutfits() {
  const weatherKey = document.getElementById('weather-select').value;
  const occasionKey = document.getElementById('event-select').value;
  const preferredStyle = document.getElementById('style-select').value;
  const engine = document.getElementById('engine-select') ? document.getElementById('engine-select').value : 'llm';

  const targetFormality = OCCASION_CONFIG[occasionKey].formality;
  const weatherInfo = WEATHER_CONFIG[weatherKey];

  const tops = wardrobe.filter(i => i.category === 'top');
  const bottoms = wardrobe.filter(i => i.category === 'bottom');
  const shoes = wardrobe.filter(i => i.category === 'shoes');
  const outerwears = wardrobe.filter(i => i.category === 'outerwear');

  if (tops.length === 0 || bottoms.length === 0 || shoes.length === 0) {
    alert('Necesitas tener al menos una prenda Superior, una Inferior y Calzado en tu armario para generar combinaciones.');
    switchTab('wardrobe');
    return;
  }

  // Show Skeleton Shimmer Loading State
  switchTab('outfits');
  const container = document.getElementById('outfits-container');
  container.innerHTML = `
    <div class="empty-state" style="padding: 40px;">
      <div class="empty-icon" style="animation: spin 1.5s infinite linear;">⚙️</div>
      <h3>Calculando mejores combinaciones...</h3>
      <p>Evaluando balance térmico, formalidad y teoría de colores en tiempo real.</p>
    </div>
  `;

  // Simulate short animation delay for smooth UX feel
  await new Promise(r => setTimeout(r, 350));

  // If API Engine is selected, try calling backend API
  if (engine === 'llm') {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          wardrobe: wardrobe,
          weather: weatherKey,
          occasion: occasionKey,
          style_preference: preferredStyle
        })
      });

      if (response.ok) {
        const data = await response.json();
        if (data.outfit) {
          const llmOutfit = {
            top: data.outfit.top,
            bottom: data.outfit.bottom,
            shoes: data.outfit.shoes,
            outerwear: data.outfit.outerwear,
            score: data.matchScore,
            reasoning: data.aiReasoning
          };
          renderOutfits([llmOutfit], OCCASION_CONFIG[occasionKey].label, weatherInfo.label);
          return;
        }
      }
    } catch (err) {
      console.warn('Servidor API no conectado. Utilizando motor de reglas local...', err);
    }
  }

  // Local Rule-Based Engine
  const candidateCombinations = [];

  tops.forEach(t => {
    bottoms.forEach(b => {
      shoes.forEach(s => {
        evaluateAndPush(t, b, s, null, targetFormality, weatherInfo, preferredStyle, candidateCombinations);
        outerwears.forEach(o => {
          evaluateAndPush(t, b, s, o, targetFormality, weatherInfo, preferredStyle, candidateCombinations);
        });
      });
    });
  });

  candidateCombinations.sort((a, b) => b.score - a.score);
  const topOutfits = candidateCombinations.slice(0, 4);
  renderOutfits(topOutfits, OCCASION_CONFIG[occasionKey].label, weatherInfo.label);
}

function evaluateAndPush(top, bottom, shoes, outerwear, targetFormality, weatherInfo, preferredStyle, list) {
  const items = [top, bottom, shoes];
  if (outerwear) items.push(outerwear);

  const avgFormality = items.reduce((acc, i) => acc + i.formality, 0) / items.length;
  const formalityDiff = Math.abs(avgFormality - targetFormality);
  const formalityScore = Math.max(0, 100 - formalityDiff * 25);

  const totalWarmth = items.reduce((acc, i) => acc + i.warmth, 0) / items.length;
  let warmthScore = 80;
  if (totalWarmth >= weatherInfo.minWarmth && totalWarmth <= weatherInfo.maxWarmth + 1) {
    warmthScore = 100;
  } else {
    const warmthDiff = Math.abs(totalWarmth - (weatherInfo.minWarmth + weatherInfo.maxWarmth) / 2);
    warmthScore = Math.max(20, 100 - warmthDiff * 25);
  }

  const colorScore = checkColorHarmony(top.color, bottom.color, shoes.color);
  const styleMatches = items.filter(i => i.style === preferredStyle).length;
  const styleBonus = (styleMatches / items.length) * 100;

  const totalScore = Math.round(
    formalityScore * 0.35 +
    warmthScore * 0.35 +
    colorScore * 0.20 +
    styleBonus * 0.10
  );

  let reasoning = [];
  if (formalityDiff <= 0.8) {
    reasoning.push(`Cumple excelente el nivel de formalidad (${avgFormality.toFixed(1)}/5) para la ocasión.`);
  }
  if (warmthScore >= 85) {
    reasoning.push(`Proporciona abrigo térmico óptimo para clima ${weatherInfo.label}.`);
  }
  if (colorScore >= 80) {
    reasoning.push(`Excelente combinación de tonos (${top.color}, ${bottom.color} y ${shoes.color}).`);
  }

  list.push({
    top,
    bottom,
    shoes,
    outerwear,
    score: Math.min(99, Math.max(60, totalScore)),
    reasoning: reasoning.join(' ') || 'Combinación equilibrada entre las prendas disponibles.'
  });
}

function renderOutfits(outfits, occasionLabel, weatherLabel, engineSuffix = '') {
  switchTab('outfits');
  const container = document.getElementById('outfits-container');
  document.getElementById('outfits-count-badge').innerText = outfits.length;

  if (outfits.length === 0) {
    container.innerHTML = `<div class="empty-state"><p>No se encontraron combinaciones recomendadas.</p></div>`;
    return;
  }

  container.innerHTML = '';

  outfits.forEach((outfit, index) => {
    const card = document.createElement('div');
    card.className = 'outfit-card';
    
    let itemsHtml = `
      <div class="outfit-item-node">
        <span style="font-size: 24px;">👔</span>
        <div>
          <div style="font-size: 11px; color: #94a3b8;">Superior</div>
          <div style="font-weight: 700; font-size: 13px;">${outfit.top.name}</div>
          <div style="font-size: 10px; color: #64748b;">Color: ${outfit.top.color}</div>
        </div>
      </div>

      <div class="outfit-item-node">
        <span style="font-size: 24px;">👖</span>
        <div>
          <div style="font-size: 11px; color: #94a3b8;">Inferior</div>
          <div style="font-weight: 700; font-size: 13px;">${outfit.bottom.name}</div>
          <div style="font-size: 10px; color: #64748b;">Color: ${outfit.bottom.color}</div>
        </div>
      </div>

      <div class="outfit-item-node">
        <span style="font-size: 24px;">👟</span>
        <div>
          <div style="font-size: 11px; color: #94a3b8;">Calzado</div>
          <div style="font-weight: 700; font-size: 13px;">${outfit.shoes.name}</div>
          <div style="font-size: 10px; color: #64748b;">Color: ${outfit.shoes.color}</div>
        </div>
      </div>
    `;

    if (outfit.outerwear) {
      itemsHtml += `
        <div class="outfit-item-node">
          <span style="font-size: 24px;">🧥</span>
          <div>
            <div style="font-size: 11px; color: #94a3b8;">Abrigo Extra</div>
            <div style="font-weight: 700; font-size: 13px;">${outfit.outerwear.name}</div>
            <div style="font-size: 10px; color: #64748b;">Color: ${outfit.outerwear.color}</div>
          </div>
        </div>
      `;
    }

    card.innerHTML = `
      <div class="outfit-header">
        <div>
          <h3 style="font-size: 16px; font-weight: 700;">Outfit Recomendado #${index + 1}${engineSuffix}</h3>
          <span style="font-size: 12px; color: #94a3b8;">${occasionLabel} • Clima ${weatherLabel}</span>
        </div>
        <div class="match-score-badge">${outfit.score}% Match</div>
      </div>

      <div class="outfit-items-flex">
        ${itemsHtml}
      </div>

      <div class="outfit-reasoning">
        <strong>💡 Justificación:</strong> ${outfit.reasoning}
      </div>
    `;

    container.appendChild(card);
  });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  initWardrobe();
});
