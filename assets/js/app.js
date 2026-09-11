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
  STORAGE_BRANCH_KEY: "elaguila_selected_branch"
};

const BRANCHES = {
  delicias: {
    id: "delicias",
    name: "Sucursal Las Delicias",
    address: "Av. Revolución 1203, Cuadrante II, Las Delicias, C.P. 86140, Villahermosa, Tab.",
    landmark: "A un lado del Centro de Salud San Joaquín",
    city: "Villahermosa, Tabasco",
    phone: "993 289 2935",
    whatsapp: "529932892935",
    badge: "Matriz / Mostrador Delicias",
    isMatriz: true,
    schedule: "Lunes a Sábado: 7:30 a 18:30 hrs | Domingo: 8:00 a 14:00 hrs"
  },
  buenavista: {
    id: "buenavista",
    name: "Sucursal Estrellas de Buena Vista",
    address: "Carr. Villahermosa a La Isla Km 5.300, Buena Vista 1ra Secc, C.P. 86280, Villahermosa, Tab.",
    landmark: "Buena Vista 1ra Secc",
    city: "Villahermosa, Tabasco",
    phone: "993 192 8313",
    whatsapp: "529931928313",
    badge: "Sucursal Buena Vista",
    isMatriz: false,
    schedule: "Lunes a Sábado: 7:30 a 18:30 hrs | Domingo: Cerrado"
  }
};

// ==========================================================================
// 2. Estado Global de la Aplicación
// ==========================================================================
const AppState = {
  masterCatalog: [],
  filteredCatalog: [],
  displayedCount: 36,
  pageSize: 36,
  selectedBranch: (localStorage.getItem(CONFIG.STORAGE_BRANCH_KEY) === "buenavista") ? "buenavista" : "delicias",
  filterCategory: "all",
  filterBrand: "all",
  searchTerm: "",
  sortMode: "name-asc",
  quoteCart: new Map(), // SKU -> { item, quantity }
  isSupabaseActive: false
};

let supabaseClient = null;

// ==========================================================================
// 3. Inicialización y Carga de Datos (Doble Fase)
// ==========================================================================
document.addEventListener("DOMContentLoaded", () => {
  initBranchSelector();
  initCartFromStorage();
  initEventListeners();
  loadCatalogData();
});

async function loadCatalogData() {
  const counterElem = document.getElementById("counter-display");
  if (counterElem) counterElem.textContent = "Conectando con inventario técnico...";

  if (
    typeof supabase !== "undefined" &&
    CONFIG.SUPABASE_URL &&
    !CONFIG.SUPABASE_URL.includes("TU_PROYECTO")
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

  generateFacetFilters();
  applyFilterPipeline();
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
  }
}

// ==========================================================================
// 4. Sucursales en Villahermosa
// ==========================================================================
function initBranchSelector() {
  const select = document.getElementById("branch-select");
  if (select) {
    select.value = AppState.selectedBranch;
    select.addEventListener("change", (e) => setBranch(e.target.value));
  }
  updateBranchUI(AppState.selectedBranch);
}

function setBranch(branchId) {
  if (!BRANCHES[branchId]) return;
  AppState.selectedBranch = branchId;
  localStorage.setItem(CONFIG.STORAGE_BRANCH_KEY, branchId);
  updateBranchUI(branchId);
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
    sendWhatsAppBtn.innerHTML = `<span>💬 Enviar Presupuesto a ${branch.name} (WhatsApp)</span>`;
  }

  // Actualizar botón flotante de WhatsApp y barra fija móvil
  const floatingWa = document.getElementById("floating-wa-btn");
  const mobileNavWa = document.getElementById("mobile-nav-wa");
  const waUrl = `https://wa.me/${branch.whatsapp}?text=${encodeURIComponent("Hola Ferretería El Águila (" + branch.name + "), me gustaría consultar existencias y cotizar un material.")}`;
  if (floatingWa) floatingWa.href = waUrl;
  if (mobileNavWa) mobileNavWa.href = waUrl;

  // Actualizar tarjetas de sucursal destacadas
  document.querySelectorAll(".branch-feature-card").forEach((card) => {
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
        scrollToCatalog();
      };
      catList.appendChild(li);
    });

    catList.firstElementChild.onclick = () => {
      AppState.filterCategory = "all";
      updateFacetSelection();
      applyFilterPipeline();
      scrollToCatalog();
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
        scrollToCatalog();
      };
      brandList.appendChild(li);
    });

    brandList.firstElementChild.onclick = () => {
      AppState.filterBrand = "all";
      updateFacetSelection();
      applyFilterPipeline();
      scrollToCatalog();
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

function applyFilterPipeline() {
  const query = AppState.searchTerm.toLowerCase().trim();

  AppState.filteredCatalog = AppState.masterCatalog.filter((item) => {
    const catName = item.category || item.categories?.name || "";
    const passCat =
      AppState.filterCategory === "all" ||
      catName.toLowerCase() === AppState.filterCategory.toLowerCase();

    const brandName = item.brand || item.brands?.name || "";
    const passBrand =
      AppState.filterBrand === "all" ||
      brandName.toLowerCase() === AppState.filterBrand.toLowerCase();

    let passSearch = true;
    if (query) {
      const nameMatch = item.name && item.name.toLowerCase().includes(query);
      const skuMatch = item.sku && item.sku.toLowerCase().includes(query);
      const codeMatch = item.manufacturer_code && item.manufacturer_code.toLowerCase().includes(query);
      const brandMatch = brandName && brandName.toLowerCase().includes(query);
      const catMatch = catName && catName.toLowerCase().includes(query);
      const descMatch = item.description && item.description.toLowerCase().includes(query);

      let attrMatch = false;
      if (item.attributes && typeof item.attributes === "object") {
        for (const [k, v] of Object.entries(item.attributes)) {
          if (String(k).toLowerCase().includes(query) || String(v).toLowerCase().includes(query)) {
            attrMatch = true;
            break;
          }
        }
      }

      passSearch = nameMatch || skuMatch || codeMatch || brandMatch || catMatch || descMatch || attrMatch;
    }

    return passCat && passBrand && passSearch;
  });

  AppState.displayedCount = AppState.pageSize;
  sortCatalog();
  renderCatalogGrid();
}

function sortCatalog() {
  switch (AppState.sortMode) {
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
      AppState.filteredCatalog.sort((a, b) => a.name.localeCompare(b.name));
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
    counter.textContent = `Mostrando ${currentShowing.toLocaleString('es-MX')} de ${totalCount.toLocaleString('es-MX')} artículos (${AppState.masterCatalog.length.toLocaleString('es-MX')} en inventario total)`;
  }

  if (totalCount === 0) {
    grid.innerHTML = `
      <div class="empty-catalog-state" style="grid-column: 1/-1; background:#fff; padding:40px; text-align:center; border-radius:12px; border:1px solid #e2e8f0;">
        <h3 style="font-size:1.2rem; margin-bottom:8px; color:#0f172a;">Sin resultados para "${escapeHtml(AppState.searchTerm)}"</h3>
        <p style="color:#64748b; margin-bottom:14px;">Prueba buscando por término general como <em>"tornillo", "cobre", "cpvc", "cable", "fandeli", "broca"</em> o limpia los filtros.</p>
        <button class="btn-hero-primary" onclick="resetAllFilters()">Restablecer Filtros</button>
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

function createProductCardElement(prod) {
  const card = document.createElement("article");
  card.className = "product-card";
  card.dataset.sku = prod.sku;

  const catName = prod.category || prod.categories?.name || "General";
  const brandName = prod.brand || prod.brands?.name || "Homologado";
  const priceFormatted = parseFloat(prod.base_price).toFixed(2);
  const featureBadge = prod.badge || "En Existencia";
  const imgUrl = prod.image || prod.image_url || "assets/images/cat-tlapaleria.jpg";
  const descText = prod.description || `${prod.name} - Calidad garantizada para obra y mantenimiento.`;

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

  card.innerHTML = `
    <div class="product-image-container">
      <img 
        src="${escapeHtml(imgUrl)}" 
        alt="${escapeHtml(prod.name)}" 
        class="product-thumb-img" 
        loading="lazy"
        onerror="this.src='assets/images/hero-storefront.jpg'"
      >
      <div class="card-badge-stock">
        <span class="stock-pulsing-dot"></span>
        <span>En Mostrador</span>
      </div>
      <div class="card-badge-feature">${escapeHtml(featureBadge)}</div>
    </div>

    <div class="product-card-body">
      <div class="product-brand-line">
        <span class="brand-name-pill">${escapeHtml(brandName)}</span>
        <span class="sku-pill">SKU: ${escapeHtml(prod.sku)}</span>
      </div>

      <h3 class="product-title" title="${escapeHtml(prod.name)}">${escapeHtml(prod.name)}</h3>
      <p class="product-description">${escapeHtml(descText)}</p>

      <div class="specs-chips-container">
        ${chipsHtml}
      </div>
    </div>

    <div class="product-card-footer">
      <div class="price-row">
        <span class="price-val">$${priceFormatted}</span>
        <span class="unit-val">x ${escapeHtml(prod.unit_measure || "PZA")}</span>
      </div>

      <div class="card-actions-bar">
        <div class="stepper-container">
          <button class="stepper-btn" onclick="stepQuantity(this, -1)">-</button>
          <input type="number" class="qty-input" min="1" max="999" value="1">
          <button class="stepper-btn" onclick="stepQuantity(this, 1)">+</button>
        </div>

        <button class="btn-add-to-quote" onclick="handleAddProductFromCard(this)">
          <span>🛒 + Cotizar</span>
        </button>
      </div>
    </div>
  `;

  return card;
}

function updatePaginationUI() {
  const paginationBox = document.getElementById("pagination-container");
  const counter = document.getElementById("counter-display");
  if (!paginationBox) return;

  const totalCount = AppState.filteredCatalog.length;
  const currentShowing = Math.min(AppState.displayedCount, totalCount);

  if (counter) {
    counter.textContent = `Mostrando ${currentShowing.toLocaleString('es-MX')} de ${totalCount.toLocaleString('es-MX')} artículos (${AppState.masterCatalog.length.toLocaleString('es-MX')} en inventario total)`;
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
      <span>📥 Cargar ${nextBatch.toLocaleString('es-MX')} productos más (${remaining.toLocaleString('es-MX')} restantes)</span>
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
    const originalText = btn.innerHTML;
    btn.classList.add("added");
    btn.innerHTML = "<span>✓ Agregado</span>";
    setTimeout(() => {
      btn.classList.remove("added");
      btn.innerHTML = originalText;
    }, 1200);
  }
}

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
          <p style="font-size: 0.8rem;">Selecciona productos de plomería, tornillería G5, cable o herramientas para cotizar de inmediato vía WhatsApp.</p>
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
        const thumb = item.image || "assets/images/hero-storefront.jpg";

        row.innerHTML = `
          <img src="${thumb}" alt="${escapeHtml(item.name)}" class="cart-item-thumb" onerror="this.src='assets/images/hero-storefront.jpg'">
          <div class="cart-item-info">
            <div class="cart-item-name" title="${escapeHtml(item.name)}">${escapeHtml(item.name)}</div>
            <div class="cart-item-sku">SKU: ${escapeHtml(sku)}</div>
            <div class="cart-item-price">$${parseFloat(item.base_price).toFixed(2)} x ${item.unit_measure || "PZA"} = <strong>$${subtotal.toFixed(2)}</strong></div>
          </div>
          <div style="display: flex; align-items: center; gap: 6px;">
            <input 
              type="number" 
              class="cart-item-qty" 
              min="1" 
              max="999" 
              value="${quantity}" 
              onchange="handleUpdateCartQty('${sku}', this.value)"
            >
            <button class="btn-remove-item" title="Eliminar partida" onclick="handleRemoveCartItem('${sku}')">&times;</button>
          </div>
        `;
        drawerList.appendChild(row);
      }
    });
  }

  if (countPill) countPill.textContent = totalItemsCount;
  const mobileCountPill = document.getElementById("mobile-cart-count");
  if (mobileCountPill) mobileCountPill.textContent = totalItemsCount;
  if (totalElem) totalElem.textContent = `$${totalMoney.toFixed(2)}`;
}

// ==========================================================================
// 8. Cierre de Cotización y Despacho WhatsApp
// ==========================================================================
function dispatchToWhatsApp() {
  if (AppState.quoteCart.size === 0) {
    alert("Tu presupuesto está vacío. Agrega productos del catálogo para poder cotizar.");
    return;
  }

  const branch = BRANCHES[AppState.selectedBranch] || BRANCHES.delicias;
  const clientNameInput = document.getElementById("quote-client-name");
  const siteInput = document.getElementById("quote-client-site");
  const notesInput = document.getElementById("quote-client-notes");

  const clientName = clientNameInput ? clientNameInput.value.trim() : "";
  const siteLocation = siteInput ? siteInput.value.trim() : "";
  const notes = notesInput ? notesInput.value.trim() : "";

  const now = new Date();
  const dateStr = now.toLocaleDateString("es-MX", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit"
  });

  const branchAddress = branch.id === "delicias"
    ? `${branch.address} (A un lado del Centro de Salud San Joaquín)`
    : branch.address;

  let msg = `*SOLICITUD DE COTIZACIÓN DE MATERIALES*\n`;
  msg += `*FERRETERÍA Y TLAPALERÍA EL ÁGUILA*\n`;
  msg += `_¡Todo lo que necesitas para tu hogar o trabajo, en un solo lugar!_\n`;
  msg += `━━━━━━━━━━━━━━━━━━━━━\n`;
  msg += `📍 *Sucursal Seleccionada:* ${branch.name}\n`;
  msg += `🏢 *Ubicación:* ${branchAddress}\n`;
  msg += `📱 *Teléfono / WhatsApp Mostrador:* ${branch.phone}\n`;
  msg += `📅 *Fecha:* ${dateStr}\n\n`;

  msg += `*DATOS DEL CLIENTE / OBRA:*\n`;
  msg += `• *Cliente / Empresa:* ${clientName || "Cliente Particular / Mostrador"}\n`;
  msg += `• *Lugar de Entrega / Obra:* ${siteLocation || "Recolección en Mostrador Villahermosa"}\n`;
  if (notes) {
    msg += `• *Notas:* ${notes}\n`;
  }
  msg += `\n*RELACIÓN DE MATERIALES SOLICITADOS:*\n`;

  let idx = 1;
  let totalEstimado = 0;

  AppState.quoteCart.forEach(({ item, quantity }, sku) => {
    const itemSubtotal = item.base_price * quantity;
    totalEstimado += itemSubtotal;
    const refCode = item.manufacturer_code ? `[Clave: ${item.manufacturer_code}]` : `[SKU: ${sku}]`;

    msg += `${idx}. ${refCode} *${item.name}*\n`;
    msg += `   └ Cantidad: *${quantity}* ${item.unit_measure || "PZA"} | Subtotal: *$${itemSubtotal.toFixed(2)}*\n`;
    idx++;
  });

  msg += `━━━━━━━━━━━━━━━━━━━━━\n`;
  msg += `*TOTAL ESTIMADO:* *$${totalEstimado.toFixed(2)} MXN*\n\n`;
  msg += `_Solicito amablemente confirmar existencias en ${branch.name}, descuentos por volumen y tiempo de entrega. Saludos cordiales._`;

  const encodedMsg = encodeURIComponent(msg);
  const targetNumber = branch.whatsapp;
  const whatsappUrl = `https://wa.me/${targetNumber}?text=${encodedMsg}`;

  window.open(whatsappUrl, "_blank");
}

// ==========================================================================
// 9. Event Listeners y Utilidades
// ==========================================================================
function initEventListeners() {
  const searchInput = document.getElementById("catalog-search-input");
  const clearBtn = document.getElementById("search-clear-btn");

  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      AppState.searchTerm = e.target.value;
      if (clearBtn) {
        clearBtn.style.display = e.target.value ? "block" : "none";
      }
      applyFilterPipeline();
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
      applyFilterPipeline();
    });
  }

  const sortSelect = document.getElementById("catalog-sort-select");
  if (sortSelect) {
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

  const openDrawer = () => {
    if (drawer) drawer.classList.add("active");
    if (backdrop) backdrop.classList.add("active");
  };

  const closeDrawer = () => {
    if (drawer) drawer.classList.remove("active");
    if (backdrop) backdrop.classList.remove("active");
  };

  if (openDrawerBtn) openDrawerBtn.addEventListener("click", openDrawer);
  if (closeDrawerBtn) closeDrawerBtn.addEventListener("click", closeDrawer);
  if (backdrop) backdrop.addEventListener("click", closeDrawer);
  if (sendWhatsAppBtn) sendWhatsAppBtn.addEventListener("click", dispatchToWhatsApp);

  window.openQuoteDrawer = openDrawer;
}

window.filterByCategoryBanner = function(catName) {
  AppState.filterCategory = catName;
  AppState.searchTerm = "";
  const searchInput = document.getElementById("catalog-search-input");
  if (searchInput) searchInput.value = "";
  updateFacetSelection();
  applyFilterPipeline();
  scrollToCatalog();
};

window.scrollToCatalog = function() {
  const elem = document.getElementById("catalog-section");
  if (elem) {
    elem.scrollIntoView({ behavior: "smooth", block: "start" });
  }
};

window.scrollToBranches = function() {
  const elem = document.getElementById("branches-section");
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
};

window.selectBranchFromCard = function (branchId) {
  setBranch(branchId);
};

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
