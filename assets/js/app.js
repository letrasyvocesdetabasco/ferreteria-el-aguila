/**
 * Ferretería y Tlapalería El Águila - Villahermosa, Tabasco
 * Motor Comercial e Interactivo de Catálogo, Sucursales y Cotizaciones WhatsApp
 */

// ==========================================================================
// 1. Configuración y Sucursales en Villahermosa
// ==========================================================================
const CONFIG = {
  SUPABASE_URL: "https://TU_PROYECTO.supabase.co",
  SUPABASE_ANON_KEY: "TU_CLAVE_ANONIMA",
  FALLBACK_DATA_URL: "data/products.json",
  STORAGE_CART_KEY: "elaguila_quote_cart",
  STORAGE_BRANCH_KEY: "elaguila_selected_branch",
  STORAGE_CUSTOMER_KEY: "el_aguila_customer_profile"
};

const BRANCHES = {
  delicias: {
    id: "delicias",
    active: true,
    name: "Sucursal Las Delicias",
    owner: "Timoteo Méndez",
    address: "Av. Revolución 1203, Cuadrante II, Las Delicias, C.P. 86140, Villahermosa, Tab.",
    landmark: "A un lado del Centro de Salud San Joaquín",
    city: "Villahermosa, Tabasco",
    phone: "993 289 2935",
    whatsapp: "529932892935",
    mapsUrl: "https://maps.app.goo.gl/vkQLYW1u62gbRRDf7",
    badge: "Sucursal Las Delicias",
    image: "assets/images/branches/fachada-delicias-tito.webp",
    isMatriz: false,
    schedule: "Lunes a Viernes: 8:00 a 18:00 hrs | Sábado: 8:00 a 15:00 hrs | Domingo: 9:00 a 14:00 hrs"
  },
  buenavista: {
    id: "buenavista",
    active: true,
    name: "Sucursal Estrellas de Buena Vista",
    owner: "Timoteo Méndez",
    address: "Carr. Villahermosa a La Isla Km 5.300, Buena Vista 1ra Secc, C.P. 86280, Villahermosa, Tab.",
    landmark: "Buena Vista 1ra Secc",
    city: "Villahermosa, Tabasco",
    phone: "993 192 8313",
    whatsapp: "529931928313",
    mapsUrl: "https://maps.app.goo.gl/w1FCsu9A2V2WqvCu5",
    badge: "Sucursal Buena Vista",
    image: "assets/images/branches/fachada-buenavista.webp",
    isMatriz: false,
    schedule: "Lunes a Viernes: 8:00 a 18:00 hrs | Sábado: 8:00 a 15:00 hrs | Domingo: 9:00 a 14:00 hrs"
  },
  gaviotas: {
    id: "gaviotas",
    active: false, // Solo exhibición: sin interacción (decorativa)
    name: "Sucursal Gaviotas Norte",
    owner: "Miguel Méndez",
    address: "Aquiles Calderón Marchena 120, Col. Gaviotas Nte., C.P. 86068, Villahermosa, Tab.",
    landmark: "Aquiles Calderón Marchena",
    city: "Villahermosa, Tabasco",
    phone: "993 200 1178",
    whatsapp: "529932001178",
    onlyWhatsApp: true,
    mapsUrl: "https://maps.app.goo.gl/qWtBwNkb8vABa5Wj8",
    badge: "Sucursal Gaviotas Norte",
    image: "assets/images/branches/fachada-gaviotas-miguel.webp",
    isMatriz: false,
    schedule: "Todos los días: 8:00 a 18:00 hrs (8:00 am a 6:00 pm)"
  },
  hidalgo: {
    id: "hidalgo",
    active: false, // Solo exhibición: sin interacción (decorativa)
    name: "Sucursal Miguel Hidalgo III Etapa",
    owner: "Salomón Méndez",
    address: "Carr. Villahermosa a La Isla, Miguel Hidalgo III Etapa, C.P. 86126, Villahermosa, Tab.",
    landmark: "Carretera a La Isla III Etapa",
    city: "Villahermosa, Tabasco",
    phone: "993 141 2679",
    whatsapp: "529931412679",
    mapsUrl: "https://maps.app.goo.gl/xnaBo218rGoQQvMZ7",
    badge: "Sucursal Miguel Hidalgo",
    image: "assets/images/branches/fachada-hidalgo-salomon.webp",
    isMatriz: false,
    schedule: "Lun a Vie: 8:00 a 18:30 hrs | Sáb: 8:00 a 17:00 hrs | Dom: 8:00 a 13:00 hrs"
  },
  joem: {
    id: "joem",
    active: false, // Solo exhibición: sin interacción (decorativa)
    name: "Sucursal Joem",
    owner: "Salomón Méndez",
    address: "Carr. Villahermosa a La Isla, Col. Miguel Hidalgo I, C.P. 86280, Villahermosa, Tab.",
    landmark: "Carretera a La Isla (Ferretería Joem)",
    city: "Villahermosa, Tabasco",
    phone: "Atención en mostrador",
    whatsapp: "",
    noDirectPhone: true,
    noWhatsApp: true,
    mapsUrl: "https://maps.app.goo.gl/y2qguKEAUhhGPpfw5",
    badge: "Sucursal Joem",
    image: "assets/images/branches/fachada-joem.webp",
    isMatriz: false,
    schedule: "Lunes a Viernes: 8:00 a 18:00 hrs | Sábado: 8:00 a 15:00 hrs"
  }
};

// Solo las sucursales activas (Las Delicias y Estrellas de Buena Vista) reciben
// cotizaciones, llamadas o selección. Las demás se muestran como exhibición.
function isActiveBranch(branchId) {
  return !!(BRANCHES[branchId] && BRANCHES[branchId].active);
}

function safeStorageGet(key) {
  try { return localStorage.getItem(key); } catch (_) { return null; }
}
function safeStorageSet(key, value) {
  try { localStorage.setItem(key, value); } catch (_) {}
}

// ==========================================================================
// 2. Estado Global de la Aplicación
// ==========================================================================
const storedBranchId = safeStorageGet(CONFIG.STORAGE_BRANCH_KEY);
const initialBranch = isActiveBranch(storedBranchId) ? storedBranchId : "delicias";

const AppState = {
  masterCatalog: [],
  filteredCatalog: [],
  displayedCount: 36,
  pageSize: 36,
  selectedBranch: initialBranch,
  filterCategory: "all",
  filterBrand: "all",
  searchTerm: "",
  sortMode: "relevance",
  quoteCart: new Map(), // SKU -> { item, quantity }
  isSupabaseActive: false,
  autoExpandedToAll: false,
  autoExpandedOrigin: null
};

let supabaseClient = null;

// ==========================================================================
// 3. Inicialización y Carga de Datos (Doble Fase)
// ==========================================================================
document.addEventListener("DOMContentLoaded", () => {
  initBranchSelector();
  initCartFromStorage();
  initEventListeners();
  initMobileEnhancements();
  loadCatalogData();
});

async function loadCatalogData() {
  const counterElem = document.getElementById("counter-display");
  if (counterElem) counterElem.textContent = "Conectando con inventario técnico...";

  const supabaseConfigured = CONFIG.SUPABASE_URL && !CONFIG.SUPABASE_URL.includes("TU_PROYECTO");
  if (supabaseConfigured && typeof supabase === "undefined") {
    try {
      await loadExternalScript("https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2");
    } catch (_) { /* sin conexión al CDN: se usa el respaldo local */ }
  }

  if (
    typeof supabase !== "undefined" &&
    supabaseConfigured
  ) {
    try {
      supabaseClient = supabase.createClient(CONFIG.SUPABASE_URL, CONFIG.SUPABASE_ANON_KEY);
      const { data, error } = await supabaseClient
        .from("products")
        .select("sku,manufacturer_code,name,slug,base_price,unit_measure,stock_status,attributes,image,badge,description,categories(name,slug),brands(name)")
        .eq("is_active", true)
        .order("name", { ascending: true });

      if (!error && Array.isArray(data) && data.length > 0) {
        AppState.masterCatalog = data;
        AppState.isSupabaseActive = true;
      } else {
        throw new Error(error?.message || "Sin datos en Supabase");
      }
    } catch (sbErr) {
      await loadFallbackCatalog();
    }
  } else {
    await loadFallbackCatalog();
  }

  // Precompute lowercase search index on each item for sub-10ms queries
  if (Array.isArray(AppState.masterCatalog)) {
    for (let i = 0; i < AppState.masterCatalog.length; i++) {
      const item = AppState.masterCatalog[i];
      const catName = item.category || item.categories?.name || "";
      const brandName = item.brand || item.brands?.name || "";
      item._s = normalizeText(
        (item.sku || "") + " " +
        (item.manufacturer_code || "") + " " +
        (item.name || "") + " " +
        brandName + " " +
        catName
      );
      item._n = normalizeText(item.name || "");
      item._img = resolveProductImage(item);
      item._photo = item._img.indexOf("assets/images/products/") === 0;
      // Orden base: primero artículos con foto real, al final nombres con símbolos "(BAJE)", "#", etc.
      item._base = (item._photo ? 0 : 2) + (/^[a-z0-9ñ]/.test(item._n) ? 0 : 4);
      item._i = i;
    }

    // Vista inicial variada: se intercalan los artículos con foto por tipo de producto
    // (válvula, broca, candado, dado…) en lugar de mostrar 30 abrazaderas seguidas.
    const seenByWord = new Map();
    for (let i = 0; i < AppState.masterCatalog.length; i++) {
      const item = AppState.masterCatalog[i];
      if (!item._photo) { item._mix = 0; continue; }
      const word = (item._n.match(/^[a-z0-9ñ]+/) || [""])[0];
      const n = seenByWord.get(word) || 0;
      seenByWord.set(word, n + 1);
      item._mix = n;
    }

    // Refresh prices of any items currently stored in AppState.quoteCart
    if (AppState.quoteCart && AppState.quoteCart.size > 0) {
      const catalogMap = new Map(AppState.masterCatalog.map(p => [p.sku, p]));
      let cartUpdated = false;
      for (const [sku, cartEntry] of AppState.quoteCart.entries()) {
        const freshItem = catalogMap.get(sku);
        if (freshItem) {
          cartEntry.item = freshItem;
          cartUpdated = true;
        }
      }
      if (cartUpdated) {
        saveCartToStorage();
        updateCartUI();
      }
    }
  }

  generateFacetFilters();
  applyStateFromUrl();
  applyFilterPipeline();
  AppState.catalogReady = true;
}

function loadExternalScript(src) {
  return new Promise((resolve, reject) => {
    const s = document.createElement("script");
    s.src = src;
    s.async = true;
    s.onload = resolve;
    s.onerror = reject;
    document.head.appendChild(s);
  });
}

async function loadFallbackCatalog() {
  try {
    const response = await fetch(CONFIG.FALLBACK_DATA_URL);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    AppState.masterCatalog = data;
    AppState.isSupabaseActive = false;
  } catch (err) {
    console.error("Error al cargar data/products.json:", err);
    const counterElem = document.getElementById("counter-display");
    if (counterElem) {
      if (window.location.protocol === "file:") {
        counterElem.innerHTML = `<span style="color: #c9242b; font-weight: bold;">⚠️ Abierto mediante file://. Por seguridad del navegador (CORS), debes abrir la tienda en tu servidor local: <a href="http://localhost:8080" style="text-decoration: underline; color: #0284c7;">http://localhost:8080</a></span>`;
      } else {
        counterElem.textContent = "No se pudo cargar el catálogo.";
      }
    }
    const grid = document.getElementById("products-container");
    if (grid && window.location.protocol !== "file:") {
      grid.innerHTML = `
        <div class="senior-empty-card">
          <div class="senior-empty-icon">📶</div>
          <h3 class="senior-empty-title">Señal débil: no cargó el catálogo</h3>
          <p class="senior-empty-desc">Revisa tu internet y vuelve a intentar. También puedes mandarnos tu lista de materiales directo por WhatsApp.</p>
          <div class="senior-empty-actions">
            <button class="btn-senior-reset" onclick="location.reload()"><span>🔄 Reintentar</span></button>
            <a class="btn-senior-wa" href="https://wa.me/${BRANCHES[AppState.selectedBranch].whatsapp}" target="_blank" rel="noopener"><span>💬 Mandar lista por WhatsApp</span></a>
          </div>
        </div>`;
    }
  }
}

// ==========================================================================
// 4. Sucursales en Villahermosa
// ==========================================================================
function openBranchSelectorDropdown(e) {
  const sel = document.getElementById("branch-select");
  if (!sel) return;
  if (e && e.target === sel) return;
  if (typeof sel.showPicker === "function") {
    try {
      sel.showPicker();
      return;
    } catch (_) {}
  }
  sel.focus();
}
window.openBranchSelectorDropdown = openBranchSelectorDropdown;

function initBranchSelector() {
  const select = document.getElementById("branch-select");
  if (select) {
    select.value = AppState.selectedBranch;
    select.addEventListener("change", (e) => setBranch(e.target.value));
  }

  const selectorBlock = document.getElementById("header-branch-selector");
  if (selectorBlock) {
    selectorBlock.addEventListener("click", openBranchSelectorDropdown);
  }

  updateBranchUI(AppState.selectedBranch);
}

function setBranch(branchId) {
  if (!isActiveBranch(branchId)) {
    // Sucursal de exhibición: se ignora y se mantiene la selección vigente
    const select = document.getElementById("branch-select");
    if (select) select.value = AppState.selectedBranch;
    return;
  }
  AppState.selectedBranch = branchId;
  safeStorageSet(CONFIG.STORAGE_BRANCH_KEY, branchId);
  updateBranchUI(branchId);
  if (typeof saveCustomerDataToCache === "function") {
    saveCustomerDataToCache();
  }
}

function updateBranchUI(branchId) {
  const branch = BRANCHES[branchId];
  if (!branch) return;

  const select = document.getElementById("branch-select");
  if (select) select.value = branchId;

  // Actualizar tarjetas selectoras dentro del cajón de cotización
  document.querySelectorAll(".drawer-branch-card").forEach((card) => {
    if (card.dataset.branchId === branchId) {
      card.classList.add("active");
    } else {
      card.classList.remove("active");
    }
  });

  const drawerBranchName = document.getElementById("drawer-selected-branch-name");
  if (drawerBranchName) drawerBranchName.textContent = branch.name;

  const drawerBranchPhone = document.getElementById("drawer-selected-branch-phone");
  if (drawerBranchPhone) drawerBranchPhone.textContent = branch.phone;

  // Actualizar texto del botón de despacho en el cajón de cotización
  const sendWhatsAppBtn = document.getElementById("whatsapp-order-btn");
  if (sendWhatsAppBtn) {
    const shortName = branch.id === "buenavista" ? "Buena Vista" : "Las Delicias";
    sendWhatsAppBtn.innerHTML = `<span>💬 Enviar a ${shortName} por WhatsApp</span>`;
    sendWhatsAppBtn.style.opacity = "1";
  }

  // Botón "Llamar" de la barra inferior y del hero: marca a la sucursal elegida
  const telHref = "tel:" + branch.phone.replace(/\D/g, "");
  document.querySelectorAll("[data-call-selected-branch]").forEach((a) => {
    a.href = telHref;
    a.setAttribute("aria-label", `Llamar a ${branch.name}`);
  });
  document.querySelectorAll("[data-selected-branch-name]").forEach((el) => {
    el.textContent = branch.id === "buenavista" ? "Buena Vista" : "Las Delicias";
  });

  // Actualizar botón flotante de WhatsApp y barra fija móvil
  const floatingWa = document.getElementById("floating-wa-btn");
  const mobileNavWa = document.getElementById("mobile-nav-wa");
  const targetWaNumber = branch.whatsapp || BRANCHES.delicias.whatsapp;
  const waUrl = `https://wa.me/${targetWaNumber}?text=${encodeURIComponent("Hola Ferretería El Águila (" + branch.name + "), me gustaría consultar existencias y cotizar un material.")}`;
  if (floatingWa) floatingWa.href = waUrl;
  if (mobileNavWa) mobileNavWa.href = waUrl;

  // Actualizar tarjetas de sucursal destacadas
  document.querySelectorAll(".branch-feature-card").forEach((card) => {
    if (!isActiveBranch(card.dataset.branchId)) return;
    if (card.dataset.branchId === branchId) {
      card.classList.add("selected-branch");
      const btn = card.querySelector(".btn-branch-select-store");
      if (btn) btn.textContent = "✓ Sucursal Seleccionada para Cotizar";
    } else {
      card.classList.remove("selected-branch");
      const btn = card.querySelector(".btn-branch-select-store");
      if (btn) btn.textContent = "Seleccionar esta Sucursal";
    }
  });
}

// ==========================================================================
// 5. Facetas y Pipeline de Filtrado
// ==========================================================================
function generateFacetFilters() {
  const categoryMap = new Map();
  const brandMap = new Map();

  AppState.masterCatalog.forEach((prod) => {
    const catName = prod.category || prod.categories?.name || "General";
    categoryMap.set(catName, (categoryMap.get(catName) || 0) + 1);

    const brandName = prod.brand || prod.brands?.name || "Homologado";
    brandMap.set(brandName, (brandMap.get(brandName) || 0) + 1);
  });

  const catList = document.getElementById("categories-facet");
  if (catList) {
    catList.innerHTML = `
      <li class="facet-item ${AppState.filterCategory === "all" ? "active" : ""}" data-category="all">
        <span>Todos los Departamentos</span>
        <span class="facet-count">${AppState.masterCatalog.length.toLocaleString('es-MX')}</span>
      </li>
    `;
    const sortedCats = Array.from(categoryMap.entries()).sort((a, b) => b[1] - a[1]);
    sortedCats.forEach(([name, count]) => {
      const li = document.createElement("li");
      li.className = `facet-item ${AppState.filterCategory === name ? "active" : ""}`;
      li.dataset.category = name;
      li.innerHTML = `<span>${escapeHtml(name)}</span><span class="facet-count">${count.toLocaleString('es-MX')}</span>`;
      li.onclick = () => {
        AppState.filterCategory = name;
        updateFacetSelection();
        applyFilterPipeline();
        syncUrlState();
      };
      catList.appendChild(li);
    });

    catList.firstElementChild.onclick = () => {
      AppState.filterCategory = "all";
      updateFacetSelection();
      applyFilterPipeline();
      syncUrlState();
    };
  }

  const brandList = document.getElementById("brands-facet");
  if (brandList) {
    brandList.innerHTML = `
      <li class="facet-item ${AppState.filterBrand === "all" ? "active" : ""}" data-brand="all">
        <span>Todas las Marcas</span>
        <span class="facet-count">${AppState.masterCatalog.length.toLocaleString('es-MX')}</span>
      </li>
    `;
    const sortedBrands = Array.from(brandMap.entries()).sort((a, b) => b[1] - a[1]);
    sortedBrands.forEach(([name, count]) => {
      const li = document.createElement("li");
      li.className = `facet-item ${AppState.filterBrand === name ? "active" : ""}`;
      li.dataset.brand = name;
      li.innerHTML = `<span>${escapeHtml(name)}</span><span class="facet-count">${count.toLocaleString('es-MX')}</span>`;
      li.onclick = () => {
        AppState.filterBrand = name;
        updateFacetSelection();
        applyFilterPipeline();
        syncUrlState();
      };
      brandList.appendChild(li);
    });

    brandList.firstElementChild.onclick = () => {
      AppState.filterBrand = "all";
      updateFacetSelection();
      applyFilterPipeline();
      syncUrlState();
    };
  }
}

function updateFacetSelection() {
  document.querySelectorAll("#categories-facet .facet-item").forEach((el) => {
    el.classList.toggle("active", el.dataset.category === AppState.filterCategory);
  });
  document.querySelectorAll("#brands-facet .facet-item").forEach((el) => {
    el.classList.toggle("active", el.dataset.brand === AppState.filterBrand);
  });
}

// --------------------------------------------------------------------------
// Búsqueda tolerante: sin acentos, plurales y orden por relevancia
// ("valvulas" encuentra "Válvula", "tornillos" encuentra "Tornillo")
// --------------------------------------------------------------------------
function normalizeText(str) {
  return String(str || "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function stemToken(token) {
  if (token.length <= 3 || /\d/.test(token)) return token;
  if (token.endsWith("ces")) return token.slice(0, -3) + "z";      // luces -> luz
  if (/[lnrdj]es$/.test(token)) return token.slice(0, -2);         // conexiones -> conexion
  if (token.endsWith("s")) return token.slice(0, -1);              // tornillos -> tornillo
  return token;
}

function buildSearchTokens(rawQuery) {
  const query = normalizeText(rawQuery);
  if (!query) return [];
  return query.split(" ").filter(Boolean).map(stemToken);
}

function itemSearchIndex(item) {
  if (!item._s) {
    item._s = normalizeText(
      (item.sku || "") + " " + (item.manufacturer_code || "") + " " + (item.name || "") + " " +
      (item.brand || item.brands?.name || "") + " " + (item.category || item.categories?.name || "")
    );
  }
  return item._s;
}

function scoreItem(item, tokens, rawNorm) {
  const name = item._n || normalizeText(item.name);
  let score = 0;
  const sku = normalizeText(item.sku);
  const code = normalizeText(item.manufacturer_code);
  if (rawNorm && (sku === rawNorm || code === rawNorm)) score += 1000;
  if (tokens.length && name.startsWith(tokens[0])) score += 300;
  for (let i = 0; i < tokens.length; i++) {
    const t = tokens[i];
    const pos = name.indexOf(t);
    if (pos === 0 || (pos > 0 && /[\s\-\/(,.]/.test(name[pos - 1]))) score += 40;
    else if (pos > 0) score += 10;
  }
  if (item._photo) score += 6;
  if (!/^[a-z0-9ñ]/.test(name)) score -= 50;
  score -= Math.min(name.length, 80) * 0.05;
  return score;
}

function applyFilterPipeline() {
  const tokens = buildSearchTokens(AppState.searchTerm);
  const hasActiveFilters = AppState.filterCategory !== "all" || AppState.filterBrand !== "all";

  const matchSearch = (item) => {
    if (tokens.length === 0) return true;
    const searchIndex = itemSearchIndex(item);
    for (let i = 0; i < tokens.length; i++) {
      if (searchIndex.indexOf(tokens[i]) === -1) return false;
    }
    return true;
  };

  // 1. Filtrado normal con departamento y marca actualmente seleccionados
  let filtered = AppState.masterCatalog.filter((item) => {
    const catName = item.category || item.categories?.name || "";
    const passCat =
      AppState.filterCategory === "all" ||
      catName.toLowerCase() === AppState.filterCategory.toLowerCase();

    const brandName = item.brand || item.brands?.name || "";
    const passBrand =
      AppState.filterBrand === "all" ||
      brandName.toLowerCase() === AppState.filterBrand.toLowerCase();

    return passCat && passBrand && matchSearch(item);
  });

  // 2. LÓGICA SENIOR-FRIENDLY (Adultos Mayores):
  // Si el usuario escribió una búsqueda y arrojó 0 resultados bajo el filtro activo,
  // pero el producto SÍ existe en el inventario general de la tienda:
  let autoExpanded = false;
  let autoExpandedOrigin = null;

  if (filtered.length === 0 && tokens.length > 0 && hasActiveFilters) {
    const globalMatches = AppState.masterCatalog.filter(matchSearch);
    if (globalMatches.length > 0) {
      filtered = globalMatches;
      autoExpanded = true;
      autoExpandedOrigin = {
        category: AppState.filterCategory,
        brand: AppState.filterBrand
      };
    }
  }

  // 3. Búsqueda aproximada: si "pijas tablaroca" no da nada, se muestran los que
  //    coinciden con la mayor cantidad de palabras (ej. todas las pijas).
  let partialMatch = false;
  if (filtered.length === 0 && tokens.length > 1) {
    let best = 0;
    const counts = new Map();
    AppState.masterCatalog.forEach((item) => {
      const idx = itemSearchIndex(item);
      let c = 0;
      for (let i = 0; i < tokens.length; i++) if (idx.indexOf(tokens[i]) !== -1) c++;
      if (c > 0) {
        counts.set(item, c);
        if (c > best) best = c;
      }
    });
    if (best > 0) {
      filtered = [];
      counts.forEach((c, item) => { if (c === best) filtered.push(item); });
      partialMatch = true;
    }
  }
  AppState.partialMatch = partialMatch;

  AppState.filteredCatalog = filtered;
  AppState.autoExpandedToAll = autoExpanded;
  AppState.autoExpandedOrigin = autoExpandedOrigin;
  AppState.displayedCount = AppState.pageSize;
  AppState.autoLoads = 0;

  updateSeniorAlertBanner();
  sortCatalog();
  renderCatalogGrid();
}

function updateSeniorAlertBanner() {
  const alertBox = document.getElementById("search-senior-alert");
  if (!alertBox) return;

  if (AppState.partialMatch) {
    alertBox.style.display = "flex";
    alertBox.className = "search-senior-alert";
    alertBox.innerHTML = `
      <div class="search-senior-alert-content">
        <span class="search-senior-alert-icon">💡</span>
        <div>
          <div class="search-senior-alert-title">No hay coincidencia exacta para "${escapeHtml(AppState.searchTerm)}"</div>
          <div class="search-senior-alert-desc">Te mostramos los artículos más parecidos. Si no ves lo que necesitas, pregúntanos por WhatsApp.</div>
        </div>
      </div>
    `;
    return;
  }

  if (AppState.autoExpandedToAll && AppState.autoExpandedOrigin) {
    const origCat = AppState.autoExpandedOrigin.category !== "all" ? AppState.autoExpandedOrigin.category : "";
    const origBrand = AppState.autoExpandedOrigin.brand !== "all" ? AppState.autoExpandedOrigin.brand : "";
    const originLabel = [origCat, origBrand].filter(Boolean).join(" / ");

    alertBox.style.display = "flex";
    alertBox.className = "search-senior-alert";
    alertBox.innerHTML = `
      <div class="search-senior-alert-content">
        <span class="search-senior-alert-icon">💡</span>
        <div>
          <div class="search-senior-alert-title">¡Buscamos en toda la ferretería para ti!</div>
          <div class="search-senior-alert-desc">
            No había resultados para <strong>"${escapeHtml(AppState.searchTerm)}"</strong> dentro de <em>${escapeHtml(originLabel)}</em>, pero <strong>encontramos ${AppState.filteredCatalog.length.toLocaleString('es-MX')} productos</strong> en otros departamentos de la tienda.
          </div>
        </div>
      </div>
      <button class="search-senior-alert-btn" onclick="resetAllFiltersKeepSearch()">Limpiar filtro y ver todo</button>
    `;
  } else {
    alertBox.style.display = "none";
    alertBox.innerHTML = "";
  }
}

function sortCatalog() {
  switch (AppState.sortMode) {
    case "relevance": {
      const tokens = buildSearchTokens(AppState.searchTerm);
      if (tokens.length) {
        const rawNorm = normalizeText(AppState.searchTerm);
        AppState.filteredCatalog.forEach((it) => { it._score = scoreItem(it, tokens, rawNorm); });
        AppState.filteredCatalog.sort((a, b) => (b._score - a._score) || ((a._i || 0) - (b._i || 0)));
      } else {
        AppState.filteredCatalog.sort((a, b) =>
          ((a._base || 0) - (b._base || 0)) || ((a._mix || 0) - (b._mix || 0)) || ((a._i || 0) - (b._i || 0)));
      }
      break;
    }
    case "price-asc":
      AppState.filteredCatalog.sort((a, b) => parseFloat(a.base_price) - parseFloat(b.base_price));
      break;
    case "price-desc":
      AppState.filteredCatalog.sort((a, b) => parseFloat(b.base_price) - parseFloat(a.base_price));
      break;
    case "name-desc":
      AppState.filteredCatalog.sort((a, b) => b.name.localeCompare(a.name));
      break;
    case "name-asc":
    default:
      // data/products.json ya viene ordenado por nombre; se restaura el orden original.
      AppState.filteredCatalog.sort((a, b) => (a._i || 0) - (b._i || 0));
      break;
  }
}

// ==========================================================================
// 6. Renderizado de Productos con Paginación y Carga Progresiva
// ==========================================================================
function renderCatalogGrid() {
  const grid = document.getElementById("products-container");
  const counter = document.getElementById("counter-display");
  const paginationBox = document.getElementById("pagination-container");
  if (!grid) return;

  grid.innerHTML = "";
  const totalCount = AppState.filteredCatalog.length;
  const currentShowing = Math.min(AppState.displayedCount, totalCount);

  if (counter) {
    counter.textContent = buildCounterText(currentShowing, totalCount);
  }

  if (totalCount === 0) {
    const branch = BRANCHES[AppState.selectedBranch] || BRANCHES.delicias;
    const waQueryUrl = `https://wa.me/${branch.whatsapp}?text=${encodeURIComponent("Hola Ferretería El Águila (" + branch.name + "), busco en la página web y no encontré: " + AppState.searchTerm + ". ¿Tienen disponible o me pueden cotizar un equivalente?")}`;

    grid.innerHTML = `
      <div class="senior-empty-card">
        <div class="senior-empty-icon">🔍</div>
        <h3 class="senior-empty-title">No encontramos resultados exactos para "${escapeHtml(AppState.searchTerm)}"</h3>
        <p class="senior-empty-desc">
          En ferretería, muchas piezas tienen diferentes medidas o nombres técnicos. <strong>Pregúntanos por WhatsApp</strong> y un encargado del mostrador te confirma existencias de inmediato.
        </p>
        
        <div class="senior-empty-actions">
          <a href="${waQueryUrl}" target="_blank" rel="noopener" class="btn-senior-wa">
            <span>💬 Preguntar en Mostrador (${branch.name})</span>
          </a>
          <button class="btn-senior-reset" onclick="resetAllFilters()">
            <span>🔄 Ver los 17,641 Productos</span>
          </button>
        </div>

        <div class="senior-quick-suggestions">
          <span>Búsquedas frecuentes en 1 clic:</span>
          <div class="senior-quick-pills">
            <button type="button" class="senior-pill-btn" onclick="quickSearch('Tornillo')">🔩 Tornillos</button>
            <button type="button" class="senior-pill-btn" onclick="quickSearch('PVC')">🚰 Tubo PVC</button>
            <button type="button" class="senior-pill-btn" onclick="quickSearch('Cable THW')">⚡ Cable THW</button>
            <button type="button" class="senior-pill-btn" onclick="quickSearch('Fandeli')">🎨 Lijas Fandeli</button>
            <button type="button" class="senior-pill-btn" onclick="quickSearch('Cobre')">🚰 Tubo Cobre</button>
            <button type="button" class="senior-pill-btn" onclick="quickSearch('Broca')">🛠️ Brocas</button>
            <button type="button" class="senior-pill-btn" onclick="quickSearch('Mezcladora')">🚿 Mezcladoras</button>
          </div>
        </div>
      </div>
    `;
    if (paginationBox) paginationBox.innerHTML = "";
    return;
  }

  const itemsToRender = AppState.filteredCatalog.slice(0, AppState.displayedCount);
  appendCardsToGrid(grid, itemsToRender);
  updatePaginationUI();
}

function appendCardsToGrid(container, items) {
  const fragment = document.createDocumentFragment();

  items.forEach((prod) => {
    const card = createProductCardElement(prod);
    fragment.appendChild(card);
  });

  container.appendChild(fragment);
}

// ==========================================================================
// Resolución de Portada para los 15 Productos Más Frecuentes
// ==========================================================================
// ==========================================================================
// Resolución de Portada Fidedigna para Productos y Categorías
// ==========================================================================
function resolveProductImage(prod) {
  if (!prod) return "assets/images/cat-tlapaleria.jpg";

  // 1. Si el producto ya tiene imagen asignada en base de datos
  if (prod.image && prod.image.startsWith("assets/images/products/")) {
    return prod.image;
  }
  if (prod.image_url && prod.image_url.startsWith("assets/images/products/")) {
    return prod.image_url;
  }

  const name = (prod.name || "").trim().toLowerCase();
  const cat = prod.category || prod.categories?.name || "";

  // 2. Validación estricta para evitar falsos positivos
  // LLAVE: ÚNICAMENTE llaves combinadas/españolas mecánicas (NUNCA válvulas, llaves de paso, llaves hembras)
  if (/^(llave[s]?\s+(combinada[s]?|española[s]?|mixta[s]?)|juego\s+(de\s+)?\d*\s*llaves\s+(combinadas|españolas))/i.test(name)) {
    if (!/(valvula|paso|hembra|macho|cerradura|duplicadora|llavero|broquero|soquet)/i.test(name)) {
      return "assets/images/products/prod-llave.webp";
    }
  }

  // TORNILLO: ÚNICAMENTE tornillos hexagonales (NUNCA abrazaderas)
  if (cat === "Tornillería y Fijación" && /^tornillo\s+hex(\.|\b)/i.test(name)) {
    if (!/(abrazadera|extractor|gato|prensa|coche|tablaroca|madera)/i.test(name)) {
      return "assets/images/products/prod-tornillo.webp";
    }
  }

  // DADO: ÚNICAMENTE dados para matraca (NUNCA soldadoras ni antorchas)
  if (cat === "Herramientas en General" && /^(dado\s+|juego\s+(de\s+)?dados)/i.test(name)) {
    if (!/(soldadora|antorcha|barra|matraca|riel|extensi[oó]n|organizador|tarraja|porta)/i.test(name)) {
      return "assets/images/products/prod-dado.webp";
    }
  }

  // VÁLVULA: ÚNICAMENTE válvulas de esfera de latón
  if (cat === "Plomería y Conexiones" && /v[aá]lvula\s+(de\s+)?esfera/i.test(name)) {
    if (!/(pvc|cpvc|plastico|plástico|alivio|seguridad|check|pie|pichancha|retenci[oó]n|descarga)/i.test(name)) {
      return "assets/images/products/prod-valvula.webp";
    }
  }

  // DESARMADOR: ÚNICAMENTE desarmadores manuales
  if (cat === "Herramientas en General" && /^(desarmador\s+|juego\s+(de\s+)?desarmadores|jgo\.?\s+(de\s+)?desarmadores)/i.test(name)) {
    if (!/(punta|portapunta|rack|gabinete)/i.test(name)) {
      return "assets/images/products/prod-desarmador.webp";
    }
  }

  // BROCA: ÚNICAMENTE brocas para taladro
  if (cat === "Herramientas en General" && /^(broca\s+|juego\s+(de\s+)?brocas|jgo\.?\s+(de\s+)?brocas)/i.test(name)) {
    if (!/(afilador|broquero|portabroca|sierra|copa|manita|router|sacabocados|forstner|gusano|autoalimentadora)/i.test(name)) {
      return "assets/images/products/prod-broca.webp";
    }
  }

  // FOCO: ÚNICAMENTE focos para socket
  if (cat === "Material Eléctrico" && /^foco\s+/i.test(name)) {
    if (!/(base|soquet|portal[aá]mpara|portafoco|tubo|balastra|reflector|circular|t10|t5)/i.test(name)) {
      return "assets/images/products/prod-foco.webp";
    }
  }

  // CANDADO: ÚNICAMENTE candados de latón o hierro
  if (/^(candado\s+|bl[ií]ster c\/\d+\s+candados)/i.test(name)) {
    if (!/(aldaba|cadena|portacandado|porta candado)/i.test(name)) {
      return "assets/images/products/prod-candado.webp";
    }
  }

  // NIPLE: ÚNICAMENTE niples rectos en Plomería
  if (cat === "Plomería y Conexiones" && /^niple\s+/i.test(name)) {
    if (!/(codo|tee|grasera|engrase)/i.test(name)) {
      return "assets/images/products/prod-niple.webp";
    }
  }

  // TUERCA: ÚNICAMENTE tuercas hexagonales en Tornillería
  if (cat === "Tornillería y Fijación" && /^tuerca\s+hex(\.|\b)/i.test(name)) {
    if (!/(abrazadera|mariposa|ciega|bellota|seguridad|inserto|uni[oó]n|nylon)/i.test(name)) {
      return "assets/images/products/prod-tuerca.webp";
    }
  }

  // EXTENSIÓN: ÚNICAMENTE extensiones eléctricas de uso rudo o domésticas
  if (cat === "Material Eléctrico" && /^extensi[oó]n(es)?\s+/i.test(name)) {
    if (/(rudo|el[eé]ctrica|dom[eé]stica|reforzada|power block|banana|polarizada|calibre|cal\.)/i.test(name)) {
      if (!/(bamb[uú]|rodillo|lavabo|fregadero|cespol|plug|corredera|escalera|p\/lav|dado|cuadro)/i.test(name)) {
        return "assets/images/products/prod-extension.webp";
      }
    }
  }

  // MANGUERA: ÚNICAMENTE mangueras de riego o jardín armadas/reforzadas
  if (/^manguera\s+/i.test(name)) {
    if (/(jard[ií]n|reforzada|armada|capas|10\s*m|15\s*m|20\s*m|25\s*m|30\s*m)/i.test(name)) {
      if (!/(nivel|compresor|aire|lavabo|fregadero|wc|alimentador|carrete|chiflon|pistola|aspersor|abrazadera|soplete|gas|motobomba|presi[oó]n|corrugado|poliducto|succi[oó]n)/i.test(name)) {
        return "assets/images/products/prod-manguera.webp";
      }
    }
  }

  // PIJA: ÚNICAMENTE pijas negras para tablaroca / fijación
  if (cat === "Tornillería y Fijación" && /^pija\s+/i.test(name)) {
    if (/(tablaroca|negra)/i.test(name) && !/(grapa|clip|taquete)/i.test(name)) {
      return "assets/images/products/prod-pija.webp";
    }
  }

  // PINZA: ÚNICAMENTE pinzas de electricista, chofer o universales
  if (cat === "Herramientas en General" && /^pinza[s]?\s+(de\s+)?(electricista|chofer|ch[oó]fer|universal)/i.test(name)) {
    if (!/(soldadora|tierra|presi[oó]n|ropa|depilar|bater[ií]a|cable)/i.test(name)) {
      return "assets/images/products/prod-pinza.webp";
    }
  }

  // CINTA: ÚNICAMENTE cinta de aislar eléctrica
  if (cat === "Material Eléctrico" && /cinta\s+(de\s+)?aisla(r|nte)/i.test(name)) {
    if (!/(sierra|m[eé]trica|tefl[oó]n|masking|canela|ducto|delimitadora|barricada)/i.test(name)) {
      return "assets/images/products/prod-cinta.webp";
    }
  }

  // Fallback seguro a imagen de la categoría o genérica
  return prod.image || prod.image_url || "assets/images/cat-tlapaleria.jpg";
}

function formatMoney(value) {
  const n = parseFloat(value);
  if (!isFinite(n)) return "$0.00";
  return "$" + n.toLocaleString("es-MX", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function createProductCardElement(prod) {
  const card = document.createElement("article");
  card.className = "product-card";
  card.dataset.sku = prod.sku;

  const catName = prod.category || prod.categories?.name || "General";
  const brandName = prod.brand || prod.brands?.name || "Homologado";
  const price = parseFloat(prod.base_price) || 0;
  const priceHtml = price > 0
    ? `<span class="price-val">${formatMoney(price)}</span>`
    : `<span class="price-val price-ask">Precio en mostrador</span>`;
  const imgUrl = prod._img || resolveProductImage(prod);
  const unit = (prod.unit_measure || "PZA").toLowerCase();
  if (!prod._photo && !(imgUrl.indexOf("assets/images/products/") === 0)) card.classList.add("no-photo");

  // Chips de Atributos Técnicos
  let chipsHtml = "";
  if (prod.attributes && typeof prod.attributes === "object") {
    chipsHtml = Object.entries(prod.attributes)
      .slice(0, 3)
      .map(([k, v]) => `<span class="spec-chip"><strong>${escapeHtml(k)}:</strong> ${escapeHtml(String(v))}</span>`)
      .join("");
  } else {
    chipsHtml = `<span class="spec-chip"><strong>Línea:</strong> ${escapeHtml(catName)}</span>`;
  }
  const descHtml = prod.description ? `<p class="product-description">${escapeHtml(prod.description)}</p>` : "";
  const featureHtml = prod.badge ? `<div class="card-badge-feature">${escapeHtml(prod.badge)}</div>` : "";

  card.innerHTML = `
    <div class="product-image-container">
      <img 
        src="${escapeHtml(optimizedImage(imgUrl))}" 
        alt="${escapeHtml(prod.name)}" 
        class="product-thumb-img" 
        loading="lazy"
        decoding="async"
        width="300" height="200"
        onerror="this.onerror=null;this.src='assets/images/opt/cat-tlapaleria-sm.webp'"
      >
      ${featureHtml}
    </div>

    <div class="product-card-body">
      <div class="product-brand-line">
        <span class="brand-name-pill">${escapeHtml(brandName)}</span>
        <span class="sku-pill">Clave: ${escapeHtml(prod.sku)}</span>
      </div>

      <h3 class="product-title" title="${escapeHtml(prod.name)}">${escapeHtml(prod.name)}</h3>
      ${descHtml}

      <div class="specs-chips-container">
        ${chipsHtml}
      </div>
    </div>

    <div class="product-card-footer">
      <div class="price-row">
        ${priceHtml}
        <span class="unit-val">/ ${escapeHtml(unit)}</span>
      </div>

      <div class="card-actions-bar">
        <div class="stepper-container">
          <button type="button" class="stepper-btn" onclick="stepQuantity(this, -1)" aria-label="Quitar uno">−</button>
          <input type="number" class="qty-input" min="1" max="999" value="1" inputmode="numeric" pattern="[0-9]*" aria-label="Cantidad">
          <button type="button" class="stepper-btn" onclick="stepQuantity(this, 1)" aria-label="Agregar uno">+</button>
        </div>

        <button type="button" class="btn-add-to-quote" onclick="handleAddProductFromCard(this)">
          <span>+ Agregar</span>
        </button>
      </div>
    </div>
  `;

  return card;
}

// Versiones ligeras (WebP) de las fotos genéricas de departamento para ahorrar datos en celular
const OPTIMIZED_IMAGES = {
  "assets/images/cat-tlapaleria.jpg": "assets/images/opt/cat-tlapaleria-sm.webp",
  "assets/images/cat-tornilleria.jpg": "assets/images/opt/cat-tornilleria-sm.webp",
  "assets/images/cat-plomeria.jpg": "assets/images/opt/cat-plomeria-sm.webp",
  "assets/images/cat-herramientas.jpg": "assets/images/opt/cat-herramientas-sm.webp",
  "assets/images/cat-electrico.jpg": "assets/images/opt/cat-electrico-sm.webp",
  "assets/images/hero-storefront.jpg": "assets/images/opt/cat-tlapaleria-sm.webp"
};
function optimizedImage(url) {
  return OPTIMIZED_IMAGES[url] || url;
}

function buildCounterText(showing, total) {
  const term = AppState.searchTerm ? ` para "${AppState.searchTerm}"` : "";
  const scope = AppState.autoExpandedToAll ? " (en toda la tienda)" : "";
  if (total === 0) return `0 resultados${term}`;
  return `${total.toLocaleString('es-MX')} ${total === 1 ? "artículo" : "artículos"}${term}${scope}`;
}

function updatePaginationUI() {
  const paginationBox = document.getElementById("pagination-container");
  const counter = document.getElementById("counter-display");
  if (!paginationBox) return;

  const totalCount = AppState.filteredCatalog.length;
  const currentShowing = Math.min(AppState.displayedCount, totalCount);

  if (counter) {
    counter.textContent = buildCounterText(currentShowing, totalCount);
  }

  if (AppState.displayedCount >= totalCount) {
    paginationBox.innerHTML = `
      <div class="pagination-stats">
        ✓ Mostrando todos los ${totalCount.toLocaleString('es-MX')} artículos técnicos encontrados.
      </div>
    `;
    return;
  }

  const remaining = totalCount - AppState.displayedCount;
  const nextBatch = Math.min(AppState.pageSize, remaining);

  paginationBox.innerHTML = `
    <button class="btn-load-more" onclick="loadMoreProducts()">
      <span>Ver ${nextBatch.toLocaleString('es-MX')} más (${remaining.toLocaleString('es-MX')} restantes)</span>
    </button>
    <div class="pagination-stats">
      Mostrando ${currentShowing.toLocaleString('es-MX')} de ${totalCount.toLocaleString('es-MX')} resultados disponibles
    </div>
  `;
}

window.loadMoreProducts = function () {
  const grid = document.getElementById("products-container");
  if (!grid) return;

  const prevCount = AppState.displayedCount;
  AppState.displayedCount += AppState.pageSize;

  const nextItems = AppState.filteredCatalog.slice(prevCount, AppState.displayedCount);
  appendCardsToGrid(grid, nextItems);
  updatePaginationUI();
};

window.stepQuantity = function (target, delta) {
  if (typeof target === "string") {
    const input = document.getElementById(`qty-${target}`);
    if (input) {
      let val = parseInt(input.value, 10) || 1;
      input.value = Math.max(1, Math.min(999, val + delta));
    }
    return;
  }
  const card = target.closest(".product-card") || target.closest(".card-actions-bar");
  if (!card) return;
  const input = card.querySelector(".qty-input");
  if (!input) return;
  let val = parseInt(input.value, 10) || 1;
  input.value = Math.max(1, Math.min(999, val + delta));
};

window.handleAddProductFromCard = function (btn) {
  const card = btn.closest(".product-card");
  if (!card) return;
  const sku = card.dataset.sku;
  const input = card.querySelector(".qty-input");
  const quantityToAdd = input ? parseInt(input.value, 10) || 1 : 1;
  addProductToCart(sku, quantityToAdd, btn);
};

// ==========================================================================
// 7. Carrito de Presupuesto
// ==========================================================================
function initCartFromStorage() {
  try {
    const raw = localStorage.getItem(CONFIG.STORAGE_CART_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) {
        parsed.forEach(({ item, quantity }) => {
          if (item?.sku && quantity > 0) {
            AppState.quoteCart.set(item.sku, { item, quantity });
          }
        });
      }
    }
  } catch (err) {
    console.warn("No se pudo cargar el carrito:", err);
  }
  updateCartUI();
}

function saveCartToStorage() {
  try {
    const serialized = Array.from(AppState.quoteCart.values());
    localStorage.setItem(CONFIG.STORAGE_CART_KEY, JSON.stringify(serialized));
  } catch (err) {
    console.warn("Error al guardar carrito:", err);
  }
}

function addProductToCart(sku, quantityToAdd, btn) {
  const product = AppState.masterCatalog.find((p) => p.sku === sku);
  if (!product) return;

  if (AppState.quoteCart.has(sku)) {
    AppState.quoteCart.get(sku).quantity += quantityToAdd;
  } else {
    AppState.quoteCart.set(sku, { item: product, quantity: quantityToAdd });
  }

  saveCartToStorage();
  updateCartUI();

  if (btn) {
    if (!btn.dataset.originalHtml) btn.dataset.originalHtml = btn.innerHTML;
    btn.classList.add("added");
    btn.innerHTML = "<span>✓ Agregado</span>";
    clearTimeout(btn._addedTimer);
    btn._addedTimer = setTimeout(() => {
      btn.classList.remove("added");
      btn.innerHTML = btn.dataset.originalHtml;
    }, 1400);
    const card = btn.closest(".product-card");
    const qty = card && card.querySelector(".qty-input");
    if (qty) qty.value = 1;
  }

  const inCart = AppState.quoteCart.get(sku).quantity;
  showToast(`✓ ${quantityToAdd} × ${product.name}`, {
    detail: inCart > quantityToAdd ? `Ya llevas ${inCart} en tu cotización` : "Agregado a tu cotización",
    actionLabel: "Ver cotización",
    action: () => window.openQuoteDrawer && window.openQuoteDrawer()
  });
  bumpCartBadges();
  if (navigator.vibrate) { try { navigator.vibrate(15); } catch (_) {} }
}

function bumpCartBadges() {
  ["cart-item-count", "mobile-cart-count"].forEach((id) => {
    const el = document.getElementById(id);
    if (!el) return;
    el.classList.remove("bump");
    void el.offsetWidth;
    el.classList.add("bump");
  });
}

// Aviso flotante breve (toast) para confirmar acciones sin interrumpir
let toastTimer = null;
function showToast(message, opts = {}) {
  let toast = document.getElementById("app-toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "app-toast";
    toast.className = "app-toast";
    toast.setAttribute("role", "status");
    toast.setAttribute("aria-live", "polite");
    document.body.appendChild(toast);
  }
  toast.innerHTML = `
    <div class="app-toast-text">
      <strong>${escapeHtml(message)}</strong>
      ${opts.detail ? `<span>${escapeHtml(opts.detail)}</span>` : ""}
    </div>
    ${opts.actionLabel ? `<button type="button" class="app-toast-action">${escapeHtml(opts.actionLabel)}</button>` : ""}
  `;
  const actionBtn = toast.querySelector(".app-toast-action");
  if (actionBtn && typeof opts.action === "function") {
    actionBtn.addEventListener("click", () => {
      toast.classList.remove("show");
      opts.action();
    });
  }
  // Siempre por encima de la barra inferior del celular, sin taparla
  const nav = document.querySelector(".mobile-bottom-nav");
  if (nav && getComputedStyle(nav).display !== "none") {
    const navTop = nav.getBoundingClientRect().top;
    toast.style.bottom = Math.max(12, Math.round(window.innerHeight - navTop + 10)) + "px";
  } else {
    toast.style.bottom = "";
  }
  toast.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), opts.duration || 3200);
}
window.showToast = showToast;

window.handleAddProduct = function (sku) {
  const qtyInput = document.getElementById(`qty-${sku}`);
  const quantityToAdd = qtyInput ? parseInt(qtyInput.value, 10) || 1 : 1;
  const btn = document.getElementById(`btn-add-${sku}`);
  addProductToCart(sku, quantityToAdd, btn);
};

window.handleUpdateCartQty = function (sku, newQtyVal) {
  const qty = parseInt(newQtyVal, 10);
  if (qty > 0 && AppState.quoteCart.has(sku)) {
    AppState.quoteCart.get(sku).quantity = qty;
    saveCartToStorage();
    updateCartUI();
  } else if (qty <= 0) {
    window.handleRemoveCartItem(sku);
  }
};

window.handleRemoveCartItem = function (sku) {
  AppState.quoteCart.delete(sku);
  saveCartToStorage();
  updateCartUI();
};

window.clearQuoteCart = function () {
  if (!AppState.quoteCart.size) return;
  if (!confirm("¿Vaciar toda la cotización?")) return;
  AppState.quoteCart.clear();
  saveCartToStorage();
  updateCartUI();
  setDrawerStep(1);
};

function updateCartUI() {
  const countPill = document.getElementById("cart-item-count");
  const drawerList = document.getElementById("cart-items-container");
  const totalElem = document.getElementById("estimated-total-amount");
  const dispatchBtn = document.getElementById("whatsapp-order-btn");

  let totalItemsCount = 0;
  let totalMoney = 0;

  if (drawerList) drawerList.innerHTML = "";

  if (AppState.quoteCart.size === 0) {
    if (drawerList) {
      drawerList.innerHTML = `
        <div style="text-align: center; color: #64748b; padding: 40px 10px;">
          <div style="font-size: 2.5rem; margin-bottom: 10px;">📋</div>
          <p style="font-weight: 700; color: #0f172a; margin-bottom: 6px;">Tu presupuesto está vacío</p>
          <p style="font-size: 0.9rem;">Busca tus materiales, toca <strong>+ Agregar</strong> y aquí se arma tu lista para mandarla por WhatsApp.</p>
          <button type="button" class="btn-empty-cart-cta" onclick="closeQuoteDrawerAndSearch()">🔍 Buscar materiales</button>
        </div>
      `;
    }
    if (dispatchBtn) dispatchBtn.disabled = true;
  } else {
    if (dispatchBtn) dispatchBtn.disabled = false;

    AppState.quoteCart.forEach(({ item, quantity }, sku) => {
      totalItemsCount += quantity;
      const subtotal = item.base_price * quantity;
      totalMoney += subtotal;

      if (drawerList) {
        const row = document.createElement("div");
        row.className = "cart-item-row";
        const thumb = resolveProductImage(item);

        const skuJs = escapeHtml(JSON.stringify(String(sku)));
        row.innerHTML = `
          <img src="${escapeHtml(optimizedImage(thumb))}" alt="" class="cart-item-thumb" loading="lazy" onerror="this.onerror=null;this.src='assets/images/opt/cat-tlapaleria-sm.webp'">
          <div class="cart-item-info">
            <div class="cart-item-name" title="${escapeHtml(item.name)}">${escapeHtml(item.name)}</div>
            <div class="cart-item-sku">Clave: ${escapeHtml(sku)}</div>
            <div class="cart-item-price">${formatMoney(item.base_price)} / ${escapeHtml((item.unit_measure || "PZA").toLowerCase())} · <strong>${formatMoney(subtotal)}</strong></div>
          </div>
          <div class="cart-item-controls">
            <div class="cart-qty-stepper">
              <button type="button" class="cart-qty-btn" aria-label="Quitar uno" onclick="handleUpdateCartQty(${skuJs}, ${quantity - 1})">−</button>
              <input 
                type="number" 
                class="cart-item-qty" 
                min="1" 
                max="999" 
                inputmode="numeric"
                aria-label="Cantidad"
                value="${quantity}" 
                onchange="handleUpdateCartQty(${skuJs}, this.value)"
              >
              <button type="button" class="cart-qty-btn" aria-label="Agregar uno" onclick="handleUpdateCartQty(${skuJs}, ${quantity + 1})">+</button>
            </div>
            <button type="button" class="btn-remove-item" title="Eliminar partida" aria-label="Eliminar" onclick="handleRemoveCartItem(${skuJs})">🗑</button>
          </div>
        `;
        drawerList.appendChild(row);
      }
    });
  }

  if (countPill) countPill.textContent = totalItemsCount;
  const mobileCountPill = document.getElementById("mobile-cart-count");
  if (mobileCountPill) {
    mobileCountPill.textContent = totalItemsCount;
    mobileCountPill.dataset.count = String(totalItemsCount);
  }
  const stepCountPill = document.getElementById("cart-item-count-step");
  if (stepCountPill) stepCountPill.textContent = totalItemsCount;
  if (totalElem) totalElem.textContent = formatMoney(totalMoney);
  const clearCartBtn = document.getElementById("btn-clear-cart");
  if (clearCartBtn) clearCartBtn.style.display = AppState.quoteCart.size ? "inline-flex" : "none";

  const btnContinue = document.getElementById("btn-continue-step-2");
  if (btnContinue) {
    btnContinue.disabled = (AppState.quoteCart.size === 0);
    btnContinue.style.opacity = (AppState.quoteCart.size === 0) ? "0.5" : "1";
    btnContinue.style.pointerEvents = (AppState.quoteCart.size === 0) ? "none" : "auto";
  }
}

// ==========================================================================
// 7.1. Control del Stepper de 2 Pasos del Cajón
// ==========================================================================
function setDrawerStep(step) {
  const step1View = document.getElementById("drawer-step-1");
  const step2View = document.getElementById("drawer-step-2");
  const step1Btn = document.getElementById("step-btn-1");
  const step2Btn = document.getElementById("step-btn-2");
  const footer1 = document.getElementById("footer-actions-step-1");
  const footer2 = document.getElementById("footer-actions-step-2");

  if (step === 2) {
    if (AppState.quoteCart.size === 0) {
      alert("Agrega al menos un artículo a tu presupuesto para ingresar tus datos de recolección.");
      return;
    }
    if (step1View) step1View.style.display = "none";
    if (step2View) step2View.style.display = "block";
    if (step1Btn) step1Btn.classList.remove("active");
    if (step2Btn) step2Btn.classList.add("active");
    if (footer1) footer1.style.display = "none";
    if (footer2) footer2.style.display = "block";

    const nameInput = document.getElementById("quote-client-name");
    if (nameInput) {
      setTimeout(() => nameInput.focus(), 150);
    }
  } else {
    if (step1View) step1View.style.display = "block";
    if (step2View) step2View.style.display = "none";
    if (step1Btn) step1Btn.classList.add("active");
    if (step2Btn) step2Btn.classList.remove("active");
    if (footer1) footer1.style.display = "block";
    if (footer2) footer2.style.display = "none";
  }
}
window.setDrawerStep = setDrawerStep;

// ==========================================================================
// 7.2. Persistencia en Cache Local y Validación de Datos del Solicitante
// ==========================================================================
const CUSTOMER_CACHE_KEY = "el_aguila_customer_profile";

function saveCustomerDataToCache() {
  try {
    const nameInput = document.getElementById("quote-client-name");
    const phoneInput = document.getElementById("quote-client-phone");
    const siteInput = document.getElementById("quote-client-site");
    const notesInput = document.getElementById("quote-client-notes");

    const profile = {
      name: nameInput ? nameInput.value.trim() : "",
      phone: phoneInput ? phoneInput.value.trim() : "",
      site: siteInput ? siteInput.value.trim() : "",
      notes: notesInput ? notesInput.value.trim() : "",
      preferredBranch: AppState.selectedBranch || "delicias",
      updatedAt: Date.now()
    };

    if (profile.name || profile.phone || profile.notes) {
      localStorage.setItem(CUSTOMER_CACHE_KEY, JSON.stringify(profile));
    }
    updateCustomerDataStatusBadge();
  } catch (e) {
    console.warn("No se pudo guardar datos del cliente en localStorage:", e);
  }
}

function loadCustomerDataFromCache() {
  try {
    const raw = localStorage.getItem(CUSTOMER_CACHE_KEY);
    if (!raw) {
      updateCustomerDataStatusBadge();
      return;
    }
    const data = JSON.parse(raw);
    if (!data || typeof data !== "object") {
      updateCustomerDataStatusBadge();
      return;
    }

    const nameInput = document.getElementById("quote-client-name");
    const phoneInput = document.getElementById("quote-client-phone");
    const notesInput = document.getElementById("quote-client-notes");

    if (nameInput && data.name && !nameInput.value) {
      nameInput.value = data.name;
    }
    if (phoneInput && data.phone && !phoneInput.value) {
      phoneInput.value = data.phone;
    }
    if (notesInput && data.notes && !notesInput.value) {
      notesInput.value = data.notes;
    }

    if (isActiveBranch(data.preferredBranch) && !safeStorageGet(CONFIG.STORAGE_BRANCH_KEY)) {
      setBranch(data.preferredBranch);
    }

    updateCustomerDataStatusBadge();
  } catch (e) {
    console.warn("Error cargando perfil de cliente desde cache:", e);
  }
}

function clearCustomerCache() {
  try {
    localStorage.removeItem(CUSTOMER_CACHE_KEY);
    const nameInput = document.getElementById("quote-client-name");
    const phoneInput = document.getElementById("quote-client-phone");
    const notesInput = document.getElementById("quote-client-notes");

    if (nameInput) {
      nameInput.value = "";
      nameInput.classList.remove("form-input-error");
    }
    if (phoneInput) {
      phoneInput.value = "";
      phoneInput.classList.remove("form-input-error");
    }
    if (notesInput) {
      notesInput.value = "";
    }

    const nameErr = document.getElementById("name-error-msg");
    if (nameErr) nameErr.style.display = "none";
    const phoneErr = document.getElementById("phone-error-msg");
    if (phoneErr) phoneErr.style.display = "none";

    updateCustomerDataStatusBadge();
  } catch (e) {
    console.warn("Error limpiando cache de cliente:", e);
  }
}

function updateCustomerDataStatusBadge() {
  const nameInput = document.getElementById("quote-client-name");
  const phoneInput = document.getElementById("quote-client-phone");
  const statusBadge = document.getElementById("customer-cache-status-badge");
  const stepperPill = document.getElementById("stepper-client-pill");

  const nameVal = nameInput ? nameInput.value.trim() : "";
  const phoneVal = phoneInput ? phoneInput.value.trim() : "";
  const phoneClean = phoneVal.replace(/\D/g, "");

  const isComplete = (nameVal.length >= 2 && phoneClean.length >= 10);

  if (stepperPill) {
    if (isComplete) {
      stepperPill.className = "stepper-pill-complete";
      stepperPill.textContent = "✓ Listo";
    } else {
      stepperPill.className = "stepper-pill-pending";
      stepperPill.textContent = "Requerido";
    }
  }

  if (statusBadge) {
    const hasStored = !!safeStorageGet(CUSTOMER_CACHE_KEY);
    if (hasStored || (nameVal && phoneVal)) {
      statusBadge.style.display = "inline-flex";
    } else {
      statusBadge.style.display = "none";
    }
  }
}

function formatPhoneInput(e) {
  const input = e.target;
  let digits = input.value.replace(/\D/g, "");
  if (digits.length > 10) digits = digits.slice(0, 10);

  let formatted = "";
  if (digits.length > 6) {
    formatted = `${digits.slice(0, 3)} ${digits.slice(3, 6)} ${digits.slice(6)}`;
  } else if (digits.length > 3) {
    formatted = `${digits.slice(0, 3)} ${digits.slice(3)}`;
  } else {
    formatted = digits;
  }
  input.value = formatted;
}

// ==========================================================================
// 8. Cierre de Cotización y Despacho WhatsApp
// ==========================================================================
function formatWhatsAppMessage(quoteCart, branch, clientData = {}, dateStr = null) {
  const branchAddress = branch.id === "delicias"
    ? `${branch.address} (A un lado del Centro de Salud San Joaquín)`
    : branch.address;

  if (!dateStr) {
    const now = new Date();
    dateStr = now.toLocaleDateString("es-MX", {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit"
    });
  }

  const clientName = clientData.clientName ? clientData.clientName.trim() : "";
  const clientPhone = clientData.clientPhone ? clientData.clientPhone.trim() : "";
  const siteLocation = clientData.siteLocation ? clientData.siteLocation.trim() : "";
  const notes = clientData.notes ? clientData.notes.trim() : "";

  let msg = `*SOLICITUD DE COTIZACIÓN DE MATERIALES*\n`;
  msg += `*FERRETERÍA Y TLAPALERÍA EL ÁGUILA*\n`;
  msg += `_¡Todo lo que necesitas para tu hogar o trabajo, en un solo lugar!_\n`;
  msg += `━━━━━━━━━━━━━━━━━━━━━\n`;
  msg += `📍 *Sucursal Seleccionada:* ${branch.name}\n`;
  msg += `🏢 *Ubicación:* ${branchAddress}\n`;
  if (branch.mapsUrl) {
    msg += `🗺️ *Google Maps:* ${branch.mapsUrl}\n`;
  }
  msg += `📱 *Teléfono / WhatsApp Mostrador:* ${branch.phone}\n`;
  msg += `📅 *Fecha:* ${dateStr}\n\n`;

  msg += `*DATOS DEL CLIENTE / RECOLECCIÓN:*\n`;
  msg += `• *Solicitante / Empresa:* ${clientName || "Cliente Particular / Mostrador"}\n`;
  if (clientPhone) {
    msg += `• *Teléfono de Contacto:* ${clientPhone}\n`;
  }
  msg += `• *Modalidad:* ${siteLocation || "Recolección en Mostrador"}\n`;
  if (notes) {
    msg += `• *Notas / Preguntas:* ${notes}\n`;
  }
  msg += `\n*RELACIÓN DE MATERIALES SOLICITADOS:*\n`;

  let idx = 1;
  let totalEstimado = 0;

  quoteCart.forEach(({ item, quantity }, sku) => {
    const itemSubtotal = item.base_price * quantity;
    totalEstimado += itemSubtotal;
    const refCode = item.manufacturer_code ? `[Clave: ${item.manufacturer_code}]` : `[SKU: ${sku}]`;

    msg += `${idx}. ${refCode} *${item.name}*\n`;
    msg += `   └ Cantidad: *${quantity}* ${item.unit_measure || "PZA"} | Subtotal: *${formatMoney(itemSubtotal)}*\n`;
    idx++;
  });

  msg += `━━━━━━━━━━━━━━━━━━━━━\n`;
  msg += `*TOTAL ESTIMADO:* *${formatMoney(totalEstimado)} MXN*\n\n`;
  msg += `_Solicito amablemente confirmar existencias en ${branch.name} para recolección en mostrador y apartar mis piezas. Saludos cordiales._`;

  const encodedMsg = encodeURIComponent(msg);
  const targetNumber = branch.whatsapp;
  const whatsappUrl = `https://wa.me/${targetNumber}?text=${encodedMsg}`;

  return {
    rawMessage: msg,
    encodedMessage: encodedMsg,
    targetNumber: targetNumber,
    totalEstimado: totalEstimado,
    whatsappUrl: whatsappUrl
  };
}

function dispatchToWhatsApp() {
  if (AppState.quoteCart.size === 0) {
    alert("Tu presupuesto está vacío. Agrega productos del catálogo para poder cotizar.");
    return;
  }

  const clientNameInput = document.getElementById("quote-client-name");
  const clientPhoneInput = document.getElementById("quote-client-phone");
  const siteInput = document.getElementById("quote-client-site");
  const notesInput = document.getElementById("quote-client-notes");
  const nameErrorMsg = document.getElementById("name-error-msg");
  const phoneErrorMsg = document.getElementById("phone-error-msg");

  if (clientNameInput) clientNameInput.classList.remove("form-input-error");
  if (clientPhoneInput) clientPhoneInput.classList.remove("form-input-error");
  if (nameErrorMsg) nameErrorMsg.style.display = "none";
  if (phoneErrorMsg) phoneErrorMsg.style.display = "none";

  const nameVal = clientNameInput ? clientNameInput.value.trim() : "";
  const phoneVal = clientPhoneInput ? clientPhoneInput.value.trim() : "";
  const phoneClean = phoneVal.replace(/\D/g, "");

  let hasError = false;

  if (!nameVal || nameVal.length < 2) {
    setDrawerStep(2);
    if (clientNameInput) {
      clientNameInput.classList.add("form-input-error");
      clientNameInput.focus();
    }
    if (nameErrorMsg) {
      nameErrorMsg.style.display = "block";
    }
    hasError = true;
  }

  if (!phoneClean || phoneClean.length < 10) {
    if (!hasError) {
      setDrawerStep(2);
      if (clientPhoneInput) {
        clientPhoneInput.focus();
      }
    }
    if (clientPhoneInput) {
      clientPhoneInput.classList.add("form-input-error");
    }
    if (phoneErrorMsg) {
      phoneErrorMsg.style.display = "block";
    }
    hasError = true;
  }

  if (hasError) {
    return;
  }

  // Guardar datos validados en cache para futuras visitas
  saveCustomerDataToCache();

  const branch = isActiveBranch(AppState.selectedBranch) ? BRANCHES[AppState.selectedBranch] : BRANCHES.delicias;

  const clientData = {
    clientName: nameVal,
    clientPhone: phoneVal,
    siteLocation: siteInput ? siteInput.value.trim() : "Recolección en mostrador",
    notes: notesInput ? notesInput.value.trim() : ""
  };

  const quoteResult = formatWhatsAppMessage(AppState.quoteCart, branch, clientData);
  const win = window.open(quoteResult.whatsappUrl, "_blank");
  if (!win) window.location.href = quoteResult.whatsappUrl;
  showToast("✓ Abriendo WhatsApp…", { detail: `Tu lista va para ${branch.name}`, duration: 4000 });
}

// ==========================================================================
// 9. Event Listeners y Utilidades
// ==========================================================================
function initEventListeners() {
  const searchInput = document.getElementById("catalog-search-input");
  const clearBtn = document.getElementById("search-clear-btn");
  const searchForm = document.getElementById("catalog-search-form");
  const searchSubmitBtn = document.getElementById("search-submit-btn");
  let searchDebounceTimer = null;

  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      AppState.searchTerm = e.target.value;
      if (clearBtn) {
        clearBtn.style.display = e.target.value ? "block" : "none";
      }
      clearTimeout(searchDebounceTimer);
      searchDebounceTimer = setTimeout(() => {
        applyFilterPipeline();
        renderSearchSuggestions();
      }, 160);
    });

    searchInput.addEventListener("focus", () => {
      if (searchInput.value.trim()) renderSearchSuggestions();
    });

    searchInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        clearTimeout(searchDebounceTimer);
        triggerCatalogSearch();
      }
    });
  }

  if (searchForm) {
    searchForm.addEventListener("submit", (e) => {
      e.preventDefault();
      clearTimeout(searchDebounceTimer);
      triggerCatalogSearch();
    });
  }

  if (searchSubmitBtn) {
    searchSubmitBtn.addEventListener("click", (e) => {
      e.preventDefault();
      clearTimeout(searchDebounceTimer);
      triggerCatalogSearch();
    });
  }

  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      if (searchInput) {
        searchInput.value = "";
        searchInput.focus();
      }
      AppState.searchTerm = "";
      clearBtn.style.display = "none";
      clearTimeout(searchDebounceTimer);
      hideSearchSuggestions();
      syncUrlState();
      applyFilterPipeline();
    });
  }

  const sortSelect = document.getElementById("catalog-sort-select");
  if (sortSelect) {
    sortSelect.value = AppState.sortMode;
    sortSelect.addEventListener("change", (e) => {
      AppState.sortMode = e.target.value;
      sortCatalog();
      renderCatalogGrid();
    });
  }

  // Drawer
  const drawer = document.getElementById("quote-panel");
  const backdrop = document.getElementById("drawer-backdrop");
  const openDrawerBtn = document.getElementById("quote-drawer-trigger");
  const closeDrawerBtn = document.getElementById("quote-close-btn");
  const sendWhatsAppBtn = document.getElementById("whatsapp-order-btn");

  let drawerHistoryPushed = false;
  const openDrawer = () => {
    loadCustomerDataFromCache();
    if (drawer && drawer.classList.contains("active")) return;
    if (drawer) drawer.classList.add("active");
    if (backdrop) backdrop.classList.add("active");
    document.body.classList.add("drawer-open");
    hideSearchSuggestions();
    const toast = document.getElementById("app-toast");
    if (toast) toast.classList.remove("show");
    // En Android el botón "Atrás" cierra la cotización en lugar de salir de la página
    try {
      history.pushState({ quoteDrawer: true }, "");
      drawerHistoryPushed = true;
    } catch (_) {}
  };

  const closeDrawer = (fromPopState) => {
    if (!drawer || !drawer.classList.contains("active")) return;
    drawer.classList.remove("active");
    if (backdrop) backdrop.classList.remove("active");
    document.body.classList.remove("drawer-open");
    if (drawerHistoryPushed && fromPopState !== true) {
      drawerHistoryPushed = false;
      try { history.back(); } catch (_) {}
    }
    drawerHistoryPushed = false;
  };

  window.addEventListener("popstate", () => {
    if (drawer && drawer.classList.contains("active")) {
      drawerHistoryPushed = false;
      closeDrawer(true);
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeDrawer();
      hideSearchSuggestions();
    }
  });

  window.closeQuoteDrawer = closeDrawer;

  if (openDrawerBtn) openDrawerBtn.addEventListener("click", openDrawer);
  if (closeDrawerBtn) closeDrawerBtn.addEventListener("click", () => closeDrawer());
  if (backdrop) backdrop.addEventListener("click", () => closeDrawer());
  if (sendWhatsAppBtn) sendWhatsAppBtn.addEventListener("click", dispatchToWhatsApp);

  // Customer Data Auto-Save, Formatting & Inline Validation
  const clientNameInput = document.getElementById("quote-client-name");
  const clientPhoneInput = document.getElementById("quote-client-phone");
  const clientNotesInput = document.getElementById("quote-client-notes");
  const nameErrorMsg = document.getElementById("name-error-msg");
  const phoneErrorMsg = document.getElementById("phone-error-msg");

  if (clientNameInput) {
    clientNameInput.addEventListener("input", () => {
      if (clientNameInput.value.trim().length >= 2) {
        clientNameInput.classList.remove("form-input-error");
        if (nameErrorMsg) nameErrorMsg.style.display = "none";
      }
      saveCustomerDataToCache();
    });
  }

  if (clientPhoneInput) {
    clientPhoneInput.addEventListener("input", (e) => {
      formatPhoneInput(e);
      const digits = clientPhoneInput.value.replace(/\D/g, "");
      if (digits.length >= 10) {
        clientPhoneInput.classList.remove("form-input-error");
        if (phoneErrorMsg) phoneErrorMsg.style.display = "none";
      }
      saveCustomerDataToCache();
    });
  }

  if (clientNotesInput) {
    clientNotesInput.addEventListener("input", () => {
      saveCustomerDataToCache();
    });
  }

  // Preload cached customer data if available
  loadCustomerDataFromCache();

  window.openQuoteDrawer = openDrawer;
}

window.filterByCategoryBanner = function(catName) {
  AppState.filterCategory = catName;
  AppState.searchTerm = "";
  const searchInput = document.getElementById("catalog-search-input");
  if (searchInput) searchInput.value = "";
  const clearBtn = document.getElementById("search-clear-btn");
  if (clearBtn) clearBtn.style.display = "none";
  updateFacetSelection();
  applyFilterPipeline();
  syncUrlState();
  scrollToResults();
};

window.triggerCatalogSearch = function() {
  const searchInput = document.getElementById("catalog-search-input");
  if (searchInput) {
    AppState.searchTerm = searchInput.value.trim();
    const clearBtn = document.getElementById("search-clear-btn");
    if (clearBtn) {
      clearBtn.style.display = searchInput.value ? "block" : "none";
    }
  }
  applyFilterPipeline();
  hideSearchSuggestions();
  syncUrlState();
  if (searchInput) searchInput.blur(); // cierra el teclado del celular para ver resultados
  scrollToResults();

  const counter = document.getElementById("counter-display");
  if (counter) {
    counter.classList.remove("highlight-pulse");
    void counter.offsetWidth;
    counter.classList.add("highlight-pulse");
  }
};

window.scrollToCatalog = function() {
  const elem = document.getElementById("catalog-section");
  if (elem) {
    elem.scrollIntoView({ behavior: "smooth", block: "start" });
  }
};

// Lleva directo a los resultados (en celular evita pasar por los filtros)
window.scrollToResults = function() {
  const elem = document.getElementById("catalog-results") || document.getElementById("catalog-section");
  if (elem) {
    elem.scrollIntoView({ behavior: "smooth", block: "start" });
  }
};

window.closeQuoteDrawerAndSearch = function() {
  if (window.closeQuoteDrawer) window.closeQuoteDrawer();
  setTimeout(() => {
    const input = document.getElementById("catalog-search-input");
    window.scrollTo({ top: 0, behavior: "smooth" });
    if (input) input.focus();
  }, 250);
};

window.scrollToBranches = function() {
  const elem = document.getElementById("branches-section");
  // Evita que la carga automática de productos empuje la sección mientras se desplaza
  AppState.suspendAutoLoad = true;
  clearTimeout(window._autoLoadResume);
  window._autoLoadResume = setTimeout(() => { AppState.suspendAutoLoad = false; }, 2500);
  if (elem) {
    elem.scrollIntoView({ behavior: "smooth", block: "start" });
  }
};

window.resetAllFilters = function () {
  AppState.filterCategory = "all";
  AppState.filterBrand = "all";
  AppState.searchTerm = "";
  const searchInput = document.getElementById("catalog-search-input");
  if (searchInput) searchInput.value = "";
  const clearBtn = document.getElementById("search-clear-btn");
  if (clearBtn) clearBtn.style.display = "none";
  updateFacetSelection();
  applyFilterPipeline();
  syncUrlState();
};

window.resetAllFiltersKeepSearch = function () {
  AppState.filterCategory = "all";
  AppState.filterBrand = "all";
  updateFacetSelection();
  applyFilterPipeline();
};

window.quickSearch = function (term) {
  AppState.filterCategory = "all";
  AppState.filterBrand = "all";
  AppState.searchTerm = term;
  const searchInput = document.getElementById("catalog-search-input");
  if (searchInput) {
    searchInput.value = term;
  }
  const clearBtn = document.getElementById("search-clear-btn");
  if (clearBtn) clearBtn.style.display = "block";
  updateFacetSelection();
  applyFilterPipeline();
  hideSearchSuggestions();
  syncUrlState();
  scrollToResults();
};

window.selectBranchFromCard = function (branchId) {
  if (!isActiveBranch(branchId)) return;
  setBranch(branchId);
  showToast(`✓ Cotizarás con ${BRANCHES[branchId].name}`);
};

// Bloqueo global: cualquier elemento marcado como decorativo no responde a toques ni clics
document.addEventListener("click", (e) => {
  const deco = e.target.closest && e.target.closest('[data-decorative="true"]');
  if (deco) {
    e.preventDefault();
    e.stopPropagation();
  }
}, true);

// ==========================================================================
// 10. Mejoras para Celular: sugerencias, carga continua, URL y cabecera
// ==========================================================================
function renderSearchSuggestions() {
  const box = document.getElementById("search-suggest");
  const input = document.getElementById("catalog-search-input");
  if (!box || !input || !AppState.masterCatalog.length) return;
  const term = input.value.trim();
  if (term.length < 2 || document.activeElement !== input) {
    hideSearchSuggestions();
    return;
  }
  const list = AppState.filteredCatalog.slice(0, 6);
  const total = AppState.filteredCatalog.length;
  if (!list.length) {
    box.innerHTML = `<div class="suggest-empty">Sin coincidencias para "<strong>${escapeHtml(term)}</strong>". Prueba con otra palabra o pregúntanos por WhatsApp.</div>`;
  } else {
    box.innerHTML = list.map((p) => {
      const price = parseFloat(p.base_price) || 0;
      const skuJs = escapeHtml(JSON.stringify(String(p.sku)));
      return `
        <div class="suggest-row">
          <img src="${escapeHtml(optimizedImage(p._img || resolveProductImage(p)))}" alt="" loading="lazy" class="suggest-thumb">
          <button type="button" class="suggest-main" onclick="openSuggestion(${skuJs})">
            <span class="suggest-name">${escapeHtml(p.name)}</span>
            <span class="suggest-price">${price > 0 ? formatMoney(price) : "Precio en mostrador"} <em>/ ${escapeHtml((p.unit_measure || "PZA").toLowerCase())}</em></span>
          </button>
          <button type="button" class="suggest-add" aria-label="Agregar a cotización" onmousedown="event.preventDefault()" onclick="quickAddFromSuggestion(${skuJs}, this)">+</button>
        </div>`;
    }).join("") + `<button type="button" class="suggest-all" onclick="triggerCatalogSearch()">Ver los ${total.toLocaleString("es-MX")} resultados →</button>`;
  }
  box.hidden = false;
  positionSearchSuggestions();
}

// En celular el cuadro de sugerencias va fijo justo debajo del buscador
function positionSearchSuggestions() {
  const box = document.getElementById("search-suggest");
  const form = document.getElementById("catalog-search-form");
  if (!box || !form || box.hidden) return;
  if (window.matchMedia("(max-width: 640px)").matches) {
    const r = form.getBoundingClientRect();
    box.style.top = Math.max(8, Math.round(r.bottom + 6)) + "px";
  } else {
    box.style.top = "";
  }
}

function hideSearchSuggestions() {
  const box = document.getElementById("search-suggest");
  if (box) box.hidden = true;
}

window.quickAddFromSuggestion = function (sku, btn) {
  addProductToCart(sku, 1, null);
  if (btn) {
    btn.textContent = "✓";
    btn.classList.add("added");
    setTimeout(() => { btn.textContent = "+"; btn.classList.remove("added"); }, 1200);
  }
};

window.openSuggestion = function (sku) {
  const prod = AppState.masterCatalog.find((p) => p.sku === sku);
  if (!prod) return;
  const input = document.getElementById("catalog-search-input");
  triggerCatalogSearch();
  // Resalta el producto elegido dentro de los resultados
  setTimeout(() => {
    const card = document.querySelector(`.product-card[data-sku="${CSS && CSS.escape ? CSS.escape(sku) : sku}"]`);
    if (card) {
      card.scrollIntoView({ behavior: "smooth", block: "center" });
      card.classList.add("flash");
      setTimeout(() => card.classList.remove("flash"), 1800);
    }
  }, 350);
  if (input) input.blur();
};

function syncUrlState() {
  try {
    const url = new URL(window.location.href);
    const q = (AppState.searchTerm || "").trim();
    if (q) url.searchParams.set("q", q); else url.searchParams.delete("q");
    if (AppState.filterCategory !== "all") url.searchParams.set("depto", AppState.filterCategory); else url.searchParams.delete("depto");
    const next = url.pathname + (url.searchParams.toString() ? "?" + url.searchParams.toString() : "") + url.hash;
    history.replaceState(history.state, "", next);
  } catch (_) {}
}

function applyStateFromUrl() {
  try {
    const params = new URLSearchParams(window.location.search);
    const q = (params.get("q") || "").trim();
    const depto = params.get("depto");
    if (depto && AppState.masterCatalog.some((p) => (p.category || p.categories?.name) === depto)) {
      AppState.filterCategory = depto;
      updateFacetSelection();
    }
    if (q) {
      AppState.searchTerm = q;
      const input = document.getElementById("catalog-search-input");
      if (input) input.value = q;
      const clearBtn = document.getElementById("search-clear-btn");
      if (clearBtn) clearBtn.style.display = "block";
    }
    if (q || depto) setTimeout(() => scrollToResults(), 300);
  } catch (_) {}
}

function initMobileEnhancements() {
  // Cierra sugerencias al tocar fuera del buscador
  document.addEventListener("click", (e) => {
    if (!e.target.closest || !e.target.closest("#catalog-search-form")) hideSearchSuggestions();
  });

  // Carga continua de productos al llegar al final (sin tener que tocar "Ver más")
  const pager = document.getElementById("pagination-container");
  if (pager && "IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        // Máximo 3 cargas automáticas por búsqueda: así siempre se puede llegar a Sucursales y al pie de página
        if (
          entry.isIntersecting &&
          AppState.catalogReady &&
          !AppState.suspendAutoLoad &&
          (AppState.autoLoads || 0) < 3 &&
          AppState.displayedCount < AppState.filteredCatalog.length
        ) {
          AppState.autoLoads = (AppState.autoLoads || 0) + 1;
          window.loadMoreProducts();
        }
      });
    }, { rootMargin: "600px 0px" });
    io.observe(pager);
  }

  // Cabecera compacta al desplazarse (deja solo el buscador visible en celular)
  let ticking = false;
  const onScroll = () => {
    ticking = false;
    document.body.classList.toggle("is-scrolled", window.scrollY > 160);
  };
  window.addEventListener("scroll", () => {
    positionSearchSuggestions();
    if (!ticking) {
      ticking = true;
      requestAnimationFrame(onScroll);
    }
  }, { passive: true });
  onScroll();

  // Service Worker: abre más rápido y funciona con señal débil en la obra
  if ("serviceWorker" in navigator && window.location.protocol === "https:") {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("sw.js").catch(() => {});
    });
  }
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// Window & Environment Bindings
window.setBranch = setBranch;
window.dispatchToWhatsApp = dispatchToWhatsApp;
window.formatWhatsAppMessage = formatWhatsAppMessage;
window.BRANCHES = BRANCHES;
window.AppState = AppState;
window.addProductToCart = addProductToCart;
window.quickSearch = quickSearch;
window.resetAllFiltersKeepSearch = resetAllFiltersKeepSearch;
window.setDrawerStep = setDrawerStep;
window.saveCustomerDataToCache = saveCustomerDataToCache;
window.loadCustomerDataFromCache = loadCustomerDataFromCache;
window.clearCustomerCache = clearCustomerCache;
window.updateCustomerDataStatusBadge = updateCustomerDataStatusBadge;
window.formatPhoneInput = formatPhoneInput;

if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    CONFIG,
    BRANCHES,
    AppState,
    setBranch,
    updateBranchUI,
    addProductToCart,
    updateCartUI,
    formatWhatsAppMessage,
    dispatchToWhatsApp,
    quickSearch,
    resetAllFiltersKeepSearch,
    setDrawerStep,
    saveCustomerDataToCache,
    loadCustomerDataFromCache,
    clearCustomerCache,
    updateCustomerDataStatusBadge,
    formatPhoneInput,
    escapeHtml
  };
}


