/**
 * Service Worker - Ferretería El Águila
 * Objetivo: que la página abra rápido y siga funcionando con señal débil en la obra.
 * - Páginas, estilos, scripts y catálogo: primero red (siempre lo más nuevo); si no hay señal, copia guardada.
 * - Imágenes: copia guardada primero (ahorra datos), se descargan solo la primera vez.
 * Para forzar actualización general, cambia CACHE_VERSION.
 */
const CACHE_VERSION = "aguila-v3";
const RUNTIME = `${CACHE_VERSION}-runtime`;
const IMAGES = `${CACHE_VERSION}-img`;

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(RUNTIME).then((cache) => cache.addAll(["./", "manifest.webmanifest"]).catch(() => {}))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => !k.startsWith(CACHE_VERSION)).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

function networkFirst(request, timeoutMs) {
  return new Promise((resolve) => {
    let settled = false;
    const fallback = () =>
      caches.match(request, { ignoreSearch: request.mode !== "navigate" }).then((cached) => {
        if (cached) return cached;
        return request.mode === "navigate" ? caches.match("./") : undefined;
      });

    const timer = setTimeout(() => {
      fallback().then((cached) => {
        if (cached && !settled) {
          settled = true;
          resolve(cached);
        }
      });
    }, timeoutMs);

    fetch(request)
      .then((response) => {
        clearTimeout(timer);
        if (response && response.ok) {
          const copy = response.clone();
          caches.open(RUNTIME).then((cache) => cache.put(request, copy)).catch(() => {});
        }
        if (!settled) {
          settled = true;
          resolve(response);
        }
      })
      .catch(() => {
        clearTimeout(timer);
        fallback().then((cached) => {
          if (!settled) {
            settled = true;
            resolve(cached || Response.error());
          }
        });
      });
  });
}

function cacheFirst(request) {
  return caches.match(request).then((cached) => {
    if (cached) return cached;
    return fetch(request).then((response) => {
      if (response && response.ok) {
        const copy = response.clone();
        caches.open(IMAGES).then((cache) => cache.put(request, copy)).catch(() => {});
      }
      return response;
    });
  });
}

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  if (request.destination === "image" || /\.(png|jpe?g|webp|svg|ico)$/i.test(url.pathname)) {
    event.respondWith(cacheFirst(request));
    return;
  }

  const isCatalog = url.pathname.endsWith(".json");
  event.respondWith(networkFirst(request, isCatalog ? 8000 : 4000));
});
