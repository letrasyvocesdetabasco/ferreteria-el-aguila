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
    name: "Sucursal Las Delicias (Matriz)",
    address: "Calle Revolución No. 1203, Col. Las Delicias (junto al Centro de Salud San Joaquín)",
    city: "Villahermosa, Tabasco",
    phone: "993 289 2935",
    whatsapp: "529932892935",
    badge: "Matriz Principal",
    isMatriz: true,
    schedule: "Lunes a Sábado: 7:30 a 18:30 hrs | Domingo: 8:00 a 14:00 hrs"
  },
  marzo: {
    id: "marzo",
    name: "Sucursal 18 de Marzo",
    address: "Revolución 1350, Local G, Cuadrante II, Col. 18 de Marzo",
    city: "Villahermosa, Tabasco",
    phone: "993 161 2163",
    whatsapp: "529931612163",
    badge: "Sucursal Cuadrante II",
    isMatriz: false,
    schedule: "Lunes a Sábado: 7:30 a 18:30 hrs"
  },
  gaviotas: {
    id: "gaviotas",
    name: "Sucursal Gaviotas Norte",
    address: "Aquiles Calderón Marchena 120, Col. Gaviotas Norte",
    city: "Villahermosa, Tabasco",
    phone: "993 289 2935",
    whatsapp: "529932892935",
    badge: "Sucursal Gaviotas",
    isMatriz: false,
    schedule: "Lunes a Sábado: 7:30 a 18:00 hrs"
  }
};

// ==========================================================================
// 2. Estado Global de la Aplicación
// ==========================================================================
const AppState = {
  masterCatalog: [],
  filteredCatalog: [],
  selectedBranch: localStorage.getItem(CONFIG.STORAGE_BRANCH_KEY) || "delicias",
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

  const drawerBranchName = document.getElementById("drawer-selected-branch-name");
  if (drawerBranchName) drawerBranchName.textContent = branch.name;

  const drawerBranchPhone = document.getElementById("drawer-selected-branch-phone");
  if (drawerBranchPhone) drawerBranchPhone.textContent = branch.phone;

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
    const catName = prod.categories?.name || "General";
    categoryMap.set(catName, (categoryMap.get(catName) || 0) + 1);

    const brandName = prod.brands?.name || "Homologado";
    brandMap.set(brandName, (brandMap.get(brandName) || 0) + 1);
  });

  const catList = document.getElementById("categories-facet");
  if (catList) {
    catList.innerHTML = `
      <li class="facet-item ${AppState.filterCategory === "all" ? "active" : ""}" data-category="all">
        <span>Todos los Departamentos</span>
        <span class="facet-count">${AppState.masterCatalog.length}</span>
      </li>
    `;
    categoryMap.forEach((count, name) => {
      const li = document.createElement("li");
      li.className = `facet-item ${AppState.filterCategory === name ? "active" : ""}`;
      li.dataset.category = name;
      li.innerHTML = `<span>${name}</span><span class="facet-count">${count}</span>`;
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
        <span class="facet-count">${AppState.masterCatalog.length}</span>
      </li>
    `;
    brandMap.forEach((count, name) => {
      const li = document.createElement("li");
      li.className = `facet-item ${AppState.filterBrand === name ? "active" : ""}`;
      li.dataset.brand = name;
      li.innerHTML = `<span>${name}</span><span class="facet-count">${count}</span>`;
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
    const passCat =
      AppState.filterCategory === "all" ||
      (item.categories?.name && item.categories.name === AppState.filterCategory);

    const passBrand =
      AppState.filterBrand === "all" ||
      (item.brands?.name && item.brands.name === AppState.filterBrand);

    let passSearch = true;
    if (query) {
      const nameMatch = item.name?.toLowerCase().includes(query);
      const skuMatch = item.sku?.toLowerCase().includes(query);
      const codeMatch = item.manufacturer_code?.toLowerCase().includes(query);
      const brandMatch = item.brands?.name?.toLowerCase().includes(query);
      const descMatch = item.description?.toLowerCase().includes(query);

      let attrMatch = false;
      if (item.attributes && typeof item.attributes === "object") {
        for (const [k, v] of Object.entries(item.attributes)) {
          if (String(k).toLowerCase().includes(query) || String(v).toLowerCase().includes(query)) {
            attrMatch = true;
            break;
          }
        }
      }

      passSearch = nameMatch || skuMatch || codeMatch || brandMatch || descMatch || attrMatch;
    }

    return passCat && passBrand && passSearch;
  });

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
// 6. Renderizado de Productos Modernos y Comerciales
// ==========================================================================
function renderCatalogGrid() {
  const grid = document.getElementById("products-container");
  const counter = document.getElementById("counter-display");
  if (!grid) return;

  grid.innerHTML = "";
  const count = AppState.filteredCatalog.length;
  if (counter) {
    counter.textContent = `Mostrando ${count} de ${AppState.masterCatalog.length} artículos técnicos`;
  }

  if (count === 0) {
    grid.innerHTML = `
      <div class="empty-catalog-state" style="grid-column: 1/-1; background:#fff; padding:40px; text-align:center; border-radius:12px; border:1px solid #e2e8f0;">
        <h3 style="font-size:1.2rem; margin-bottom:8px; color:#0f172a;">Sin resultados para "${escapeHtml(AppState.searchTerm)}"</h3>
        <p style="color:#64748b; margin-bottom:14px;">Prueba buscando por término general como <em>"tornillo", "cobre", "cpvc", "cable", "fandeli"</em> o limpia los filtros.</p>
        <button class="btn-hero-primary" onclick="resetAllFilters()">Restablecer Filtros</button>
      </div>
    `;
    return;
  }

  AppState.filteredCatalog.forEach((prod) => {
    const card = document.createElement("article");
    card.className = "product-card";

    // Chips de Atributos Técnicos
    let chipsHtml = "";
    if (prod.attributes && typeof prod.attributes === "object") {
      chipsHtml = Object.entries(prod.attributes)
        .slice(0, 3)
        .map(([k, v]) => `<span class="spec-chip"><strong>${escapeHtml(k)}:</strong> ${escapeHtml(String(v))}</span>`)
        .join("");
    }

    const brandName = prod.brands?.name || "Homologado";
    const priceFormatted = parseFloat(prod.base_price).toFixed(2);
    const mfgCodeStr = prod.manufacturer_code ? ` | Clave: ${escapeHtml(prod.manufacturer_code)}` : "";
    const featureBadge = prod.badge || "Garantizado";
    const imgUrl = prod.image || "assets/images/hero-storefront.jpg";

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

        <h3 class="product-title">${escapeHtml(prod.name)}</h3>
        <p class="product-description">${escapeHtml(prod.description || "")}</p>

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
            <button class="stepper-btn" onclick="stepQuantity('${prod.sku}', -1)">-</button>
            <input type="number" id="qty-${prod.sku}" class="qty-input" min="1" max="999" value="1">
            <button class="stepper-btn" onclick="stepQuantity('${prod.sku}', 1)">+</button>
          </div>

          <button class="btn-add-to-quote" id="btn-add-${prod.sku}" onclick="handleAddProduct('${prod.sku}')">
            <span>🛒 + Cotizar</span>
          </button>
        </div>
      </div>
    `;

    grid.appendChild(card);
  });
}

window.stepQuantity = function(sku, delta) {
  const input = document.getElementById(`qty-${sku}`);
  if (!input) return;
  let val = parseInt(input.value, 10) || 1;
  val = Math.max(1, Math.min(999, val + delta));
  input.value = val;
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

window.handleAddProduct = function (sku) {
  const product = AppState.masterCatalog.find((p) => p.sku === sku);
  if (!product) return;

  const qtyInput = document.getElementById(`qty-${sku}`);
  const quantityToAdd = qtyInput ? parseInt(qtyInput.value, 10) || 1 : 1;

  if (AppState.quoteCart.has(sku)) {
    AppState.quoteCart.get(sku).quantity += quantityToAdd;
  } else {
    AppState.quoteCart.set(sku, { item: product, quantity: quantityToAdd });
  }

  saveCartToStorage();
  updateCartUI();

  const btn = document.getElementById(`btn-add-${sku}`);
  if (btn) {
    const originalText = btn.innerHTML;
    btn.classList.add("added");
    btn.innerHTML = "<span>✓ Agregado</span>";
    setTimeout(() => {
      btn.classList.remove("added");
      btn.innerHTML = originalText;
    }, 1200);
  }
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
    alert("El presupuesto no tiene productos agregados.");
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

  let msg = `*SOLICITUD DE COTIZACIÓN DE MATERIALES*\n`;
  msg += `*FERRETERÍA Y TLAPALERÍA EL ÁGUILA*\n`;
  msg += `━━━━━━━━━━━━━━━━━━━━━\n`;
  msg += `📍 *Sucursal Destino:* ${branch.name}\n`;
  msg += `🏢 *Dirección:* ${branch.address}\n`;
  msg += `📅 *Fecha:* ${dateStr}\n\n`;

  msg += `*DATOS DEL SOLICITANTE / OBRA:*\n`;
  msg += `• *Cliente / Empresa:* ${clientName || "Mostrador / Contratista"}\n`;
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
  msg += `_Solicito amablemente confirmar existencias en sucursal, descuentos por volumen y tiempo de entrega. Saludos cordiales._`;

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
