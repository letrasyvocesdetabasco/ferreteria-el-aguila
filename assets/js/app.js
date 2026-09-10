/**
 * Ferretería y Tlapalería El Águila - Villahermosa, Tabasco
 * Motor de Catálogo Técnico Paramétrico y Presupuestador de Obra por WhatsApp
 * 
 * Arquitectura Jamstack de alto rendimiento con doble fase (Supabase Client + Contingencia JSON)
 */

// ==========================================================================
// 1. Configuración y Sucursales en Villahermosa
// ==========================================================================
const CONFIG = {
  SUPABASE_URL: "https://TU_PROYECTO.supabase.co", // Reemplazar con URL de Supabase si aplica
  SUPABASE_ANON_KEY: "TU_CLAVE_ANONIMA",          // Reemplazar con Anon Key de Supabase
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
    schedule: "Lunes a Sábado: 7:30 - 18:30 | Domingo: 8:00 - 14:00"
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
    schedule: "Lunes a Sábado: 7:30 - 18:30"
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
    schedule: "Lunes a Sábado: 7:30 - 18:00"
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

  // Intentar inicializar cliente de Supabase si hay credenciales válidas
  if (
    typeof supabase !== "undefined" &&
    CONFIG.SUPABASE_URL &&
    !CONFIG.SUPABASE_URL.includes("TU_PROYECTO")
  ) {
    try {
      supabaseClient = supabase.createClient(CONFIG.SUPABASE_URL, CONFIG.SUPABASE_ANON_KEY);
      const { data, error } = await supabaseClient
        .from("products")
        .select("sku,manufacturer_code,name,slug,base_price,unit_measure,stock_status,attributes,categories(name,slug),brands(name)")
        .eq("is_active", true)
        .order("name", { ascending: true });

      if (!error && Array.isArray(data) && data.length > 0) {
        AppState.masterCatalog = data;
        AppState.isSupabaseActive = true;
        console.log("Catálogo cargado en vivo desde Supabase PostgREST:", data.length, "ítems");
      } else {
        throw new Error(error?.message || "Sin datos en Supabase");
      }
    } catch (sbErr) {
      console.warn("Supabase no disponible. Conmutando a contingencia local JSON:", sbErr);
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
    console.log("Catálogo cargado desde contingencia local data/products.json:", data.length, "ítems");
  } catch (err) {
    console.error("Error crítico al cargar el catálogo local:", err);
    document.getElementById("products-container").innerHTML = `
      <div class="empty-catalog-state">
        <h3>Error de Carga</h3>
        <p>No se pudo cargar el archivo local <code>data/products.json</code>. Verifica la conexión o servidor.</p>
      </div>
    `;
  }
}

// ==========================================================================
// 4. Sucursales en Villahermosa
// ==========================================================================
function initBranchSelector() {
  const select = document.getElementById("branch-select");
  if (!select) return;

  select.value = AppState.selectedBranch;
  updateBranchUI(AppState.selectedBranch);

  select.addEventListener("change", (e) => {
    setBranch(e.target.value);
  });
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

  // Actualizar tarjetas en el modal si está abierto
  document.querySelectorAll(".branch-detail-card").forEach((card) => {
    if (card.dataset.branchId === branchId) {
      card.classList.add("active-branch");
    } else {
      card.classList.remove("active-branch");
    }
  });
}

// ==========================================================================
// 5. Facetas y Pipeline de Filtrado Paramétrico
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

  // Renderizar Facetas de Departamentos
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
      };
      catList.appendChild(li);
    });

    catList.firstElementChild.onclick = () => {
      AppState.filterCategory = "all";
      updateFacetSelection();
      applyFilterPipeline();
    };
  }

  // Renderizar Facetas de Marcas
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
      };
      brandList.appendChild(li);
    });

    brandList.firstElementChild.onclick = () => {
      AppState.filterBrand = "all";
      updateFacetSelection();
      applyFilterPipeline();
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
    // Filtro por Departamento
    const passCat =
      AppState.filterCategory === "all" ||
      (item.categories?.name && item.categories.name === AppState.filterCategory);

    // Filtro por Marca
    const passBrand =
      AppState.filterBrand === "all" ||
      (item.brands?.name && item.brands.name === AppState.filterBrand);

    // Búsqueda cruzada multi-campo
    let passSearch = true;
    if (query) {
      const nameMatch = item.name?.toLowerCase().includes(query);
      const skuMatch = item.sku?.toLowerCase().includes(query);
      const codeMatch = item.manufacturer_code?.toLowerCase().includes(query);
      const brandMatch = item.brands?.name?.toLowerCase().includes(query);
      const descMatch = item.description?.toLowerCase().includes(query);

      // Búsqueda en atributos técnicos JSONB
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

  // Ordenamiento
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
// 6. Renderizado de la Cuadrícula Técnica (Estilo McMaster-Carr)
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
      <div class="empty-catalog-state">
        <h3>Sin resultados coincidentes</h3>
        <p>No se encontraron partidas para "${escapeHtml(AppState.searchTerm)}" con los filtros seleccionados.</p>
        <button class="btn-reset-filter" onclick="resetAllFilters()" style="margin-top: 10px; padding: 6px 14px; background: var(--primary); color: #fff; border-radius: 4px;">
          Restablecer Filtros
        </button>
      </div>
    `;
    return;
  }

  AppState.filteredCatalog.forEach((prod) => {
    const card = document.createElement("article");
    card.className = "product-card";

    // Generar tabla técnica de atributos (hasta 4 atributos destacados)
    let specsHtml = "";
    if (prod.attributes && typeof prod.attributes === "object") {
      const entries = Object.entries(prod.attributes).slice(0, 4);
      if (entries.length > 0) {
        specsHtml = `
          <table class="specs-table">
            <tbody>
              ${entries
                .map(
                  ([k, v]) => `
                <tr>
                  <td class="spec-key">${escapeHtml(k)}:</td>
                  <td class="spec-val">${escapeHtml(String(v))}</td>
                </tr>
              `
                )
                .join("")}
            </tbody>
          </table>
        `;
      }
    }

    const brandName = prod.brands?.name || "Homologado";
    const priceFormatted = parseFloat(prod.base_price).toFixed(2);
    const mfgCodeStr = prod.manufacturer_code ? ` | Clave: ${escapeHtml(prod.manufacturer_code)}` : "";

    card.innerHTML = `
      <div>
        <div class="product-top-row">
          <span class="sku-tag">SKU: ${escapeHtml(prod.sku)}${mfgCodeStr}</span>
          <span class="brand-tag">${escapeHtml(brandName)}</span>
        </div>
        <h3 class="product-title">${escapeHtml(prod.name)}</h3>
        <div class="stock-indicator">
          <span class="stock-dot"></span>
          <span>Disponible en mostrador físico</span>
        </div>
        <p class="product-description">${escapeHtml(prod.description || "")}</p>
        ${specsHtml}
      </div>
      <div class="product-bottom-bar">
        <div class="pricing-row">
          <span class="price-display">$${priceFormatted}</span>
          <span class="unit-label">x ${escapeHtml(prod.unit_measure || "PZA")}</span>
        </div>
        <div class="card-action-row">
          <input type="number" id="qty-${prod.sku}" class="qty-input" min="1" max="9999" value="1" title="Cantidad">
          <button class="btn-add-to-quote" id="btn-add-${prod.sku}" onclick="handleAddProduct('${prod.sku}')">
            <span>+ Añadir al Presupuesto</span>
          </button>
        </div>
      </div>
    `;

    grid.appendChild(card);
  });
}

// ==========================================================================
// 7. Manejo del Carrito de Cotización y Presupuesto
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
    console.warn("No se pudo cargar el carrito guardado:", err);
  }
  updateCartUI();
}

function saveCartToStorage() {
  try {
    const serialized = Array.from(AppState.quoteCart.values());
    localStorage.setItem(CONFIG.STORAGE_CART_KEY, JSON.stringify(serialized));
  } catch (err) {
    console.warn("Error al guardar carrito en localStorage:", err);
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

  // Feedback visual momentáneo en el botón
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
        <div class="cart-empty-message">
          <p>No hay partidas agregadas al presupuesto.</p>
          <p style="font-size: 0.78rem; margin-top: 6px; color: #7a869a;">
            Explora el catálogo y pulsa <strong>"+ Añadir al Presupuesto"</strong> para cotizar tornillería, plomería, cable o herramientas.
          </p>
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
        row.innerHTML = `
          <div class="cart-item-info">
            <div class="cart-item-name" title="${escapeHtml(item.name)}">${escapeHtml(item.name)}</div>
            <div class="cart-item-sku">SKU: ${escapeHtml(sku)}${item.manufacturer_code ? ` | Clave: ${escapeHtml(item.manufacturer_code)}` : ""}</div>
            <div class="cart-item-price">$${parseFloat(item.base_price).toFixed(2)} x ${item.unit_measure || "PZA"} = <strong>$${subtotal.toFixed(2)}</strong></div>
          </div>
          <div style="display: flex; align-items: center; gap: 6px;">
            <input 
              type="number" 
              class="cart-item-qty" 
              min="1" 
              max="9999" 
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
  if (totalElem) totalElem.textContent = `$${totalMoney.toFixed(2)}`;
}

// ==========================================================================
// 8. Cierre de Cotización y Envío hacia WhatsApp
// ==========================================================================
function dispatchToWhatsApp() {
  if (AppState.quoteCart.size === 0) {
    alert("El presupuesto está vacío. Añade partidas desde el catálogo técnico.");
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

  // Construcción del mensaje formal estructurado
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
    msg += `   └ Cantidad: *${quantity}* ${item.unit_measure || "PZA"} | P.U: $${parseFloat(item.base_price).toFixed(2)} | Subtotal: *$${itemSubtotal.toFixed(2)}*\n`;
    idx++;
  });

  msg += `━━━━━━━━━━━━━━━━━━━━━\n`;
  msg += `*TOTAL ESTIMADO:* *$${totalEstimado.toFixed(2)} MXN*\n\n`;
  msg += `_Solicito amablemente confirmar existencias físicas en sucursal, tiempo de entrega en obra y condiciones de pago. Saludos cordiales._`;

  const encodedMsg = encodeURIComponent(msg);
  const targetNumber = branch.whatsapp;
  const whatsappUrl = `https://wa.me/${targetNumber}?text=${encodedMsg}`;

  window.open(whatsappUrl, "_blank");
}

// ==========================================================================
// 9. Event Listeners y Modales
// ==========================================================================
function initEventListeners() {
  // Buscador con debounce simple
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

  // Ordenamiento
  const sortSelect = document.getElementById("catalog-sort-select");
  if (sortSelect) {
    sortSelect.addEventListener("change", (e) => {
      AppState.sortMode = e.target.value;
      sortCatalog();
      renderCatalogGrid();
    });
  }

  // Drawer de Cotización
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

  // Modal de Sucursales en Villahermosa
  const branchesModal = document.getElementById("branches-modal");
  const openBranchesBtn = document.getElementById("btn-view-branches");
  const closeBranchesBtn = document.getElementById("btn-close-branches-modal");

  const openBranchesModal = () => {
    if (branchesModal) branchesModal.classList.add("active");
  };

  const closeBranchesModal = () => {
    if (branchesModal) branchesModal.classList.remove("active");
  };

  if (openBranchesBtn) openBranchesBtn.addEventListener("click", openBranchesModal);
  if (closeBranchesBtn) closeBranchesBtn.addEventListener("click", closeBranchesModal);
  if (branchesModal) {
    branchesModal.addEventListener("click", (e) => {
      if (e.target === branchesModal) closeBranchesModal();
    });
  }
}

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

window.selectBranchFromModal = function (branchId) {
  setBranch(branchId);
  const modal = document.getElementById("branches-modal");
  if (modal) modal.classList.remove("active");
};

// Utilidad para escape seguro de cadenas en el DOM
function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
