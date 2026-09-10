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
let generatedOutfits = [];
let favoriteOutfits = [];

const CATEGORY_ICONS = {
  top: '<img src="assets/top.svg" class="cat-icon-img" alt="Superior">',
  bottom: '<img src="assets/bottom.svg" class="cat-icon-img" alt="Inferior">',
  shoes: '<img src="assets/shoes.svg" class="cat-icon-img" alt="Calzado">',
  outerwear: '<img src="assets/outerwear.svg" class="cat-icon-img" alt="Abrigo">'
};
const CATEGORY_LABELS = { top: 'Superior', bottom: 'Inferior', shoes: 'Calzado', outerwear: 'Abrigo' };

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

const NEUTRAL_COLORS = ['negro', 'blanco', 'gris', 'beige'];

function checkColorHarmony(c1, c2, c3) {
  let score = 70;
  let neutrals = [c1, c2, c3].filter(c => NEUTRAL_COLORS.includes(c)).length;
  if (neutrals >= 2) score += 20;
  if ((c1 === 'negro' && c2 === 'blanco') || (c1 === 'blanco' && c2 === 'negro')) score += 10;
  if ((c1 === 'azul' && c2 === 'beige') || (c1 === 'beige' && c2 === 'azul')) score += 10;
  if (c1 === c2) score += 10;
  return Math.min(100, score);
}

// Collapsible Accordion Card Toggle
function toggleAccordion(bodyId, arrowId) {
  const body = document.getElementById(bodyId);
  const arrow = document.getElementById(arrowId);
  if (!body) return;

  const isCollapsed = body.classList.contains('collapsed');
  if (isCollapsed) {
    body.classList.remove('collapsed');
    if (arrow) arrow.classList.remove('collapsed');
  } else {
    body.classList.add('collapsed');
    if (arrow) arrow.classList.add('collapsed');
  }
}

// Custom Accordion Dropdown Component (100% Contained, Zero Native Overflow)
function toggleCustomDropdown(dropdownId) {
  const dropdown = document.getElementById(dropdownId);
  if (!dropdown) return;
  
  // Close other dropdowns first
  document.querySelectorAll('.custom-dropdown').forEach(d => {
    if (d !== dropdown) d.classList.remove('open');
  });

  dropdown.classList.toggle('open');
}

function selectCustomOption(type, value, labelText, dropdownId) {
  const dropdown = document.getElementById(dropdownId);
  if (!dropdown) return;

  if (type === 'style') {
    document.getElementById('style-select').value = value;
    document.getElementById('label-style').innerText = labelText;
  } else if (type === 'engine') {
    document.getElementById('engine-select').value = value;
    document.getElementById('label-engine').innerText = labelText;
  }

  dropdown.querySelectorAll('.dropdown-option').forEach(opt => opt.classList.remove('active'));
  event.target.classList.add('active');
  dropdown.classList.remove('open');
}

// Global click outside listener for dropdowns
document.addEventListener('click', (e) => {
  if (!e.target.closest('.custom-dropdown')) {
    document.querySelectorAll('.custom-dropdown').forEach(d => d.classList.remove('open'));
  }
});

// Toast Feedback System
function showToast(msg) {
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  toast.className = 'toast-msg';
  toast.innerText = msg;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 2500);
}

// Mobbin Trending Outfits Carousel
function renderTrendingCarousel() {
  const track = document.getElementById('carousel-track');
  if (!track) return;
  track.innerHTML = '';

  const trendingSamples = [
    { name: 'Oficina Minimalista', score: 98, top: 'Camisa Oxford Blanca', bottom: 'Pantalón de Vestir Negro', shoes: 'Zapatos de Cuero Café', tag: '💼 Oficina' },
    { name: 'Universidad Templado', score: 95, top: 'Buzo de Lana Gris', bottom: 'Jeans Azules Oscuros', shoes: 'Tenis Blancos Urbano', tag: '👟 Casual' },
    { name: 'Noche Elegante', score: 96, top: 'Camisa Oxford Azul', bottom: 'Pantalón Chino Beige', shoes: 'Botas de Cuero Negras', tag: '🎉 Fiesta' },
    { name: 'Urbano Streetwear', score: 92, top: 'Camiseta Negra Básica', bottom: 'Jeans Negros Ajustados', shoes: 'Tenis Blancos Urbano', tag: '🌆 Urbano' },
    { name: 'Cita Nocturna', score: 94, top: 'Suéter de Punto Marrón', bottom: 'Pantalón de Vestir Negro', shoes: 'Zapatos Formales Negros', tag: '🌹 Cita' }
  ];

  trendingSamples.forEach(sample => {
    const card = document.createElement('div');
    card.className = 'carousel-card';
    card.onclick = () => {
      showToast(`🔥 Viendo tendencia: ${sample.name}`);
      generateOutfits();
    };
    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 11.5px; font-weight: 800; background: rgba(168, 85, 247, 0.25); color: #c084fc; padding: 4px 12px; border-radius: 20px; border: 1px solid rgba(168, 85, 247, 0.4);">${sample.tag}</span>
        <span style="font-family: var(--font-display); font-weight: 900; font-size: 13px; color: #00ff9d;">${sample.score}% Match</span>
      </div>
      <div class="carousel-card-item" style="font-weight: 800; font-size: 15px; color: #fff; margin-top: 2px;">${sample.name}</div>
      <div style="font-size: 12.5px; color: var(--text-muted); display: flex; flex-direction: column; gap: 4px; overflow: hidden;">
        <span class="carousel-card-item">👔 ${sample.top}</span>
        <span class="carousel-card-item">👖 ${sample.bottom}</span>
        <span class="carousel-card-item">👟 ${sample.shoes}</span>
      </div>
    `;
    track.appendChild(card);
  });
}

// Mobbin "🎲 Sorpréndeme" Random Outfit Generator
function generateSurpriseOutfit() {
  const weatherKeys = Object.keys(WEATHER_CONFIG);
  const occasionKeys = Object.keys(OCCASION_CONFIG);
  
  const randomWeather = weatherKeys[Math.floor(Math.random() * weatherKeys.length)];
  const randomOccasion = occasionKeys[Math.floor(Math.random() * occasionKeys.length)];

  document.getElementById('weather-select').value = randomWeather;
  document.getElementById('event-select').value = randomOccasion;

  document.querySelectorAll('.visual-pill').forEach(pill => {
    if (pill.dataset.value === randomWeather || pill.dataset.value === randomOccasion) {
      pill.classList.add('active');
    }
  });

  generateOutfits();
  showToast(`🎲 Outfit Sorpresa generado para ${OCCASION_CONFIG[randomOccasion].label}!`);
}

// Live Search Filter
function handleLiveSearch(query) {
  const q = query.toLowerCase().trim();
  if (!q) {
    renderWardrobe('all');
    if (generatedOutfits.length > 0) {
      renderOutfits(generatedOutfits, 'Filtro', 'En vivo');
    }
    return;
  }

  const filteredItems = wardrobe.filter(i => 
    i.name.toLowerCase().includes(q) || 
    i.color.toLowerCase().includes(q) || 
    i.category.toLowerCase().includes(q)
  );
  
  const wContainer = document.getElementById('wardrobe-container');
  if (wContainer) {
    wContainer.innerHTML = '';
    filteredItems.forEach(item => {
      const card = document.createElement('div');
      card.className = 'item-card';
      card.innerHTML = `
        <div class="piece-icon">${CATEGORY_ICONS[item.category] || '👔'}</div>
        <div style="font-weight: 700; font-size: 14px; color: #fff;">${item.name}</div>
        <div style="font-size: 11px; color: var(--text-muted);">Color: ${item.color} | ${CATEGORY_LABELS[item.category]}</div>
      `;
      wContainer.appendChild(card);
    });
  }
}

// Visual Pills Selector
function selectPillOption(type, value, element) {
  const container = element.parentElement;
  container.querySelectorAll('.visual-pill').forEach(p => p.classList.remove('active'));
  element.classList.add('active');

  if (type === 'weather') {
    document.getElementById('weather-select').value = value;
  } else if (type === 'event') {
    document.getElementById('event-select').value = value;
  }
}

// Preset Loader
function loadPresetPack(packType, btnElement) {
  if (packType === 'full') {
    wardrobe = [...INITIAL_ITEMS];
  } else if (PRESET_PACKS[packType]) {
    wardrobe = [...PRESET_PACKS[packType]];
  }

  saveWardrobe();
  renderWardrobe('all');
  showToast(`✓ Armario cargado (${wardrobe.length} prendas)`);
}

// Init Wardrobe
function initWardrobe() {
  const saved = localStorage.getItem('styleai_wardrobe');
  if (saved) {
    try { wardrobe = JSON.parse(saved); } catch(e) { wardrobe = [...INITIAL_ITEMS]; }
  } else {
    wardrobe = [...INITIAL_ITEMS];
    saveWardrobe();
  }

  const savedFavs = localStorage.getItem('styleai_favs');
  if (savedFavs) {
    try { favoriteOutfits = JSON.parse(savedFavs); } catch(e) { favoriteOutfits = []; }
  }

  renderWardrobe('all');
  updateBadges();
  renderTrendingCarousel();
}

function saveWardrobe() {
  localStorage.setItem('styleai_wardrobe', JSON.stringify(wardrobe));
  updateBadges();
}

function updateBadges() {
  document.getElementById('items-count-badge').innerText = wardrobe.length;
  document.getElementById('favs-count-badge').innerText = favoriteOutfits.length;
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
  showToast(`✓ Prenda "${name}" guardada`);
}

function deleteItem(id) {
  if (confirm('¿Deseas eliminar esta prenda del armario?')) {
    wardrobe = wardrobe.filter(i => i.id !== id);
    saveWardrobe();
    renderWardrobe('all');
    showToast('✓ Prenda eliminada');
  }
}

function renderWardrobe(categoryFilter = 'all') {
  const container = document.getElementById('wardrobe-container');
  if (!container) return;
  container.innerHTML = '';

  const filtered = categoryFilter === 'all' ? wardrobe : wardrobe.filter(i => i.category === categoryFilter);

  if (filtered.length === 0) {
    container.innerHTML = `<div class="empty-state"><div style="font-size: 40px;">👕</div><p>No hay prendas en esta categoría.</p></div>`;
    return;
  }

  filtered.forEach(item => {
    const card = document.createElement('div');
    card.className = 'item-card';
    card.style.cssText = 'background: var(--bg-surface); border: 1.5px solid var(--border-subtle); padding: 16px; border-radius: 16px; position: relative; display: flex; flex-direction: column; gap: 8px;';
    card.innerHTML = `
      <button class="btn-delete" onclick="deleteItem('${item.id}')" title="Eliminar">✕</button>
      <div style="font-size: 28px;">${CATEGORY_ICONS[item.category] || '👔'}</div>
      <div style="font-weight: 700; font-size: 14px; color: #fff;">${item.name}</div>
      <div style="font-size: 11px; color: var(--text-muted);">${CATEGORY_LABELS[item.category]} • ${item.color}</div>
    `;
    container.appendChild(card);
  });
}

function filterCategory(cat, btn) {
  document.querySelectorAll('.visual-pill').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderWardrobe(cat);
}

function switchTab(tab) {
  document.getElementById('tab-outfits-btn').classList.toggle('active', tab === 'outfits');
  document.getElementById('tab-wardrobe-btn').classList.toggle('active', tab === 'wardrobe');
  document.getElementById('tab-favs-btn').classList.toggle('active', tab === 'favs');

  document.getElementById('tab-outfits').style.display = tab === 'outfits' ? 'block' : 'none';
  document.getElementById('tab-wardrobe').style.display = tab === 'wardrobe' ? 'block' : 'none';
  document.getElementById('tab-favs').style.display = tab === 'favs' ? 'block' : 'none';

  if (tab === 'favs') {
    renderFavorites();
  }
}

async function generateOutfits() {
  const weatherKey = document.getElementById('weather-select').value;
  const occasionKey = document.getElementById('event-select').value;
  const preferredStyle = document.getElementById('style-select').value;
  const engine = document.getElementById('engine-select').value;

  const targetFormality = OCCASION_CONFIG[occasionKey].formality;
  const weatherInfo = WEATHER_CONFIG[weatherKey];

  const tops = wardrobe.filter(i => i.category === 'top');
  const bottoms = wardrobe.filter(i => i.category === 'bottom');
  const shoes = wardrobe.filter(i => i.category === 'shoes');
  const outerwears = wardrobe.filter(i => i.category === 'outerwear');

  if (tops.length === 0 || bottoms.length === 0 || shoes.length === 0) {
    alert('Necesitas al menos una prenda Superior, una Inferior y Calzado en tu armario.');
    switchTab('wardrobe');
    return;
  }

  switchTab('outfits');
  const container = document.getElementById('outfits-container');
  container.innerHTML = `
    <div class="empty-state" style="padding: 48px;">
      <div style="font-size: 36px; animation: spin 1.2s infinite linear;">⚙️</div>
      <h3 style="color: #fff; font-family: var(--font-display);">Calculando combinaciones...</h3>
      <p>Analizando abrigo térmico, formalidad y colores.</p>
    </div>
  `;

  await new Promise(r => setTimeout(r, 250));

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
          generatedOutfits = [{
            top: data.outfit.top,
            bottom: data.outfit.bottom,
            shoes: data.outfit.shoes,
            outerwear: data.outfit.outerwear,
            score: data.matchScore,
            reasoning: data.aiReasoning
          }];
          renderOutfits(generatedOutfits, OCCASION_CONFIG[occasionKey].label, weatherInfo.label);
          showToast('⚡ Recomendación calculada');
          return;
        }
      }
    } catch (err) {
      console.warn('Servidor API no disponible. Utilizando motor por reglas local.', err);
    }
  }

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
  generatedOutfits = candidateCombinations.slice(0, 4);
  renderOutfits(generatedOutfits, OCCASION_CONFIG[occasionKey].label, weatherInfo.label);
  showToast('⚡ Combinaciones calculadas');
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
  if (formalityDiff <= 0.8) reasoning.push(`Cumple excelente el nivel de formalidad (${avgFormality.toFixed(1)}/5) para la ocasión.`);
  if (warmthScore >= 85) reasoning.push(`Proporciona abrigo térmico óptimo para clima ${weatherInfo.label}.`);
  if (colorScore >= 80) reasoning.push(`Excelente combinación de tonos (${top.color}, ${bottom.color} y ${shoes.color}).`);

  list.push({
    top, bottom, shoes, outerwear,
    score: Math.min(99, Math.max(60, totalScore)),
    reasoning: reasoning.join(' ') || 'Combinación equilibrada entre las prendas disponibles.'
  });
}

function renderOutfits(outfits, occasionLabel, weatherLabel) {
  const container = document.getElementById('outfits-container');
  document.getElementById('outfits-count-badge').innerText = outfits.length;

  if (outfits.length === 0) {
    container.innerHTML = `<div class="empty-state"><p>No se encontraron combinaciones.</p></div>`;
    return;
  }

  container.innerHTML = '';

  outfits.forEach((outfit, index) => {
    const card = document.createElement('div');
    card.className = 'mobbin-card';
    
    let piecesHtml = `
      <div class="piece-item">
        <div class="piece-icon">${CATEGORY_ICONS.top}</div>
        <div>
          <div style="font-size: 11.5px; color: var(--text-muted); font-weight: 600;">Superior</div>
          <div style="font-weight: 800; font-size: 14px; color: #fff;">${outfit.top.name}</div>
        </div>
      </div>

      <div class="piece-item">
        <div class="piece-icon">${CATEGORY_ICONS.bottom}</div>
        <div>
          <div style="font-size: 11.5px; color: var(--text-muted); font-weight: 600;">Inferior</div>
          <div style="font-weight: 800; font-size: 14px; color: #fff;">${outfit.bottom.name}</div>
        </div>
      </div>

      <div class="piece-item">
        <div class="piece-icon">${CATEGORY_ICONS.shoes}</div>
        <div>
          <div style="font-size: 11.5px; color: var(--text-muted); font-weight: 600;">Calzado</div>
          <div style="font-weight: 800; font-size: 14px; color: #fff;">${outfit.shoes.name}</div>
        </div>
      </div>
    `;

    if (outfit.outerwear) {
      piecesHtml += `
        <div class="piece-item">
          <div class="piece-icon">${CATEGORY_ICONS.outerwear}</div>
          <div>
            <div style="font-size: 11.5px; color: var(--text-muted); font-weight: 600;">Abrigo Extra</div>
            <div style="font-weight: 800; font-size: 14px; color: #fff;">${outfit.outerwear.name}</div>
          </div>
        </div>
      `;
    }

    const techBodyId = `tech-body-${index}`;
    const techArrowId = `tech-arrow-${index}`;

    card.innerHTML = `
      <div class="mobbin-card-header">
        <div>
          <h3 style="font-family: var(--font-display); font-size: 19px; font-weight: 800; color: #fff;">Outfit Recomendado #${index + 1}</h3>
          <span style="font-size: 13px; color: var(--accent-cyan); font-weight: 600;">${occasionLabel} • Clima ${weatherLabel}</span>
        </div>
        <div class="match-badge">${outfit.score}% Match</div>
      </div>

      <div class="outfit-pieces-grid">
        ${piecesHtml}
      </div>

      <div class="reasoning-box">
        <strong>💡 Justificación:</strong> ${outfit.reasoning}
      </div>

      <!-- Desplegable Técnico Interno -->
      <div style="border-top: 1.5px solid rgba(255, 255, 255, 0.1); padding-top: 12px;">
        <div style="display: flex; justify-content: space-between; align-items: center; cursor: pointer;" onclick="toggleAccordion('${techBodyId}', '${techArrowId}')">
          <span style="font-size: 13px; font-weight: 800; color: var(--accent-cyan); display: flex; align-items: center; gap: 6px;">
            📊 Desglose de Compatibilidad Térmica & Formalidad
          </span>
          <span id="${techArrowId}" class="accordion-arrow collapsed">▼</span>
        </div>

        <div id="${techBodyId}" class="accordion-body collapsed" style="margin-top: 12px; gap: 10px;">
          <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;">
            <div style="background: rgba(8, 13, 25, 0.8); padding: 12px; border-radius: 12px; border: 1px solid var(--border-subtle);">
              <div style="font-size: 11.5px; color: var(--text-dim);">Nivel Térmico Promedio</div>
              <div style="font-size: 15px; font-weight: 800; color: var(--accent-pink);">
                ${((outfit.top.warmth + outfit.bottom.warmth + outfit.shoes.warmth + (outfit.outerwear ? outfit.outerwear.warmth : 0)) / (outfit.outerwear ? 4 : 3)).toFixed(1)} / 5.0
              </div>
            </div>
            <div style="background: rgba(8, 13, 25, 0.8); padding: 12px; border-radius: 12px; border: 1px solid var(--border-subtle);">
              <div style="font-size: 11.5px; color: var(--text-dim);">Formalidad Promedio</div>
              <div style="font-size: 15px; font-weight: 800; color: var(--accent-emerald);">
                ${((outfit.top.formality + outfit.bottom.formality + outfit.shoes.formality + (outfit.outerwear ? outfit.outerwear.formality : 0)) / (outfit.outerwear ? 4 : 3)).toFixed(1)} / 5.0
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card-actions">
        <button class="btn-action btn-fav" onclick="toggleFavorite(${index})">⭐ Favorito</button>
        <button class="btn-action" onclick="copyOutfitToClipboard(${index})">📋 Copiar</button>
        <button class="btn-action" onclick="openOutfitModal(${index})">🔍 Detalle</button>
      </div>
    `;

    container.appendChild(card);
  });
}

function toggleFavorite(index) {
  const outfit = generatedOutfits[index];
  if (!outfit) return;

  const exists = favoriteOutfits.some(f => f.top.name === outfit.top.name && f.bottom.name === outfit.bottom.name);
  if (exists) {
    favoriteOutfits = favoriteOutfits.filter(f => !(f.top.name === outfit.top.name && f.bottom.name === outfit.bottom.name));
    showToast('⭐ Eliminado de Favoritos');
  } else {
    favoriteOutfits.push(outfit);
    showToast('⭐ Guardado en Favoritos!');
  }
  localStorage.setItem('styleai_favs', JSON.stringify(favoriteOutfits));
  updateBadges();
}

function renderFavorites() {
  const container = document.getElementById('favs-container');
  if (!container) return;
  container.innerHTML = '';

  if (favoriteOutfits.length === 0) {
    container.innerHTML = `<div class="empty-state"><div style="font-size: 40px;">⭐</div><p>No has guardado outfits favoritos aún.</p></div>`;
    return;
  }

  favoriteOutfits.forEach((outfit, index) => {
    const card = document.createElement('div');
    card.className = 'mobbin-card';
    card.innerHTML = `
      <div class="mobbin-card-header">
        <h3 style="font-family: var(--font-display); font-size: 16px; font-weight: 700; color: #fff;">Favorito #${index + 1}</h3>
        <div class="match-badge">${outfit.score}% Match</div>
      </div>
      <div style="font-size: 13px; color: var(--text-main);">
        👔 ${outfit.top.name} • 👖 ${outfit.bottom.name} • 👟 ${outfit.shoes.name}
      </div>
    `;
    container.appendChild(card);
  });
}

function openOutfitModal(index) {
  const outfit = generatedOutfits[index];
  if (!outfit) return;

  document.getElementById('modal-title').innerText = `Outfit Recomendado #${index + 1} (${outfit.score}% Match)`;
  
  let modalHtml = `
    <div style="display: flex; flex-direction: column; gap: 16px;">
      <div style="background: rgba(168, 85, 247, 0.12); border: 1.5px solid rgba(168, 85, 247, 0.35); padding: 16px; border-radius: 14px;">
        <strong style="color: #c084fc;">💡 Justificación Completa:</strong>
        <p style="margin-top: 6px; font-size: 14px; color: #e2e8f0;">${outfit.reasoning}</p>
      </div>

      <h4 style="font-family: var(--font-display); font-size: 16px; color: #fff;">Prendas del Conjunto:</h4>
      <ul style="list-style: none; display: flex; flex-direction: column; gap: 10px;">
        <li style="background: rgba(14, 21, 37, 0.9); padding: 12px 16px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center;">
          <span>👔 <strong>Superior:</strong> ${outfit.top.name}</span>
          <span style="font-size: 12px; color: var(--text-muted);">Color: ${outfit.top.color}</span>
        </li>
        <li style="background: rgba(14, 21, 37, 0.9); padding: 12px 16px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center;">
          <span>👖 <strong>Inferior:</strong> ${outfit.bottom.name}</span>
          <span style="font-size: 12px; color: var(--text-muted);">Color: ${outfit.bottom.color}</span>
        </li>
        <li style="background: rgba(14, 21, 37, 0.9); padding: 12px 16px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center;">
          <span>👟 <strong>Calzado:</strong> ${outfit.shoes.name}</span>
          <span style="font-size: 12px; color: var(--text-muted);">Color: ${outfit.shoes.color}</span>
        </li>
        ${outfit.outerwear ? `
        <li style="background: rgba(14, 21, 37, 0.9); padding: 12px 16px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center;">
          <span>🧥 <strong>Abrigo:</strong> ${outfit.outerwear.name}</span>
          <span style="font-size: 12px; color: var(--text-muted);">Color: ${outfit.outerwear.color}</span>
        </li>` : ''}
      </ul>

      <button class="btn btn-primary" onclick="copyOutfitToClipboard(${index})" style="margin-top: 8px;">
        📋 Copiar al Portapapeles
      </button>
    </div>
  `;

  document.getElementById('modal-body').innerHTML = modalHtml;
  document.getElementById('detail-modal').classList.add('open');
}

function closeModal(event) {
  if (event && event.target !== document.getElementById('detail-modal')) return;
  document.getElementById('detail-modal').classList.remove('open');
}

function copyOutfitToClipboard(index) {
  const outfit = generatedOutfits[index];
  if (!outfit) return;

  const text = `Outfit StyleAI (${outfit.score}% Match):\n- Superior: ${outfit.top.name}\n- Inferior: ${outfit.bottom.name}\n- Calzado: ${outfit.shoes.name}${outfit.outerwear ? '\n- Abrigo: ' + outfit.outerwear.name : ''}\n\nJustificación: ${outfit.reasoning}`;

  navigator.clipboard.writeText(text).then(() => {
    showToast('📋 Outfit copiado al portapapeles');
  }).catch(() => {
    showToast('📋 Outfit copiado');
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initWardrobe();
});
